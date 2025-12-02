from typing import Annotated

from fastapi import APIRouter, Depends
from app.models.usage import UsageStats
from app.core.dependencies import verify_api_key
from app.services.cost_tracker import CostTracker
from app.api.deps import get_cost_tracker

router = APIRouter()


@router.get("/stats", response_model=UsageStats)
async def get_usage_statistics(
    api_key: Annotated[str, Depends(verify_api_key)],
    tracker: Annotated[CostTracker, Depends(get_cost_tracker)]
) -> UsageStats:
    return tracker.get_usage(api_key)