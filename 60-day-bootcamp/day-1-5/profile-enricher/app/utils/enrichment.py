import httpx
import asyncio
import os
from typing import Dict, Any, Optional
import time
from app.utils import logging
import random

EXTERNAL_API_URL: str = os.getenv("EXTERNAL_API_URL", "http://localhost:8000/dummy-enrich")
EXTERNAL_API_TIMEOUT: float = float(os.getenv("EXTERNAL_API_TIMEOUT", "5"))
MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
BACKOFF_BASE: float = float(os.getenv("BACKOFF_BASE", "0.5"))

async def exponential_backoff_sleep(attempt: int) -> None:
    # base * 2^attempt + jitter
    jitter = random.uniform(0, 0.1)
    delay = BACKOFF_BASE * (2 ** attempt) + jitter
    await asyncio.sleep(delay)

async def enrich_with_retries(
        payload, 
        client: httpx.AsyncClient, 
        timeout: float = EXTERNAL_API_TIMEOUT, 
        max_retries: int = MAX_RETRIES) -> Dict[str, Any]:
    
    last_exc: Optional[Exception] = None

    for attempt in range(max_retries):
        start = time.perf_counter()
        try:
            resp = await client.post(EXTERNAL_API_URL, json=payload, timeout=timeout)
            print(f"\n\nresp: {resp.json()}\n\n")
            duration = time.perf_counter() - start
            logging.log_json(event="enrichment_attempt", attempt=attempt, status_code=resp.status_code, duration_s=duration)
            resp.raise_for_status()
            return resp.json()
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            last_exc = exc
            duration = time.perf_counter() - start
            logging.log_json(event="enrichment_error", attempt=attempt, error=str(exc), duration_s=duration)
            await exponential_backoff_sleep(attempt)

    raise last_exc or RuntimeError("Unknown enrichment failure")