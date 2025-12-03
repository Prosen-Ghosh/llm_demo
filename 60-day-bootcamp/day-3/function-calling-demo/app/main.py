from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import ChatRequest, ChatResponse, ChatMessage, ToolResult
from app.services.llm_client import LLMClient
from app.services.tool_executor import ToolExecutor
from app.tools.registry import tool_registry
from app.utils.logger import logger
from typing import List
import json

app = FastAPI(
    title="Function Calling Demo",
    description="Enterprise-grade function calling system with OpenRouter",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_client = LLMClient()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "tools_registered": len(tool_registry.get_all_tools())}


@app.get("/tools")
async def list_tools():
    tools = tool_registry.get_all_tools()
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters_schema.model_json_schema()
            }
            for tool in tools
        ]
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        # Initialize conversation
        messages = request.conversation_history.copy()
        messages.append(ChatMessage(role="user", content=request.message))
        
        tool_schemas = tool_registry.get_ollama_schemas()
        all_tool_results: List[ToolResult] = []
        max_iterations = 5  # Prevent infinite loops
        
        for iteration in range(max_iterations):
            # Call LLM
            response = await llm_client.chat(
                messages=llm_client.format_messages(messages),
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                tools=tool_schemas
            )
            
            assistant_message = response.get("message", {})
            tool_calls = llm_client.parse_tool_calls(response)
            
            # No tool calls - final response reached
            if not tool_calls:
                final_content = assistant_message.get("content", "")
                messages.append(ChatMessage(
                    role="assistant",
                    content=final_content
                ))
                
                return ChatResponse(
                    response=final_content,
                    tool_results=all_tool_results,
                    conversation_history=messages
                )
            
            # Execute tool calls in parallel
            logger.info("executing_tools", tool_count=len(tool_calls), iteration=iteration)
            
            messages.append(ChatMessage(
                role="assistant",
                content=assistant_message.get("content") or "",
                tool_calls=tool_calls
            ))
            
            tool_execution_data = [
                {"name": tc.name, "arguments": tc.arguments}
                for tc in tool_calls
            ]
            
            tool_results = await ToolExecutor.execute_parallel(tool_execution_data)
            all_tool_results.extend(tool_results)
            
            # Add tool results to messages
            for tool_call, result in zip(tool_calls, tool_results):
                tool_message_content = json.dumps({
                    "status": result.status.value,
                    "result": result.result,
                    "error": result.error
                }) if result.status != "success" else json.dumps(result.result)
                
                messages.append(ChatMessage(
                    role="tool",
                    content=tool_message_content,
                    tool_call_id=tool_call.id
                ))
        
        # Max iterations reached
        raise HTTPException(
            status_code=500,
            detail="Maximum tool calling iterations reached"
        )
        
    except Exception as e:
        logger.error("chat_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))