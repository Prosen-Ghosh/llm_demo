from typing import Optional
from fastapi import HTTPException

from app.core.orchestrator import LLMOrchestrator

_orchestrator: Optional[LLMOrchestrator] = None


def set_orchestrator(orchestrator: LLMOrchestrator):
    global _orchestrator
    _orchestrator = orchestrator


def get_orchestrator() -> LLMOrchestrator:
    if not _orchestrator:
        raise HTTPException(
            status_code=500,
            detail="Orchestrator not initialized"
        )
    return _orchestrator