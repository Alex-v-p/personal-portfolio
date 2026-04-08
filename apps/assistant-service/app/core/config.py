from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Assistant Service"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8002
    database_url: str = "postgresql+psycopg://portfolio_user:portfolio_pass@postgres:5432/portfolio_platform"
    secret_key: str = "change-me"
    redis_url: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
