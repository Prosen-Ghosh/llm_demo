# tests/test_api.py
from fastapi.testclient import TestClient
from src.main import app
import uuid

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_ingest_validation_error():
    payload = {
        "documents": [
            {
                "id": "string",
                "content": "string",
                "source": "manual",
                "created_at": "2026-01-11T17:22:29.646Z",
                "metadata": {
                    "additionalProp1": {}
                }
            }
        ]
    }
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_ingest_success():
    payload = {
        "documents": [
            {
                "id": str(uuid.uuid4()),
                "title": "string",
                "content": "string",
                "source": "manual",
                "created_at": "2026-01-11T17:22:29.646Z",
                "metadata": {
                    "additionalProp1": {}
                }
            }
        ]
    }
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["processed_count"] == 1
    assert "document_ids" in data