from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.db.base import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    category = Column(String(length=120), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(length=3), nullable=False, default="USD")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

