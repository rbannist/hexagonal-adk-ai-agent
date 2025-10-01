import uuid

from .base_domain_event import DomainEvent


class MarketingImageModifiedEvent(DomainEvent): # Primitives for decoupling, serialisation, versioning, and clarity of intent.
    def __init__(
        self,
        id: str,
        url: str,
        description: str,
        keywords: dict,
        generation_model: str,
        generation_parameters: dict,
        dimensions: dict,
        size: str,
        mime_type: str,
        checksum: str,
        created_at: str,
        last_modified_at: str,
        event_id: str = None,
        event_type: str = None,
        event_source: str = None,
        event_occurred_on: str = None,
    ):
        event_type = DomainEvent.get_event_type("modified") if event_type is None else event_type
        event_data = {
            "id": id,
            "url": url,
            "description": description,
            "keywords": keywords,
            "generation_model": generation_model,
            "generation_parameters": generation_parameters,
            "dimensions": dimensions,
            "size": size,
            "mime_type": mime_type,
            "checksum": checksum,
            "created_at": created_at,
            "last_modified_at": last_modified_at,
        }
        super().__init__(
            id=str(uuid.uuid4()) if not event_id else event_id,
            type=event_type,
            data=event_data,
            version="1.0",
        )
