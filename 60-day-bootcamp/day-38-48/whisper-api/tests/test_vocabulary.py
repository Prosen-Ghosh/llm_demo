import pytest
from unittest.mock import MagicMock
from app.whisper import whisper_service

def test_custom_vocabulary_passing(client, dummy_audio, monkeypatch):
    mock_transcribe = MagicMock()
    mock_transcribe.return_value = ([], MagicMock(language="en", duration=1.0))
    
    if whisper_service.model is None:
        whisper_service.model = MagicMock()
        
    monkeypatch.setattr(whisper_service.model, "transcribe", mock_transcribe)

    with open(dummy_audio, "rb") as f:
        client.post(
            "/v2/batch-transcribe?keywords=Jashore,Khulna,Benapole",
            files=[("files", ("vocab_test.wav", f, "audio/wav"))]
        )
    
    import time
    time.sleep(0.5)

    call_args = mock_transcribe.call_args
    assert call_args is not None
    
    kwargs = call_args[1]
    assert "initial_prompt" in kwargs
    assert kwargs["initial_prompt"] == "Glossary: Jashore,Khulna,Benapole."