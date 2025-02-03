from abc import ABC, abstractmethod
from typing import List


class BaseCommand(ABC):
    REQUIRED_ARGUMENTS = []
    POSSIBLE_OPTIONS = []

    def __init__(self, arguments: List[str]):
        self._args = arguments

    @abstractmethod
    def validate_args(self):
        pass
