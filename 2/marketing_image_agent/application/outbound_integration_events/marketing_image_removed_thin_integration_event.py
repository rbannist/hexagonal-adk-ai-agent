import uuid

from .base_outbound_integration_event import IntegrationEvent


class MarketingImageRemovedThinIntegrationEvent(IntegrationEvent):
    """
    A thin integration event that signifies a marketing image has been removed.
    It contains minimal information, primarily the ID of the image, to notify
    other bounded contexts of the state change.
    """

    def __init__(
        self,
        id: str,
        removed_by: str,
        removed_at: str,
        event_id: str = None,
        event_type: str = None,
    ):
        event_type = IntegrationEvent.get_event_type("removed") if event_type is None else event_type
        event_data = {
            "id": id,
            "removed_by": removed_by,
            "removed_at": removed_at,
        }

        super().__init__(id=str(uuid.uuid4()) if not event_id else event_id, type=event_type, data=event_data, version="1.0")