import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


from app.user.services import user_service
from app.user.models.user import User
from app.user.schemas.user_schema import UserCreate

class TestGetUserWithProject:
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock(spec=Session)
    
    @pytest.fixture
    def mock_user(self):
        return User(
            id=1,
            name="testuser",
            email="testuser@example.com",
        )


    @pytest.mark.description("사용자가 없을 경우 404 에외 발생")
    def test_error_when_user_not_found(self, mock_db_session):
        # When
        mock_db_session.query().options().filter().first.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            user_service.get_user_with_project(mock_db_session, 999)

        #Then
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found"

    @pytest.mark.description("유저 조회중 db 에러 발생할 경우 예외 발생")
    def test_error_when_db_error(self, mock_db_session):
        # Given
        
        # When
        mock_db_session.query().options().filter().first.side_effect = SQLAlchemyError("Database error")

        # Then
        with pytest.raises(SQLAlchemyError) as exc_info:
            user_service.get_user_with_project(mock_db_session, "nonexistent-email@example.com")
        
        assert exc_info.value.args[0] == "Database error" 

    @pytest.mark.description("조회 성공")
    def test_success(self, mock_db_session, mock_user):
        # Given
        # When
        mock_db_session.query().options().filter().first.return_value = mock_user

        # Then
        result = user_service.get_user_with_project(mock_db_session, 1)
        assert result == mock_user

class TestGetUserWithProject:
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock(spec=Session)
    
    @pytest.fixture
    def mock_user(self):
        return User(
            id=1,
            name="testuser",
            email="testuser@example.com",
        )

    @pytest.fixture
    def mock_user_create(self):
        return UserCreate(name="test project", email="test@naver.com", password="123")

    @pytest.mark.description("유저 생성중 db 에러 발생할 경우 예외 발생")
    def test_create_user_db_error(self, mock_db_session, mock_user_create):
        # When
        mock_db_session.add.side_effect = SQLAlchemyError("Database error")
        mock_db_session.commit.side_effect = SQLAlchemyError("Database error")

        # Then
        with pytest.raises(SQLAlchemyError) as exc_info:
            user_service.create_user(mock_db_session, mock_user_create)
        
        assert exc_info.value.args[0] == "Database error"

    @pytest.mark.description("사용자 생성 성공")
    def test_create_user_success(self, mock_db_session, mock_user_create):
        # When
        mock_db_session.add.return_value = None 
        mock_db_session.commit.return_value = None
        
        # Then
        result = user_service.create_user(mock_db_session, mock_user_create)
        assert result.name == "test project"
        assert result.email == "test@naver.com"
        assert result.password == "123"
