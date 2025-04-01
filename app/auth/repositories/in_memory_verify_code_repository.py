from fastapi import HTTPException
from typing import Optional, Dict
from cachetools import TTLCache

from .verify_code_repository import VerifyCodeRepository


class InMemoryVerifyCodeRepository(VerifyCodeRepository):
    def __init__(self, max_cache_size: int = 100, ttl_seconds: int = 180):
        self.storage = TTLCache(maxsize=max_cache_size, ttl=ttl_seconds)

    def save(self, key: str) -> str:
        value = self._generate_random_number()
        self.storage[key] = value
        return value

    def get(self, key: str) -> str:
        result = self.storage.get(key)
        
        if result is None:
            raise HTTPException(status_code=400, detail="no value")
        
        return result

    def delete(self, key: str) -> None:
        self.storage.pop(key, None)