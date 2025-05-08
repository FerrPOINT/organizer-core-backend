from pydantic import BaseModel


class UserLoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
