from typing import Dict, Any
from datetime import datetime
from urllib.parse import urlparse

from .base_integration_event_factory import IntegrationEventFactory
from ..outbound_integration_events.base_outbound_integration_event import IntegrationEvent
from ..outbound_integration_events.marketing_image_generated_thin_integration_event import MarketingImageGeneratedThinIntegrationEvent
from ..outbound_integration_events.marketing_image_modified_thin_integration_event import MarketingImageModifiedThinIntegrationEvent
from ..outbound_integration_events.marketing_image_approved_thin_integration_event import MarketingImageApprovedThinIntegrationEvent
from ..outbound_integration_events.marketing_image_rejected_thin_integration_event import MarketingImageRejectedThinIntegrationEvent
from ..outbound_integration_events.marketing_image_removed_thin_integration_event import MarketingImageRemovedThinIntegrationEvent
from ..outbound_integration_events.marketing_image_metadata_changed_thin_integration_event import MarketingImageMetadataChangedThinIntegrationEvent
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

    def __init__(self, storage_provider: str, gcs_project_id: str, gcs_bucket_location: str, gcs_bucket_name: str):
        self.storage_provider = storage_provider
        self.gcs_project_id = gcs_project_id
        self.gcs_bucket_location = gcs_bucket_location
        self.gcs_bucket_name = gcs_bucket_name

    def _create_claim_check_token(self, url: str, checksum: str) -> str:
        """Creates a claim check token from the image URL and checksum."""
        parsed_url = urlparse(url)
        # Assumes path is /<bucket>/<filename>
        filename = parsed_url.path.split('/', 2)[-1]
        return f"{self.storage_provider}:{self.gcs_project_id}:{self.gcs_bucket_location}:{self.gcs_bucket_name}:{filename}:{checksum}"


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

        claim_check_token = self._create_claim_check_token(event_data["url"], event_data["checksum"])
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
            claim_check_token=claim_check_token,
        )

        return marketing_image_generated_thin_integration_event

    def create_marketing_image_modified_thin_integration_event(self, marketing_image_modified_domain_event: MarketingImageModifiedEvent) -> MarketingImageModifiedThinIntegrationEvent:
        event_data = marketing_image_modified_domain_event.data

        claim_check_token = self._create_claim_check_token(event_data["url"], event_data["checksum"])
        marketing_image_modified_thin_integration_event = MarketingImageModifiedThinIntegrationEvent(
            id=event_data["id"],
            modified_at=event_data["modified_at"],
            modified_by=event_data["modified_by"],
            url=event_data["url"],
            description=event_data["description"],
            dimensions=event_data["dimensions"],
            size=event_data["size"],
            mime_type=event_data["mime_type"],
            checksum=event_data["checksum"],
            claim_check_token=claim_check_token,
        )

        return marketing_image_modified_thin_integration_event

    def create_marketing_image_approved_thin_integration_event(self, marketing_image_approved_domain_event: MarketingImageApprovedEvent) -> MarketingImageApprovedThinIntegrationEvent:
        event_data = marketing_image_approved_domain_event.data

        claim_check_token = self._create_claim_check_token(event_data["url"], event_data["checksum"])
        marketing_image_approved_thin_integration_event = MarketingImageApprovedThinIntegrationEvent(
            id=event_data["id"],
            approved_by=event_data["approved_by"],
            approved_at=event_data["approved_at"],
            claim_check_token=claim_check_token,
        )

        return marketing_image_approved_thin_integration_event

    def create_marketing_image_rejected_thin_integration_event(self, marketing_image_rejected_domain_event: MarketingImageRejectedEvent) -> MarketingImageRejectedThinIntegrationEvent:
        event_data = marketing_image_rejected_domain_event.data

        claim_check_token = self._create_claim_check_token(event_data["url"], event_data["checksum"])
        marketing_image_rejected_thin_integration_event = MarketingImageRejectedThinIntegrationEvent(
            id=event_data["id"],
            rejected_by=event_data["rejected_by"],
            rejected_at=event_data["rejected_at"],
            claim_check_token=claim_check_token,
        )

        return marketing_image_rejected_thin_integration_event
    
    def create_marketing_image_removed_thin_integration_event(self, marketing_image_removed_domain_event: MarketingImageRemovedEvent) -> MarketingImageRemovedThinIntegrationEvent:
        event_data = marketing_image_removed_domain_event.data

        claim_check_token = self._create_claim_check_token(event_data["url"], event_data["checksum"])
        marketing_image_removed_thin_integration_event = MarketingImageRemovedThinIntegrationEvent(
            id=event_data["id"],
            removed_by=event_data["removed_by"],
            removed_at=event_data["removed_at"],
            claim_check_token=claim_check_token,
        )

        return marketing_image_removed_thin_integration_event

    def create_marketing_image_metadata_changed_thin_integration_event(self, marketing_image_metadata_changed_domain_event: MarketingImageMetadataChangedEvent) -> MarketingImageMetadataChangedThinIntegrationEvent:
        event_data = marketing_image_metadata_changed_domain_event.data
        claim_check_token = self._create_claim_check_token(event_data["url"], event_data["checksum"])

        changed_metadata = {
            "description": event_data.get("description"),
            "keywords": event_data.get("keywords"),
            "dimensions": event_data.get("dimensions"),
            "size": event_data.get("size"),
            "url": event_data.get("url"),
        }

        marketing_image_metadata_changed_thin_integration_event = MarketingImageMetadataChangedThinIntegrationEvent(
            id=event_data["id"],
            changed_at=event_data["changed_at"],
            changed_by=event_data["changed_by"],
            claim_check_token=claim_check_token,
            **changed_metadata,
        )

        return marketing_image_metadata_changed_thin_integration_event



    def create_from_domain_event(self, domain_event: DomainEvent):
        """Method to create an integration event from a domain event."""
        if isinstance(domain_event, MarketingImageGeneratedEvent):
            return self.create_marketing_image_generated_thin_integration_event(domain_event)
        elif isinstance(domain_event, MarketingImageModifiedEvent):
            return self.create_marketing_image_modified_thin_integration_event(domain_event)
        elif isinstance(domain_event, MarketingImageApprovedEvent):
            return self.create_marketing_image_approved_thin_integration_event(domain_event)
        elif isinstance(domain_event, MarketingImageRejectedEvent):
            return self.create_marketing_image_rejected_thin_integration_event(domain_event)
        elif isinstance(domain_event, MarketingImageRemovedEvent):
            return self.create_marketing_image_removed_thin_integration_event(domain_event)
        elif isinstance(domain_event, MarketingImageMetadataChangedEvent):
            return self.create_marketing_image_metadata_changed_thin_integration_event(domain_event)
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

    def marketing_image_modified_thin_integration_event_to_dict(self, marketing_image_modified_thin_integration_event: MarketingImageModifiedThinIntegrationEvent) -> dict:
        """Method to serialise a MarketingImageModifiedThinIntegrationEvent to a dictionary."""
        return {
            "id": marketing_image_modified_thin_integration_event.id,
            "type": marketing_image_modified_thin_integration_event.type,
            "data": self._to_dict_recursive(marketing_image_modified_thin_integration_event.data),
            "source": marketing_image_modified_thin_integration_event.source,
            "version": marketing_image_modified_thin_integration_event.version,
            "occurred_at": marketing_image_modified_thin_integration_event.occurred_at.isoformat() + "Z",
            "metadata": self._to_dict_recursive(marketing_image_modified_thin_integration_event.metadata),
        }

    def marketing_image_approved_thin_integration_event_to_dict(self, marketing_image_approved_thin_integration_event: MarketingImageApprovedThinIntegrationEvent) -> dict:
        """Method to serialise a MarketingImageApprovedThinIntegrationEvent to a dictionary."""
        return {
            "id": marketing_image_approved_thin_integration_event.id,
            "type": marketing_image_approved_thin_integration_event.type,
            "data": self._to_dict_recursive(marketing_image_approved_thin_integration_event.data),
            "source": marketing_image_approved_thin_integration_event.source,
            "version": marketing_image_approved_thin_integration_event.version,
            "occurred_at": marketing_image_approved_thin_integration_event.occurred_at.isoformat() + "Z",
            "metadata": self._to_dict_recursive(marketing_image_approved_thin_integration_event.metadata),
        }
    
    def marketing_image_rejected_thin_integration_event_to_dict(self, marketing_image_rejected_thin_integration_event: MarketingImageRejectedThinIntegrationEvent) -> dict:
        """Method to serialise a MarketingImageRejectedThinIntegrationEvent to a dictionary."""
        return {
            "id": marketing_image_rejected_thin_integration_event.id,
            "type": marketing_image_rejected_thin_integration_event.type,
            "data": self._to_dict_recursive(marketing_image_rejected_thin_integration_event.data),
            "source": marketing_image_rejected_thin_integration_event.source,
            "version": marketing_image_rejected_thin_integration_event.version,
            "occurred_at": marketing_image_rejected_thin_integration_event.occurred_at.isoformat() + "Z",
            "metadata": self._to_dict_recursive(marketing_image_rejected_thin_integration_event.metadata),
        }
    
    def marketing_image_removed_thin_integration_event_to_dict(self, marketing_image_removed_thin_integration_event: MarketingImageRemovedThinIntegrationEvent) -> dict:
        """Method to serialise a MarketingImageRemovedThinIntegrationEvent to a dictionary."""
        return {
            "id": marketing_image_removed_thin_integration_event.id,
            "type": marketing_image_removed_thin_integration_event.type,
            "data": self._to_dict_recursive(marketing_image_removed_thin_integration_event.data),
            "source": marketing_image_removed_thin_integration_event.source,
            "version": marketing_image_removed_thin_integration_event.version,
            "occurred_at": marketing_image_removed_thin_integration_event.occurred_at.isoformat() + "Z",
            "metadata": self._to_dict_recursive(marketing_image_removed_thin_integration_event.metadata),
        }

    def marketing_image_metadata_changed_thin_integration_event_to_dict(self, marketing_image_metadata_changed_thin_integration_event: MarketingImageMetadataChangedThinIntegrationEvent) -> dict:
        """Method to serialise a MarketingImageMetadataChangedThinIntegrationEvent to a dictionary."""
        return {
            "id": marketing_image_metadata_changed_thin_integration_event.id,
            "type": marketing_image_metadata_changed_thin_integration_event.type,
            "data": self._to_dict_recursive(marketing_image_metadata_changed_thin_integration_event.data),
            "source": marketing_image_metadata_changed_thin_integration_event.source,
            "version": marketing_image_metadata_changed_thin_integration_event.version,
            "occurred_at": marketing_image_metadata_changed_thin_integration_event.occurred_at.isoformat() + "Z",
            "metadata": self._to_dict_recursive(marketing_image_metadata_changed_thin_integration_event.metadata),
        }


    def to_dict(self, integration_event: IntegrationEvent):
        """Method to serialise an integration event to a dictionary."""
        if isinstance(integration_event, MarketingImageGeneratedThinIntegrationEvent):
            return self.marketing_image_generated_thin_integration_event_to_dict(integration_event)
        elif isinstance(integration_event, MarketingImageModifiedThinIntegrationEvent):
            return self.marketing_image_modified_thin_integration_event_to_dict(integration_event)
        elif isinstance(integration_event, MarketingImageApprovedThinIntegrationEvent):
            return self.marketing_image_approved_thin_integration_event_to_dict(integration_event)
        elif isinstance(integration_event, MarketingImageRejectedThinIntegrationEvent):
            return self.marketing_image_rejected_thin_integration_event_to_dict(integration_event)
        elif isinstance(integration_event, MarketingImageRemovedThinIntegrationEvent):
            return self.marketing_image_removed_thin_integration_event_to_dict(integration_event)
        elif isinstance(integration_event, MarketingImageMetadataChangedThinIntegrationEvent):
            return self.marketing_image_metadata_changed_thin_integration_event_to_dict(integration_event)
        else:
            raise ValueError(f"Unknown event type for serialisation: {type(integration_event)}")