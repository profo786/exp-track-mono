from sqlalchemy import text

from . import models  # noqa: F401 - imported for metadata discovery
from .base import Base
from .session import engine


def init_db() -> None:
    """Ensure the database is reachable; schema is managed via Alembic."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

