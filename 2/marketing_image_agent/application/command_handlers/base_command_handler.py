from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..command_objects.base_command_object import Command as command


T = TypeVar("T", bound=command)  # Generic type for commands, bound to Command


class BaseCommandHandler(ABC, Generic[T]):
    """
    Base class for command handlers.  All concrete command handlers should inherit from this class.
    """

    @abstractmethod
    def handle(self, command: T):
        """Handles the given command."""
        pass
