from typing import Dict
from app.core.config import settings
from app.models.chat import Provider
from app.providers import StreamingProviderBase, OpenRouterProvider, OllamaProvider

class ProviderManager:
    def __init__(self):
        self.providers: Dict[str, StreamingProviderBase] = {}
    
    def initialize(self):
        # OpenRouter (required)
        self.providers["openrouter"] = OpenRouterProvider(
            api_key=settings.openrouter_api_key,
            timeout=settings.request_timeout
        )
        print("✅ OpenRouter provider initialized")
        
        # Ollama (optional - may not be running)
        self.providers["ollama"] = OllamaProvider(
            base_url=settings.ollama_base_url,
            timeout=settings.request_timeout
        )
        print("✅ Ollama provider initialized (will fail gracefully if not running)")
    
    async def cleanup(self):
        for name, provider in self.providers.items():
            await provider.close()
            print(f"✅ Closed {name} provider")
    
    def get_provider(self, provider_type: Provider) -> StreamingProviderBase:
        provider = self.providers.get(provider_type.value)
        if not provider:
            raise ValueError(f"Provider {provider_type} not configured")
        return provider
    
    def list_providers(self) -> list[str]:
        return list(self.providers.keys())

provider_manager = ProviderManager()