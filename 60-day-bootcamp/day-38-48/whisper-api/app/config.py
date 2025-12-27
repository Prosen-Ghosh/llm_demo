from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Faster Whisper API"
    VERSION: str = "1.0.0"
    DEBUG_MODE: bool = False
    LOG_LEVEL: str = "INFO"
    
    # We will use this in Phase 2 for model storage
    MODEL_PATH: str = "/root/.cache/huggingface"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"  # Optional but recommended
    )

settings = Settings()