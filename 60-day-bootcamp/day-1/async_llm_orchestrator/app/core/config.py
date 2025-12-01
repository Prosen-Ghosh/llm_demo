from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_api_key: str = ""
    openrouter_api_key: str = ""
    max_concurrent_requests: int = 10
    request_timeout: int = 30
    max_retries: int = 3
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"