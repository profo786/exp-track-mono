from datetime import datetime
from pydantic import BaseModel, Field


class ExpenseBase(BaseModel):
    amount: float = Field(gt=0, description="Expense amount must be positive")
    currency: str = Field(default="USD", max_length=3, description="Currency code (ISO 4217)")
    category: str = Field(default="other", max_length=120, description="Expense category")


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: float | None = Field(default=None, gt=0, description="Expense amount")
    currency: str | None = Field(default=None, max_length=3, description="Currency code")
    category: str | None = Field(default=None, max_length=120, description="Expense category")


class ExpenseRead(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

