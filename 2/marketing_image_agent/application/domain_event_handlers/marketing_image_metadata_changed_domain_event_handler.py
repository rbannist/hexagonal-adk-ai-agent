from .base_domain_event_handler import BaseDomainEventHandler
from ..ports.domain_event_output_port import DomainEventOutputPort
from ..ports.domain_event_input_port import DomainEventInputPort
from ..services.change_marketing_image_metadata_driven_service import ChangeMarketingImageMetadataDrivenService
from ...domain.events.marketing_image_metadata_changed_event import MarketingImageMetadataChangedEvent


class MarketingImageMetadataChangedDomainEventHandler(BaseDomainEventHandler, DomainEventInputPort[MarketingImageMetadataChangedEvent]):
    def __init__(
        self,
        driven_service: ChangeMarketingImageMetadataDrivenService,
        domain_event_dispatcher: DomainEventOutputPort,
    ):
        self.driven_service = driven_service
        domain_event_dispatcher.register(MarketingImageMetadataChangedEvent, self)

    def handle(self, domain_event: MarketingImageMetadataChangedEvent):
        """Handles the MarketingImageMetadataChangedEvent domain event by calling the driven service."""
        marketing_image_metadata_changed_domain_event_driven_service_response = self.driven_service.marketing_image_metadata_changed(domain_event)
        return marketing_image_metadata_changed_domain_event_driven_service_response