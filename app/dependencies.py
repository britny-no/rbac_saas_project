from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = app.state.db_manager.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)):
    if token != "valid_token": 
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    return User(username="testuser", role="admin")