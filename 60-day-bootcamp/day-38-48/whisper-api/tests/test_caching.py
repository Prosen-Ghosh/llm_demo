import pytest
import time
from app.caching import results_cache

def test_cache_hit_mechanism(client, dummy_audio):
    with open(dummy_audio, "rb") as f:
        resp1 = client.post(
            "/v2/batch-transcribe?language=en",
            files=[("files", ("fileA.wav", f, "audio/wav"))]
        )
    job_id_1 = resp1.json()[0]
    
    for _ in range(10):
        if client.get(f"/v2/jobs/{job_id_1}").json()["status"] == "completed":
            break
        time.sleep(1)

    with open(dummy_audio, "rb") as f:
        resp2 = client.post(
            "/v2/batch-transcribe?language=en",
            files=[("files", ("fileB_duplicate.wav", f, "audio/wav"))]
        )
    job_id_2 = resp2.json()[0]
    
    for _ in range(10):
        data = client.get(f"/v2/jobs/{job_id_2}").json()
        if data["status"] == "completed":
            assert data["result"]["cached"] is True
            break
        time.sleep(1)