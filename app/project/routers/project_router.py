from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.dependencies import get_db
from app.logging_config import get_logger
from app.project.services import project_service
from app.project.schemas.project_schema import CreateProjectRequest


router = APIRouter()
logger = get_logger("Project")


@router.post("/project")
def sign_up(create_project_request: CreateProjectRequest, db: Session = Depends(get_db)):
    project_service.create_project(db, 1, create_project_request)