from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user_schema import UserCreate

def get_user(db: Session, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, email=user.email, full_name=user.full_name, password=user.password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
