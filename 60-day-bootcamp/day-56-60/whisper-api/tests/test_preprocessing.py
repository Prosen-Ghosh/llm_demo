import pytest
import wave
import os
from app.preprocessing import normalize_audio

def test_normalization_properties(dummy_audio):
    processed_path = normalize_audio(str(dummy_audio))
    
    assert os.path.exists(processed_path)
    assert processed_path != str(dummy_audio)

    with wave.open(processed_path, 'r') as wf:
        channels = wf.getnchannels()
        framerate = wf.getframerate()
        assert channels == 1, f"Expected Mono (1), got {channels}"
        assert framerate == 16000, f"Expected 16kHz, got {framerate}"

    os.remove(processed_path)