from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
