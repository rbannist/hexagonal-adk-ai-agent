from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..outbound_integration_events.base_outbound_integration_event import (
    IntegrationEvent as integration_event,
)


T = TypeVar(
    "T", bound=integration_event
)  # Generic type for integration events, bound to integration_event


class BaseIntegrationEventHandler(ABC, Generic[T]):
    """
    Base class for integration event handlers.  All concrete integration event handlers should inherit from this class.
    """

    @abstractmethod
    def handle(self, integration_event: T):
        """Handles the given integration event."""
        pass
