from pydantic import BaseModel

from app.enums import RoleEnum

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True
