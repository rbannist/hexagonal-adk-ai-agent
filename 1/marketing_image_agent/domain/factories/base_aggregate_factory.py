from abc import ABC, abstractmethod


class AggregateFactory(ABC):
    """
    Abstract base class for aggregate factories.
    These factories are responsible for creating complex objects (Entities, ValueObjects, Aggregates)
    and ensuring their invariants are met during creation.
    """

    @abstractmethod
    def create(self, *args, **kwargs):
        """Abstract method to create an object."""
        pass
