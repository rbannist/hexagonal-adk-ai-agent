import uuid

from .base_outbound_integration_event import IntegrationEvent


class MarketingImageMetadataChangedThinIntegrationEvent(IntegrationEvent):
    """
    A thin integration event that signifies a marketing image has had its metadata changed.
    """

    def __init__(
        self,
        id: str,
        changed_by: str,
        changed_at: str,
        event_id: str = None,
        event_type: str = None,
        **kwargs,
    ):
        event_type = IntegrationEvent.get_event_type("metadata-changed") if event_type is None else event_type
        event_data = {
            "id": id,
            "changed_by": changed_by,
            "changed_at": changed_at,
        }

        changed_metadata = {k: v for k, v in kwargs.items() if v is not None}
        if changed_metadata:
            event_data["changed_metadata"] = changed_metadata

        super().__init__(id=str(uuid.uuid4()) if not event_id else event_id, type=event_type, data=event_data, version="1.0")