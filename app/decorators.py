import os
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from functools import wraps
from typing import List
from jose import JWTError, jwt
from app.enums import UserRoleEnum

def role_required(allowed_roles: List[UserRoleEnum]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if request is None:
                raise HTTPException(status_code=400, detail="Request object is missing")

            try:
                cookie_key = os.environ.get('COOKIE_KEY')
                token = request.cookies.get(cookie_key)
                if not token:
                    raise HTTPException(status_code=401, detail="Not authenticated")

                payload = jwt.decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms=[os.environ.get('JWT_ALGORITHM')])
                role = payload.get("role")
                if role not in [r.value for r in allowed_roles]:
                    raise HTTPException(status_code=403, detail="Not authorized")

            except JWTError:
                raise HTTPException(status_code=401, detail="Invalid token")

            return await func(*args, **kwargs)
        return wrapper
    return decorator
