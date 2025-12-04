from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest, ChatResponse, HealthResponse
from app.api.dependencies import get_agent
from app.utils.streaming import format_sse_data

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, agent = Depends(get_agent)):
    result = agent.invoke({
        "messages": [{"role": "user", "content": request.query}]
    })
    
    return ChatResponse(
        response=result["messages"][-1].content,
        query=request.query
    )

@router.post("/chat-stream")
async def chat_stream(request: ChatRequest, agent = Depends(get_agent)):
    async def stream_generator():
        for chunk in agent.stream({
            "messages": [{"role": "user", "content": request.query}]
        }, stream_mode="values"):
            
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                data = {"type": "reasoning", "content": latest_message.content}
                yield format_sse_data("reasoning", data)
            
            # Stream tool calls
            if hasattr(latest_message, 'tool_calls') and latest_message.tool_calls:
                for call in latest_message.tool_calls:
                    data = {
                        "type": "tool_call",
                        "tool": call['name'],
                        "args": call['args']
                    }
                    yield format_sse_data("tool_call", data)
    
    return StreamingResponse(stream_generator(), media_type="text/event-stream")

@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")