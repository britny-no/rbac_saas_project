from sqlalchemy import Column, BigInteger, String, DateTime, func
from sqlalchemy.orm import validates, relationship
from app.database import Base


class Project(Base):
    __tablename__ = 'project'
    __table_args__ = (
        {"comment": "프로젝트"},
    )

    id = Column(BigInteger, primary_key=True, comment='인덱스')
    name = Column(String(20), unique=False, index=False, comment='이름')
    create_at = Column(DateTime, nullable=False, server_default=func.now(), comment='생성일')
    update_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='수정일')
    delete_at = Column(DateTime, nullable=True, comment='삭제일')


    users = relationship("UserProject",  back_populates="project")
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}