from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ...domain.events.base_domain_event import DomainEvent as domain_event


T = TypeVar(
    "T", bound=domain_event
)  # Generic type for domain_events, bound to domain_event


class BaseDomainEventHandler(ABC, Generic[T]):
    """
    Base class for domain event handlers.  All concrete domain event handlers should inherit from this class.
    """

    @abstractmethod
    def handle(self, domain_event: T):
        """Handles the given domain event."""
        pass