from pydantic import BaseModel, validator

from app.enums import UserRoleEnum

class LoginRequest(BaseModel):
    email: str
    password: str


class SignUpRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: UserRoleEnum

