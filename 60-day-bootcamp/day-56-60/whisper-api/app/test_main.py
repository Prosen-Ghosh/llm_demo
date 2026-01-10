from fastapi.testclient import TestClient
from app.main import app
import wave
import struct
import os
import pytest

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data
    assert data["cpu_cores_available"] > 0

def test_health_check_model_status():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["model_loaded"] is True
    assert "model_size" in data

def test_internal_transcription_flow():
    response = client.post("/test-transcribe")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "processing_time" in data
    assert "result" in data

@pytest.fixture
def valid_wav_file(tmp_path):
    """
    Fixture that creates a valid 1-second silent WAV file
    and returns the path.
    """
    file_path = tmp_path / "test_speech.wav"
    with wave.open(str(file_path), 'w') as f:
        f.setparams((1, 2, 44100, 44100, 'NONE', 'not compressed'))
        # Write 1 second of silence
        for _ in range(44100):
            value = struct.pack('<h', 0)
            f.writeframes(value)
    return file_path

def test_transcribe_endpoint(valid_wav_file):
    with open(valid_wav_file, "rb") as f:
        response = client.post(
            "/transcribe",
            files={"file": ("test_speech.wav", f, "audio/wav")}
        )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["filename"] == "test_speech.wav"
    assert "text" in data
    assert "language" in data

def test_invalid_extension():
    response = client.post(
        "/transcribe",
        files={"file": ("test.txt", b"dummy content", "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]