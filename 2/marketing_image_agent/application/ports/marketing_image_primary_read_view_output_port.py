from abc import ABC, abstractmethod
from typing import TypeVar

from .base_output_port import BaseOutputPort
from ...domain.events.base_domain_event import DomainEvent


T = TypeVar("T")

class MarketingImagePrimaryReadViewOutputPort(BaseOutputPort[T], ABC):
    """
    Abstract base class for the marketing image primary read view output port.
    """

    @abstractmethod
    def project(self, domain_event: DomainEvent) -> None:
        """
        Builds or updates the marketing image primary read view based on a marketing image domain event.

        Args:
            domain_event: The domain event to use to build or update the marketing image primary read view.
        """
        raise NotImplementedError