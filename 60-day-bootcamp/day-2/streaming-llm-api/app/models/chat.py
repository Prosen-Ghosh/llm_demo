from datetime import datetime
from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class Provider(str, Enum):
    OPENROUTER = "openrouter"
    OLLAMA = "ollama"


class Message(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    role: Literal["system", "user", "assistant"]
    content: str = Field(..., min_length=1, max_length=50000)
    
    @field_validator("content")
    @classmethod
    def validate_content_not_empty(cls, v: str) -> str:
        if not v or v.isspace():
            raise ValueError("Content cannot be empty or whitespace only")
        return v


class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    provider: Provider = Provider.OPENROUTER
    model: str = Field(
        default="meta-llama/llama-3.2-3b-instruct:free",
        description="Model name (use :free suffix for OpenRouter free models)"
    )
    messages: list[Message] = Field(..., min_length=1, max_length=50)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4000)
    stream: bool = Field(default=False, description="Enable streaming responses")
    
    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str, info) -> str:
        provider = info.data.get("provider")
        
        if provider == Provider.OPENROUTER:
            # List of known free models
            free_models = [
                "meta-llama/llama-3.2-3b-instruct:free",
                "google/gemini-flash-1.5:free",
                "mistralai/mistral-7b-instruct:free",
                "qwen/qwen-2-7b-instruct:free",
            ]
            # Just log a warning, don't block
            if not v.endswith(":free") and v not in free_models:
                print(f"⚠️  Warning: {v} may not be free on OpenRouter")
        
        return v


class ChatResponse(BaseModel):
    id: str
    model: str
    provider: str
    content: str
    role: Literal["assistant"] = "assistant"
    usage: dict[str, int] = Field(
        default_factory=lambda: {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    )
    latency_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    finish_reason: Optional[str] = None


class StreamChunk(BaseModel):
    id: str
    model: str
    provider: str
    delta: str
    finish_reason: Optional[str] = None
    index: int = 0