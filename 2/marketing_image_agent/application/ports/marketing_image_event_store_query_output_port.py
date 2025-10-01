from abc import ABC, abstractmethod
from typing import Optional, List, TypeVar
from datetime import datetime
import uuid

from .base_output_port import BaseOutputPort

from ...domain.events.marketing_image_accepted_event import MarketingImageAcceptedEvent
from ...domain.events.marketing_image_rejected_event import MarketingImageRejectedEvent
from ...domain.events.marketing_image_removed_event import MarketingImageRemovedEvent
from ...domain.events.marketing_image_modified_event import MarketingImageModifiedEvent
from ...domain.events.marketing_image_generated_event import MarketingImageGeneratedEvent
from ...domain.events.marketing_image_metadata_changed_event import MarketingImageMetadataChangedEvent

T = TypeVar("T")


class MarketingImageDomainEventEventStoreQueryOutputPort(BaseOutputPort[T], ABC):
    """
    Abstract base class for a marketing image event store query-only output port.
    """

    @abstractmethod
    def retrieve_by_event_id(self, id: uuid.UUID, aggregate_id: uuid.UUID = None) -> Optional[MarketingImageGeneratedEvent | MarketingImageModifiedEvent | MarketingImageAcceptedEvent | MarketingImageRejectedEvent | MarketingImageRemovedEvent | MarketingImageMetadataChangedEvent]:
        """
        Retrieves a marketing image domain event by its event ID.

        Args:
            id: The ID of the marketing image domain event to retrieve.
            (Optional) aggregate_id: The ID of the aggregate that the event belongs to.

        Returns:
            The MarketingImage domain event, or None if not found.
        """
        raise NotImplementedError
    
    @abstractmethod
    def retrieve_by_aggregate_id(self, aggregate_id: uuid.UUID, event_type: str = None, start_date: datetime = None, end_date: datetime = None) -> List[MarketingImageGeneratedEvent | MarketingImageModifiedEvent | MarketingImageAcceptedEvent | MarketingImageRejectedEvent | MarketingImageRemovedEvent | MarketingImageMetadataChangedEvent]:
        """
        Retrieves all marketing image domain events for a specific aggregate ID.

        Args:
            aggregate_id: The ID of the aggregate to retrieve events for.
            (Optional) event_type: The type of marketing image domain events to retrieve.
            (Optional) start_date: The start date to filter events by.
            (Optional) end_date: The end date to filter events by.

        Returns:
            A list of MarketingImage domain events.
        """
        raise NotImplementedError


    @abstractmethod
    def retrieve_by_event_type(self, event_type: str, aggregate_id: uuid.UUID = None, start_date: datetime = None, end_date: datetime = None) -> List[MarketingImageGeneratedEvent | MarketingImageModifiedEvent | MarketingImageAcceptedEvent | MarketingImageRejectedEvent | MarketingImageRemovedEvent | MarketingImageMetadataChangedEvent]:
        """
        Retrieves all marketing image domain events of a specific type.

        Args:
            event_type: The type of marketing image domain events to retrieve.
            (Optional) aggregate_id: The ID of the aggregate to retrieve events for.
            (Optional) start_date: The start date to filter events by.
            (Optional) end_date: The end date to filter events by.

        Returns:
            A list of MarketingImage domain events.
        """
        raise NotImplementedError

    @abstractmethod
    def retrieve_all(self) -> List[MarketingImageGeneratedEvent | MarketingImageModifiedEvent | MarketingImageAcceptedEvent | MarketingImageRejectedEvent | MarketingImageRemovedEvent | MarketingImageMetadataChangedEvent]:
        """
        Retrieves all marketing image domain events.

        Returns:
            A list of MarketingImage domain events.
        """
        raise NotImplementedError