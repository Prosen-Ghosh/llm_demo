from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Faster Whisper API"
    VERSION: str = "1.0.0"
    DEBUG_MODE: bool = False
    LOG_LEVEL: str = "INFO"

    WHISPER_MODEL_SIZE: str = "large-v3"
    DEVICE: str = "cpu"
    COMPUTE_TYPE: str = "int8_float32"
    CPU_THREADS: int = 1
    
    MODEL_CACHE_DIR: str = "/root/.cache/huggingface"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"  # Optional but recommended
    )

settings = Settings()