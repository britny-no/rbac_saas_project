import os
from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.config import settings
from app.decorators import required_role
from app.dependencies import get_db
from app.auth.schemas.auth_schema import LoginRequest, SignUpRequest, SignUpResponse
from app.auth.services import auth_service
from app.enums import RoleEnum

router = APIRouter()


@router.get("/auth/check/{project_id}")
@required_role([RoleEnum.VIEWER])
def check(request: Request, project_id: int):
    return "1"

@router.post("/auth/sign-up", response_model = SignUpResponse)
def sign_up(sign_up_request: SignUpRequest, db: Session = Depends(get_db)):
    user = auth_service.sign_up(db, sign_up_request)
    return user


@router.post("/auth/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    access_token = auth_service.login(db, login_request)

    # JWT 토큰을 쿠키에 설정
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key=settings.cookie_key, 
        value=access_token, 
        httponly=True,  # JavaScript에서 접근할 수 없게 설정
        secure=False,    # HTTPS에서만 전송되도록 설정 (배포 시 필수)
        max_age=timedelta(minutes=settings.cookie_expire_minutes),
        expires=datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(minutes=settings.cookie_expire_minutes)  # 쿠키 만료 시간
    )
    return response
