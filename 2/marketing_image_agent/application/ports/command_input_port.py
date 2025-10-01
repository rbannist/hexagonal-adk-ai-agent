from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .base_input_port import BaseInputPort

T = TypeVar("T")


class CommandInputPort(BaseInputPort[T], ABC, Generic[T]):
    @abstractmethod
    def handle(self, command: T):
        """
        Handle a command.

        Args:
            command (T): The command to handle.
        """
