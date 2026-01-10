# /app/app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # This should ignore extra fields
    )
    
    # Ollama Configuration
    ollama_base_url: str = "http://ollama:11434"
    ollama_model: str = "gpt-oss:120b-cloud"
    ollama_api_key: str = ""
    
    # OpenRouter Configuration
    openrouter_api_key: str = ""
    openrouter_model: str = "meta-llama/llama-3.2-3b-instruct:free"
    
    # Application Settings
    environment: str = "development"
    log_level: str = "INFO"
    max_retries: int = 2
    enable_openrouter_fallback: bool = True
    database_url: str = "sqlite+aiosqlite:///./data/prompts.db"


# Create an instance
settings = Settings()