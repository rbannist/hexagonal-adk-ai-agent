from ...domain.events.marketing_image_generated_event import MarketingImageGeneratedEvent
from ..ports.marketing_image_integration_event_messaging_output_port import MarketingImageIntegrationEventMessagingOutputPort
from ..ports.marketing_image_integration_event_event_store_output_port import MarketingImageIntegrationEventEventStoreOutputPort
from ..ports.marketing_image_primary_read_view_output_port import MarketingImagePrimaryReadViewOutputPort
# from ..outbound_integration_events.marketing_image_generated_thin_integration_event import MarketingImageGeneratedThinIntegrationEvent
from ..factories.marketing_image_thin_integration_event_factory import MarketingImageIntegrationEventsFactory


class GenerateMarketingImageDrivenService:
    def __init__(
        self,
        marketing_image_integration_event_messaging: MarketingImageIntegrationEventMessagingOutputPort,
        marketing_image_integration_event_event_store: MarketingImageIntegrationEventEventStoreOutputPort,
        marketing_image_primary_read_view: MarketingImagePrimaryReadViewOutputPort
    ):
        self.marketing_image_integration_event_messaging = marketing_image_integration_event_messaging
        self.marketing_image_integration_event_event_store = marketing_image_integration_event_event_store
        self.marketing_image_primary_read_view = marketing_image_primary_read_view

    def marketing_image_generated(self, marketing_image_generated_domain_event: MarketingImageGeneratedEvent) -> dict:
        self.marketing_image_generated_thin_integration_event = MarketingImageIntegrationEventsFactory().create_from_domain_event(marketing_image_generated_domain_event)
        self.publish_marketing_image_generated_thin_integration_event_response = self.marketing_image_integration_event_messaging.publish(self.marketing_image_generated_thin_integration_event)
        return self.publish_marketing_image_generated_thin_integration_event_response