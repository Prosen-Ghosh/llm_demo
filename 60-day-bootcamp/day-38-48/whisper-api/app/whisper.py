from faster_whisper import WhisperModel
from app.config import settings
import logging
import time

logger = logging.getLogger("whisper-api")

class WhisperService:
    _instance = None
    model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WhisperService, cls).__new__(cls)
        return cls._instance

    def load_model(self):
        if self.model is not None:
            logger.info("Model already loaded.")
            return

        logger.info(f"Loading Whisper model: {settings.WHISPER_MODEL_SIZE}...")
        start_time = time.time()
        
        try:
            self.model = WhisperModel(
                model_size_or_path=settings.WHISPER_MODEL_SIZE,
                device=settings.DEVICE,
                compute_type=settings.COMPUTE_TYPE,
                cpu_threads=settings.CPU_THREADS,
                download_root=settings.MODEL_CACHE_DIR
            )
            
            duration = time.time() - start_time
            logger.info(f"Model loaded successfully in {duration:.2f} seconds.")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise e

    def transcribe_file(self, file_path: str):
        if not self.model:
            raise RuntimeError("Model not loaded. Please restart the service.")

        segments, info = self.model.transcribe(
            file_path, 
            beam_size=5,
            language="en", # Defaulting to English for Phase 2
            condition_on_previous_text=False
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

        return {
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "text": full_text.strip(),
            "segments": results
        }

whisper_service = WhisperService()