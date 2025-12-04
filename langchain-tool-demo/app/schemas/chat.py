from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    query: str

class HealthResponse(BaseModel):
    status: str