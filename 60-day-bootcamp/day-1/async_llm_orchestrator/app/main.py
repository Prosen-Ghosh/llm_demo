import os
from contextlib import asynccontextmanager
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.core.config import Settings
from app.core.orchestrator import LLMOrchestrator
from app.routers import batch_router, health_router
from app.routers.dependencies import set_orchestrator

load_dotenv()

# Global settings and orchestrator instances
settings = Settings()
orchestrator: LLMOrchestrator | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global orchestrator
    orchestrator = LLMOrchestrator(settings)
    set_orchestrator(orchestrator)
    yield
    if orchestrator:
        await orchestrator.close()


app = FastAPI(
    title="Async LLM Orchestrator",
    description="Production-grade async LLM request handler",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(health_router, tags=['health'])
app.include_router(batch_router, tags=['users'])