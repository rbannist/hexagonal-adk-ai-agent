import os
import uuid
from datetime import datetime
from typing import Optional, List

from google.cloud import firestore

from ....shared.utils import DataManipulationUtils

from ....application.ports.marketing_image_repository_output_port import MarketingImageRepositoryOutputPort
from ....domain.entities.marketing_image_aggregate import MarketingImage
from ....domain.factories.marketing_image_aggregate_factory import MarketingImageAggregateFactory
from ....domain.factories.marketing_image_domain_events_factory import MarketingImageDomainEventsFactory


data_manipulation_utils = DataManipulationUtils()


class MarketingImageAggregateFirestoreRepository(MarketingImageRepositoryOutputPort):
    """
    Firestore implementation of the MarketingImageRepositoryOutputPort.
    This repository relies on a factory to convert between domain aggregates
    and dictionary representations for persistence.
    """

    def __init__(self, google_cloud_project: str = None, db_location: str = None, db_name: str = None, aggregate_collection_name: str = None, domain_event_collection_name: str = None):
        if not google_cloud_project:
            self.google_cloud_project = os.getenv("GOOGLE_CLOUD_REPOSITORY_ADAPTER_PROJECT", "rbal-assisted-prj1")
        else:
            self.google_cloud_project = google_cloud_project
        
        if not db_location:
            self.db_location = os.getenv("GOOGLE_CLOUD_REPOSITORY_ADAPTER_LOCATION", "europe-west4")
        else:
            self.db_location = db_location
        
        if not db_name:
            self.db_name = os.getenv("GOOGLE_CLOUD_FIRESTORE_REPOSITORY_ADAPTER_DATABASE", "claim-check-ew4-1")
        else:
            self.db_name = db_name
        
        if not aggregate_collection_name:
            self.aggregate_collection_name = os.getenv("GOOGLE_CLOUD_FIRESTORE_REPOSITORY_ADAPTER_COLLECTION_MARKETING_IMAGES", "marketing-image-aggregates")
        else:
            self.aggregate_collection_name = aggregate_collection_name
        
        if not domain_event_collection_name:
            self.domain_event_collection_name = os.getenv("GOOGLE_CLOUD_FIRESTORE_REPOSITORY_ADAPTER_COLLECTION_MARKETING_IMAGE_EVENTS", "marketing-image-domain-events")
        else:
            self.domain_event_collection_name = domain_event_collection_name

        self.aggregate_factory = MarketingImageAggregateFactory()
        self.domain_events_factory = MarketingImageDomainEventsFactory()
        self.db = firestore.Client(project=self.google_cloud_project, database=self.db_name)

    def _convert_keys_snake_to_camel_case(self, data: dict) -> dict:
        return DataManipulationUtils.convert_keys_snake_to_camel_case(data)

    def _convert_keys_camel_to_snake_case(self, data: dict) -> dict:
        return {DataManipulationUtils.camel_to_snake_case(k): v for k, v in data.items()}

    def _pre_persist_processing(self, data: dict) -> dict:
        """
        Processes the data to convert datetime objects to ISO format strings
        and handles timestamp strings by parsing them into datetime objects.
        """
        processed_data = data.copy()
        for k, v in processed_data.items():
            if isinstance(v, datetime):
                processed_data[k] = v.isoformat()  # Convert datetime to ISO format string
            elif isinstance(v, str):
                try:
                    processed_data[k] = datetime.fromisoformat(v)  # Attempt to parse timestamp strings
                except ValueError:
                    pass  # If parsing fails, assume it's not a timestamp and leave it as is
        return processed_data

    def save(self, marketing_image: MarketingImage) -> None:
        """
        Saves a marketing image aggregate and its domain events to Firestore.
        This method uses a batch write to ensure atomicity and handles both
        the creation of new aggregates and the update of existing ones.
        """
        aggregate_doc_id = str(marketing_image.id)
        aggregate_type = marketing_image.__class__.__name__
        aggregate_data = self.aggregate_factory.to_dict(marketing_image)
        domain_events = aggregate_data.pop("events_list", [])

        # Check if a 'removed' event is present
        removed_event = None
        for event in domain_events:
            if "removed" in event.get("type", "").lower():
                removed_event = event
                break

        batch = self.db.batch()

        if removed_event:
            # If a 'removed' event exists, delete the aggregate and save only that event.
            print(f"Processing removal for marketing image aggregate with ID {aggregate_doc_id}")
            aggregate_ref = self.db.collection(self.aggregate_collection_name).document(aggregate_doc_id)
            batch.delete(aggregate_ref)

            event_doc_id = str(removed_event["id"])
            print(f"Saving {removed_event['type']} event with ID {event_doc_id}")
            event_ref = self.db.collection(self.domain_event_collection_name).document(event_doc_id)
            event_data = self._convert_keys_snake_to_camel_case(removed_event)
            processed_event_data = self._pre_persist_processing(event_data)
            batch.set(event_ref, processed_event_data)
            
            batch.commit()
            marketing_image.clear_domain_events()
            print(f"Removed {aggregate_type} {aggregate_doc_id} and saved its domain event (ID: {event_doc_id})")

        else:
            # Save/Update the aggregate and its events
            print(f"Saving marketing image aggregate with ID {aggregate_doc_id}")
            aggregate_ref = self.db.collection(self.aggregate_collection_name).document(aggregate_doc_id)
            
            if "events_list" in aggregate_data:
                del aggregate_data["events_list"]
            
            aggregate_data_camel_case = self._convert_keys_snake_to_camel_case(aggregate_data)
            processed_aggregate_data = self._pre_persist_processing(aggregate_data_camel_case)
            batch.set(aggregate_ref, processed_aggregate_data)

            event_id_list = []
            for event in domain_events:
                domain_event_type = event["type"]
                event_doc_id = str(event["id"])
                print(f"Saving {domain_event_type} event with ID {event_doc_id}")
                event_id_list.append(event_doc_id)
                event_ref = self.db.collection(self.domain_event_collection_name).document(event_doc_id)
                event_data = self._convert_keys_snake_to_camel_case(event)
                processed_event_data = self._pre_persist_processing(event_data)
                batch.set(event_ref, processed_event_data)

            batch.commit()
            marketing_image.clear_domain_events()
            print(f"Saved {aggregate_type} {aggregate_doc_id} and its {len(event_id_list)} domain events (IDs: {', '.join(event_id_list)})")

        return marketing_image


    def retrieve_by_id(self, id: uuid.UUID) -> Optional[MarketingImage]:
        """
        Retrieves a marketing image aggregate from Firestore by its ID.
        """
        doc_ref = self.db.collection(self.aggregate_collection_name).document(str(id))
        doc = doc_ref.get()
        if doc.exists:
            # Use the factory to reconstitute the aggregate from the Firestore document
            data = self._convert_keys_camel_to_snake_case(doc.to_dict())

            return self.aggregate_factory.from_dict(data)  # type: ignore
        return None

    def retrieve_all(self) -> List[MarketingImage]:
        """
        Retrieves all marketing image aggregates from Firestore.
        """
        docs = self.db.collection(self.aggregate_collection_name).stream()
        # Convert the Firestore document to a dictionary and then to snake_case
        marketing_images = []
        for doc in docs:
            data = self._convert_keys_camel_to_snake_case(doc.to_dict())
            marketing_images.append(self.aggregate_factory.from_dict(data)) # type: ignore
        return marketing_images

    def remove(self, image_id: uuid.UUID) -> None:
        """
        Performs a hard delete of a marketing image aggregate from Firestore.
        """
        doc_ref = self.db.collection(self.aggregate_collection_name).document(str(image_id))
        doc_ref.delete()