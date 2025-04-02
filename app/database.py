import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from app.config import settings


if not settings.sqlalchemy_database_url:
    raise ValueError("SQLALCHEMY_DATABASE_URL not set")


engine = create_engine(
    settings.sqlalchemy_database_url,
    pool_size=10,
    max_overflow=5,
    pool_recycle=1,
    pool_pre_ping=True 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
Base = declarative_base()

async def check_db_connection():
    global engine, SessionLocal

    while True:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1")) 
        except Exception as e:
            print(e)
            print("🔴 DB 연결 끊김! 연결 시도...")
            reconnect()
        finally:
            await asyncio.sleep(5) 

def reconnect():
    global engine, SessionLocal

    engine.dispose()
    engine = create_engine(
        settings.sqlalchemy_database_url,
        pool_size=10,
        max_overflow=5,
        pool_recycle=1,
        pool_pre_ping=True 
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

