from abc import ABC, abstractmethod
from typing import Optional

class Handler(ABC):
    @abstractmethod
    def process(self) -> None:
        """Method that every handler must implement to perform its task"""
        pass
