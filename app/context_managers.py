import traceback
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from fastapi import HTTPException

from app.logging_config import get_logger

logger = get_logger("ContextManager")



@contextmanager
def transaction(db: Session):
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close()
