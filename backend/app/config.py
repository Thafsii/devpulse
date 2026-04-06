"""
DevPulse Backend — Configuration
"""
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
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

    # App — comma-separated origins can be set via env var CORS_ORIGINS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "https://*.netlify.app"]
    DEBUG: bool = False

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Allow CORS_ORIGINS to be a comma-separated string in the env file."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


settings = Settings()

