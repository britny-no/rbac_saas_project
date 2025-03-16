from pydantic import BaseModel

from app.enums import UserRoleEnum

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: UserRoleEnum

class User(UserBase):
    id: int
    full_name: str

    class Config:
        orm_mode = True
