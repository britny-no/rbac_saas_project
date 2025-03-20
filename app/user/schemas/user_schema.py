from pydantic import BaseModel

from app.enums import UserRoleEnum

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: UserRoleEnum

class User(UserBase):
    id: int
    class Config:
        orm_mode = True
