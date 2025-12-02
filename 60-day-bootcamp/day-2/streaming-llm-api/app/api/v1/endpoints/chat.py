from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException, Request
from sse_starlette.sse import EventSourceResponse
import asyncio
from app.models.chat import ChatRequest, ChatResponse, Provider
from app.models.usage import RateLimitInfo, RequestContext
from app.core.dependencies import verify_api_key, rate_limiter, get_request_context
from app.services.provider_manager import ProviderManager
from app.api.deps import get_provider_manager, get_cost_tracker
from app.services.cost_tracker import CostTracker

router = APIRouter()


@router.post("/completions", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    response: Response,
    api_key: Annotated[str, Depends(verify_api_key)],
    rate_limit: Annotated[RateLimitInfo, Depends(rate_limiter)],
    context: Annotated[RequestContext, Depends(get_request_context)],
    pm: Annotated[ProviderManager, Depends(get_provider_manager)],
    tracker: Annotated[CostTracker, Depends(get_cost_tracker)]
) -> ChatResponse:
    # Add rate limit headers to response
    response.headers["X-RateLimit-Limit"] = str(rate_limit.limit)
    response.headers["X-RateLimit-Remaining"] = str(rate_limit.requests_remaining)
    response.headers["X-RateLimit-Reset"] = rate_limit.reset_at.isoformat()
    
    # Get appropriate provider
    try:
        provider = pm.get_provider(request.provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Execute completion
    result = await provider.complete(request)
    tracker.record_usage(
        api_key=api_key,
        prompt_tokens=result.usage.get("prompt_tokens", 0),
        completion_tokens=result.usage.get("completion_tokens", 0),
        model=request.model
    )

    # Structured logging
    print(
        f"[{context.request_id}] "
        f"{context.client_ip} -> "
        f"{request.provider}/{request.model} -> "
        f"{result.latency_ms:.0f}ms -> "
        f"{result.usage.get('total_tokens', 0)} tokens"
    )
    
    return result


@router.post("/stream")
async def chat_completion_stream(
    request: ChatRequest,
    fast_request: Request,
    api_key: Annotated[str, Depends(verify_api_key)],
    rate_limit: Annotated[RateLimitInfo, Depends(rate_limiter)],
    context: Annotated[RequestContext, Depends(get_request_context)],
    pm: Annotated[ProviderManager, Depends(get_provider_manager)]
):
    request.stream = True
    try:
        provider = pm.get_provider(request.provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    print(f"[{context.request_id}] " f"STREAM START: {context.client_ip} -> {request.provider}/{request.model}")
    
    async def event_generator():
        try:
            chunk_count = 0
            cancelled = False

            async def is_disconnected() -> bool:
                return await fast_request.is_disconnected()
            
            async for chunk in provider.stream(request, disconnect_check=is_disconnected):
                yield { "event": "message", "data": chunk.model_dump_json() }
                chunk_count += 1

                if chunk.finish_reason == "cancelled":
                    cancelled = True
                    break

            if cancelled:
                yield { "event": "cancelled", "data": f'{{"status": "cancelled", "chunks": {chunk_count}}}' }
                print(f"[{context.request_id}] " f"STREAM CANCELLED: {chunk_count} chunks (client disconnected)")
            else:
                yield { "event": "done", "data": f'{{"status": "complete", "chunks": {chunk_count}}}' }
                print(f"[{context.request_id}] " f"STREAM END: {chunk_count} chunks")
        
        except asyncio.CancelledError:
            print(f"[{context.request_id}] STREAM CANCELLED (AsyncIO)")
            yield { "event": "cancelled", "data": '{"status": "cancelled", "reason": "connection_lost"}' }
            raise
        except Exception as e:
            print(f"[{context.request_id}] STREAM ERROR: {str(e)}")
            yield { "event": "error", "data": f'{{"error": "{str(e)}"}}' }
    
    return EventSourceResponse(event_generator())
