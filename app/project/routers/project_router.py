from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.dependencies import get_db
from app.logging_config import get_logger



router = APIRouter()
logger = get_logger("Project")


@router.post("/project/${}")
def sign_up(sign_up_request: SignUpRequest, db: Session = Depends(get_db)):
    auth_service.sign_up(db, sign_up_request)