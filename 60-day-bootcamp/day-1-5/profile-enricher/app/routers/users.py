from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import JSONResponse
import os
import asyncio
import time
from app.models.user_profile import UserProfile
from app.utils import logging, enrichment
from pydantic import ValidationError
import httpx

MAX_CONCURRENCY: int = int(os.getenv("MAX_CONCURRENCY", "8"))

router = APIRouter()

_concurrency_semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

def get_semaphore() -> asyncio.Semaphore:
    return _concurrency_semaphore

@router.post("/users", status_code=200)
async def create_and_enrich_user(req: Request, sem: asyncio.Semaphore = Depends(get_semaphore)) -> JSONResponse:
    payload = await req.json()
    validation_start = time.perf_counter()

    try:
        user = UserProfile.model_validate(payload)
        validation_duration = time.perf_counter() - validation_start

        logging.log_json(event="validation_success", user_id=user.user_id, duration_s=validation_duration)
    except ValidationError as e:
        validation_duration = time.perf_counter() - validation_start
        logging.log_json(event="validation_failed", error=e.errors(), duration_s=validation_duration)
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": e.errors()})

    async with sem:
        async with httpx.AsyncClient() as client:
            enrich_start = time.perf_counter()
            try:
                enriched = await enrichment.enrich_with_retries(user.to_public_dict(), client)
                enrich_duration = time.perf_counter() - enrich_start
                logging.log_json(event="enrichment_success", user_id=user.user_id, duration_s=enrich_duration)
            except Exception as exc:
                enrich_duration = time.perf_counter() - enrich_start
                logging.log_json(event="enrichment_failed", user_id=user.user_id, error=str(exc), duration_s=enrich_duration)
                # Return 502 for bad upstream enrichment, hide internal details
                raise HTTPException(status_code=502, detail="Upstream enrichment failed")
                

        
    result = {"user": user.to_public_dict(), "enrichment": enriched}
    return JSONResponse(status_code=200, content=result)