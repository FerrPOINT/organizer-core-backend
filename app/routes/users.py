from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.dto.user import User as UserDto
from app.models.user import User as DBUser

router = APIRouter()


@router.get("/users/me", response_model=UserDto)
def get_me(current_user: DBUser = Depends(get_current_user)):
    return UserDto.model_validate(current_user)
