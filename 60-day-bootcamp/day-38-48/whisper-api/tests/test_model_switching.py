import pytest
from app.config import settings

def test_model_switching_flow(client, dummy_audio):
    response = client.get("/health")
    assert response.json()["status"] == "healthy"
    
    response = client.put("/system/model?model_size=base")
    assert response.status_code == 200
    assert response.json()["current_model"] == "base"
    with open(dummy_audio, "rb") as f:
        response = client.post(
            "/transcribe?language=en",
            files={"file": ("test.wav", f, "audio/wav")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "base"
    client.put("/system/model?model_size=tiny")