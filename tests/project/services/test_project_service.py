import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.project.services.project_service import create_project
from app.project.models.project import Project

@pytest.mark.description("사용자가 없을 경우 404 에외 발생")
def test__not_found():
    # Given
    db = MagicMock(spec=Session)

    # When
    db.query().options().filter().first.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        get_user(db, 999)

    #Then
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"