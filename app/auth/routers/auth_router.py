import os
from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.decorators import role_required
from app.dependencies import get_db
from app.auth.schemas.auth_schema import LoginRequest, SignUpRequest
from app.auth.services import auth_service
from app.enums import UserRoleEnum

router = APIRouter()

COOKIE_EXPIRE_MINUTES = int(os.environ.get('COOKIE_EXPIRE_MINUTES', 30))

@router.get("/auth/check")
@role_required([UserRoleEnum.USER])
async def check(request: Request):
    return "1"

@router.post("/auth/sign-up")
def sign_up(sign_up_request: SignUpRequest, db: Session = Depends(get_db)):
    auth_service.sign_up(db, sign_up_request)


@router.post("/auth/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    access_token = auth_service.login(db, login_request)

    # JWT 토큰을 쿠키에 설정
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key=os.environ.get('COOKIE_KEY'), 
        value=access_token, 
        httponly=True,  # JavaScript에서 접근할 수 없게 설정
        secure=False,    # HTTPS에서만 전송되도록 설정 (배포 시 필수)
        max_age=timedelta(minutes=COOKIE_EXPIRE_MINUTES),
        expires=datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(minutes=COOKIE_EXPIRE_MINUTES)  # 쿠키 만료 시간
    )
    return response
