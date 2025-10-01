from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Any

from .base_output_port import BaseOutputPort

T = TypeVar("T")


class DomainEventOutputPort(BaseOutputPort[T], ABC, Generic[T]):
    @abstractmethod  # Used by handlers
    def register(self, domain_event_type: Type[T], handler: Any):
        """
        Register a domain event handler.

        Args:
            domain_event_type (Type[T]): The type of domain event to register the handler for.
            handler (Any): The handler to register.
        """

    @abstractmethod  # Used by the dispatcher
    def dispatch(self, domain_event: T):
        """
        Dispatch a domain event.

        Args:
            domain_event (T): The domain event to dispatch.
        """