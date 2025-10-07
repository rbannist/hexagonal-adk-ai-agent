from typing import Dict, Any
from datetime import datetime

from .base_integration_event_factory import IntegrationEventFactory
from ..outbound_integration_events.base_outbound_integration_event import IntegrationEvent
from ..outbound_integration_events.marketing_image_generated_thin_integration_event import MarketingImageGeneratedThinIntegrationEvent
from ...domain.events.base_domain_event import DomainEvent
from ...domain.events.marketing_image_generated_event import MarketingImageGeneratedEvent
from ...domain.events.marketing_image_modified_event import MarketingImageModifiedEvent
from ...domain.events.marketing_image_approved_event import MarketingImageApprovedEvent
from ...domain.events.marketing_image_rejected_event import MarketingImageRejectedEvent
from ...domain.events.marketing_image_removed_event import MarketingImageRemovedEvent
from ...domain.events.marketing_image_metadata_changed_event import MarketingImageMetadataChangedEvent


class MarketingImageIntegrationEventsFactory(IntegrationEventFactory):
    """
    Factory for creating and/or reconstituting Integration Events.
    """

    def _to_dict_recursive(self, data: Any) -> Any:
        """
        Recursively converts objects to dictionaries if they have a `to_dict` method.
        Also handles datetimes, lists, and dictionaries.
        """
        if hasattr(data, "to_dict") and callable(data.to_dict):
            return data.to_dict()
        if isinstance(data, datetime):
            return data.isoformat() + "Z"
        if isinstance(data, list):
            return [self._to_dict_recursive(item) for item in data]
        if isinstance(data, dict):
            return {key: self._to_dict_recursive(value) for key, value in data.items()}
        return data
    
    def create_marketing_image_generated_thin_integration_event(self, marketing_image_generated_domain_event: MarketingImageGeneratedEvent) -> MarketingImageGeneratedThinIntegrationEvent:
        event_data = marketing_image_generated_domain_event.data

        marketing_image_generated_thin_integration_event = MarketingImageGeneratedThinIntegrationEvent(
            id=event_data["id"],
            url=event_data["url"],
            description=event_data["description"],
            dimensions=event_data["dimensions"],
            size=event_data["size"],
            mime_type=event_data["mime_type"],
            checksum=event_data["checksum"],
            created_by=event_data["created_by"],
            created_at=event_data["created_at"],
        )

        return marketing_image_generated_thin_integration_event
    
    def create_from_domain_event(self, domain_event: DomainEvent):
        """Method to create an integration event from a domain event."""
        if isinstance(domain_event, MarketingImageGeneratedEvent):
            return self.create_marketing_image_generated_thin_integration_event(domain_event)
        # elif isinstance(domain_event, MarketingImageModifiedEvent):
        #     return self.to_marketing_image_modified_event_dict(domain_event)
        # elif isinstance(domain_event, MarketingImageApprovedEvent):
        #     return self.to_marketing_image_approved_event_dict(domain_event)
        # elif isinstance(domain_event, MarketingImageRejectedEvent):
        #     return self.to_marketing_image_rejected_event_dict(domain_event)
        # elif isinstance(domain_event, MarketingImageRemovedEvent):
        #     return self.to_marketing_image_removed_event_dict(domain_event)
        # elif isinstance(domain_event, MarketingImageMetadataChangedEvent):
        #     return self.to_marketing_image_metadata_changed_event_dict(domain_event)
        else:
            raise ValueError(f"Unknown event type for serialisation: {type(domain_event)}")

    def reconstitute(self, integration_event_dict: Dict):
        """Method to reconstitute an integration event from a dictionary."""
        pass

    def marketing_image_generated_thin_integration_event_to_dict(self, marketing_image_generated_thin_integration_event: MarketingImageGeneratedThinIntegrationEvent) -> dict:
        """Method to serialise a MarketingImageGeneratedThinIntegrationEvent to a dictionary."""
        return {
            "id": marketing_image_generated_thin_integration_event.id,
            "type": marketing_image_generated_thin_integration_event.type,
            "data": self._to_dict_recursive(marketing_image_generated_thin_integration_event.data),
            "source": marketing_image_generated_thin_integration_event.source,
            "version": marketing_image_generated_thin_integration_event.version,
            "occurred_at": marketing_image_generated_thin_integration_event.occurred_at.isoformat() + "Z",
            "metadata": self._to_dict_recursive(marketing_image_generated_thin_integration_event.metadata),
        }

    def to_dict(self, integration_event: IntegrationEvent):
        """Method to serialise an integration event to a dictionary."""
        if isinstance(integration_event, MarketingImageGeneratedThinIntegrationEvent):
            return self.marketing_image_generated_thin_integration_event_to_dict(integration_event)
        # elif isinstance(integration_event, MarketingImageModifiedThinIntegrationEvent):
        #     return self.marketing_image_modified_thin_integration_event_to_dict(integration_event)
        # elif isinstance(integration_event, MarketingImageApprovedThinIntegrationEvent):
        #     return self.marketing_image_approved_thin_integration_event_to_dict(integration_event)
        # elif isinstance(integration_event, MarketingImageRejectedThinIntegrationEvent):
        #     return self.marketing_image_rejected_thin_integration_event_to_dict(integration_event)
        # elif isinstance(integration_event, MarketingImageRemovedThinIntegrationEvent):
        #     return self.marketing_image_removed_thin_integration_event_to_dict(integration_event)
        # elif isinstance(integration_event, MarketingImageMetadataChangedThinIntegrationEvent):
        #     return self.marketing_image_metadata_changed_thin_integration_event_to_dict(integration_event)
        else:
            raise ValueError(f"Unknown event type for serialisation: {type(integration_event)}")