"""Application settings, loaded from environment variables.

Every setting comes from the environment (Docker Compose passes the values from `.env`).
Required values have no default, so a missing or invalid one stops the app at start-up
with a message naming the variable. Secrets use `SecretStr`, so they are masked in
logs, tracebacks and `repr()`.
"""

from functools import lru_cache
from typing import Literal
from urllib.parse import quote

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # env_ignore_empty: `LLM_API_KEY=` counts as not set, and an empty required value is missing.
    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore", env_ignore_empty=True)

    # PostgreSQL (accounts and chat history)
    postgres_user: str
    postgres_password: SecretStr
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Neo4j (notes, concepts, links)
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: SecretStr = Field(min_length=8)

    # Authentication. HS256 needs a long random key.
    jwt_secret: SecretStr = Field(min_length=32)
    jwt_algorithm: Literal["HS256"] = "HS256"
    access_token_expire_minutes: int = Field(default=60, gt=0)

    # LLM provider. Optional until the intelligence layer is built (#23, #29).
    llm_provider: Literal["openai", "anthropic"] = "openai"
    llm_api_key: SecretStr | None = None

    # Browser origins allowed to call the API, comma-separated.
    cors_origins: str = "http://localhost:5173"

    @property
    def database_url(self) -> str:
        """SQLAlchemy URL, with the user and password escaped so `@`, `:` or `/` are safe."""
        user = quote(self.postgres_user, safe="")
        password = quote(self.postgres_password.get_secret_value(), safe="")
        return (
            f"postgresql+psycopg://{user}:{password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return the settings, read once. Use as a FastAPI dependency or call directly."""
    return Settings()
