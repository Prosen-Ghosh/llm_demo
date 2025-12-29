def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_transcribe_flow(client, dummy_audio):
    with open(dummy_audio, "rb") as f:
        response = client.post(
            "/transcribe",
            files={"file": ("test.wav", f, "audio/wav")}
        )
    assert response.status_code == 200
    assert "text" in response.json()
    assert "duration" in response.json()

def test_unsupported_file_type(client):
    response = client.post(
        "/transcribe",
        files={"file": ("test.txt", b"hello world", "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]