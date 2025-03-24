import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.user.models.user import User
from app.auth.services import auth_service
from app.user.services import user_service
from app.auth.schemas.auth_schema import LoginRequest, SignUpRequest


class TestSignUp:
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock(spec=Session)

    @pytest.fixture
    def mock_sign_up_request(self):
        return SignUpRequest(
            name="testuser",
            password="password123",
            email="testuser@example.com"
        )

    @pytest.fixture
    def mock_user(self):
        return User(
            id=1,
            name="testuser",
            email="testuser@example.com",
        )


    @pytest.mark.description("유저 서비스 에러로 예외 발생")
    @patch("app.user.services.user_service.create_user")
    def test_create_user_error(self, mock_create_user, mock_db_session, mock_sign_up_request, mock_user):
        # When
        mock_create_user.side_effect = Exception("General service error")
        with pytest.raises(Exception) as exception:
            auth_service.sign_up(mock_db_session, mock_sign_up_request)

        # Then
        assert str(exception.value) == "General service error"

    @pytest.mark.description("회원가입 성공")
    @patch("app.user.services.user_service.create_user")
    def test_success(self, mock_create_user, mock_db_session, mock_sign_up_request, mock_user):
        # When
        mock_create_user.return_value = mock_user
        result = auth_service.sign_up(mock_db_session, mock_sign_up_request)

        #Then
        assert result.name == mock_user.name
        assert result.email == mock_user.email
