from typing import Dict

from .base_domain_event_factory import DomainEventFactory
from ..events.base_domain_event import DomainEvent
from ..events.marketing_image_generated_event import MarketingImageGeneratedEvent
from ..events.marketing_image_modified_event import MarketingImageModifiedEvent
from ..events.marketing_image_accepted_event import MarketingImageAcceptedEvent
from ..events.marketing_image_rejected_event import MarketingImageRejectedEvent
from ..events.marketing_image_removed_event import MarketingImageRemovedEvent
from ..events.marketing_image_metadata_changed_event import MarketingImageMetadataChangedEvent


class MarketingImageDomainEventsFactory(DomainEventFactory):
    """
    Factory for mapping and reconstituting MarketingImage domain event objects.
    """

    def to_marketing_image_generated_event_dict(self, event: MarketingImageGeneratedEvent) -> Dict:
        """Serialises a MarketingImageGeneratedEvent object into a dictionary."""
        return {
            "id": event.id,
            "type": event.type,
            "data": {
                "id": event.data["id"],
                "url": event.data["url"],
                "description": event.data["description"],
                "keywords": event.data["keywords"],
                "generation_model": event.data["generation_model"],
                "generation_parameters": event.data["generation_parameters"],
                "dimensions": event.data["dimensions"],
                "size": event.data["size"],
                "mime_type": event.data["mime_type"],
            },
            "source": event.source,
            "version": event.version,
            "occurred_at": event.occurred_at.isoformat() + "Z",
        }

    def to_marketing_image_modified_event_dict(self, event: MarketingImageModifiedEvent) -> Dict:
        """Serialises a MarketingImageModifiedEvent object into a dictionary."""
        return {
            "id": event.id,
            "type": event.type,
             "data": {
                "id": event.data["id"],
                "url": event.data["url"],
                "description": event.data["description"],
                "keywords": event.data["keywords"],
                "generation_model": event.data["generation_model"],
                "generation_parameters": event.data["generation_parameters"],
                "dimensions": event.data["dimensions"],
                "size": event.data["size"],
                "mime_type": event.data["mime_type"],
            },
            "source": event.source,
            "version": event.version,
            "occurred_at": event.occurred_at.isoformat() + "Z",
        }

    def to_marketing_image_accepted_event_dict(self, event: MarketingImageAcceptedEvent) -> Dict:
        """Serialises a MarketingImageAcceptedEvent object into a dictionary."""
        return {
            "id": event.id,
            "type": event.type,
            "data": {
                "id": event.data["id"],
                "url": event.data["url"],
                "checksum": event.data["checksum"],
                "created_at": event.data["created_at"],
            },
            "source": event.source,
            "version": event.version,
            "occurred_at": event.occurred_at.isoformat() + "Z",
        }

    def to_marketing_image_rejected_event_dict(self, event: MarketingImageRejectedEvent) -> Dict:
        """Serialises a MarketingImageRejectedEvent object into a dictionary."""
        return {
            "id": event.id,
            "type": event.type,
            "data": {
                "id": event.data["id"],
                "url": event.data["url"],
                "checksum": event.data["checksum"],
                "created_at": event.data["created_at"],
            },
            "source": event.source,
            "version": event.version,
            "occurred_at": event.occurred_at.isoformat() + "Z",
        }

    def to_marketing_image_removed_event_dict(self, event: MarketingImageRemovedEvent) -> Dict:
        """Serialises a MarketingImageRemovedEvent object into a dictionary."""
        return {
            "id": event.id,
            "type": event.type,
            "data": {
                "id": event.data["id"],
                "url": event.data["url"],
                "size": event.data["size"],
                "checksum": event.data["checksum"],
            },
            "source": event.source,
            "version": event.version,
            "occurred_at": event.occurred_at.isoformat() + "Z",
        }

    def to_marketing_image_metadata_changed_event_dict(self, event: MarketingImageMetadataChangedEvent) -> Dict:
        """Serialises a MarketingImageMetadataChangedEvent object into a dictionary."""
        return {
            "id": event.id,
            "type": event.type,
            "data": {
                "id": event.data["id"],
                "url": event.data["url"],
                "description": event.data["description"],
                "keywords": event.data["keywords"],
            },
            "source": event.source,
            "version": event.version,
            "occurred_at": event.occurred_at.isoformat() + "Z",
        }

    def to_dict(self, event: DomainEvent) -> Dict:
        """
        Serialises a DomainEvent object into a dictionary.
        """
        if isinstance(event, MarketingImageGeneratedEvent):
            return self.to_marketing_image_generated_event_dict(event)
        elif isinstance(event, MarketingImageModifiedEvent):
            return self.to_marketing_image_modified_event_dict(event)
        elif isinstance(event, MarketingImageAcceptedEvent):
            return self.to_marketing_image_accepted_event_dict(event)
        elif isinstance(event, MarketingImageRejectedEvent):
            return self.to_marketing_image_rejected_event_dict(event)
        elif isinstance(event, MarketingImageRemovedEvent):
            return self.to_marketing_image_removed_event_dict(event)
        elif isinstance(event, MarketingImageMetadataChangedEvent):
            return self.to_marketing_image_metadata_changed_event_dict(event)
        else:
            raise ValueError(f"Unknown event type for serialization: {type(event)}")

    def reconstitute(self, data: Dict):
        """Reconstitutes a domain event from a dictionary."""
        event_type = data["type"] # Error if not present
        event_id = data.get("id") # None if not present
        event_data = data["data"]

        if event_type == DomainEvent.get_event_type("generated"):
            return self.reconstitute_marketing_image_generated_event(event_data, event_id) if isinstance(event_data, dict) else None
        elif event_type == DomainEvent.get_event_type("modified"):
            return self.reconstitute_marketing_image_modified_event(event_data, event_id) if isinstance(event_data, dict) else None
        elif event_type == DomainEvent.get_event_type("accepted"):
            return self.reconstitute_marketing_image_accepted_event(event_data, event_id) if isinstance(event_data, dict) else None
        elif event_type == DomainEvent.get_event_type("rejected"):
            return self.reconstitute_marketing_image_rejected_event(event_data, event_id) if isinstance(event_data, dict) else None
        elif event_type == DomainEvent.get_event_type("removed"):
            return self.reconstitute_marketing_image_removed_event(event_data, event_id) if isinstance(event_data, dict) else None
        elif event_type == DomainEvent.get_event_type("metadata-changed"):
            return self.reconstitute_marketing_image_metadata_changed_event(event_data, event_id) if isinstance(event_data, dict) else None
        else:
            raise ValueError(f"Unknown event type: {event_type}")

    def reconstitute_marketing_image_generated_event(self, data: Dict, event_id: str = None):
        """Reconstitutes a MarketingImageGeneratedEvent from a dictionary."""
        # print(f"Reconstituting MarketingImageGeneratedEvent with Event ID {event_id} and Aggregate ID {data.get('id')}")
        marketing_image_generated_event = MarketingImageGeneratedEvent(
            event_id=event_id,
            id=data["id"],
            url=data["url"],
            description=data["description"],
            keywords=data["keywords"],
            generation_model=data["generation_model"],
            generation_parameters=data["generation_parameters"],
            dimensions=data["dimensions"],
            size=data["size"],
            mime_type=data["mime_type"],
            checksum=data["checksum"],
            created_by=data["created_by"],
            created_at=data["created_at"],
            last_modified_at=data["last_modified_at"],
        )
        print(f"Reconstituted MarketingImageGeneratedEvent with Event ID {marketing_image_generated_event.id} and Aggregate ID {marketing_image_generated_event.data["id"]}")
        return marketing_image_generated_event

    def reconstitute_marketing_image_modified_event(self, data: Dict):
        """Reconstitutes a MarketingImageModifiedEvent from a dictionary."""
        return MarketingImageModifiedEvent(
            id=data["id"],
            url=data["url"],
            description=data["description"],
            keywords=data["keywords"],
            generation_model=data["generation_model"],
            generation_parameters=data["generation_parameters"],
            dimensions=data["dimensions"],
            size=data["size"],
            mime_type=data["mime_type"],
            checksum=data["checksum"],
            created_by=data["created_by"],
            created_at=data["created_at"],
            last_modified_at=data["last_modified_at"],
        )

    def reconstitute_marketing_image_accepted_event(self, data: Dict):
        """Reconstitutes a MarketingImageAcceptedEvent from a dictionary."""
        return MarketingImageAcceptedEvent(
            id=data["id"],
            url=data["url"],
            checksum=data["checksum"],
            created_at=data["created_at"],
            last_modified_at=data["last_modified_at"],
        )

    def reconstitute_marketing_image_rejected_event(self, data: Dict):
        """Reconstitutes a MarketingImageRejectedEvent from a dictionary."""
        return MarketingImageRejectedEvent(
            id=data["id"],
            url=data["url"],
            checksum=data["checksum"],
            created_at=data["created_at"],
            last_modified_at=data["last_modified_at"],
        )

    def reconstitute_marketing_image_removed_event(self, data: Dict):
        """Reconstitutes a MarketingImageRemovedEvent from a dictionary."""
        return MarketingImageRemovedEvent(
            id=data["id"],
            url=data["url"],
            size=data["size"],
            checksum=data["checksum"],
            created_at=data["created_at"],
            last_modified_at=data["last_modified_at"],
        )

    def reconstitute_marketing_image_metadata_changed_event(self, data: Dict):
        """Reconstitutes a MarketingImageMetadataChangedEvent from a dictionary."""
        return MarketingImageMetadataChangedEvent(
            id=data["id"],
            url=data["url"],
            description=data["description"],
            keywords=data["keywords"],
            created_at=data["created_at"],
            last_modified_at=data["last_modified_at"],
        )