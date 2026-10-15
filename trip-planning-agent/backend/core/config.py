from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

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

    # API Keys
    llm_api_key: SecretStr = SecretStr("")
    aviationstack_api_key: SecretStr = SecretStr("")
    tavily_api_key: SecretStr = SecretStr("")
    weather_api_key: SecretStr = SecretStr("")

    # Trip Planning Defaults
    default_origin_data: str = "SL"

    aviationstack_endpoint: str = "http://api.aviationstack.com/v1/flights"


@lru_cache
def get_settings() -> Settings:
    return Settings()
