import uuid

from .base_domain_event import DomainEvent


class MarketingImageRejectedEvent(DomainEvent): # Primitives for decoupling, serialisation, versioning, and clarity of intent.
    def __init__(
        self,
        id: str,
        rejected_at: str,
        rejected_by: str,
        url: str,
        checksum: str,
        event_id: str = None,
        event_type: str = None,
        event_source: str = None,
        event_occurred_on: str = None,
    ):
        event_type = DomainEvent.get_event_type("rejected") if event_type is None else event_type
        event_data = {
            "id": id,
            "rejected_at": rejected_at,
            "rejected_by": rejected_by,
            "url": url,
            "checksum": checksum,
        }
        super().__init__(
            id=str(uuid.uuid4()) if not event_id else event_id,
            type=event_type,
            data=event_data,
            version="1.0",
        )