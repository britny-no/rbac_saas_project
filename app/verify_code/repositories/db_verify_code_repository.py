from sqlalchemy.orm import Session

from verify_code_repository import VerifyCodeRepository


class DBVerifyCodeRepository(VerifyCodeRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, key: str) -> str:
        pass

    def get(self, key: str) -> str:
        pass

    def delete(self, key: str) -> None:
        pass
