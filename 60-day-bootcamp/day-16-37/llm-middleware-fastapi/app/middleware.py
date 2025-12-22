import uuid
from fastapi import Request

async def request_context_middleware(request: Request, call_next):
    request.state.req_id = str(uuid.uuid4())

    raw_q = request.query_params.get("q", "")
    request.state.sanitized_q = raw_q.strip()

    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.req_id
    return response
