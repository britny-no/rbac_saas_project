from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import validates
from app.database import Base
from app.enums import UserRoleEnum


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(20), unique=False, index=False)
    email = Column(String(50), unique=True, index=True)
    full_name = Column(String(20))
    password = Column(String)
    role = Column(String(20))


    @validates('role')
    def validate_role(self, key, role):
        if role not in [item.value for item in UserRoleEnum]:
            raise ValueError(f"Invalid role: {role}")
        return role
