from __future__ import annotations

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Portfolio API"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8001
    database_url: str = "postgresql+psycopg://portfolio_user:portfolio_pass@postgres:5432/portfolio_platform"
    secret_key: str = "change-me"
    redis_url: str = "redis://redis:6379/0"
    cors_allowed_origins: str = "http://localhost:4200,http://127.0.0.1:4200"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def cors_allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(',') if origin.strip()]


settings = Settings()
