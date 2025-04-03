import os
import sys
import asyncio
from sqlalchemy import create_engine
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends
from contextlib import asynccontextmanager
from sqlalchemy import create_engine

from app.exceptions import sqlalchemy_exception_handler, http_exception_handler
from app.project.routers.project_router import router as project_router
from app.user.routers.user_router import router as user_router
from app.auth.routers.auth_router import router as auth_router
from app.config import settings
from app.database import  DatabaseManager
from app.redis import RedisManager
from app.user.models.user import User
from app.user.models.user_project import UserProject
from app.project.models.project import Project

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_manager = RedisManager(settings.redis_host, settings.redis_port)
    db_manager = DatabaseManager(settings.sqlalchemy_database_url)

    app.state.redis_manager = redis_manager
    app.state.db_manager = db_manager


    task = asyncio.create_task(redis_manager.check_connection())
    task2 = asyncio.create_task(db_manager.check_connection())

    yield

    await asyncio.to_thread(task.cancel) 
    await asyncio.to_thread(task2.cancel)  

    await redis_manager.close()
    await asyncio.to_thread(db_manager.close)  

app = FastAPI(lifespan=lifespan)


app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(project_router)
app.include_router(user_router)
app.include_router(auth_router)



