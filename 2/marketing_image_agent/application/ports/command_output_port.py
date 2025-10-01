from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Any

from .base_output_port import BaseOutputPort

T = TypeVar("T")


class CommandOutputPort(BaseOutputPort[T], ABC, Generic[T]):
    @abstractmethod   # Used by handlers
    def register(self, command_type: Type[T], handler: Any):
        """
        Register a command handler.

        Args:
            command_type (Type[T]): The type of command to register the handler for.
            handler (Any): The handler to register.
        """
    
    @abstractmethod  # Used by the dispatcher
    def dispatch(self, command: T):
        """
        Dispatch a command.

        Args:
            command (T): The command to dispatch.
        """
