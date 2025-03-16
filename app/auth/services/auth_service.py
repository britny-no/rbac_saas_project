from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.user.services.user_service import create_user, get_user
from app.auth.schemas.auth_schema import LoginRequest, SignUpRequest

def sign_up(db: Session, sign_up_request: SignUpRequest):
    return create_user(db, sign_up_request)


def login(db: Session, login_request: LoginRequest):
    user = get_user(db, login_request.email)
    if not user or user.password != login_request.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    return 
