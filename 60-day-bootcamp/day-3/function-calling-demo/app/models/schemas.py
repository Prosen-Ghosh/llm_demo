from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum


class ToolStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: Dict[str, Any]


class ToolResult(BaseModel):
    tool_name: str
    status: ToolStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: float


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system|tool)$")
    content: str
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_history: List[ChatMessage] = Field(default_factory=list)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4000)


class ChatResponse(BaseModel):
    response: str
    tool_results: List[ToolResult] = Field(default_factory=list)
    conversation_history: List[ChatMessage]