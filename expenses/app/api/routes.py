from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.auth import get_current_user_id
from app.db.models import Expense
from app.schema.exp import ExpenseCreate, ExpenseRead, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/health", summary="Service healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok", "service": "expenses"}


@router.post(
    "/",
    response_model=ExpenseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense",
)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> ExpenseRead:
    """Create a new expense record."""
    db_expense = Expense(
        user_id=current_user_id,
        amount=expense.amount,
        currency=expense.currency,
        category=expense.category,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return ExpenseRead.model_validate(db_expense)


@router.get(
    "/",
    response_model=List[ExpenseRead],
    summary="List all expenses",
)
def list_expenses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> List[ExpenseRead]:
    """List expenses for the authenticated user."""
    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == current_user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [ExpenseRead.model_validate(expense) for expense in expenses]


@router.get(
    "/{expense_id}",
    response_model=ExpenseRead,
    summary="Get expense by ID",
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> ExpenseRead:
    """Get a specific expense by its ID."""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense or expense.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} not found",
        )
    return ExpenseRead.model_validate(expense)


@router.put(
    "/{expense_id}",
    response_model=ExpenseRead,
    summary="Update an expense",
)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> ExpenseRead:
    """Update an existing expense."""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense or expense.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} not found",
        )
    
    # Update only provided fields
    update_data = expense_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)
    
    db.commit()
    db.refresh(expense)
    return ExpenseRead.model_validate(expense)


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense",
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> None:
    """Delete an expense by its ID."""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense or expense.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} not found",
        )
    
    db.delete(expense)
    db.commit()
    return None


@router.get(
    "/user/{user_id}",
    response_model=List[ExpenseRead],
    summary="Get all expenses for a user",
)
def get_user_expenses(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> List[ExpenseRead]:
    """Get all expenses for a specific user."""
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot access another user's expenses",
        )
    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == current_user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [ExpenseRead.model_validate(expense) for expense in expenses]
