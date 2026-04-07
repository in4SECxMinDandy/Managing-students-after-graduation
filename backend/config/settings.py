"""Application settings."""
from functools import lru_cache
from typing import Annotated

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: Annotated[str, Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/qlsvsdh",
        validation_alias="DATABASE_URL",
    )]
    database_url_sync: Annotated[str | None, Field(default=None, validation_alias="DATABASE_URL_SYNC")] = None

    @computed_field
    @property
    def sync_database_url(self) -> str:
        """Get sync database URL for Alembic CLI."""
        if self.database_url_sync:
            return self.database_url_sync
        url = str(self.database_url)
        return url.replace("postgresql+asyncpg", "postgresql+psycopg2")

    # Security
    secret_key: str = Field(default="change-me", validation_alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", validation_alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=1440, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_days: int = Field(
        default=7, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS"
    )

    # CORS — store as comma-separated string so .env does not need JSON (list[str] breaks DotEnv)
    cors_origins_raw: str = Field(
        default="http://localhost:8501",
        validation_alias="CORS_ORIGINS",
    )

    @computed_field
    @property
    def cors_origins(self) -> list[str]:
        return [x.strip() for x in self.cors_origins_raw.split(",") if x.strip()]

    # App info
    app_name: str = "QLSVSDH"
    app_version: str = "0.1.0"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
