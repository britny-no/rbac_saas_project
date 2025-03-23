from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)):
    # 여기서 토큰을 디코딩하고, 사용자 정보를 가져옵니다.
    # 예시에서는 간단히 사용자 정보를 반환합니다.
    print(token)
    if token != "valid_token":  # 이 부분을 실제 인증 로직으로 바꿔야 합니다.
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # 예시 사용자, 실제로는 DB나 다른 시스템에서 정보를 가져옵니다.
    return User(username="testuser", role="admin")