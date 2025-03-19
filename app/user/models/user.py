from sqlalchemy import Column, BigInteger, String, DateTime, func
from sqlalchemy.orm import validates
from app.database import Base
from app.enums import UserRoleEnum


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, comment='인덱스')
    email = Column(String(50), unique=True, index=True, comment='이메일')
    password = Column(String(100), comment='비밀번호')
    name = Column(String(20), unique=False, index=False, comment='이름')
    create_at = Column(DateTime, nullable=False, server_default=func.now(), comment='생성일')
    update_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='수정일')
    delete_at = Column(DateTime, nullable=True, comment='삭제일')



    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
