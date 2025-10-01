from abc import ABC, abstractmethod
from typing import Optional, List, TypeVar
import uuid

from .base_output_port import BaseOutputPort

from ...domain.entities.marketing_image_aggregate import MarketingImage

T = TypeVar("T")


class MarketingImageRepositoryOutputPort(BaseOutputPort[T], ABC):
    """
    Abstract base class for the marketing image repository output port.
    """

    @abstractmethod
    def save(self, marketing_image: MarketingImage) -> None:
        """
        Saves a marketing image aggregate.

        Args:
            marketing_image: The MarketingImage aggregate to persist.
        """
        raise NotImplementedError

    @abstractmethod
    def retrieve_by_id(self, id: uuid.UUID) -> Optional[MarketingImage]:
        """
        Retrieves a marketing image aggregate by its ID.

        Args:
            id: The ID of the marketing image to retrieve.

        Returns:
            The MarketingImage aggregate, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def retrieve_all(self) -> List[MarketingImage]:
        """
        Retrieves all marketing image aggregates.

        Returns:
            A list of MarketingImage aggregates.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(self, id: uuid.UUID) -> None:
        """
        Removes a marketing image aggregate by its ID.

        Args:
            id: The ID of the marketing image to remove.
        """
        raise NotImplementedError
