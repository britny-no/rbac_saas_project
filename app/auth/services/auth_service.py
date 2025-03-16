from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.user.services.user_service import create_user
from app.auth.schemas.auth_schema import LoginRequest, SignUpRequest

def sign_up(db: Session, sign_up_request: SignUpRequest):
    return create_user(db, sign_up_request)
