from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.user import UserOut, UserCreate, UserUpdate
from app.db.models.user import User
from app.db.repository import user as crud
from app.db.session_factory import get_db
from app.services.roles import require_allowed_update, require_self_or_admin, require_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserOut])
def list_users(
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db),
        skip=0,
        limit=100
):
    return crud.get_users(db, skip, limit)


@router.post("/", response_model=UserOut)
def create_user(
        user_in: UserCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    if crud.get_user_by_name(db, user_in.name):
        raise HTTPException(400, "Username already exists")
    return crud.create_user(db, user_in)


@router.get("/{user_id}", response_model=UserOut)
def read_user(
        user_id: int,
        current_user: User = Depends(require_self_or_admin),
        db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.put("/", response_model=UserOut)
def update_user(
        user_in: UserUpdate,
        current_user: User = Depends(require_allowed_update),
        db: Session = Depends(get_db)
):
    user = crud.get_user(db, user_in.id)
    if not user:
        raise HTTPException(404, "User not found")
    return crud.update_user(db, user, user_in)


@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    user = crud.get_user(db, user_id)
    if not user or not current_user:
        raise HTTPException(404, "User not found")
    crud.delete_user(db, user)
    return {"detail": "Deleted"}
