import pytest
from functools import wraps
from typing import List
from fastapi import HTTPException, Request
from jose import jwt
from unittest.mock import AsyncMock, MagicMock

from app.decorators import required_role
from app.config import settings
from app.enums import RoleEnum

class TestRequiredRole:

    @pytest.fixture
    def mock_request(self):
        return AsyncMock()

    @pytest.fixture
    def mock_sample_handler(self):
        @required_role([RoleEnum.ADMIN])
        async def handler(request: Request):
            return {"message": "Success"}

        return handler

    @pytest.mark.asyncio
    @pytest.mark.description("요청 객체가 없을 경우 에러 뱉기")
    async def test_missing_request_object(self, mock_request, mock_sample_handler):
        # Given

        # When
        with pytest.raises(HTTPException) as exc_info:
            await mock_sample_handler()

        # Then
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Request object is missing"

    @pytest.mark.asyncio
    @pytest.mark.description("쿠키 키 없을경우 예외 발생")
    async def test_no_token(self, mock_request, mock_sample_handler):
        # Given
        mock_request.cookies.get.return_value = None

        # When
        with pytest.raises(HTTPException) as exc_info:
            await mock_sample_handler(request=mock_request)

        # Then
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Bad Request"

    @pytest.mark.asyncio
    @pytest.mark.description("토큰 없을경우 예외 발생")
    async def test_no_token(self, mock_request, mock_sample_handler):
        # Given
        mock_request.cookies.get.return_value = None
        mock_request.cookies.__contains__.side_effect = lambda key: key == settings.cookie_key

        # When
        with pytest.raises(HTTPException) as exc_info:
            await mock_sample_handler(request=mock_request)

        # Then
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Not authenticated"
        
    @pytest.mark.asyncio
    @pytest.mark.description("허용되지 않은 권한일경우 예외 발생")
    async def test_invalid_role(self, mock_request, mock_sample_handler):
        #Given
        token = jwt.encode({"role": "user"}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        
        mock_request.cookies.get.return_value = token
        mock_request.cookies.__contains__.side_effect = lambda key: key == settings.cookie_key


        # When
        with pytest.raises(HTTPException) as exc_info:
            await mock_sample_handler(request=mock_request)

        # Then
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Not authorized"

    @pytest.mark.asyncio
    @pytest.mark.description("유효하지 않은 토큰일 경우 에러 뱉기")
    async def test_invalid_token(self, mock_request, mock_sample_handler):
        # Given
        mock_request.cookies.get.return_value = "invalid_token"
        mock_request.cookies.__contains__.side_effect = lambda key: key == settings.cookie_key

        # When
        with pytest.raises(HTTPException) as exc_info:
            await mock_sample_handler(request=mock_request)

        # Then
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid token"

    @pytest.mark.asyncio
    @pytest.mark.description("성공")
    async def test_success(self, mock_request, mock_sample_handler):
        #Given
        token = jwt.encode({"role": "admin"}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        
        mock_request.cookies.get.return_value = token 
        mock_request.cookies.__contains__.side_effect = lambda key: key == settings.cookie_key


        #When
        response = await mock_sample_handler(request=mock_request)

        # Then
        assert response == {"message": "Success"}


