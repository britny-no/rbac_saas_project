from abc import ABC, abstractmethod
from typing import Dict

class EmailSender(ABC):
    @abstractmethod
    def send(self, user_id: int) -> Dict[str, str]:
        pass