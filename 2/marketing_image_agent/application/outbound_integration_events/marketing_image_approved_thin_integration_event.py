import uuid

from .base_outbound_integration_event import IntegrationEvent


class MarketingImageApprovedThinIntegrationEvent(IntegrationEvent):
    """
    A thin integration event that signifies a marketing image has been approved.
    It contains minimal information, primarily the ID of the image, to notify
    other bounded contexts of the state change.
    """

    def __init__(
        self,
        id: str,
        approved_by: str,
        approved_at: str,
        claim_check_token: str,
        event_id: str = None,
        event_type: str = None,
    ):
        event_type = IntegrationEvent.get_event_type("approved") if event_type is None else event_type
        event_data = {
            "id": id,
            "approved_by": approved_by,
            "approved_at": approved_at,
            "claim_check_token": claim_check_token,
        }

        super().__init__(id=str(uuid.uuid4()) if not event_id else event_id, type=event_type, data=event_data, version="1.0")