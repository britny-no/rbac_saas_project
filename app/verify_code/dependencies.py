from .repositories import VerifyCodeRepository, RedisVerifyCodeRepository

def get_verify_code_repository() -> VerifyCodeRepository:
    return RedisVerifyCodeRepository()
