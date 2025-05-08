from fastapi import Depends, HTTPException, Path

from api.schemas.user import UserUpdate
from app.db.models.user import User
from app.services.auth import get_current_user


def require_self_or_admin(user_id: int = Path(...), current_user: User = Depends(get_current_user)) -> User:
    if require_admin(current_user) or current_user.id == user_id:
        return current_user
    raise HTTPException(status_code=403, detail="Access denied")


def require_allowed_update(user_in: UserUpdate, current_user: User = Depends(get_current_user)) -> User:
    if user_in.role and user_in.role != current_user.role:
        return require_admin(current_user)
    else:
        return require_self_or_admin(user_in.id, current_user)


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role == "admin":
        return current_user
    raise HTTPException(status_code=403, detail="Access denied")


def role_required(*allowed_roles: str):
    def wrapper(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

    return wrapper
