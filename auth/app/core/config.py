from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field


PROJECT_ROOT = Path(__file__).resolve().parents[3]
_ENV_CANDIDATES = [
    PROJECT_ROOT / ".env",
    PROJECT_ROOT / "auth" / ".env",
]
for env_path in _ENV_CANDIDATES:
    if env_path.exists():
        load_dotenv(env_path, override=False)


def _require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(
            f"{var_name} is not set. Ensure your .env is loaded or export the variable."
        )
    return value


class Settings(BaseModel):
    database_url: str = Field(
        default_factory=lambda: _require_env("AUTH_DATABASE_URL")
    )
    jwt_secret_key: str = Field(
        default_factory=lambda: os.getenv("AUTH_JWT_SECRET")
    )
    jwt_algorithm: str = Field(
        default_factory=lambda: os.getenv("AUTH_JWT_ALGORITHM")
    )
    access_token_expire_minutes: int = Field(
        default_factory=lambda: int(os.getenv("AUTH_JWT_EXPIRE_MINUTES"))
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

