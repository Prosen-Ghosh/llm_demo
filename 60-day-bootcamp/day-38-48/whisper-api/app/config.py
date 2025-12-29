from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Faster Whisper API"
    VERSION: str = "1.0.0"
    DEBUG_MODE: bool = False
    LOG_LEVEL: str = "INFO"

    DEFAULT_MODEL_SIZE: str = "large-v3"
    ALLOWED_MODELS: List[str] = ["tiny", "base", "small", "medium", "large-v2", "large-v3"]
    DEVICE: str = "cpu"
    COMPUTE_TYPE: str = "int8_float32"
    CPU_THREADS: int = 2
    NUMBER_OF_WORKERS: int = 4
    
    MODEL_CACHE_DIR: str = "/root/.cache/huggingface"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"  # Optional but recommended
    )

settings = Settings()