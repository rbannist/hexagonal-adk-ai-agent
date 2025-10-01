from typing import Dict, Type

from ....application.ports.domain_event_output_port import DomainEventOutputPort
from ....application.ports.domain_event_input_port import DomainEventInputPort
from ....domain.events.base_domain_event import DomainEvent


class InMemoryDomainEventDispatcher(DomainEventOutputPort):
    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], DomainEventInputPort] = {}

    def register(self, domain_event_type: Type[DomainEvent], handler: DomainEventInputPort):
        self._handlers[domain_event_type] = handler

    def dispatch(self, domain_event: DomainEvent):
        handler = self._handlers.get(type(domain_event))
        if handler:
            response = handler.handle(domain_event)
            return response
        else:
            raise ValueError(f"No handler registered for domain event type: {type(domain_event)}")