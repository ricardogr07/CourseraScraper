from abc import ABC, abstractmethod
from typing import Optional
from utils.logger import Logger

class Handler(ABC):

    def __init__(self):
        self.logger = Logger("CourseraScraper.log")

    @abstractmethod
    def process(self) -> None:
        """Method that every handler must implement to perform its task"""
        pass
