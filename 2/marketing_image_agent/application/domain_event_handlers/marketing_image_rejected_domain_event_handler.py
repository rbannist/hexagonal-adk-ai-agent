from .base_domain_event_handler import BaseDomainEventHandler
from ..ports.domain_event_output_port import DomainEventOutputPort
from ..ports.domain_event_input_port import DomainEventInputPort
from ..services.reject_marketing_image_driven_service import RejectMarketingImageDrivenService
from ...domain.events.marketing_image_rejected_event import MarketingImageRejectedEvent


class MarketingImageRejectedDomainEventHandler(BaseDomainEventHandler, DomainEventInputPort[MarketingImageRejectedEvent]):
    def __init__(
        self,
        driven_service: RejectMarketingImageDrivenService,
        domain_event_dispatcher: DomainEventOutputPort,
    ):
        self.driven_service = driven_service
        domain_event_dispatcher.register(MarketingImageRejectedEvent, self)

    def handle(self, domain_event: MarketingImageRejectedEvent):
        """Handles the MarketingImageRejectedEvent domain event by calling the driven service."""
        marketing_image_rejected_domain_event_driven_service_response = self.driven_service.marketing_image_rejected(domain_event)
        return marketing_image_rejected_domain_event_driven_service_response