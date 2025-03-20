import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.user.services.user_service import get_user
from app.user.models.user import User

@pytest.mark.description("사용자가 없을 경우 404 에러 발생 시나리오")
def test_get_user_not_found():
    # Given
    db = MagicMock(spec=Session)

    # When
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        get_user(db, 999)

    #Then
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


@pytest.mark.description("사용자 조회 성공 시나리오")
def test_get_user_success():
    # Given
    db = MagicMock(spec=Session)
    mock_user = User(id=1, name="testuser", email="test@example.com")

    # When
    db.query().filter().first.return_value = mock_user

    # Then
    result = get_user(db, 1)
    assert result == mock_user
    db.query().filter().first.assert_called_once()