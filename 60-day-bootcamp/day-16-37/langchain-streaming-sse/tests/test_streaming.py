import pytest
from streaming import stream_llm_response, stream_chat_response


@pytest.mark.asyncio
async def test_stream_llm_response():
    query = "Count to 3"
    token_count = 0
    
    async for event in stream_llm_response(query, temperature=0.1, max_tokens=50):
        if event.startswith("data: "):
            token_count += 1
    
    assert token_count > 0


@pytest.mark.asyncio
async def test_stream_chat_response():
    memory_store = {}
    session_id = "test_session"
    
    message = "Hello"
    token_count = 0
    
    async for event in stream_chat_response(
        message, session_id, memory_store, temperature=0.1
    ):
        if event.startswith("data: "):
            token_count += 1
    
    assert token_count > 0
    assert session_id in memory_store


if __name__ == "__main__":
    pytest.main([__file__, "-v"])