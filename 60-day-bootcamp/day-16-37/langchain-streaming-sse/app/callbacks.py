import asyncio
import time
from typing import Any, Dict, List
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.outputs.llm_result import LLMResult


class StreamingCallbackHandler(AsyncCallbackHandler):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue
        self.start_time = None
        self.first_token_time = None
        self.token_count = 0
        
    async def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        self.start_time = time.time()
        self.token_count = 0
        await self.queue.put({ "type": "start", "timestamp": self.start_time })
    
    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        if self.first_token_time is None:
            self.first_token_time = time.time()
            ttft = self.first_token_time - self.start_time
            await self.queue.put({ "type": "metric", "metric": "time_to_first_token", "value": ttft })
        
        self.token_count += 1
        await self.queue.put({ "type": "token", "content": token })
    
    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        end_time = time.time()
        total_time = end_time - self.start_time
        
        tokens_per_sec = (
            self.token_count / total_time 
            if self.token_count > 0 and total_time > 0 
            else 0
        )
        
        await self.queue.put({
            "type": "end",
            "tokens": self.token_count,
            "duration": total_time,
            "tokens_per_sec": tokens_per_sec
        })
        await self.queue.put(None)  # Signal completion
    
    async def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        await self.queue.put({ "type": "error", "error": str(error) })
        await self.queue.put(None)  # Signal completion


class MetricsCallbackHandler(AsyncCallbackHandler):
    def __init__(self):
        self.metrics = {
            "total_tokens": 0,
            "total_time": 0.0,
            "request_count": 0,
            "error_count": 0
        }
        self.start_time = None
    
    async def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        self.start_time = time.time()
        self.metrics["request_count"] += 1
    
    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.metrics["total_tokens"] += 1
    
    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.metrics["total_time"] += elapsed
    
    async def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        self.metrics["error_count"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        request_count = self.metrics["request_count"]
        
        avg_time = (
            self.metrics["total_time"] / request_count
            if request_count > 0
            else 0.0
        )
        avg_tokens = (
            self.metrics["total_tokens"] / request_count
            if request_count > 0
            else 0.0
        )
        
        return {
            **self.metrics,
            "avg_time_per_request": round(avg_time, 3),
            "avg_tokens_per_request": round(avg_tokens, 1)
        }
    
    def reset(self) -> None:
        self.metrics = {
            "total_tokens": 0,
            "total_time": 0.0,
            "request_count": 0,
            "error_count": 0
        }
        self.start_time = None