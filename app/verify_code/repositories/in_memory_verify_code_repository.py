from fastapi import HTTPException
from typing import Optional, Dict
from cachetools import TTLCache

from .verify_code_repository import VerifyCodeRepository


class InMemoryVerifyCodeRepository(VerifyCodeRepository):
    _instance = None

    def __new__(cls, max_cache_size: int = 100, ttl_seconds: int = 180):
        if not cls._instance:
            cls._instance = super(InMemoryVerifyCodeRepository, cls).__new__(cls)
            cls._instance.storage = TTLCache(maxsize=max_cache_size, ttl=ttl_seconds)
        return cls._instance

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