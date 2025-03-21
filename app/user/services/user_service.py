from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user_schema import UserCreate

def get_user(db: Session, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    # INNER JOIN 기본 사용
    db_user_with_projects = db.query(User, UserProject).join(UserProject).filter(User.email == email).first()
    print(db_user_with_projects)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email,  password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
