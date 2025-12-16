from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.deps import get_db
from ..core.auth import get_current_user_id
from ..db.models.profile import Profile
from ..schema.user import UserBase, UserCreate, UserUpdate


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/health", summary="Service healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok", "service": "users"}


@router.post("/create", response_model=UserBase, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> UserBase:
    """
    Create a profile for the authenticated user. The profile id is taken from the JWT `sub`.
    """
    # Prevent duplicate profiles for the same auth user or email
    if db.query(Profile).filter(Profile.id == current_user_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="profile already exists for this user",
        )
    if db.query(Profile).filter(Profile.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already in use",
        )

    user = Profile(
        id=current_user_id,
        email=payload.email,
        display_name=payload.display_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_model=list[UserBase])
def list_users(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> list[UserBase]:
    # For now return all profiles; current_user_id ensures caller is authenticated
    _ = current_user_id
    return db.query(Profile).all()


@router.get("/{user_id}", response_model=UserBase)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> UserBase:
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot access another user's profile",
        )
    user = db.query(Profile).filter(Profile.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    return user


@router.put("/{user_id}", response_model=UserBase)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> UserBase:
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot update another user's profile",
        )
    user = db.query(Profile).filter(Profile.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )

    if payload.email and payload.email != user.email:
        duplicate = (
            db.query(Profile)
            .filter(Profile.email == payload.email, Profile.id != user_id)
            .first()
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email already in use",
            )
        user.email = payload.email

    if payload.display_name is not None:
        user.display_name = payload.display_name

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> None:
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot delete another user's profile",
        )
    user = db.query(Profile).filter(Profile.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    db.delete(user)
    db.commit()
