import time
from app.whisper import whisper_service

def test_inference_speed(dummy_audio):
    start_time = time.perf_counter()
    
    for _ in range(3):
        whisper_service.transcribe_file(str(dummy_audio))
        
    avg_time = (time.perf_counter() - start_time) / 3
    print(f"\nAverage Inference Time (CPU): {avg_time:.4f}s")
    assert avg_time < 5.0 