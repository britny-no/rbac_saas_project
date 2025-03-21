from pydantic import BaseModel, validator

from app.enums import RoleEnum

class LoginRequest(BaseModel):
    email: str
    password: str


class SignUpRequest(BaseModel):
    name: str
    email: str
    password: str

