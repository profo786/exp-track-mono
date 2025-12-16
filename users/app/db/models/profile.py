from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    display_name = Column(String(length=255), nullable=False)

