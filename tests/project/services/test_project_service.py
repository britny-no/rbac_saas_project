import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.project.services.project_service import create_project
from app.project.models.project import Project
from app.project.schemas.project_schema import CreateProjectRequest


@pytest.mark.description("프로젝트 생성중 db 에러 발생할 경우 예외 발생")
def test_create_project_db_error():
    # Given
    db = MagicMock(spec=Session)
    
    # When
    db.add.side_effect = SQLAlchemyError("Database error")
    db.commit.side_effect = SQLAlchemyError("Database error")

    # Then
    with pytest.raises(SQLAlchemyError) as exc_info:
        create_project(db, 1, CreateProjectRequest(name="test project"))
    
    assert exc_info.value.args[0] == "Database error"


@pytest.mark.description("프로젝트 생성 성공")
def test_create_project_success():
    # Given
    db = MagicMock(spec=Session)
    
    # When
    db.add.return_value = None 
    db.commit.return_value = None

    # Then
    result = create_project(db, 1, CreateProjectRequest(name="test project"))

    assert result.name == "test project"
    assert result.users[0].user_id ==  1