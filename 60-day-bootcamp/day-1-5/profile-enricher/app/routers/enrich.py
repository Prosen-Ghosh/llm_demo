from fastapi import APIRouter
import os
from dotenv import load_dotenv
import time
import random

load_dotenv()

ENV: str = os.getenv("ENV", "development")

router = APIRouter()
# This should be an external service; implemented here for demonstration purposes
@router.post("/dummy-enrich")
async def enrich(payload: dict):
    time.sleep(0.1)

    user_id = payload.get("userId")

    enriched = {
        "risk_score": round(random.random(), 3),
        "is_adult": payload.get("age", 0) >= 18,
        "postal_hash": hash(payload.get("address", {}).get("postalCode", "")) % 10000,
        "user_category": "high_value" if payload.get("age", 0) > 25 else "standard",
        "source_user_id": user_id,
    }

    return enriched