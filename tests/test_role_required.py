import pytest
from functools import wraps
from typing import List
from fastapi import HTTPException, Request
from jose import jwt
from unittest.mock import AsyncMock

from app.decorators import required_role
from app.config import settings
from app.enums import RoleEnum

@required_role([RoleEnum.ADMIN])
async def sample_handler(request: Request):
    return {"message": "Success"}

@pytest.mark.asyncio
async def test_valid_admin_role():
    request = AsyncMock()
    token = jwt.encode({"role": "admin"}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    request.cookies.get.return_value = token

    response = await sample_handler(request=request)
    assert response == {"message": "Success"}

@pytest.mark.asyncio
async def test_invalid_role():
    request = AsyncMock()
    token = jwt.encode({"role": "user"}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    request.cookies.get.return_value = token

    with pytest.raises(HTTPException) as exc_info:
        await sample_handler(request=request)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not authorized"

@pytest.mark.asyncio
@pytest.mark.description("토큰 없을경우 에러 뱉기")
async def test_no_token():
    request = AsyncMock()
    request.cookies.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await sample_handler(request=request)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Not authenticated"

@pytest.mark.asyncio
@pytest.mark.description("유효하지 않은 토큰일 경우 에러 뱉기")
async def test_invalid_token():
    request = AsyncMock()
    request.cookies.get.return_value = "invalid_token"

    with pytest.raises(HTTPException) as exc_info:
        await sample_handler(request=request)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"

@pytest.mark.asyncio
@pytest.mark.description("요청 객체가 없을 경우 에러 뱉기")
async def test_missing_request_object():
    with pytest.raises(HTTPException) as exc_info:
        await sample_handler()

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Request object is missing"