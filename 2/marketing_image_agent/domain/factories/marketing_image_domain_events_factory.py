from typing import Dict

from .base_domain_event_factory import DomainEventFactory
from ..events.base_domain_event import DomainEvent
from ..events.marketing_image_generated_event import MarketingImageGeneratedEvent
from ..events.marketing_image_modified_event import MarketingImageModifiedEvent
from ..events.marketing_image_approved_event import MarketingImageApprovedEvent
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
                "checksum": event.data["checksum"],
                "created_by": event.data["created_by"],
                "created_at": event.data["created_at"],
                "last_modified_at": event.data["last_modified_at"],
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
                "checksum": event.data["checksum"],
                "modified_by": event.data["modified_by"],
                "modified_at": event.data["modified_at"],
            },
            "source": event.source,
            "version": event.version,
            "occurred_at": event.occurred_at.isoformat() + "Z",
        }

    def to_marketing_image_approved_event_dict(self, event: MarketingImageApprovedEvent) -> Dict:
        """Serialises a MarketingImageApprovedEvent object into a dictionary."""
        return {
            "id": event.id,
            "type": event.type,
            "data": {
                "id": event.data["id"],
                "url": event.data["url"],
                "approved_by": event.data["approved_by"],
                "approved_at": event.data["approved_at"],
                "checksum": event.data["checksum"],
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
                "rejected_by": event.data["rejected_by"],
                "rejected_at": event.data["rejected_at"],
                "checksum": event.data["checksum"],
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
                "removed_by": event.data["removed_by"],
                "removed_at": event.data["removed_at"],
                "size": event.data["size"],
                "checksum": event.data["checksum"],
            },
            "source": event.source,
            "version": event.version,
            "occurred_at": event.occurred_at.isoformat() + "Z",
        }

    def to_marketing_image_metadata_changed_event_dict(self, event: MarketingImageMetadataChangedEvent) -> Dict:
        """Serialises a MarketingImageMetadataChangedEvent object into a dictionary."""
        result = {
            "id": event.id,
            "type": event.type,
            "data": {
                "id": event.data["id"],
                "changed_by": event.data["changed_by"],
                "changed_at": event.data["changed_at"],
            },
            "source": event.source,
            "version": event.version,
            "occurred_at": event.occurred_at.isoformat() + "Z",
        }
        if event.data.get("url") is not None:
            result["data"]["url"] = event.data["url"]
        if event.data.get("description") is not None:
            result["data"]["description"] = event.data["description"]
        if event.data.get("dimensions") is not None:
            result["data"]["dimensions"] = event.data["dimensions"]
        if event.data.get("size") is not None:
            result["data"]["size"] = event.data["size"]
        if event.data.get("keywords") is not None:
            result["data"]["keywords"] = event.data["keywords"]
        return result
    def to_dict(self, event: DomainEvent) -> Dict:
        """
        Serialises a DomainEvent object into a dictionary.
        """
        if isinstance(event, MarketingImageGeneratedEvent):
            return self.to_marketing_image_generated_event_dict(event)
        elif isinstance(event, MarketingImageModifiedEvent):
            return self.to_marketing_image_modified_event_dict(event)
        elif isinstance(event, MarketingImageApprovedEvent):
            return self.to_marketing_image_approved_event_dict(event)
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
        elif event_type == DomainEvent.get_event_type("approved"):
            return self.reconstitute_marketing_image_approved_event(event_data, event_id) if isinstance(event_data, dict) else None
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

    def reconstitute_marketing_image_modified_event(self, data: Dict, event_id: str = None):
        """Reconstitutes a MarketingImageModifiedEvent from a dictionary."""
        return MarketingImageModifiedEvent(
            event_id=event_id,
            id=data["id"],
            url=data["url"],
            description=data["description"],
            keywords=data["keywords"],
            generation_model=data["generation_model"],
            generation_parameters=data["generation_parameters"],
            dimensions=data.get("dimensions"),
            size=data.get("size"),
            mime_type=data.get("mime_type"),
            checksum=data["checksum"],
            modified_by=data["modified_by"],
            modified_at=data["modified_at"],
        )

    def reconstitute_marketing_image_approved_event(self, data: Dict, event_id: str = None):
        """Reconstitutes a MarketingImageApprovedEvent from a dictionary."""
        return MarketingImageApprovedEvent(
            event_id=event_id,
            id=data["id"],
            url=data["url"],
            checksum=data["checksum"],
            approved_by=data["approved_by"],
            approved_at=data["approved_at"],
        )

    def reconstitute_marketing_image_rejected_event(self, data: Dict, event_id: str = None):
        """Reconstitutes a MarketingImageRejectedEvent from a dictionary."""
        return MarketingImageRejectedEvent(
            event_id=event_id,
            id=data["id"],
            url=data["url"],
            checksum=data["checksum"],
            rejected_by=data["rejected_by"],
            rejected_at=data["rejected_at"],
        )

    def reconstitute_marketing_image_removed_event(self, data: Dict, event_id: str = None):
        """Reconstitutes a MarketingImageRemovedEvent from a dictionary."""
        return MarketingImageRemovedEvent(
            event_id=event_id,
            id=data["id"],
            url=data["url"],
            removed_by=data["removed_by"],
            removed_at=data["removed_at"],
            size=data["size"],
            checksum=data["checksum"],
        )

    def reconstitute_marketing_image_metadata_changed_event(self, data: Dict, event_id: str = None):
        """Reconstitutes a MarketingImageMetadataChangedEvent from a dictionary."""
        return MarketingImageMetadataChangedEvent(
            event_id=event_id,
            id=data["id"],
            url=data.get("url"),
            description=data.get("description"),
            keywords=data.get("keywords"),
            dimensions=data.get("dimensions"),
            size=data.get("size"),
            changed_by=data["changed_by"],
            changed_at=data["changed_at"],
        )