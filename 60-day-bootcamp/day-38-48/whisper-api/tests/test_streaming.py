import pytest
import httpx
import json

@pytest.mark.asyncio
async def test_streaming_endpoint(dummy_audio):
    url = "http://localhost:8000/stream?language=en"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        with open(dummy_audio, "rb") as f:
            async with client.stream(
                "POST", 
                url, 
                files={"file": ("stream_test.wav", f, "audio/wav")}
            ) as response:
                
                assert response.status_code == 200
                chunk_count = 0
                async for line in response.aiter_lines():
                    if not line.strip(): 
                        continue 
                    
                    if line.startswith("data: "):
                        data_str = line.replace("data: ", "")
                        
                        if data_str == "[DONE]":
                            break
                        
                        data = json.loads(data_str)
                        chunk_count += 1
                        
                        if data.get("type") == "metadata":
                            assert "duration" in data
                        elif data.get("type") == "segment":
                            assert "text" in data

                assert chunk_count > 0