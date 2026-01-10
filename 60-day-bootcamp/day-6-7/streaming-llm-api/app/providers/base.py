from abc import ABC, abstractmethod
from typing import AsyncIterator, Callable, Optional
import httpx
import asyncio
from app.models.chat import ChatRequest, ChatResponse, StreamChunk


class StreamingProviderBase(ABC):
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def close(self):
        await self.client.aclose()
    
    @abstractmethod
    async def stream(
        self, 
        request: ChatRequest, 
        disconnect_check: Optional[Callable[[], bool]] = None
    ) -> AsyncIterator[StreamChunk]:
        pass
    
    @abstractmethod
    async def complete(self, request: ChatRequest) -> ChatResponse:
        pass