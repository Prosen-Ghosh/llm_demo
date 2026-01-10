from app.models.models import LLMRequest
from app.providers.base import LLMProviderBase


class OllamaProvider(LLMProviderBase):
    BASE_URL = "https://ollama.com/v1/chat/completions"

    async def _make_request(self, req: LLMRequest) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": req.model,
            "messages": [{"role": m.role, "content": m.content} for m in req.messages],
            "temperature": req.temperature,
            "max_tokens": req.max_tokens
        }

        response = await self.client.post(self.BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        return {
            "content": data["choices"][0]["message"]["content"],
            "usage": {
                "prompt": data.get("usage", {}).get("prompt_tokens", 0),
                "completion": data.get("usage", {}).get("completion_tokens", 0),
                "total": data.get("usage", {}).get("total_tokens", 0)
            }
        }