import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, timezone

from app.enums import RoleEnum
from app.vo import UserClaims
from app.config import settings
from app.user.models.user_project import UserProject
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
        # Given
        mock_create_user.side_effect = Exception("General service error")
        
        # When
        with pytest.raises(Exception) as exception:
            auth_service.sign_up(mock_db_session, mock_sign_up_request)

        # Then
        assert str(exception.value) == "General service error"

    @pytest.mark.description("회원가입 성공")
    @patch("app.user.services.user_service.create_user")
    def test_success(self, mock_create_user, mock_db_session, mock_sign_up_request, mock_user):
        # Given
        mock_create_user.return_value = mock_user
        
        # When
        result = auth_service.sign_up(mock_db_session, mock_sign_up_request)

        #Then
        assert result.name == mock_user.name
        assert result.email == mock_user.email

class TestLogin:
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock(spec=Session)

    @pytest.fixture
    def mock_login_request(self):
        return LoginRequest(
            email="testuser@example.com",
            password="password123",
        )

    @pytest.fixture
    def mock_user(self):
        project = UserProject(
            id = 1,
            user_id = 1,
            role = RoleEnum.VIEWER
        )
        return User(
            id=1,
            name="testuser",
            email="testuser@example.com",
            password = "password123",
            projects = [project]
        )

    @pytest.mark.description("유저 서비스 에러로 예외 발생")
    @patch("app.user.services.user_service.get_user_with_project")
    def test_error_when_user_service_error(self, mock_get_user_with_project, mock_db_session, mock_login_request):
        # Given
        mock_get_user_with_project.side_effect = Exception("General service error")
        
        # When
        with pytest.raises(Exception) as exception:
            auth_service.login(mock_db_session, mock_login_request)

        #Then
        assert str(exception.value) == "General service error"


    @pytest.mark.description("비밀번호가 다를 경우 예외 발생")
    @patch("app.user.services.user_service.get_user_with_project")
    def test_error_when_user_not_found(self, mock_get_user_with_project, mock_db_session):
        # Given
        mock_user = User(
            id=1,
            name="testuser",
            email="testuser@example.com",
            password="wrong_password",
        )
        mock_login_request = LoginRequest(
            email="testuser@example.com",
            password="password123",
        )
        mock_get_user_with_project.return_value = mock_user

        # When
        with pytest.raises(HTTPException) as exception:
            auth_service.login(mock_db_session, mock_login_request)

        # Then
        assert exception.value.status_code == 400
        assert exception.value.detail == "Incorrect username or password"


    @pytest.mark.description("로그인 성공")
    @patch("app.user.services.user_service.get_user_with_project")
    def test_success(self, mock_get_user_with_project, mock_db_session, mock_login_request, mock_user):
        # Given
        mock_get_user_with_project.return_value = mock_user

        # When
        result = auth_service.login(mock_db_session, mock_login_request)

        # Then
        assert isinstance(result, str)
        assert result

class TestCreateAccessToken:
    @pytest.mark.description("참여 프로젝트 없을 경우 토큰 생성 성공")
    @patch("jose.jwt.encode")
    def test_create_access_token(self, mock_encode):
        # Given
        mock_data = UserClaims(id=1, project_roles={})
        mock_encode.return_value = "mocked_token"

        # When
        token = auth_service.create_access_token(mock_data)
        to_encode_arg = mock_encode.call_args[0][0]

        # Then
        assert "exp" in to_encode_arg
        exp = to_encode_arg["exp"]
        
        expected_exp = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(minutes=int(settings.jwt_expire_minutes))
        assert abs((exp - expected_exp).total_seconds()) < 5 

        assert token == "mocked_token"

    @pytest.mark.description("참여 프로젝트 있을 경우 토큰 생성 성공")
    @patch("jose.jwt.encode")
    def test_create_access_token(self, mock_encode):
        # Given
        mock_data = UserClaims(id=1, project_roles={1: RoleEnum.VIEWER})
        mock_encode.return_value = "mocked_token"

        # When
        token = auth_service.create_access_token(mock_data)
        to_encode_arg = mock_encode.call_args[0][0]

        # Then
        assert "exp" in to_encode_arg
        exp = to_encode_arg["exp"]
        
        expected_exp = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(minutes=int(settings.jwt_expire_minutes))
        assert abs((exp - expected_exp).total_seconds()) < 5 

        assert token == "mocked_token"


