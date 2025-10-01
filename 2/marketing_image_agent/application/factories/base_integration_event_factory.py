from abc import ABC, abstractmethod


class IntegrationEventFactory(ABC):
    """
    Abstract base class for integration event factories.
    These factories are responsible for creating and/or reconstituting Integration Events.
    """

    @abstractmethod
    def create_from_domain_event(self, *args, **kwargs):
        """Abstract method to create an integration event from a domain event."""
        pass

    @abstractmethod
    def reconstitute(self, *args, **kwargs):
        """Abstract method to reconstitute an integration event from a dictionary."""
        pass