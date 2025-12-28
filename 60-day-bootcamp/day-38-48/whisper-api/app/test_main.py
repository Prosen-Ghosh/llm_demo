from fastapi.testclient import TestClient
from app.main import app

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