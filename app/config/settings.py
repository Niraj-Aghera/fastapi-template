"""Application settings class."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

from app.utils.enums import AppEnv

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    """Application settings class.

    This class contains all the settings for the application.
    """

    # Use model_config for Pydantic v2
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: AppEnv = Field(
        AppEnv.LOCAL,
        alias="APP_ENV",
        description="Application runtime environment (local/dev/prod)",
    )

    # Application settings
    application_name: str = Field("fastapi-template", alias="APPLICATION_NAME")
    host: str = Field("0.0.0.0", alias="HOST")
    port: int = Field(5000, alias="PORT")
    worker_count: int = Field(0, alias="WORKER_COUNT", description="Number of Gunicorn workers (0 for auto)")

    # Docker settings
    cpu_limit: str = Field("1.00", alias="CPU_LIMIT")
    memory_limit: str = Field("2G", alias="MEMORY_LIMIT")
    db_cpu_limit: str = Field("1.00", alias="DB_CPU_LIMIT")
    db_memory_limit: str = Field("2G", alias="DB_MEMORY_LIMIT")
    health_check_url: str = Field("http://localhost:5000/api/health/", alias="HEALTH_CHECK_URL")

    # CORS settings
    cors_allow_origins: str = Field("*", alias="CORS_ALLOW_ORIGINS")
    cors_allow_methods: str = Field("GET,POST,PUT,DELETE,PATCH", alias="CORS_ALLOW_METHODS")
    cors_allow_headers: str = Field("Content-Type,Authorization", alias="CORS_ALLOW_HEADERS")

    # API Key Authentication settings
    enable_api_key: bool = Field(False, alias="API_KEY_ENABLED")
    api_key: str = Field(..., alias="API_KEY")
    api_key_exclude_paths_list: list[str] = Field(
        ["/api/health", "/docs", "/redoc", "/api/v1/openapi.json"],
        alias="API_KEY_EXCLUDE_PATHS",
    )

    # Database configuration
    postgres_database_host: str = Field(..., alias="POSTGRES_DATABASE_HOST")
    postgres_database_name: str = Field(..., alias="POSTGRES_DATABASE_NAME")
    postgres_database_username: str = Field(..., alias="POSTGRES_DATABASE_USERNAME")
    postgres_database_password: str = Field(..., alias="POSTGRES_DATABASE_PASSWORD")
    postgres_database_port: int = Field(5432, alias="POSTGRES_DATABASE_PORT")
    postgres_database_echo: bool = Field(False, alias="POSTGRES_DATABASE_ECHO")

    @property
    def postgres_database_url(self) -> str:
        """Returns the URL for the postgres database with asyncpg driver."""
        return str(
            URL.build(
                scheme="postgresql+asyncpg",
                host=self.postgres_database_host,
                port=self.postgres_database_port,
                user=self.postgres_database_username,
                password=self.postgres_database_password,
                path=f"/{self.postgres_database_name}",
            )
        )

settings = Settings()