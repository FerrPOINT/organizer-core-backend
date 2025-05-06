from fastapi import APIRouter, Depends

from app.dto.user import User as UserDto
from app.models.user import User as DBUser
from app.services.auth import get_current_user

router = APIRouter()


@router.get("/users/me", response_model=UserDto)
def get_me(current_user: DBUser = Depends(get_current_user)):
    return UserDto.model_validate(current_user)
