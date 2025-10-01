from .base_domain_event_handler import BaseDomainEventHandler
from ..ports.domain_event_output_port import DomainEventOutputPort
from ..ports.domain_event_input_port import DomainEventInputPort
from ..services.generate_marketing_image_driven_service import GenerateMarketingImageDrivenService
from ...domain.events.marketing_image_generated_event import MarketingImageGeneratedEvent


class MarketingImageGeneratedDomainEventHandler(BaseDomainEventHandler, DomainEventInputPort[MarketingImageGeneratedEvent]):
    def __init__(
        self,
        driven_service: GenerateMarketingImageDrivenService,
        domain_event_dispatcher: DomainEventOutputPort,
    ):
        self.driven_service = driven_service
        domain_event_dispatcher.register(MarketingImageGeneratedEvent, self)

    def handle(self, domain_event: MarketingImageGeneratedEvent):
        """Handles the MarketingImageGeneratedEvent domain event by calling the driven service."""
        marketing_image_generated_domain_event_driven_service_response = self.driven_service.marketing_image_generated(domain_event)
        return marketing_image_generated_domain_event_driven_service_response