from datetime import datetime
from .base_value_object import ValueObject


class Timestamp(ValueObject):
    """
    Represents a specific point in time.
    """

    def __init__(self, timestamp: datetime = None):
        self.timestamp = timestamp if timestamp is not None else datetime.now()
    
    def __eq__(self, other):
        if not isinstance(other, Timestamp):
            return False
        return self.timestamp == other.timestamp

    def __hash__(self):
        return hash(self.timestamp)

    @classmethod
    def from_string(cls, timestamp: str):
        return Timestamp(timestamp=datetime.fromisoformat(timestamp))
    
    def to_string(self):
        return self.timestamp.isoformat()
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(timestamp=datetime.fromisoformat(data["timestamp"])) # Convert string
    
    def to_dict(self):
        return {"timestamp": self.timestamp.isoformat()} # String

    def __str__(self):
        return self.timestamp.isoformat()

    def __repr__(self):
        return f"Timestamp(timestamp={self.timestamp})"


class CreatedAt(Timestamp):
    """
    Represents the creation timestamp of an entity.
    """

    def __init__(self, timestamp: datetime = None):
        super().__init__(timestamp)

    @classmethod
    def now(cls):
        return cls(datetime.now())
    def __repr__(self):
        return f"CreatedAt(timestamp={self.timestamp})"


class LastModifiedAt(Timestamp):
    """
    Represents the last modified timestamp of an entity.
    """

    def __init__(self, timestamp: datetime = None):
        super().__init__(timestamp)

    @classmethod
    def now(cls):
        return cls(datetime.now())
    def __repr__(self):
        return f"LastModifiedAt(timestamp={self.timestamp})"