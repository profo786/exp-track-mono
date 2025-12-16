from . import models  # noqa: F401 - populate metadata
from .base import Base
from .session import engine


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

