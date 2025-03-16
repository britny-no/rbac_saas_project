from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.auth.schemas.auth_schema import LoginRequest, SignUpRequest
from app.auth.services import auth_service

# 설정 값들
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer 객체 (토큰 URL 설정)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 사용자 DB (가짜 사용자 DB)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "password": "password123"
    }
}

@router.post("/auth/sign-up")
def sign_up(sign_up_request: SignUpRequest, db: Session = Depends(get_db)):
    auth_service.sign_up(db, sign_up_request)


@router.post("/auth/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    auth_service.login(db, login_request)

    access_token = create_access_token(data={"sub": login_request.username})
    
    # # JWT 토큰을 쿠키에 설정
    # response = JSONResponse(content={"message": "Login successful"})
    # response.set_cookie(
    #     key="access_token", 
    #     value=access_token, 
    #     httponly=True,  # JavaScript에서 접근할 수 없게 설정
    #     secure=False,    # HTTPS에서만 전송되도록 설정 (배포 시 필수)
    #     max_age=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),  # 토큰 만료 시간 설정
    #     expires=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # 쿠키 만료 시간
    # )
    return "1"
