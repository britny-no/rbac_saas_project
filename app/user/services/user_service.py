from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.context_managers import transaction
from ..models.user import User
from ..models.user_project import UserProject
from ..schemas.user_schema import UserCreate

def get_user(db: Session, email: str) -> User:
    user_with_projects = (
        db.query(User)
        .options(joinedload(User.projects))
        .filter(User.email == email)
        .first()
    )

    if user_with_projects is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_with_projects

def create_user(db: Session, user: UserCreate) -> User:
    with transaction(db) as session:
        db_user = User(name=user.name, email=user.email,  password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    return db_user