from sqlalchemy.orm import Session

from app.api.schemas.user import UserCreate, UserUpdate
from app.db.models.user import User
from app.services.auth import get_password_hash


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_name(db: Session, name: str) -> User | None:
    return db.query(User).filter_by(name=name).first()


def get_users(db: Session, skip=0, limit=100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    for field, value in data.model_dump(exclude_unset=True).items():
        if field == "password":
            user.hashed_password = get_password_hash(value)
        else:
            setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
