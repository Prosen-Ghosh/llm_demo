import httpx
import json
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.models.schemas import ChatMessage, ToolCall

class LLMClient:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.api_key = settings.ollama_api_key
        self.model = settings.default_model
    
    async def chat(
        self,
        messages: List[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        tools: Optional[List[dict]] = None
    ) -> Dict[str, Any]:
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        if tools:
            payload["tools"] = tools
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error {e.response.status_code}: {e.response.text}")
            raise
        except Exception as e:
            print(f"Error: {e}")
            raise

    def parse_tool_calls(self, response: Dict[str, Any]) -> Optional[List[ToolCall]]:
        message = response.get("message", {})
        tool_calls = message.get("tool_calls", [])
        
        if not tool_calls:
            return None
        
        parsed = []
        for call in tool_calls:
            func = call.get("function", {})
            args = func.get("arguments", {})
            
            parsed.append(ToolCall(
                id=call.get("id", f"call_{len(parsed)}"),
                name=func.get("name"),
                arguments=args
            ))
        
        return parsed
    
    def format_messages(self, history: List[ChatMessage]) -> List[Dict[str, Any]]:
        formatted = []
        for msg in history:
            formatted_msg = { "role": msg.role, "content": msg.content }
            if msg.tool_calls:
                formatted_msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": tc.arguments  # Keep as dict
                        }
                    }
                    for tc in msg.tool_calls
                ]
            
            if msg.tool_call_id:
                formatted_msg["tool_call_id"] = msg.tool_call_id
            
            formatted.append(formatted_msg)
        
        return formatted