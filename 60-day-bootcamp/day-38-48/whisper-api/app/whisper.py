from faster_whisper import WhisperModel
from app.config import settings
import logging
import time
import gc

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

    def transcribe_file(self, file_path: str, language: str = "en"):
        if not self.model:
            raise RuntimeError("Model not loaded. Please restart the service.")

        segments, info = self.model.transcribe(
            file_path, 
            beam_size=7,
            best_of= 5,
            language=language,
            condition_on_previous_text=False,
            temperature=[0.6, 0.7, 0.8, 0.9, 1.0],
            vad_filter=True,
            vad_parameters={"threshold": 0.5, "min_speech_duration_ms": 250},
            patience=1.5
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
        return {
            "language": info.language,
            "model_used": self.current_model_size,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "text": full_text.strip(),
            "segments": results
        }

whisper_service = WhisperService()