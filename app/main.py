import os
import sys
import asyncio
from sqlalchemy import create_engine
import redis.asyncio as redis
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
from app.database import engine, Base, check_db_connection
from app.user.models.user import User
from app.user.models.user_project import UserProject
from app.project.models.project import Project

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

redis_client: redis.Redis | None = redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)

def create_redis_client():
    return redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)
    
async def check_redis_connection(app: FastAPI):
    while True:
        try:
            if app.state.redis_client:
                await app.state.redis_client.ping()  # Redis 연결 확인
            else:
                print("🔴 Redis 연결 끊김, 재연결 시도 중...")
                app.state.redis_client = create_redis_client()  # 새로운 Redis 클라이언트 생성
                app.state.redis_client.ping()
        except redis.ConnectionError:
            print("🔴 Redis 연결 실패! 재시도 중...")
        finally:
            await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis_client = create_redis_client()

    Base.metadata.create_all(bind=engine)
    
    task = asyncio.create_task(check_redis_connection(app))
    task2 = asyncio.create_task(check_db_connection())

    yield

    await asyncio.to_thread(task.cancel) 
    await asyncio.to_thread(task2.cancel)  
    await app.state.redis_client.close()

app = FastAPI(lifespan=lifespan)


@app.get("/get")
async def get_value():
    try:
        value = await redis_client.get("key")
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found in Redis")
        return {"key": value}
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis 연결 오류: {str(e)}")

app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(project_router)
app.include_router(user_router)
app.include_router(auth_router)



