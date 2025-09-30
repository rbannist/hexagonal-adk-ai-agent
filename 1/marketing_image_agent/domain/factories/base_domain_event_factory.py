from abc import ABC, abstractmethod


class DomainEventFactory(ABC):
    """
    Abstract base class for domain event factories.
    These factories are responsible for creating and/or reconstituting Domain Events.
    """

    @abstractmethod
    def reconstitute(self, *args, **kwargs):
        """Abstract method to reconstitute a domain event from a dictionary."""
        pass