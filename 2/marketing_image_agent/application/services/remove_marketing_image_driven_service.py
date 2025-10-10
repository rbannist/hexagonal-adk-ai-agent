from ...domain.events.marketing_image_removed_event import MarketingImageRemovedEvent
from ..ports.marketing_image_integration_event_messaging_output_port import MarketingImageIntegrationEventMessagingOutputPort
from ..factories.marketing_image_thin_integration_event_factory import MarketingImageIntegrationEventsFactory


class RemoveMarketingImageDrivenService:
    def __init__(
        self,
        integration_event_prefix: str,
        marketing_image_integration_events_factory: MarketingImageIntegrationEventsFactory,
        marketing_image_integration_event_messaging: MarketingImageIntegrationEventMessagingOutputPort,
    ):
        self.integration_event_prefix = integration_event_prefix
        self.marketing_image_integration_events_factory = marketing_image_integration_events_factory
        self.marketing_image_integration_event_messaging = marketing_image_integration_event_messaging

    def marketing_image_removed(self, marketing_image_removed_domain_event: MarketingImageRemovedEvent) -> dict:
        self.marketing_image_removed_thin_integration_event = self.marketing_image_integration_events_factory.create_from_domain_event(marketing_image_removed_domain_event)
        self.publish_marketing_image_removed_thin_integration_event_response = self.marketing_image_integration_event_messaging.publish(self.marketing_image_removed_thin_integration_event)
        return self.publish_marketing_image_removed_thin_integration_event_response