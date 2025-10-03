import os
import uuid
from datetime import datetime
from abc import ABC
from typing import Dict, Any


service_name = os.getenv("SERVICE_1_NAME", "marketing-creative-agent")

class DomainEvent(ABC): # Primitives for decoupling, serialisation, versioning, and clarity of intent.
    """Base class for domain events."""

    @staticmethod
    def get_event_type(event_name: str):
        prefix = os.getenv("DOMAIN_EVENT_PREFIX", "ai.dev.domain-event.marketing-image")
        return f"{prefix}.{event_name}"

    def __init__(
        self,
        id: str,
        type: str,
        data: Dict[str, Any],
        version: str = "1.0",
        occurred_at: datetime = None,
        time: datetime = None,
    ):
  
        self.id = id or str(uuid.uuid4())  # Unique ID, default to UUID
        self.type = type  # Domain event type
        self.data = data  # Actual domain event data
        self.source = service_name  # Source of the domain event (application service)
        self.version = version  # Domain event schema version
        self.occurred_at = occurred_at or datetime.utcnow()  # Timestamp
        self.time = self.occurred_at

    @classmethod
    def from_dict(cls, data: Dict) -> "DomainEvent":
        return cls(
            type=data["type"],
            data=data["data"],
            source=data.get("source", service_name),
            version=data.get("version", "1.0"),
            id=data.get("id"),
            occurred_at=data.get("occurred_at"),
            time=data.get("occurred_at"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "data": self.data,
            "source": self.source,
            "version": self.version,
            "occurred_at": self.occurred_at.isoformat() + "Z",
            "time": self.occurred_at.isoformat() + "Z",
        }