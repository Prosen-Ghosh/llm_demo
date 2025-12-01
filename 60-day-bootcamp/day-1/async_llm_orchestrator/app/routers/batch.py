from fastapi import APIRouter, Depends
from typing import Dict
from app.models.models import BatchLLMRequest, BatchLLMResponse
from app.core.orchestrator import LLMOrchestrator
from app.routers.dependencies import get_orchestrator

router = APIRouter()

@router.post("/batch")
async def process_batch(batch: BatchLLMRequest, orchestrator: LLMOrchestrator = Depends(get_orchestrator)) -> BatchLLMResponse:
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")
    
    return await orchestrator.execute_batch(batch)