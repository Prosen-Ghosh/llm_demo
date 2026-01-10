from datetime import datetime
from enum import Enum
from typing import Literal, Optional
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    ConfigDict
)

class LLMProvider(str, Enum):
    OPENROUTER = "openrouter"
    OLLAMA = 'ollama'

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
    
class LLMRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=True)

    provider: LLMProvider
    model: str = Field(..., min_length=1)
    messages: list[Message] = Field(..., min_length=1)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=32000)
    request_id: Optional[str] = None

    @field_validator("model")
    @classmethod
    def validate_model_format(cls, v: str) -> str:
        """Ensure model names are lowercase and valid"""
        v = v.lower().strip()
        if not v:
            raise ValueError("Model name cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_provider_model_compatibility(self) -> "LLMRequest":
        provider_models = {
            "ollama": ["deepseek-r1:8b", "gpt-oss:120b-cloud"],
            "openrouter": ["x-ai/grok-4.1-fast:free", "z-ai/glm-4.5-air:free", "google/gemma-3-27b-it:free"]  # OpenRouter supports many models
        }
        
        if self.provider != "openrouter":
            valid_models = provider_models.get(self.provider, [])
            if not any(self.model.startswith(m) for m in valid_models):
                raise ValueError(
                    f"Model '{self.model}' not compatible with provider '{self.provider}'"
                )
        return self
    
class BatchLLMRequest(BaseModel):
    requests: list[LLMRequest] = Field(..., min_length=1, max_length=100)
    
    @field_validator("requests")
    @classmethod
    def validate_unique_request_ids(cls, v: list[LLMRequest]) -> list[LLMRequest]:
        ids = [req.request_id for req in v if req.request_id]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate request_ids found")
        return v
    
class LLMResponse(BaseModel):
    request_id: Optional[str]
    provider: str
    model: str
    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None
    
    @model_validator(mode="after")
    def validate_token_sum(self) -> "LLMResponse":
        if self.total_tokens > 0:
            expected = self.prompt_tokens + self.completion_tokens
            if expected != self.total_tokens and expected > 0:
                # Allow for slight discrepancies but warn
                print(f"Total Token Sum discrepancies found: {expected}")
                pass
        return self


class BatchLLMResponse(BaseModel):
    """Batch response with metadata"""
    responses: list[LLMResponse]
    total_requests: int
    successful: int
    failed: int
    total_latency_ms: float
    average_latency_ms: float