from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user_schema import UserCreate, User
from ..services.user_service import get_user, create_user
from app.dependencies import get_db
from app.logging_config import get_logger



router = APIRouter()
logger = get_logger("App")


@router.post("/user/", response_model=User)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    logger.info("getting users")
    return get_user(db=db, user_id=user_id)
