from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # Ollama Configuration
    ollama_api_key: str
    ollama_base_url: str = "http://localhost:11434"
    default_model: str = "gpt-oss:120b-cloud"
    
    # Tool Execution
    tool_timeout_seconds: int = 5
    max_tool_retries: int = 3
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/tool_execution.jsonl"
    
    # API Settings
    api_rate_limit: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()