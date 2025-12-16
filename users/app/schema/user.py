import email
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: int
    email: EmailStr
    display_name: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    display_name: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    display_name: str | None = None
    
