from .repositories import VerifyCodeRepository, InMemoryVerifyCodeRepository

def get_verify_code_repository() -> VerifyCodeRepository:
    return InMemoryVerifyCodeRepository()
