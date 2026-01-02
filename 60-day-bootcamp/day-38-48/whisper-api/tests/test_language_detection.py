import pytest
from unittest.mock import MagicMock
from app.whisper import whisper_service

def test_auto_detection_spanish(client, dummy_audio, monkeypatch):
    mock_info = MagicMock()
    mock_info.language = "en"
    mock_info.language_probability = 0.98
    mock_info.duration = 5.0
    
    def mock_segments():
        return []
        
    def mock_transcribe(*args, **kwargs):
        assert kwargs.get("language") is None
        return (mock_segments(), mock_info)

    monkeypatch.setattr(whisper_service.model, "transcribe", mock_transcribe)

    with open(dummy_audio, "rb") as f:
        response = client.post(
            "/v2/batch-transcribe?language=auto",
            files=[("files", ("english_test.wav", f, "audio/wav"))]
        )
    
    job_id = response.json()[0]
    
    import time
    time.sleep(0.5)
    
    status_response = client.get(f"/v2/jobs/{job_id}")
    data = status_response.json()
    
    assert data["status"] == "completed"
    result = data["result"]
    
    assert result["language"] == "en"