from sqlalchemy import Column, BigInteger, String, DateTime, func, TIMESTAMP, ForeignKeyConstraint
from sqlalchemy.orm import validates, relationship
from app.database import Base


class UserProject(Base):
    __tablename__ = "user_project"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"], ["user.id"], ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["project_id"], ["project.id"], ondelete="CASCADE"
        ),
        {"comment": "유저 프로젝트 관계 테이블"},
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="인덱스")
    user_id = Column(BigInteger, nullable=False, index=True, comment="인덱스")
    project_id = Column(BigInteger, nullable=False, index=True, comment="인덱스")
    role = Column(String(20), default="viewer", nullable=False, comment="역할")
    create_at = Column(DateTime, nullable=False, server_default=func.now(), comment='생성일')

    user = relationship("User", back_populates="projects")
    project = relationship("Project", back_populates="users")

    def __repr__(self):
        return (
            f"<UserProject(id={self.id}, user_id={self.user_id}, "
            f"project_id={self.project_id}, role={self.role}, create_at={self.create_at})>"
        )

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "role": self.role,
            "create_at": self.create_at,
        }