# app/dto/user.py
from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    id: int
    username: str = Field(alias="name")  # 🔁 name из ORM будет попадать сюда
    email: str
    role: str
    model_config = ConfigDict(from_attributes=True)  # ⬅️ важно для маппинга


class UserLoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
