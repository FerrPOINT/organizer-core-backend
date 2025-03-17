from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(150), unique=True, nullable=True, index=True)
    role = Column(String(50), default='user', nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
