from abc import ABC, abstractmethod


class ValueObject(ABC):
    """Base class for all value objects in the domain."""

    @abstractmethod
    def __eq__(self, other):
        """Value objects are equal if their attributes are equal."""
        raise NotImplementedError

    @abstractmethod
    def __hash__(self):
        """Returns a hash value for the value object."""
        raise NotImplementedError

    @classmethod
    def from_string(cls, value: str):
        """Returns a value object from a string representation."""
        raise NotImplementedError
    
    @abstractmethod
    def to_string(self) -> str:
        """Returns a string representation of the value object."""
        raise NotImplementedError
    
    @classmethod
    def from_dict(self, data: dict):
        """Returns a value object from a dictionary representation."""
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns a dictionary representation of the value object."""
        raise NotImplementedError
