from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app.auth import authenticate_user
from app.auth import create_access_token
from app.db import get_db
from app.dto.user import AuthResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # без / в начале


@router.post("/token", response_model=AuthResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user: raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.name})
    return AuthResponse(access_token=access_token, token_type="bearer")
