import pytest
import time
from app.whisper import whisper_service

def test_turbo_vs_accurate_speed(dummy_audio):
    whisper_service.transcribe_file(str(dummy_audio), beam_size=1)
    
    start = time.perf_counter()
    whisper_service.transcribe_file(str(dummy_audio), beam_size=1, best_of=1)
    turbo_time = time.perf_counter() - start
    
    start = time.perf_counter()
    whisper_service.transcribe_file(str(dummy_audio), beam_size=5, best_of=5)
    accurate_time = time.perf_counter() - start
    
    print(f"\nTurbo: {turbo_time:.4f}s | Accurate: {accurate_time:.4f}s")
    