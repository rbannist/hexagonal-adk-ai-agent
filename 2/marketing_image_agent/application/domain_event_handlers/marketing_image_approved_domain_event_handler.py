from .base_domain_event_handler import BaseDomainEventHandler
from ..ports.domain_event_output_port import DomainEventOutputPort
from ..ports.domain_event_input_port import DomainEventInputPort
from ..services.approve_marketing_image_driven_service import ApproveMarketingImageDrivenService
from ...domain.events.marketing_image_approved_event import MarketingImageApprovedEvent


class MarketingImageApprovedDomainEventHandler(BaseDomainEventHandler, DomainEventInputPort[MarketingImageApprovedEvent]):
    def __init__(
        self,
        driven_service: ApproveMarketingImageDrivenService,
        domain_event_dispatcher: DomainEventOutputPort,
    ):
        self.driven_service = driven_service
        domain_event_dispatcher.register(MarketingImageApprovedEvent, self)

    def handle(self, domain_event: MarketingImageApprovedEvent):
        """Handles the MarketingImageApprovedEvent domain event by calling the driven service."""
        marketing_image_approved_domain_event_driven_service_response = self.driven_service.marketing_image_approved(domain_event)
        return marketing_image_approved_domain_event_driven_service_response