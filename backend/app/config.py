"""
DevPulse Backend — Configuration
"""
from typing import Any
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
    )

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    # OpenAI
    OPENAI_API_KEY: str = ""

    # GitHub
    GITHUB_PAT: str = ""

    # Product Hunt
    PRODUCTHUNT_TOKEN: str = ""

    # Scheduler
    SCRAPE_INTERVAL_HOURS: int = 2

    # CORS — stored as a raw string, parsed to list by the validator below.
    # Using str avoids pydantic-settings' JSON-decode attempt for list[str] fields.
    CORS_ORIGINS: Any = "http://localhost:3000,https://*.netlify.app"
    DEBUG: bool = False

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse CORS_ORIGINS from a comma-separated string or a list."""
        if isinstance(v, list):
            return [str(o).strip() for o in v if str(o).strip()]
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return ["http://localhost:3000"]


settings = Settings()
