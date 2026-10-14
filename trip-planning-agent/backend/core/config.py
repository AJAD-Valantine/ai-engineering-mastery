import os
import urllib.parse
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

# Resolve .env file path relative to this backend package
_backend_dir = Path(__file__).resolve().parent.parent
_env_candidates = [
    str(_backend_dir / ".env"),
    str(Path.cwd() / "backend" / ".env"),
    str(Path.cwd() / ".env"),
]
_env_file = next((f for f in _env_candidates if Path(f).exists()), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_env_file,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    db_engine: Literal["postgresql", "postgresql+psycopg"] = "postgresql"
    db_username: str = "postgres"
    db_password: SecretStr = SecretStr("")
    db_host: str = "127.0.0.1"
    db_port: int = 5432
    db_name: str = "travel-agent"

    @property
    def database_url(self) -> URL:
        driver = self.db_engine
        if driver == "postgresql":
            try:
                import psycopg  # noqa: F401
                driver = "postgresql+psycopg"
            except ImportError:
                pass

        return URL.create(
            drivername=driver,
            username=self.db_username,
            password=self.db_password.get_secret_value(),
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

    @property
    def db_conn_str(self) -> str:
        """Returns standard PostgreSQL connection string with URL-encoded password."""
        pwd = urllib.parse.quote_plus(self.db_password.get_secret_value())
        return f"postgresql://{self.db_username}:{pwd}@{self.db_host}:{self.db_port}/{self.db_name}"

    # API Keys
    llm_api_key: SecretStr = SecretStr("")
    aviationstack_api_key: SecretStr = SecretStr("")
    tavily_api_key: SecretStr = SecretStr("")
    weather_api_key: SecretStr = SecretStr("")

    # LangSmith / Observability
    langsmith_tracing: bool = True
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langsmith_api_key: SecretStr = SecretStr("")
    langsmith_agent_id: str = "travel-agent"
    langsmith_agent_environment: str = "local"

    # Trip Planning Defaults
    default_origin_data: str = "SL"

    aviationstack_endpoint: str = "http://api.aviationstack.com/v1/flights"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    # Sync LangSmith tracing to standard LangChain environment variables
    if settings.langsmith_tracing and settings.langsmith_api_key.get_secret_value():
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key.get_secret_value()
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langsmith_endpoint
        os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_agent_id

    return settings
