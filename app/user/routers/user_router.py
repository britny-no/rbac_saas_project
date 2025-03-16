from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user_schema import UserCreate, User
from ..services.user_service import get_user, create_user
from app.dependencies import get_db
from app.logging_config import get_logger



router = APIRouter()
logger = get_logger("App")


