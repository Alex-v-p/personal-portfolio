from pydantic import AliasChoices, Field
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

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
