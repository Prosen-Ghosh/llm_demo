from fastapi import APIRouter
from typing import Dict

router = APIRouter()

@router.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}