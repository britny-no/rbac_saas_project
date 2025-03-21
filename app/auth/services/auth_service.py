import os
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from app.config import settings
from app.user.models.user import User
from app.user.services.user_service import create_user, get_user
from app.auth.schemas.auth_schema import LoginRequest, SignUpRequest



def sign_up(db: Session, sign_up_request: SignUpRequest):
    return create_user(db, sign_up_request)


def login(db: Session, login_request: LoginRequest) -> User:
    user = get_user(db, login_request.email)
    if not user or user.password != login_request.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={
        "user_id": 1
    })
    
    return access_token

# JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=int(settings.jwt_expire_minutes))):
    to_encode = data.copy()
    expire = datetime.utcnow().replace(tzinfo=timezone.utc)+ expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt
