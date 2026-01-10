import asyncio
import os
import json
from typing import AsyncGenerator, Optional
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from app.callbacks import StreamingCallbackHandler


async def stream_llm_response(query: str, temperature: float = 0.7, max_tokens: int = 2048) -> AsyncGenerator[str, None]:
    queue = asyncio.Queue()
    callback = StreamingCallbackHandler(queue)
    
    llm = ChatOllama(
        base_url=os.getenv("OLLAMA_API_URL", "http://ollama:11434"),
        model=os.getenv("OLLAMA_MODEL", "llama2"),
        temperature=temperature,
        num_predict=max_tokens,
        callbacks=[callback]
    )
    
    async def generate():
        try:
            response = await llm.ainvoke(
                [{"role": "user", "content": query}]
            )
            
            if hasattr(response, 'content'):
                content = response.content
                for i in range(0, len(content), 3):  # Stream in chunks
                    await queue.put({ "type": "token", "content": content[i:i+3] })
                    await asyncio.sleep(0.01)  # Small delay for streaming effect
            else:
                text = str(response)
                for i in range(0, len(text), 3):
                    await queue.put({ "type": "token", "content": text[i:i+3] })
                    await asyncio.sleep(0.01)
                    
        except Exception as e:
            await queue.put({"type": "error", "error": str(e)})
        finally:
            await queue.put(None) 
    task = asyncio.create_task(generate())
    
    try:
        while True:
            message = await queue.get()
            
            if message is None:  # End signal
                yield "event: end\ndata: {\"type\": \"end\"}\n\n"
                break
            
            if message["type"] == "token":
                yield f"data: {json.dumps({'type': 'token', 'content': message['content']})}\n\n"
            elif message["type"] == "error":
                yield f"event: error\ndata: {json.dumps({'error': message['error']})}\n\n"
    
    except asyncio.CancelledError:
        pass
    finally:
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


async def stream_chat_response(
    message: str,
    session_id: str,
    checkpointer: InMemorySaver,
    temperature: float = 0.7
) -> AsyncGenerator[str, None]:
    queue = asyncio.Queue()
    
    # Initialize callback and LLM
    callback = StreamingCallbackHandler(queue)
    
    llm = ChatOllama(
        base_url=os.getenv("OLLAMA_API_URL", "http://ollama:11434"),
        model=os.getenv("OLLAMA_MODEL", "llama2"),
        temperature=temperature,
        callbacks=[callback]
    )
    
    # Use a simpler approach without agent for now
    async def generate():
        try:
            # Stream directly from LLM
            async for chunk in llm.astream(
                {"role": "user", "content": message}
            ):
                if hasattr(chunk, 'content'):
                    await queue.put({"type": "token", "content": chunk.content})
                elif isinstance(chunk, dict) and 'content' in chunk:
                    await queue.put({"type": "token", "content": chunk['content']})
        except Exception as e:
            await queue.put({"type": "error", "error": str(e)})
        finally:
            await queue.put(None)
    
    task = asyncio.create_task(generate())
    
    # Stream tokens as SSE
    try:
        while True:
            msg = await queue.get()
            
            if msg is None:
                yield "event: end\ndata: {\"type\": \"end\"}\n\n"
                break
            
            if msg["type"] == "token":
                yield f"data: {json.dumps({'type': 'token', 'content': msg['content']})}\n\n"
            elif msg["type"] == "error":
                yield f"event: error\ndata: {json.dumps({'error': msg['error']})}\n\n"
    
    except asyncio.CancelledError:
        pass
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass