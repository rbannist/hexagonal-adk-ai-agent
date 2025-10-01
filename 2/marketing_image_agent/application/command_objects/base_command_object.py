from typing import Dict, Any
from abc import ABC
import uuid
from datetime import datetime


class Command(ABC):
    """Base class for command objects."""

    def __init__(
        self,
        type: str,
        data: Dict[str, Any],
        source: str,
        version: str = "1.0",
        id: str | None = None,
        time: datetime | None = None,
        metadata: Dict[str, Any] | None = None,
    ):
        self.type = type  # Command type
        self.data = data  # Actual command data
        self.source = source  # Source of the command (application service)
        self.version = version  # Command schema version
        self.id = id or str(uuid.uuid4())  # Unique ID, default to UUID
        self.time = time or datetime.utcnow()  # Timestamp
        self.metadata = metadata if metadata is not None else {}  # Initialise metadata

    @classmethod
    def from_dict(cls, data: Dict) -> "Command":
        # The 'type' is hardcoded in subclasses, so we don't pass it here.
        # Subclasses can override this if they have more complex instantiation logic.
        command_data = data.copy()
        command_data.pop("type", None)  # Remove type to avoid passing it to subclass __init__
        command_data.pop("time", None) # Will be set by base __init__ if not present
        command_data.pop("id", None) # Will be set by base __init__ if not present
        return cls(**command_data)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "data": self.data,
            "source": self.source,
            "version": self.version,
            "time": self.time.isoformat() + "Z",
            "metadata": self.metadata,
        }
