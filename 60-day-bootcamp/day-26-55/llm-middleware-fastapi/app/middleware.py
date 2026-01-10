import uuid
import logging
from fastapi import Request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def request_context_middleware(request: Request, call_next):
    req_id = str(uuid.uuid4())
    request.state.req_id = req_id

    raw_q = request.query_params.get("q", "")
    sanitized_q = raw_q.strip()
    request.state.sanitized_q = sanitized_q

    logger.info(f"Request ID: {req_id} - Query: '{sanitized_q}'")

    response = await call_next(request)
    response.headers["X-Request-ID"] = req_id

    logger.info(f"Request ID: {req_id} - Response sent")
    return response
