from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .base_input_port import BaseInputPort

T = TypeVar("T")


class DomainEventInputPort(BaseInputPort[T], ABC, Generic[T]):
    @abstractmethod
    def handle(self, domain_event: T):
        """
        Handle a domain event.

        Args:
            domain_event (T): The domain event to handle.
        """
