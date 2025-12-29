import pytest
from unittest.mock import MagicMock
from app.whisper import whisper_service

# Mock the internal transcribe method to avoid needing real Bangla audio files
# just to test the API logic flow.
def mock_transcribe_bn(file_path, language="en"):
    return {
        "language": "bn",
        "language_probability": 0.95,
        "duration": 5.0,
        "model_used": "tiny", # Simulating we are on tiny
        "text": "আমি বাংলায় কথা বলি",
        "segments": []
    }

def test_bangla_warning_on_tiny_model(client, dummy_audio, monkeypatch):
    whisper_service.current_model_size = "tiny"
    
    monkeypatch.setattr(whisper_service, "transcribe_file", mock_transcribe_bn)
    with open(dummy_audio, "rb") as f:
        response = client.post(
            "/transcribe?language=bn",
            files={"file": ("test.wav", f, "audio/wav")}
        )
            
    assert response.status_code == 200
    data = response.json()
    
    assert data["language"] == "bn"
    assert "system_warning" in data
    assert "may yield poor results" in data["system_warning"]["message"]
    assert "আমি বাংলায় কথা বলি" in data["text"]

def test_no_warning_on_english(client, dummy_audio, monkeypatch):
    whisper_service.current_model_size = "tiny"
    monkeypatch.setattr(whisper_service, "transcribe_file", lambda f, language: {
        "language": "en", "language_probability": 0.99, "duration": 1.0, 
        "model_used": "tiny", "text": "Hello", "segments": []
    })

    with open(dummy_audio, "rb") as f:
        response = client.post(
            "/transcribe?language=en",
            files={"file": ("test.wav", f, "audio/wav")}
        )
    
    data = response.json()
    assert "system_warning" not in data