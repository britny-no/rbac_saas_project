import os
import sys
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends

from app.exceptions import sqlalchemy_exception_handler, http_exception_handler
from app.project.routers.project_router import router as project_router
from app.user.routers.user_router import router as user_router
from app.auth.routers.auth_router import router as auth_router
from app.config import settings
from app.database import engine, Base
from app.user.models.user import User
from app.user.models.user_project import UserProject
from app.project.models.project import Project

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


app = FastAPI()

app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(project_router)
app.include_router(user_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

