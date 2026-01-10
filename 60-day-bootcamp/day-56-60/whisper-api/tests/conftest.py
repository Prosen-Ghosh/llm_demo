import pytest
import wave
import struct
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def dummy_audio(tmp_path):
    file_path = tmp_path / "test.wav"
    with wave.open(str(file_path), 'w') as f:
        f.setparams((1, 2, 44100, 44100, 'NONE', 'not compressed'))
        for _ in range(44100):
            value = struct.pack('<h', 0)
            f.writeframes(value)
    return file_path