from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.api.schemas.email_str import EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str
    is_active: bool


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]
    password: Optional[str] = None
    is_active: Optional[bool]


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
