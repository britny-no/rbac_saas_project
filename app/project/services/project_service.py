from sqlalchemy.orm import Session, joinedload

from app.enums import RoleEnum
from app.context_managers import transaction
from app.user.models.user_project import UserProject
from app.project.models.project import Project
from app.project.schemas.project_schema import CreateProjectRequest


def create_project(db:Session, user_id: int, project: CreateProjectRequest) -> Project:
    with transaction(db):
        db_project = Project(name=project.name)
        db_user_project = UserProject(user_id=user_id, project_id=db_project.id, role=RoleEnum.PO)
        db_project.users.append(db_user_project)  

        db.add(db_project)

        db.commit()
        db.refresh(db_project)

        return db_project