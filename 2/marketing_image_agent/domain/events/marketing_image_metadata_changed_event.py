import uuid
from typing import Optional, List, Dict
from .base_domain_event import DomainEvent


class MarketingImageMetadataChangedEvent(DomainEvent): # Primitives for decoupling, serialisation, versioning, and clarity of intent.
    def __init__(
        self,
        id: str,
        created_at: str,
        last_modified_at: str,
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
            "created_at": created_at,
            "last_modified_at": last_modified_at,
        }
        if url is not None:
            event_data["url"] = url
        if description is not None:
            event_data["description"] = description
        if keywords is not None:
            event_data["keywords"] = keywords
        if dimensions is not None:
            event_data["dimensions"] = dimensions
        if size is not None:
            event_data["size"] = size
        super().__init__(
            id=str(uuid.uuid4()) if not event_id else event_id,
            type=event_type,
            data=event_data,
            version="1.0",
        )