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
    media_storage_endpoint: str = Field(
        default='minio:9000',
        validation_alias=AliasChoices('MEDIA_STORAGE_ENDPOINT', 'PORTFOLIO_API_MEDIA_STORAGE_ENDPOINT'),
    )
    media_storage_access_key: str = Field(
        default='minioadmin',
        validation_alias=AliasChoices('MEDIA_STORAGE_ACCESS_KEY', 'PORTFOLIO_API_MEDIA_STORAGE_ACCESS_KEY'),
    )
    media_storage_secret_key: str = Field(
        default='minioadmin',
        validation_alias=AliasChoices('MEDIA_STORAGE_SECRET_KEY', 'PORTFOLIO_API_MEDIA_STORAGE_SECRET_KEY'),
    )
    media_storage_secure: bool = Field(
        default=False,
        validation_alias=AliasChoices('MEDIA_STORAGE_SECURE', 'PORTFOLIO_API_MEDIA_STORAGE_SECURE'),
    )
    media_public_bucket: str = Field(
        default='portfolio',
        validation_alias=AliasChoices('MEDIA_PUBLIC_BUCKET', 'PORTFOLIO_API_MEDIA_PUBLIC_BUCKET'),
    )
    media_max_upload_bytes: int = Field(
        default=10_485_760,
        validation_alias=AliasChoices('MEDIA_MAX_UPLOAD_BYTES', 'PORTFOLIO_API_MEDIA_MAX_UPLOAD_BYTES'),
    )
    github_stats_username: str = Field(
        default='Alex-v-p',
        validation_alias=AliasChoices('GITHUB_STATS_USERNAME', 'PORTFOLIO_API_GITHUB_STATS_USERNAME'),
    )
    github_api_token: str = Field(
        default='',
        validation_alias=AliasChoices('GITHUB_API_TOKEN', 'PORTFOLIO_API_GITHUB_API_TOKEN'),
    )
    github_stats_lookback_days: int = Field(
        default=365,
        validation_alias=AliasChoices('GITHUB_STATS_LOOKBACK_DAYS', 'PORTFOLIO_API_GITHUB_STATS_LOOKBACK_DAYS'),
    )

    knowledge_embedding_backend: str = Field(
        default='ollama',
        validation_alias=AliasChoices('KNOWLEDGE_EMBEDDING_BACKEND', 'PORTFOLIO_API_KNOWLEDGE_EMBEDDING_BACKEND'),
    )
    knowledge_embedding_model: str = Field(
        default='nomic-embed-text',
        validation_alias=AliasChoices('KNOWLEDGE_EMBEDDING_MODEL', 'PORTFOLIO_API_KNOWLEDGE_EMBEDDING_MODEL'),
    )
    knowledge_embedding_base_url: str = Field(
        default='http://ollama:11434',
        validation_alias=AliasChoices('KNOWLEDGE_EMBEDDING_BASE_URL', 'PORTFOLIO_API_KNOWLEDGE_EMBEDDING_BASE_URL'),
    )
    knowledge_embedding_api_key: str = Field(
        default='',
        validation_alias=AliasChoices('KNOWLEDGE_EMBEDDING_API_KEY', 'PORTFOLIO_API_KNOWLEDGE_EMBEDDING_API_KEY'),
    )
    knowledge_embedding_timeout_seconds: float = Field(
        default=20.0,
        validation_alias=AliasChoices('KNOWLEDGE_EMBEDDING_TIMEOUT_SECONDS', 'PORTFOLIO_API_KNOWLEDGE_EMBEDDING_TIMEOUT_SECONDS'),
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
