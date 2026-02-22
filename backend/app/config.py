from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings parsed from environment variables.
    """
    # Server
    backend_port: int = 8000
    
    # CORS
    allowed_origins: str = "http://localhost:3000"

    # LLM Providers
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None
    ollama_base_url: str = "http://ollama:11434"

    # Redis
    redis_url: str = "redis://redis:6379"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated string to list of origins."""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache()
def get_settings() -> Settings:
    """
    Dependency injection for settings.
    lru_cache ensures we only load the .env file once.
    """
    return Settings()
