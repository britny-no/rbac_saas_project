from abc import ABC, abstractmethod
from typing import Optional
import random
import string

class VerifyCodeService(ABC):
    @abstractmethod
    def save(self, key: str) -> str:
        pass

    @abstractmethod
    def get(self, key: str) -> str:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    def _generate_random_number(length: int = 6) -> int:
        return random.randint(10**(length-1), 10**length - 1)

