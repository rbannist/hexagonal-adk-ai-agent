from abc import ABC, abstractmethod
from typing import TypeVar

from .base_output_port import BaseOutputPort
from ..outbound_integration_events.base_outbound_integration_event import IntegrationEvent
# from ..outbound_integration_events.marketing_image_generated_thin_integration_event import MarketingImageGeneratedThinIntegrationEvent


T = TypeVar("T")

class MarketingImageIntegrationEventEventStoreOutputPort(BaseOutputPort[T], ABC):
    """
    Abstract base class for the marketing image integration event event store output port.
    """

    @abstractmethod
    def save(self, integration_event: IntegrationEvent) -> None:
        """
        Saves a marketing image integration event.

        Args:
            integration_event: The integration event to persist.
        """
        raise NotImplementedError