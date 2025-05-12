import os
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from app.config import settings
from app.vo import UserClaims
from app.user.models.user import User
from app.user.services import user_service
from app.auth.schemas.auth_schema import LoginRequest, SignUpRequest

# 클래스로 route에서 depends(db session, repository) 커플링 문제 발생
# auth_service만 클래스화할려 했는데 service, repository 생성후 주입 로직이 분리됨. 
# 이게 객체지향에 익숙하지 않은 다른 FastAPI 개발자에게 익숙하지 않을수도 있으므로 커플링 발생해도 우선 진행

def sign_up(db: Session, sign_up_request: SignUpRequest) -> User:
    return user_service.create_user(db, sign_up_request)


def login(db: Session, login_request: LoginRequest) -> str:
    user = user_service.get_user_with_project(db, login_request.email)
    if not user or user.password != login_request.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    project_roles = {project.project_id: project.role for project in user.projects}
    user_claims = UserClaims(id=user.id, project_roles=project_roles)
    access_token = create_access_token(user_claims=user_claims)
    
    return access_token

def create_access_token(user_claims: UserClaims):
    to_dict = user_claims.dict()
    expires_delta = timedelta(minutes=int(settings.jwt_expire_minutes))
    expire = datetime.utcnow().replace(tzinfo=timezone.utc)+ expires_delta
    to_dict.update({"exp": expire})
    encoded_jwt = jwt.encode(to_dict, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def generate_verify_code():
    pass

def confirm_verify_code():
    pass