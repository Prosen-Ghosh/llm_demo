from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Streaming LLM API"
    version: str = "2.0.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    
    # OpenRouter (Required)
    openrouter_api_key: str
    
    # Ollama (Optional)
    ollama_base_url: str = "http://localhost:11434"
    ollama_default_model: str = "deepseek-r1:8b"
    
    # Rate Limiting
    max_requests_per_minute: int = 20
    
    # Request Configuration
    request_timeout: int = 60
    
    # Security
    api_key_min_length: int = 10
    
    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()