import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import time
from app.streaming import stream_llm_response, stream_chat_response
from app.callbacks import MetricsCallbackHandler
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from fastapi.middleware.cors import CORSMiddleware
from app.models import StreamRequest, ChatRequest, GenerateRequest

# Load environment
load_dotenv()

# Initialize app
app = FastAPI(
    title="LangChain Streaming API",
    description="Real-time LLM token streaming with SSE",
    version="1.0.0"
)

# Add after creating app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global checkpointer for conversation persistence (replaces memory_store dict)
checkpointer = InMemorySaver()
metrics_handler = MetricsCallbackHandler()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as f:
        return f.read()


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ollama_url": os.getenv("OLLAMA_API_URL"),
        "model": os.getenv("OLLAMA_MODEL", "llama2")
    }


@app.post("/stream")
async def stream_response(request: StreamRequest):
    return StreamingResponse(
        stream_llm_response(
            query=request.query,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/stream/chat")
async def stream_chat(request: ChatRequest):
    return StreamingResponse(
        stream_chat_response(
            message=request.message,
            session_id=request.session_id,
            checkpointer=checkpointer,  # Use checkpointer instead of dict
            temperature=request.temperature
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )


@app.post("/generate")
async def generate_response(request: GenerateRequest):
    start_time = time.time()
    
    llm = ChatOllama(
        base_url=os.getenv("OLLAMA_API_URL", "http://ollama:11434"),
        model=os.getenv("OLLAMA_MODEL", "llama2"),
        temperature=request.temperature,
        callbacks=[metrics_handler]
    )
    
    # Use invoke with message dict instead of agenerate
    response = await llm.ainvoke(
        {"role": "user", "content": request.query}
    )
    elapsed = time.time() - start_time
    
    # Extract content from AIMessage
    response_text = response.content if hasattr(response, 'content') else str(response)
    
    return {
        "response": response_text,
        "time_seconds": round(elapsed, 3),
        "streaming": False
    }


@app.get("/metrics")
async def get_metrics():
    return metrics_handler.get_metrics()


@app.delete("/chat/{session_id}")
async def clear_chat_history(session_id: str):
    return {
        "message": f"To clear session {session_id}, delete from your backend storage",
        "note": "LangGraph checkpointer handles thread-level state automatically"
    }


def create_ollama_agent(temperature: float = 0.7):
    llm = ChatOllama(
        base_url=os.getenv("OLLAMA_API_URL", "http://ollama:11434"),
        model=os.getenv("OLLAMA_MODEL", "llama2"),
        temperature=temperature,
        callbacks=[metrics_handler]
    )
    
    # Create agent with checkpointer for conversation persistence
    agent = create_agent(
        model=llm,
        tools=[],  # Add tools here if needed
        checkpointer=checkpointer,
        system_prompt="You are a helpful assistant."
    )
    
    return agent


@app.post("/agent/invoke")
async def agent_invoke(request: ChatRequest):
    start_time = time.time()
    
    agent = create_ollama_agent(temperature=request.temperature)
    
    # Invoke with thread_id for state persistence
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": request.message}]},
        config={"configurable": {"thread_id": request.session_id}}
    )
    
    elapsed = time.time() - start_time
    
    # Extract final message from agent result
    final_message = result["messages"][-1]
    response_text = (
        final_message.content 
        if hasattr(final_message, 'content') 
        else str(final_message)
    )
    
    return {
        "response": response_text,
        "time_seconds": round(elapsed, 3),
        "session_id": request.session_id,
        "streaming": False
    }