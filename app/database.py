import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import text

from app.config import settings
from app.logging_config import get_logger

logger = get_logger("DatabaseManager")
Base = declarative_base()

class DatabaseManager:
    def __init__(self, db_url: str):
        if not db_url:
            raise ValueError("SQLALCHEMY_DATABASE_URL not set")

        self.db_url = db_url
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False)
        self.is_reconnecting = False 
        self.initialize_database()


    def _create_engine(self):
        return create_engine(
            self.db_url,
            pool_size=10,
            max_overflow=5,
            pool_recycle=1,
            pool_pre_ping=True
        )

    def initialize_database(self):
        Base.metadata.create_all(bind=self.engine)

    async def reconnect(self):
        if self.is_reconnecting:
            return
        
        self.is_reconnecting = True
        try:
            self.engine.dispose()
            self.engine = self._create_engine()
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False)
        except Exception as e:
            logger.warn("🔴 DB 연결 실패")
        self.is_reconnecting = False
        

    async def check_connection(self):
        while True:
            try:
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
            except Exception as e:
                await self.reconnect()
            finally:
                await asyncio.sleep(5)


db_manager = DatabaseManager(settings.sqlalchemy_database_url)
