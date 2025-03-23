import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


from app.user.services.user_service import get_user, create_user
from app.user.models.user import User
from app.user.schemas.user_schema import UserCreate


@pytest.mark.description("사용자가 없을 경우 404 에외 발생")
def test_get_user_not_found():
    # Given
    db = MagicMock(spec=Session)

    # When
    db.query().options().filter().first.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        get_user(db, 999)

    #Then
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"

@pytest.mark.description("유저 조회중 db 에러 발생할 경우 예외 발생")
def test_get_user_db_error():
    # Given
    db = MagicMock(spec=Session)
    
    # When
    db.query().options().filter().first.side_effect = SQLAlchemyError("Database error")

    # Then
    with pytest.raises(SQLAlchemyError) as exc_info:
        get_user(db, "nonexistent-email@example.com")
    
    assert exc_info.value.args[0] == "Database error" 

@pytest.mark.description("사용자 조회 성공")
def test_get_user_success():
    # Given
    db = MagicMock(spec=Session)
    mock_user = User(id=1, name="testuser", email="test@example.com")

    # When
    db.query().options().filter().first.return_value = mock_user

    # Then
    result = get_user(db, 1)
    assert result == mock_user


@pytest.mark.description("유저 생성중 db 에러 발생할 경우 예외 발생")
def test_create_user_db_error():
    # Given
    db = MagicMock(spec=Session)
    
    # When
    db.add.side_effect = SQLAlchemyError("Database error")
    db.commit.side_effect = SQLAlchemyError("Database error")

    # Then
    with pytest.raises(SQLAlchemyError) as exc_info:
        create_user(db, UserCreate(name="test project", email="test@naver.com", password="123"))
    
    assert exc_info.value.args[0] == "Database error"

@pytest.mark.description("사용자 생성 성공")
def test_create_user_success():
    # Given
    db = MagicMock(spec=Session)

    # When
    db.add.return_value = None 
    db.commit.return_value = None
    
    # Then
    result = create_user(db, UserCreate(name="test project", email="test@naver.com", password="123"))
    assert result.name == "test project"
    assert result.email == "test@naver.com"
    assert result.password == "123"
