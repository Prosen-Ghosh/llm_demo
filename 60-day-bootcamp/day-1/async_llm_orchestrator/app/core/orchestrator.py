import asyncio
from typing import Dict

from app.models.models import BatchLLMRequest, BatchLLMResponse, LLMRequest, LLMResponse
from app.providers.base import LLMProviderBase
from app.providers.ollama import OllamaProvider
from app.providers.openrouter import OpenRouterProvider
from app.core.config import Settings

class LLMOrchestrator:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.semaphore = asyncio.Semaphore(settings.max_concurrent_requests)
        self.providers: Dict[str, LLMProviderBase] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        if self.settings.openrouter_api_key:
            self.providers["openrouter"] = OpenRouterProvider(
                api_key=self.settings.openrouter_api_key,
                timeout=self.settings.request_timeout,
                max_retries=self.settings.max_retries
            )

        if self.settings.ollama_api_key:
            self.providers["ollama"] = OllamaProvider(
                api_key=self.settings.ollama_api_key,
                timeout=self.settings.request_timeout,
                max_retries=self.settings.max_retries
            )

    async def close(self):
        for provider in set(self.providers.values()):
            await provider.close()

    async def _execute_single_request(self, request: LLMRequest) -> LLMResponse:
        async with self.semaphore:  # Rate limiting
            provider = self.providers.get(request.provider)
            if not provider:
                return LLMResponse(
                    request_id=request.request_id,
                    provider=request.provider,
                    model=request.model,
                    content="",
                    latency_ms=0.0,
                    error=f"Provider '{request.provider}' not configured"
                )
            
            try:
                return await provider.execute(request)
            except Exception as e:
                return LLMResponse(
                    request_id=request.request_id,
                    provider=request.provider,
                    model=request.model,
                    content="",
                    latency_ms=0.0,
                    error=f"Failed after retries: {str(e)}"
                )
            
    async def execute_batch(self, batch: BatchLLMRequest) -> BatchLLMResponse:
        start_time = asyncio.get_event_loop().time()
        
        # Create tasks for all requests
        tasks = [
            self._execute_single_request(req)
            for req in batch.requests
        ]

        # Execute concurrently with gather
        responses = await asyncio.gather(*tasks, return_exceptions=False)
        
        total_latency = (asyncio.get_event_loop().time() - start_time) * 1000
        successful = sum(1 for r in responses if not r.error)
        failed = len(responses) - successful
        
        return BatchLLMResponse(
            responses=responses,
            total_requests=len(responses),
            successful=successful,
            failed=failed,
            total_latency_ms=total_latency,
            average_latency_ms=total_latency / len(responses) if responses else 0
        )