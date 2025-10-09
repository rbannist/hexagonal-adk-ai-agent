from .base_domain_event_handler import BaseDomainEventHandler
from ..ports.domain_event_output_port import DomainEventOutputPort
from ..ports.domain_event_input_port import DomainEventInputPort
from ..services.remove_marketing_image_driven_service import RemoveMarketingImageDrivenService
from ...domain.events.marketing_image_removed_event import MarketingImageRemovedEvent


class MarketingImageRemovedDomainEventHandler(BaseDomainEventHandler, DomainEventInputPort[MarketingImageRemovedEvent]):
    def __init__(
        self,
        driven_service: RemoveMarketingImageDrivenService,
        domain_event_dispatcher: DomainEventOutputPort,
    ):
        self.driven_service = driven_service
        domain_event_dispatcher.register(MarketingImageRemovedEvent, self)

    def handle(self, domain_event: MarketingImageRemovedEvent):
        """Handles the MarketingImageRemovedEvent domain event by calling the driven service."""
        marketing_image_removed_domain_event_driven_service_response = self.driven_service.marketing_image_removed(domain_event)
        return marketing_image_removed_domain_event_driven_service_response