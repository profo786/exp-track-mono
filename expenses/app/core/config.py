from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv
from pydantic import SecretStr, Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env from project root or expenses/.env
PROJECT_ROOT = Path(__file__).resolve().parents[3]

for env_path in (
    PROJECT_ROOT / ".env",
    PROJECT_ROOT / "expenses" / ".env",
):
    if env_path.exists():
        load_dotenv(env_path, override=False)
        break


class Settings(BaseSettings):
    database_url: SecretStr = Field(
        validation_alias=AliasChoices("EXPENSES_DATABASE_URL", "DATABASE_URL")
    )
    jwt_secret_key: SecretStr = Field(
        validation_alias=AliasChoices("AUTH_JWT_SECRET", "EXPENSES_JWT_SECRET")
    )
    jwt_algorithm: str = Field(
        default="HS256",
        validation_alias=AliasChoices("AUTH_JWT_ALGORITHM", "EXPENSES_JWT_ALGORITHM"),
    )

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore",
        case_sensitive=False
    )

    @property
    def db_url(self) -> str:
        return self.database_url.get_secret_value()

    @property
    def jwt_secret(self) -> str:
        return self.jwt_secret_key.get_secret_value()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
