import time
import pytest
from app.jobs import JobStatus

def test_batch_upload_and_poll(client, dummy_audio):
    with open(dummy_audio, "rb") as f1, open(dummy_audio, "rb") as f2:
        response = client.post(
            "/v2/batch-transcribe?language=en",
            files=[
                ("files", ("audio1.wav", f1, "audio/wav")),
                ("files", ("audio2.wav", f2, "audio/wav"))
            ]
        )
    
    assert response.status_code == 200
    job_ids = response.json()
    assert len(job_ids) == 2
    
    target_job = job_ids[0]
    max_retries = 10
    
    for _ in range(max_retries):
        response = client.get(f"/v2/jobs/{target_job}")
        assert response.status_code == 200
        data = response.json()
        
        status = data["status"]
        if status == JobStatus.COMPLETED:
            assert "text" in data["result"]
            break
        elif status == JobStatus.FAILED:
            pytest.fail(f"Job failed: {data.get('error')}")
        
        time.sleep(1)
    else:
        pytest.fail("Job timed out (stuck in processing)")