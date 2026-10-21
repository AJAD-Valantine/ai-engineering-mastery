from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=r"C:\Users\HP\OneDrive\Documents\Repos\ai-engineering-mastery\agentic-rag\.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    llm_api_key: SecretStr
    tavily_api_key: SecretStr
    pinecone_api_key: SecretStr


@lru_cache
def get_settings() -> Settings:
    return Settings() #type: ignore
