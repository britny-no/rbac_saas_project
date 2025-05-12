from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from functools import wraps
from typing import List
from jose import JWTError, jwt

from app.enums import RoleEnum
from app.config import settings


def decode_jwt_token(token: str, secret_key: str, algorithm: str) -> dict:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def required_role(allowed_roles: List[RoleEnum]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            project_id = kwargs.get("project_id")
            cookie_key = settings.cookie_key

            if project_id is None or request is None or cookie_key not in  request.cookies:
                raise HTTPException(status_code=400, detail="Bad Request")

            token = request.cookies.get(cookie_key)
            if not token:
                raise HTTPException(status_code=401, detail="Not authenticated")

            payload = decode_jwt_token(token, settings.jwt_secret_key, settings.jwt_algorithm)

            project_roles = payload.get("project_roles")
            if project_roles is None :
                raise HTTPException(status_code=400, detail="Bad Request")
            participated_role = project_roles.get(str(project_id))

            if participated_role not in [r.value for r in allowed_roles]:
                raise HTTPException(status_code=403, detail="Not authorized")


            return func(*args, **kwargs)
        return wrapper
    return decorator
