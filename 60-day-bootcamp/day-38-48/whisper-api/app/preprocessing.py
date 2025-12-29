import ffmpeg
import os
import logging
from pathlib import Path

logger = logging.getLogger("whisper-api")

def normalize_audio(input_path: str) -> str:
    try:
        path_obj = Path(input_path)
        output_path = path_obj.parent / f"{path_obj.stem}_processed.wav"
        
        logger.info(f"Normalizing audio: {input_path} -> {output_path}")
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, str(output_path), ar=16000, ac=1, acodec='pcm_s16le')
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
        
        return str(output_path)

    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else str(e)
        logger.error(f"FFmpeg conversion failed: {error_message}")
        raise RuntimeError(f"Audio processing failed: {error_message}")