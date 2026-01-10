from typing import Optional, Tuple
from pydantic import ValidationError
from app.core.logging import get_logger
from app.models.schemas import InvoiceData, ExtractionResult
from app.services.ollama_extractor import OllamaExtractor
from app.services.openrouter_extractor import OpenRouterExtractor
from app.core.config import settings

logger = get_logger(__name__)


class ExtractionRepairEngine:
    def __init__(self):
        self.ollama = OllamaExtractor()
        self.openrouter = OpenRouterExtractor()
        self.max_retries = settings.max_retries
    
    async def __aenter__(self):
        await self.ollama.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.ollama.__aexit__(exc_type, exc_val, exc_tb)
    
    async def extract_with_repair(
        self,
        invoice_text: str,
        prefer_strategy: Optional[str] = None
    ) -> ExtractionResult:
        if prefer_strategy == "openrouter":
            strategies = ["openrouter", "ollama"]
        else:
            strategies = ["ollama", "openrouter"] if settings.enable_openrouter_fallback else ["ollama"]
        
        last_error: Optional[str] = None
        retry_count = 0
        
        for strategy in strategies:
            for attempt in range(self.max_retries + 1):
                try:
                    logger.info(
                        "extraction_attempt",
                        strategy=strategy,
                        attempt=attempt + 1,
                        retry_count=retry_count
                    )
                    
                    # Extract using the current strategy
                    if strategy == "ollama":
                        raw_data = await self.ollama.extract(invoice_text, last_error)
                    else:
                        raw_data = await self.openrouter.extract(invoice_text, last_error)
                    
                    # Validate with Pydantic
                    validated_data = InvoiceData.model_validate(raw_data)
                    
                    # Success!
                    return ExtractionResult(
                        success=True,
                        data=validated_data,
                        confidence_score=self._calculate_confidence(validated_data),
                        strategy_used=strategy,
                        retry_count=retry_count
                    )
                
                except ValidationError as e:
                    retry_count += 1
                    last_error = self._format_validation_error(e)
                    
                    logger.warning(
                        "validation_failed",
                        strategy=strategy,
                        attempt=attempt + 1,
                        error=last_error,
                        raw_data_sample=str(raw_data)[:200] if 'raw_data' in locals() else None
                    )
                    
                    # Store partial data for final result if all retries fail
                    partial_data = raw_data if 'raw_data' in locals() else None
                    
                    # If this was the last retry for this strategy, move to next strategy
                    if attempt >= self.max_retries:
                        break
                    
                    # Otherwise, retry with error feedback
                    continue
                
                except Exception as e:
                    logger.error(
                        "extraction_failed",
                        strategy=strategy,
                        attempt=attempt + 1,
                        error=str(e),
                        error_type=type(e).__name__
                    )
                    
                    # Fatal error, try next strategy immediately
                    break
        
        # All strategies exhausted
        return ExtractionResult(
            success=False,
            errors=[f"All extraction strategies failed. Last error: {last_error}"],
            confidence_score=0.0,
            strategy_used="all_failed",
            retry_count=retry_count,
            partial_data=partial_data if 'partial_data' in locals() else None
        )
    
    def _format_validation_error(self, error: ValidationError) -> str:
        errors = []
        for err in error.errors():
            field = " -> ".join(str(loc) for loc in err["loc"])
            msg = err["msg"]
            errors.append(f"Field '{field}': {msg}")
        
        return "\n".join(errors)
    
    def _calculate_confidence(self, data: InvoiceData) -> float:
        score = 0.6  # Base score for valid required fields
        
        # Bonus for optional fields
        optional_bonus = 0.0
        if data.due_date:
            optional_bonus += 0.1
        if data.vendor.address:
            optional_bonus += 0.1
        if data.vendor.tax_id:
            optional_bonus += 0.1
        if data.notes:
            optional_bonus += 0.1
        
        return min(score + optional_bonus, 1.0)