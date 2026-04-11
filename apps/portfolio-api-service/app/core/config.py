from __future__ import annotations

from functools import lru_cache

from pydantic import AliasChoices, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default='Portfolio API', validation_alias=AliasChoices('APP_NAME', 'PORTFOLIO_API_NAME'))
    app_env: str = Field(default='development', validation_alias=AliasChoices('APP_ENV', 'PORTFOLIO_API_ENV'))
    app_host: str = Field(default='0.0.0.0', validation_alias=AliasChoices('APP_HOST', 'PORTFOLIO_API_HOST'))
    app_port: int = Field(default=8011, validation_alias=AliasChoices('APP_PORT', 'PORTFOLIO_API_PORT'))
    database_url: str = Field(
        default='postgresql+psycopg://portfolio_user:portfolio_pass@postgres:5432/portfolio_platform',
        validation_alias=AliasChoices('DATABASE_URL', 'PORTFOLIO_API_DB_URL'),
    )
    secret_key: str = Field(default='change-me', validation_alias=AliasChoices('SECRET_KEY', 'PORTFOLIO_API_SECRET_KEY'))
    redis_url: str = Field(
        default='redis://redis:6379/0',
        validation_alias=AliasChoices('REDIS_URL', 'PORTFOLIO_API_REDIS_URL'),
    )
    cors_allowed_origins: str = Field(
        default='http://localhost:4200,http://127.0.0.1:4200',
        validation_alias=AliasChoices('CORS_ALLOWED_ORIGINS', 'PORTFOLIO_API_CORS_ALLOWED_ORIGINS'),
    )
    media_public_base_url: str = Field(
        default='http://localhost:9000',
        validation_alias=AliasChoices('MEDIA_PUBLIC_BASE_URL', 'PORTFOLIO_API_MEDIA_PUBLIC_BASE_URL'),
    )
    admin_access_token_expire_minutes: int = Field(
        default=480,
        validation_alias=AliasChoices('ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES', 'PORTFOLIO_API_ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES'),
    )

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @computed_field  # type: ignore[prop-decorator]
    @property
    def cors_allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(',') if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
