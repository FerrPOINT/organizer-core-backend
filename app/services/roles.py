from fastapi import Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.db.session_factory import get_db
from app.services.auth import get_current_user


def is_self_or_admin(user_id: int = Path(...), db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)) -> User:
    if is_admin(current_user) or current_user.id == user_id:
        return current_user
    raise HTTPException(status_code=403, detail="Access denied")


def is_admin(current_user: User = Depends(get_current_user)) -> bool:
    return current_user.role == "admin"


def role_required(*allowed_roles: str):
    def wrapper(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

    return wrapper
