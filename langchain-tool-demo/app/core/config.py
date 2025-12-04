from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Shopping Assistant API"
    ollama_model: str = "gpt-oss:120b-cloud"
    ollama_base_url: str = "http://host.docker.internal:11434"
    
    class Config:
        env_file = ".env"

settings = Settings()