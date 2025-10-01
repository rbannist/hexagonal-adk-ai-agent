import os
import uuid
from datetime import datetime
from abc import ABC
from typing import Dict, Any


service_name = os.getenv("SERVICE_NAME", "marketing-creative-agent")

def _to_dict_recursive(data: Any) -> Any:
    """
    Recursively converts objects to dictionaries if they have a `to_dict` method.
    Also handles datetimes, lists, and dictionaries.
    """
    if hasattr(data, "to_dict") and callable(data.to_dict):
        return data.to_dict()
    if isinstance(data, datetime):
        return data.isoformat() + "Z"
    if isinstance(data, list):
        return [_to_dict_recursive(item) for item in data]
    if isinstance(data, dict):
        return {key: _to_dict_recursive(value) for key, value in data.items()}
    return data

class IntegrationEvent(ABC):
    """Base class for integration events."""

    @staticmethod
    def get_event_type(event_name: str):
        prefix = os.getenv("INTEGRATION_EVENT_PREFIX", "ai.dev.integrationevent.marketing-image")
        return f"{prefix}.{event_name}"

    def __init__(
        self,
        type: str,
        data: Dict[str, Any],
        version: str = "1.0",
        specversion: str = "1.0",
        source:  str | None = None,
        id: str | None = None,
        occurred_at: datetime = None,
        metadata: Dict[str, Any] | None = None,
    ):
        self.type = type  # Integration event type
        self.data = data  # Actual integration event data
        self.source = service_name  # Source of the integration event
        self.version = version  # Integration event schema version
        self.specversion = specversion  # For compatibility with CloudEvents standard
        self.id = id or str(uuid.uuid4())  # Unique ID, default to UUID
        self.occurred_at = occurred_at or datetime.utcnow()  # Timestamp
        self.metadata = metadata if metadata is not None else {}  # Initialise metadata

    def from_dict(cls, data: Dict) -> "IntegrationEvent":
        return cls(
            type=data["type"],
            data=data["data"],
            source=data.get("source", service_name),
            version=data.get("version", "1.0"),
            id=data.get("id"),
            occurred_at=data.get("occurred_at"),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "data": _to_dict_recursive(self.data),
            "source": self.source,
            "version": self.version,
            "occurred_at": self.occurred_at.isoformat() + "Z",
            "metadata": self.metadata,
        }
