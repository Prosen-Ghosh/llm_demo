import json
from typing import Optional
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings
from app.core.logging import get_logger
from app.models.schemas import InvoiceData

logger = get_logger(__name__)


class OpenRouterExtractor:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = settings.openrouter_model
    
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
            "openrouter_extraction_started",
            model=self.model,
            is_retry=validation_error is not None
        )
        
        system_prompt = self._build_system_prompt(validation_error)
        
        # Define the function schema
        function_schema = {
            "name": "extract_invoice_data",
            "description": "Extract structured data from an invoice",
            "parameters": InvoiceData.model_json_schema()
        }
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Extract invoice data from:\n\n{invoice_text}"}
                ],
                tools=[{"type": "function", "function": function_schema}],
                tool_choice={"type": "function", "function": {"name": "extract_invoice_data"}},
                temperature=0.1
            )
            
            # Extract function call arguments
            tool_call = response.choices[0].message.tool_calls[0]
            extracted_data = json.loads(tool_call.function.arguments)
            
            logger.info(
                "openrouter_extraction_success",
                model=self.model,
                fields_extracted=len(extracted_data)
            )
            
            return extracted_data
            
        except Exception as e:
            logger.error(
                "openrouter_extraction_error",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def _build_system_prompt(self, validation_error: Optional[str] = None) -> str:
        base_prompt = """You are an expert invoice data extraction system.
            Extract ALL information from the invoice accurately.

            CRITICAL RULES:
            1. Dates must be in YYYY-MM-DD format
            2. All monetary values must be numbers without currency symbols
            3. Validate: line_total = quantity * unit_price
            4. Validate: total_amount = subtotal + tax_amount
            5. Vendor name is REQUIRED

            Be precise. Do not invent information."""

        if validation_error:
            base_prompt += f"\n\nPREVIOUS ERROR: {validation_error}\nCorrect this in your response."
        
        return base_prompt