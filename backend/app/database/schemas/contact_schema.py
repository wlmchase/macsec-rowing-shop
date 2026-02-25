from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime

class ContactBase(BaseModel):
    email: EmailStr
    message: str

class ContactResponse(BaseModel):
    id: UUID4
    email: EmailStr
    message: str
    created_at: datetime

    class Config:
        from_attributes = True