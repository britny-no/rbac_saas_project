from pydantic import BaseModel
from typing import Dict

from app.enums import RoleEnum

class UserClaims(BaseModel):
    id: int
    project_roles: Dict[int, RoleEnum]


