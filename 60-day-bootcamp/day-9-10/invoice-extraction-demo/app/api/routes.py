from fastapi import APIRouter, HTTPException, status
from app.models.schemas import ExtractionRequest, ExtractionResult
from app.services.repair_engine import ExtractionRepairEngine
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post(
    "/extract",
    response_model=ExtractionResult,
    status_code=status.HTTP_200_OK,
    summary="Extract structured data from invoice text",
    description="""
    Extract invoice data into a validated Pydantic schema.
    
    Supports multiple extraction strategies:
    - Ollama with JSON schema enforcement (default)
    - OpenRouter with function calling (fallback)
    - Automatic retry with validation error feedback
    
    Returns field-level validation status and confidence scores.
    """
)
async def extract_invoice(request: ExtractionRequest) -> ExtractionResult:
    logger.info(
        "extraction_request_received",
        text_length=len(request.invoice_text),
        prefer_strategy=request.prefer_strategy
    )
    
    try:
        async with ExtractionRepairEngine() as engine:
            result = await engine.extract_with_repair(
                invoice_text=request.invoice_text,
                prefer_strategy=request.prefer_strategy
            )
        
        if not result.success:
            logger.warning(
                "extraction_failed",
                errors=result.errors,
                retry_count=result.retry_count
            )
        
        return result
    
    except Exception as e:
        logger.error(
            "extraction_endpoint_error",
            error=str(e),
            error_type=type(e).__name__
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction failed: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint"
)
async def health_check():
    return {"status": "healthy", "service": "invoice-extraction-demo"}