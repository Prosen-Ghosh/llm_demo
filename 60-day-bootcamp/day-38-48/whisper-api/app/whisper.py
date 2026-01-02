from faster_whisper import WhisperModel
from app.config import settings
import logging
import time
import gc
import json
from typing import Optional

logger = logging.getLogger("whisper-api")

class WhisperService:
    _instance = None
    model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WhisperService, cls).__new__(cls)
        return cls._instance

    def load_model(self, model_size: str = None):
        target_size = model_size or settings.DEFAULT_MODEL_SIZE

        if self.model is not None and self.current_model_size == target_size:
            logger.info(f"Model {target_size} is already loaded.")
            return

        logger.info(f"Switching model to: {target_size}...")
        start_time = time.time()
        
        try:
            if self.model:
                del self.model
                gc.collect()
                logger.info("Previous model unloaded.")

            self.model = WhisperModel(
                model_size_or_path=target_size,
                device=settings.DEVICE,
                compute_type=settings.COMPUTE_TYPE,
                cpu_threads=settings.CPU_THREADS,
                num_workers=settings.NUMBER_OF_WORKERS,
                download_root=settings.MODEL_CACHE_DIR
            )
            self.current_model_size = target_size
            duration = time.time() - start_time
            logger.info(f"Model loaded successfully in {duration:.2f} seconds.")
        except Exception as e:
            logger.error(f"Failed to load model {target_size}: {str(e)}")
            raise e

    def transcribe_file(
            self, 
            file_path: str, 
            language: Optional[str] = None,
            beam_size: int = 5, 
            best_of: int = 5, 
            patience: float = 1.0,
            initial_prompt: str = None
    ):
        if not self.model:
            raise RuntimeError("Model not loaded. Please restart the service.")

        target_language = None if language == "auto" else language
        start_time = time.time()
        
        segments, info = self.model.transcribe(
            file_path, 
            beam_size=beam_size,
            best_of=best_of,
            language=target_language,
            condition_on_previous_text=False,
            temperature=0.0 if beam_size == 1 else [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            vad_filter=True,
            vad_parameters={"threshold": 0.5, "min_speech_duration_ms": 250},
            patience=patience,
            initial_prompt=initial_prompt
        )

        results = []
        full_text = ""
        
        for segment in segments:
            results.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            })
            full_text += segment.text + " "

        print(f"Segments: {segments}")
        inference_time = time.time() - start_time

        if target_language is None:
            logger.info(f"Detected language '{info.language}' with probability {info.language_probability:.2f}")

        return {
            "language": info.language,
            "model_used": self.current_model_size,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "inference_time": round(inference_time, 4),
            "real_time_factor": round(inference_time / info.duration, 2),
            "text": full_text.strip(),
            "segments": results
        }
    
    def stream_transcribe(
        self, 
        file_path: str, 
        language: str = "en",
        beam_size: int = 5,
        best_of: int = 5,
        patience: float = 1.0
    ):
        if not self.model:
            raise RuntimeError("Model not loaded. Please restart the service.")

        segments, info = self.model.transcribe(
            file_path, 
            beam_size=beam_size,
            best_of=best_of,
            language=language,
            condition_on_previous_text=False,
            temperature=0.0 if beam_size == 1 else [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            vad_filter=True,
            vad_parameters={"threshold": 0.5, "min_speech_duration_ms": 250},
            patience=patience
        )

        metadata = {
            "type": "metadata",
            "language": info.language,
            "duration": info.duration
        }
        yield f"data: {json.dumps(metadata)}\n\n"

        for segment in segments:
            chunk = {
                "type": "segment",
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            }
            yield f"data: {json.dumps(chunk)}\n\n"

        yield "data: [DONE]\n\n"

whisper_service = WhisperService()