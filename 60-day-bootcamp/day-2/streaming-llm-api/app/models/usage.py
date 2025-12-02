from datetime import datetime
from pydantic import BaseModel

class RateLimitInfo(BaseModel):
    requests_remaining: int
    reset_at: datetime
    limit: int


class RequestContext(BaseModel):
    request_id: str
    client_ip: str
    api_key_prefix: str
    timestamp: datetime
    endpoint: str
    method: str

class UsageStats(BaseModel):
    total_requests: int = 0
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    estimated_cost_usd: float = 0.0