import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.project.services import project_service
from app.project.models.project import Project
from app.project.schemas.project_schema import CreateProjectRequest


class TestCreateProject:
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock(spec=Session)

    @pytest.fixture
    def mock_create_project_request(self):
        return CreateProjectRequest(name="test project")

    @pytest.mark.description("프로젝트 생성중 db 에러 발생할 경우 예외 발생")
    def test_create_project_db_error(self, mock_db_session, mock_create_project_request):
        #Given
        mock_user_id = 1

        mock_db_session.add.side_effect = SQLAlchemyError("Database error")
        mock_db_session.commit.side_effect = SQLAlchemyError("Database error")

        # When
        with pytest.raises(SQLAlchemyError) as exc_info:
            project_service.create_project(mock_db_session, mock_user_id, mock_create_project_request)
        
        # Then
        assert exc_info.value.args[0] == "Database error"


    @pytest.mark.description("프로젝트 생성 성공")
    def test_create_project_success(self, mock_db_session, mock_create_project_request):
        #Given
        mock_user_id = 1

        mock_db_session.add.return_value = None 
        mock_db_session.commit.return_value = None

        # When
        result = project_service.create_project(mock_db_session, mock_user_id, mock_create_project_request)

        # Then
        assert result.name == "test project"
        assert result.users[0].user_id ==  1