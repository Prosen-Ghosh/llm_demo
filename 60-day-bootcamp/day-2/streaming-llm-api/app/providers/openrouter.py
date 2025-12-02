import json
import time
from typing import AsyncIterator, Optional, Callable
import httpx
import asyncio
from app.providers.base import StreamingProviderBase
from app.models.chat import ChatRequest, ChatResponse, StreamChunk


class OpenRouterProvider(StreamingProviderBase):
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    def __init__(self, api_key: str, timeout: int = 60):
        super().__init__(timeout)
        self.api_key = api_key
    
    def _prepare_payload(self, request: ChatRequest) -> dict:
        return {
            "model": request.model,
            "messages": [
                {"role": msg.role, "content": msg.content}
                for msg in request.messages
            ],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": request.stream
        }
    
    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Engineering Bootcamp Day 2"
        }
    
    async def stream(
            self, 
            request: ChatRequest,
            disconnect_check: Optional[Callable[[], bool]] = None
        ) -> AsyncIterator[StreamChunk]:

        payload = self._prepare_payload(request)
        payload["stream"] = True
        
        index = 0
        chunk_id = f"chatcmpl-{int(time.time())}"
        
        try:
            async with self.client.stream(
                "POST",
                self.BASE_URL,
                json=payload,
                headers=self._get_headers()
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if disconnect_check and await disconnect_check():
                        print(f"Client disconnected, stopping stream (chunk {index})")
                        await response.aclose()
                        yield StreamChunk(
                            id=chunk_id,
                            model=request.model,
                            provider="openrouter",
                            delta="[CANCELLED: Client disconnected]",
                            finish_reason="cancelled",
                            index=index
                        )
                        return
                    # Skip empty lines and done marker
                    if not line.strip() or line.strip() == "data: [DONE]":
                        continue
                    
                    # Parse SSE data
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            
                            if "choices" in data and len(data["choices"]) > 0:
                                choice = data["choices"][0]
                                delta = choice.get("delta", {})
                                content = delta.get("content", "")
                                
                                if content:
                                    yield StreamChunk(
                                        id=chunk_id,
                                        model=request.model,
                                        provider="openrouter",
                                        delta=content,
                                        finish_reason=choice.get("finish_reason"),
                                        index=index
                                    )
                                    index += 1
                                
                                # Handle finish
                                if choice.get("finish_reason"):
                                    break
                        
                        except json.JSONDecodeError:
                            continue
        except asyncio.CancelledError:
            print(f"Stream cancelled (asyncio.CancelledError)")
            yield StreamChunk(
                id=chunk_id,
                model=request.model,
                provider="openrouter",
                delta="[CANCELLED: Request cancelled]",
                finish_reason="cancelled",
                index=index
            )
            raise
        except httpx.HTTPStatusError as e:
            # Graceful error handling in stream
            error_msg = f"HTTP {e.response.status_code}: {e.response.text[:100]}"
            yield StreamChunk(
                id=chunk_id,
                model=request.model,
                provider="openrouter",
                delta=f"[ERROR: {error_msg}]",
                finish_reason="error",
                index=index
            )
        
        except Exception as e:
            yield StreamChunk(
                id=chunk_id,
                model=request.model,
                provider="openrouter",
                delta=f"[ERROR: {str(e)}]",
                finish_reason="error",
                index=index
            )
    
    async def complete(self, request: ChatRequest) -> ChatResponse:
        start_time = time.perf_counter()
        
        payload = self._prepare_payload(request)
        payload["stream"] = False
        
        try:
            response = await self.client.post(
                self.BASE_URL,
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            data = response.json()
            
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            return ChatResponse(
                id=data.get("id", f"chatcmpl-{int(time.time())}"),
                model=request.model,
                provider="openrouter",
                content=data["choices"][0]["message"]["content"],
                usage=data.get("usage", {}),
                latency_ms=latency_ms,
                finish_reason=data["choices"][0].get("finish_reason")
            )
        
        except httpx.HTTPStatusError as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            error_content = f"HTTP {e.response.status_code}: {e.response.text[:200]}"
            
            return ChatResponse(
                id=f"error-{int(time.time())}",
                model=request.model,
                provider="openrouter",
                content=error_content,
                latency_ms=latency_ms,
                finish_reason="error"
            )