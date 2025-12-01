from fastapi import APIRouter
import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

ENV: str = os.getenv("ENV", "development")

router = APIRouter()

@router.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "env": ENV}