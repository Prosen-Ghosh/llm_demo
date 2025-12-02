import json
import time
from typing import AsyncIterator, Callable, Optional
import httpx
import asyncio
from app.providers.base import StreamingProviderBase
from app.models.chat import ChatRequest, ChatResponse, StreamChunk

class OllamaProvider(StreamingProviderBase):
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 60):
        super().__init__(timeout)
        self.base_url = base_url.rstrip("/")
    
    async def stream(
            self, 
            request: ChatRequest,
            disconnect_check: Optional[Callable[[], bool]] = None
        ) -> AsyncIterator[StreamChunk]:

        url = f"{self.base_url}/api/chat"        
        payload = {
            "model": request.model,
            "messages": [
                {"role": msg.role, "content": msg.content}
                for msg in request.messages
            ],
            "stream": True,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens
            }
        }
        
        index = 0
        chunk_id = f"ollama-{int(time.time())}"
        
        try:
            async with self.client.stream("POST", url, json=payload) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if disconnect_check and await disconnect_check():
                        print(f"Client disconnected (Ollama), stopping stream")
                        await response.aclose()
                        yield StreamChunk(
                            id=chunk_id,
                            model=request.model,
                            provider="ollama",
                            delta="[CANCELLED: Client disconnected]",
                            finish_reason="cancelled",
                            index=index
                        )
                        return
                    
                    if not line.strip():
                        continue
                    
                    try:
                        data = json.loads(line)
                        content = data.get("message", {}).get("content", "")
                        
                        if content:
                            yield StreamChunk(
                                id=chunk_id,
                                model=request.model,
                                provider="ollama",
                                delta=content,
                                finish_reason="stop" if data.get("done") else None,
                                index=index
                            )
                            index += 1
                        
                        if data.get("done"):
                            break
                    
                    except json.JSONDecodeError:
                        continue
        except asyncio.CancelledError:
            print(f"Ollama stream cancelled")
            yield StreamChunk(
                id=chunk_id,
                model=request.model,
                provider="ollama",
                delta="[CANCELLED]",
                finish_reason="cancelled",
                index=index
            )
            raise
        except httpx.HTTPError as e:
            yield StreamChunk(
                id=chunk_id,
                model=request.model,
                provider="ollama",
                delta=f"[ERROR: Ollama unavailable - {str(e)}. Install: https://ollama.ai]",
                finish_reason="error",
                index=index
            )
    
    async def complete(self, request: ChatRequest) -> ChatResponse:
        start_time = time.perf_counter()
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": request.model,
            "messages": [
                {"role": msg.role, "content": msg.content}
                for msg in request.messages
            ],
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens
            }
        }
        
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            return ChatResponse(
                id=f"ollama-{int(time.time())}",
                model=request.model,
                provider="ollama",
                content=data["message"]["content"],
                usage={
                    "prompt_tokens": data.get("prompt_eval_count", 0),
                    "completion_tokens": data.get("eval_count", 0),
                    "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                },
                latency_ms=latency_ms,
                finish_reason="stop"
            )
        
        except httpx.HTTPError as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            return ChatResponse(
                id=f"error-{int(time.time())}",
                model=request.model,
                provider="ollama",
                content=f"Ollama error: {str(e)}. Ensure Ollama is running.",
                latency_ms=latency_ms,
                finish_reason="error"
            )