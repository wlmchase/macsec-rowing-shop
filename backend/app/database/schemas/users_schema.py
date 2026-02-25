from pydantic import BaseModel, EmailStr, UUID4
from app.database.models.models import Role
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[Role] = None

class UserResponse(UserBase):
    id: UUID4
    is_admin: bool
    is_active: bool

    class Config:
        from_attributes = True