from . import models  # noqa: F401 - imported for metadata discovery
from .base import Base
from .session import engine


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

