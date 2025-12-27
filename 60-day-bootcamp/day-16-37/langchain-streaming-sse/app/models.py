from pydantic import BaseModel, Field

class StreamRequest(BaseModel):
    query: str = Field(..., description="User query")
    temperature: float = Field(0.7, ge=0.0, le=1.0, description="Sampling temperature")
    max_tokens: int = Field(2048, ge=1, le=4096, description="Maximum tokens")


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    session_id: str = Field(..., description="Session identifier")
    temperature: float = Field(0.7, ge=0.0, le=1.0)


class GenerateRequest(BaseModel):
    query: str
    temperature: float = 0.7