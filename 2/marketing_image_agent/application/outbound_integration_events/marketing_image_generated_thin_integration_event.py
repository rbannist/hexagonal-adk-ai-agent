import uuid

from .base_outbound_integration_event import IntegrationEvent


class MarketingImageGeneratedThinIntegrationEvent(IntegrationEvent):

    def __init__(
        self,
        id: str,
        url: str,
        description: str,
        dimensions: dict,
        size: str,
        mime_type: str,
        checksum: str,
        created_by: str,
        created_at: str,
        event_id: str = None,
        event_type: str = None,
        event_source: str = None,
        event_occurred_on: str = None,
    ):
        event_type = IntegrationEvent.get_event_type("generated") if event_type is None else event_type
        event_data = {
            "id": id,
            "url": url,
            "description": description,
            "dimensions": dimensions,
            "size": size,
            "mime_type": mime_type,
            "checksum": checksum,
            "created_by": created_by,
            "created_at": created_at,
        }

        super().__init__(
            id=str(uuid.uuid4()) if not event_id else event_id,
            type=event_type,  # Integration event type
            data=event_data,  # Actual integration event data
            version="1.0",  # Integration event schema version
        )