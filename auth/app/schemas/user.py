from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(BaseModel):
    id: int
    email: str

    model_config = {
        "from_attributes": True
    }

