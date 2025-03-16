import sys
import os
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import sqlalchemy_exception_handler, http_exception_handler
from app.user.routers.user_router import router as user_router

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


app = FastAPI()

app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(user_router)

