from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime as DateTime


class UserCreate(BaseModel):
    username: str
    email: EmailStr


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    created_at: DateTime
    updated_at: DateTime

    class Config:
        model_config = ConfigDict(from_attributes=True)
