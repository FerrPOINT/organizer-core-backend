from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.dto.email_str import EmailStr


class UserBase(BaseModel):
    name: str = Field(alias="name")  # 🔁 name из ORM будет попадать сюда
    email: Optional[EmailStr] = None
    role: str = "user"
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(alias="name")  # 🔁 name из ORM будет попадать сюда
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
