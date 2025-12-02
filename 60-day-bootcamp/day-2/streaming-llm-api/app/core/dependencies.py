import time
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Annotated, Optional
import asyncio
from fastapi import Depends, Header, HTTPException, Request, status
from cachetools import TTLCache

from app.core.config import settings
from app.models.usage import UsageStats, RateLimitInfo, RequestContext

async def check_client_disconnect(request: Request):
    async def is_disconnected() -> bool:
        try:
            if await request.is_disconnected():
                return True
            return False
        except Exception:
            return True
    
    return is_disconnected

async def verify_api_key(
    x_api_key: Annotated[Optional[str], Header()] = None,
    authorization: Annotated[Optional[str], Header()] = None
) -> str:
    api_key = x_api_key
    
    # Check Authorization header if X-API-Key not provided
    if not api_key and authorization:
        if authorization.startswith("Bearer "):
            api_key = authorization[7:]
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Provide via X-API-Key header or Authorization: Bearer token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Validate format
    if len(api_key) < settings.api_key_min_length:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid API key format (minimum {settings.api_key_min_length} characters)"
        )
    
    return api_key

class RateLimiter:
    def __init__(self, requests_per_minute: int = 20):
        self.requests_per_minute = requests_per_minute
        # TTL cache: auto-expires entries after 60 seconds
        self.buckets: TTLCache = TTLCache(maxsize=10000, ttl=60)
    
    def _get_client_id(self, request: Request) -> str:
        """Extract client identifier from request"""
        # Check X-Forwarded-For for proxied requests
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Fallback to direct client IP
        if request.client:
            return request.client.host
        
        return "unknown"
    
    async def __call__(self, request: Request) -> RateLimitInfo:
        client_id = self._get_client_id(request)
        current_time = time.time()
        
        # Get or initialize bucket
        if client_id not in self.buckets:
            self.buckets[client_id] = {
                "count": 0,
                "reset_at": current_time + 60
            }
        
        bucket = self.buckets[client_id]
        
        # Reset if window expired
        if current_time > bucket["reset_at"]:
            bucket["count"] = 0
            bucket["reset_at"] = current_time + 60
        
        # Check limit
        if bucket["count"] >= self.requests_per_minute:
            reset_datetime = datetime.fromtimestamp(bucket["reset_at"])
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Resets at {reset_datetime.isoformat()}",
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(bucket["reset_at"])),
                    "Retry-After": str(int(bucket["reset_at"] - current_time))
                }
            )
        
        # Increment counter
        bucket["count"] += 1
        
        return RateLimitInfo(
            requests_remaining=self.requests_per_minute - bucket["count"],
            reset_at=datetime.fromtimestamp(bucket["reset_at"]),
            limit=self.requests_per_minute
        )


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=settings.max_requests_per_minute)

async def get_request_context(
    request: Request,
    api_key: str = Depends(verify_api_key)
) -> RequestContext:
    client_ip = request.client.host if request.client else "unknown"
    
    return RequestContext(
        request_id=str(uuid.uuid4()),
        client_ip=client_ip,
        api_key_prefix=api_key[:8] + "...",
        timestamp=datetime.utcnow(),
        endpoint=str(request.url.path),
        method=request.method
    )