import sys
import os

from fastapi import FastAPI
from .user.routers.user_router import router as user_router

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


app = FastAPI()

app.include_router(user_router)

