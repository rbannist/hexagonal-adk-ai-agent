import uuid

from .base_outbound_integration_event import IntegrationEvent

class MarketingImageModifiedThinIntegrationEvent(IntegrationEvent):

    def __init__(
        self,
        id: str,
        modified_by: str,
        modified_at: str,
        url: str,
        description: str,
        dimensions: dict,
        size: str,
        mime_type: str,
        checksum: str,
        claim_check_token: str,
        event_id: str = None,
        event_type: str = None,
        event_source: str = None,
        event_occurred_on: str = None,
    ):
        event_type = IntegrationEvent.get_event_type("modified") if event_type is None else event_type
        event_data = {
            "id": id,
            "modified_at": modified_at,
            "modified_by": modified_by,
            "url": url,
            "description": description,
            "dimensions": dimensions,
            "size": size,
            "mime_type": mime_type,
            "checksum": checksum,
            "claim_check_token": claim_check_token,
        }

        super().__init__(
            id=str(uuid.uuid4()) if not event_id else event_id,
            type=event_type,  # Integration event type
            data=event_data,  # Actual integration event data
            version="1.0",  # Integration event schema version
        )