from functools import wraps
from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse

def roles_required(required_roles: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(request, current_user: User = Depends(get_current_user), *args, **kwargs):
            if current_user.role not in required_roles:
                raise HTTPException(
                    status_code=403, detail="You do not have access to this resource"
                )
            return await func(request, current_user, *args, **kwargs)
        return wrapper
    return decorator
