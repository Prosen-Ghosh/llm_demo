import time
from abc import ABC, abstractmethod
from typing import Optional
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from app.models.models import LLMRequest, LLMResponse

class RateLimitError(Exception):
    pass

class LLMProviderBase(ABC):
    def __init__(self, api_key: str, timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def close(self):
        await self.client.aclose()
    
    @abstractmethod
    async def _make_request(self, request: LLMRequest) -> dict:
        pass
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, RateLimitError)),
        reraise=True
    )
    async def execute(self, request: LLMRequest) -> LLMResponse:
        start_time = time.perf_counter()
        error_msg: Optional[str] = None
        content = ""
        tokens = {"prompt": 0, "completion": 0, "total": 0}
        
        try:
            response_data = await self._make_request(request)
            content = response_data.get("content", "")
            tokens = response_data.get("usage", tokens)
            
        except httpx.TimeoutException as e:
            error_msg = f"Request timeout: {str(e)}"
            raise
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                error_msg = "Rate limit exceeded"
                raise RateLimitError(error_msg)
            error_msg = f"HTTP {e.response.status_code}: {str(e)}"
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
        
        finally:
            latency_ms = (time.perf_counter() - start_time) * 1000
        
        return LLMResponse(
            request_id=request.request_id,
            provider=request.provider,
            model=request.model,
            content=content,
            prompt_tokens=tokens.get("prompt", 0),
            completion_tokens=tokens.get("completion", 0),
            total_tokens=tokens.get("total", 0),
            latency_ms=latency_ms,
            error=error_msg
        )