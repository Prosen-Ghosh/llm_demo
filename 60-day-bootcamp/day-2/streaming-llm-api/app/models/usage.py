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