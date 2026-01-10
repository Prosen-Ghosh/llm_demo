from fastapi import APIRouter, Depends
from typing import Annotated

from app.services.provider_manager import ProviderManager
from app.api.deps import get_provider_manager
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check(
    pm: Annotated[ProviderManager, Depends(get_provider_manager)]
):
    return {
        "status": "healthy",
        "version": settings.version,
        "environment": settings.environment,
        "providers": pm.list_providers()
    }