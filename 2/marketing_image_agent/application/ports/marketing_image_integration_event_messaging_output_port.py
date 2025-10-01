from abc import ABC, abstractmethod
from typing import TypeVar

from .base_output_port import BaseOutputPort
from ..outbound_integration_events.base_outbound_integration_event import IntegrationEvent


T = TypeVar("T")

class MarketingImageIntegrationEventMessagingOutputPort(BaseOutputPort[T], ABC):
    """
    Abstract base class for the marketing image integration event messaging output port.
    """

    @abstractmethod
    def publish(self, integration_event: IntegrationEvent) -> None:
        """
        Publishes a marketing image integration event to a broker/queue/topic.

        Args:
            integration_event: The integration event to publish.
        """
        raise NotImplementedError