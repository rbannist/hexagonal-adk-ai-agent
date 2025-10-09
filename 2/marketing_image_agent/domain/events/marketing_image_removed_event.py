import uuid

from .base_domain_event import DomainEvent


class MarketingImageRemovedEvent(DomainEvent): # Primitives for decoupling, serialisation, versioning, and clarity of intent.
    def __init__(
        self,
        id: str,
        removed_at: str,
        removed_by: str,
        url: str,
        size: str,
        checksum: str,
        event_id: str = None,
        event_type: str = None,
        event_source: str = None,
        event_occurred_on: str = None,
    ):
        event_type = DomainEvent.get_event_type("removed") if event_type is None else event_type
        event_data = {
            "id": id,
            "removed_at": removed_at,
            "removed_by": removed_by,
            "url": url,
            "size": size,
            "checksum": checksum,
        }
        super().__init__(
            id=str(uuid.uuid4()) if not event_id else event_id,
            type=event_type,
            data=event_data,
            version="1.0",
        )