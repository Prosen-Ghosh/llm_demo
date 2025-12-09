import json
from typing import Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings
from app.core.logging import get_logger
from app.models.schemas import InvoiceData

logger = get_logger(__name__)


class OllamaExtractor:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.client = httpx.AsyncClient(timeout=120.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def extract(
        self,
        invoice_text: str,
        validation_error: Optional[str] = None
    ) -> dict:
        logger.info(
            "ollama_extraction_started",
            model=self.model,
            is_retry=validation_error is not None
        )
        
        system_prompt = self._build_system_prompt(validation_error)
        json_schema = InvoiceData.model_json_schema()
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract invoice data from:\n\n{invoice_text}"}
            ],
            "format": json_schema,  # Ollama JSON schema enforcement
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for factual extraction
                "top_p": 0.9
            }
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["message"]["content"]

            if content.startswith("```json"):
                import re
                # Use regex to remove the code block markers
                content = re.sub(r'^```json\s*', '', content, flags=re.MULTILINE)
                content = re.sub(r'\s*```$', '', content, flags=re.MULTILINE)
                    
            extracted_data = json.loads(content)
            
            logger.info(
                "ollama_extraction_success",
                model=self.model,
                fields_extracted=len(extracted_data)
            )
            
            return extracted_data
            
        except httpx.HTTPError as e:
            logger.error(
                "ollama_http_error",
                error=str(e),
                status_code=getattr(e.response, 'status_code', None)
            )
            raise
        except json.JSONDecodeError as e:
            logger.error(
                "ollama_json_parse_error",
                error=str(e),
                content=content[:200]
            )
            raise
        except Exception as e:
            logger.error(
                "ollama_extraction_error",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def _build_system_prompt(self, validation_error: Optional[str] = None) -> str:
        
        base_prompt = """You are an expert invoice data extraction system.
            Extract ALL information from the invoice into the provided JSON schema.

            CRITICAL RULES:
            1. Extract dates in YYYY-MM-DD format
            2. Extract all monetary values as numbers (no currency symbols)
            3. Ensure line_total = quantity * unit_price for each item
            4. Ensure total_amount = subtotal + tax_amount
            5. If a field is not present in the invoice, use null for optional fields
            6. The vendor name is REQUIRED - extract it even if partially visible

            Be precise and accurate. Do not hallucinate information."""

        if validation_error:
            base_prompt += f"\n\nPREVIOUS ATTEMPT FAILED WITH ERROR:\n{validation_error}\n\nPlease correct the error in this attempt."
        
        return base_prompt