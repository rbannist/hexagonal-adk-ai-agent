import uuid
from typing import Optional, List, Dict
from .base_domain_event import DomainEvent


class MarketingImageMetadataChangedEvent(DomainEvent): # Primitives for decoupling, serialisation, versioning, and clarity of intent.
    def __init__(
        self,
        id: str,
        changed_at: str,
        changed_by: str,
        url: Optional[str] = None,
        description: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        dimensions: Optional[Dict[str, int]] = None,
        size: Optional[int] = None,
        event_id: str = None,
        event_type: str = None,
        event_source: str = None,
        event_occurred_on: str = None,
    ):
        event_type = DomainEvent.get_event_type("metadata-changed") if event_type is None else event_type
        event_data = {
            "id": id,
            "changed_at": changed_at,
            "changed_by": changed_by,
        }
        # Only add optional fields to event_data if they are not None
        optional_fields = {
            "url": url,
            "description": description,
            "keywords": keywords,
            "dimensions": dimensions,
            "size": size,
        }
        event_data.update({k: v for k, v in optional_fields.items() if v is not None})

        super().__init__(
            id=str(uuid.uuid4()) if not event_id else event_id,
            type=event_type,
            data=event_data,
            version="1.0",
        )