from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

Base = declarative_base()


if not settings.sqlalchemy_database_url:
    raise ValueError("SQLALCHEMY_DATABASE_URL not set")

engine = create_engine(settings.sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

