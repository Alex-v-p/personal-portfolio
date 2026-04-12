from __future__ import annotations

from functools import lru_cache

from pydantic import AliasChoices, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default='Assistant Service', validation_alias=AliasChoices('APP_NAME', 'ASSISTANT_API_NAME'))
    app_env: str = Field(default='development', validation_alias=AliasChoices('APP_ENV', 'ASSISTANT_API_ENV'))
    app_host: str = Field(default='0.0.0.0', validation_alias=AliasChoices('APP_HOST', 'ASSISTANT_API_HOST'))
    app_port: int = Field(default=8012, validation_alias=AliasChoices('APP_PORT', 'ASSISTANT_API_PORT'))
    database_url: str = Field(
        default='postgresql+psycopg://portfolio_user:portfolio_pass@postgres:5432/portfolio_platform',
        validation_alias=AliasChoices('DATABASE_URL', 'ASSISTANT_API_DB_URL'),
    )
    secret_key: str = Field(default='change-me', validation_alias=AliasChoices('SECRET_KEY', 'ASSISTANT_API_SECRET_KEY'))
    redis_url: str = Field(
        default='redis://redis:6379/0',
        validation_alias=AliasChoices('REDIS_URL', 'ASSISTANT_API_REDIS_URL'),
    )
    cors_allowed_origins: str = Field(
        default='http://localhost:4200,http://127.0.0.1:4200',
        validation_alias=AliasChoices('CORS_ALLOWED_ORIGINS', 'ASSISTANT_API_CORS_ALLOWED_ORIGINS'),
    )
    provider_backend: str = Field(
        default='mock',
        validation_alias=AliasChoices('ASSISTANT_PROVIDER_BACKEND', 'PROVIDER_BACKEND'),
    )
    provider_model: str = Field(
        default='qwen2.5:3b',
        validation_alias=AliasChoices('ASSISTANT_PROVIDER_MODEL', 'PROVIDER_MODEL'),
    )
    provider_base_url: str = Field(
        default='http://ollama:11434',
        validation_alias=AliasChoices('ASSISTANT_PROVIDER_BASE_URL', 'PROVIDER_BASE_URL'),
    )
    provider_api_key: str = Field(
        default='',
        validation_alias=AliasChoices('ASSISTANT_PROVIDER_API_KEY', 'PROVIDER_API_KEY'),
    )
    retrieval_chunk_limit: int = Field(
        default=5,
        validation_alias=AliasChoices('ASSISTANT_RETRIEVAL_CHUNK_LIMIT', 'RETRIEVAL_CHUNK_LIMIT'),
    )
    retrieval_candidate_limit: int = Field(
        default=18,
        validation_alias=AliasChoices('ASSISTANT_RETRIEVAL_CANDIDATE_LIMIT', 'RETRIEVAL_CANDIDATE_LIMIT'),
    )
    max_history_messages: int = Field(
        default=10,
        validation_alias=AliasChoices('ASSISTANT_MAX_HISTORY_MESSAGES', 'MAX_HISTORY_MESSAGES'),
    )

    retrieval_embedding_backend: str = Field(
        default='ollama',
        validation_alias=AliasChoices('ASSISTANT_RETRIEVAL_EMBEDDING_BACKEND', 'RETRIEVAL_EMBEDDING_BACKEND'),
    )
    retrieval_embedding_model: str = Field(
        default='nomic-embed-text',
        validation_alias=AliasChoices('ASSISTANT_RETRIEVAL_EMBEDDING_MODEL', 'RETRIEVAL_EMBEDDING_MODEL'),
    )
    retrieval_embedding_base_url: str = Field(
        default='http://ollama:11434',
        validation_alias=AliasChoices('ASSISTANT_RETRIEVAL_EMBEDDING_BASE_URL', 'RETRIEVAL_EMBEDDING_BASE_URL'),
    )
    retrieval_embedding_api_key: str = Field(
        default='',
        validation_alias=AliasChoices('ASSISTANT_RETRIEVAL_EMBEDDING_API_KEY', 'RETRIEVAL_EMBEDDING_API_KEY'),
    )
    retrieval_embedding_timeout_seconds: float = Field(
        default=20.0,
        validation_alias=AliasChoices('ASSISTANT_RETRIEVAL_EMBEDDING_TIMEOUT_SECONDS', 'RETRIEVAL_EMBEDDING_TIMEOUT_SECONDS'),
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
