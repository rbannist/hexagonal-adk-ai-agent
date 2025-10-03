import uuid
from typing import Dict, Any

from .base_aggregate_factory import AggregateFactory
from .marketing_image_domain_events_factory import MarketingImageDomainEventsFactory

from ..entities.marketing_image_aggregate import MarketingImage
from ..value_objects.image_id import ImageId
from ..value_objects.image_url import ImageUrl
from ..value_objects.image_description import ImageDescription
from ..value_objects.image_keywords import ImageKeywords
from ..value_objects.image_generation_model import ImageGenerationModel
from ..value_objects.image_generation_parameters import ImageGenerationParameters
from ..value_objects.image_dimensions import ImageDimensions
from ..value_objects.image_size import ImageSize
from ..value_objects.status import Status
from ..value_objects.user_id import CreatedBy
from ..value_objects.mime_type import MimeType
from ..value_objects.checksum import Checksum
from ..value_objects.timestamp import CreatedAt, LastModifiedAt


class MarketingImageAggregateFactory(AggregateFactory):
    """
    Factory for creating and reconstituting MarketingImage aggregate objects.
    It handles the transformation between dictionary representations and domain objects.
    """

    def from_dict(self, data: Dict[str, Any]) -> MarketingImage:
        """
        Reconstitutes a MarketingImage aggregate from a dictionary.
        """
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary.")

        # Create Value Objects from the dictionary data
        image_id = ImageId.from_dict(data={"id": data["id"]}) if data.get("id") else ImageId(uuid.uuid4())
        url = ImageUrl.from_dict(data={"url": data["url"]}) if data.get("url") else None
        description = ImageDescription.from_dict(data={"description": data["description"]}) if data.get("description") else None
        keywords = ImageKeywords.from_dict(data={"keywords": data["keywords"]}) if data.get("keywords") else None
        generation_model = ImageGenerationModel.from_dict(data={"model": data["generation_model"]}) if data.get("generation_model") else None
        generation_parameters = ImageGenerationParameters.from_dict(data={"parameters": data["generation_parameters"]}) if data.get("generation_parameters") else None
        dimensions = ImageDimensions.from_dict(data=data["dimensions"]) if data.get("dimensions") else None
        status = Status.from_dict(data={"status": data["status"]}) if data.get("status") else None
        size = ImageSize.from_dict(data={"size": data["size"]}) if data.get("size") else None
        mime_type = MimeType.from_dict(data={"mime_type": data["mime_type"]}) if data.get("mime_type") else None
        checksum = Checksum.from_dict(data={"checksum": data["checksum"]}) if data.get("checksum") else None
        created_by = CreatedBy.from_dict(data={"user_id": data["created_by"]}) if data.get("created_by") else None
        created_at = CreatedAt.from_string(timestamp=data["created_at"]) if isinstance(data.get("created_at"), str) else CreatedAt.now()
        last_modified_at = LastModifiedAt.from_string(timestamp=data["last_modified_at"]) if isinstance(data.get("last_modified_at"), str) else None
        
        # Create domain events list from the dictionary data
        events_list = []
        for event_data in data.get("events_list", []):
            event = MarketingImageDomainEventsFactory().reconstitute(data=event_data)
            if event:
                # print(f"Adding {event.__class__.__name__} with {event.id} to Aggregate {event.data["id"]} domain events list")
                events_list.append(event)
                print(f"Added {event.__class__.__name__} with {event.id} to Aggregate {event.data["id"]} domain events list")
                # print(f"Domain events list length: {events_list.__len__()}")


        # Instantiate the aggregate with the value objects and domain events list
        marketing_image = MarketingImage(
            id=image_id,
            url=url,
            description=description,
            keywords=keywords,
            generation_model=generation_model,
            generation_parameters=generation_parameters,
            dimensions=dimensions,
            status=status,
            size=size,
            mime_type=mime_type,
            checksum=checksum,
            created_by=created_by,
            created_at=created_at,
            last_modified_at=last_modified_at,
            events_list=events_list
        )

        return marketing_image

    def to_dict(self, marketing_image: MarketingImage) -> Dict[str, Any]:
        """
        Serialises a MarketingImage aggregate into a dictionary (with its events list included).
        """
        return {
            "id": str(marketing_image.id.id) if marketing_image.id else None,
            "url": marketing_image.url.url if marketing_image.url else None,
            "description": marketing_image.description.description if marketing_image.description else None,
            "keywords": marketing_image.keywords.keywords if marketing_image.keywords else None,
            "generation_model": marketing_image.generation_model.model if marketing_image.generation_model else None,
            "generation_parameters": marketing_image.generation_parameters.parameters if marketing_image.generation_parameters else None,
            "dimensions": marketing_image.dimensions.to_dict() if marketing_image.dimensions else None,
            "status": marketing_image.status.status.value if marketing_image.status else None,
            "size": marketing_image.size.size if marketing_image.size else None,
            "mime_type": marketing_image.mime_type.mime_type if marketing_image.mime_type else None,
            "checksum": marketing_image.checksum.checksum if marketing_image.checksum else None,
            "created_by": str(marketing_image.created_by.user_id) if marketing_image.created_by else None,
            "created_at": marketing_image.created_at.to_string() if marketing_image.created_at else None,
            "last_modified_at": marketing_image.last_modified_at.to_string() if marketing_image.last_modified_at else None,
            "events_list": [event.to_dict() for event in marketing_image.events_list] if hasattr(marketing_image, "events_list") else [],
        }

    def to_dict_without_events(self, marketing_image: MarketingImage) -> Dict[str, Any]:
        """
        Serialises a MarketingImage aggregate into a dictionary (without its events list included).
        """
        image_dict = self.to_dict(marketing_image)
        image_dict.pop("events_list", None)  # Remove events_list if it exists
        return image_dict
    
    def create(self, data: Dict[str, Any]) -> Dict:
        """
        Creates a MarketingImage aggregate from a dictionary of data and then returns a dictionary representation.
        """
        marketing_image = self.from_dict(data)
        marketing_image_return_dict = self.to_dict(marketing_image)
        return marketing_image_return_dict
    
    def generate(self, data: Dict[str, Any]) -> Dict:
        """
        Creates a MarketingImage aggregate from a dictionary of data and then
        calls the object's generate method before
        returning a dictionary representation.
        """
        marketing_image = self.from_dict(data)
        marketing_image.generate()
        marketing_image_return_dict = self.to_dict(marketing_image)
        return marketing_image_return_dict

    def accept(self, data: Dict[str, Any]) -> Dict:
        """
        Reconstitutes a MarketingImage aggregate from a dictionary of data and then
        calls the object's accept method before
        returning a dictionary representation.
        """
        marketing_image = self.from_dict(data)
        marketing_image.accept()
        marketing_image_return_dict = self.to_dict(marketing_image)
        return marketing_image_return_dict

    def reject(self, data: Dict[str, Any]) -> Dict:
        """
        Reconstitutes a MarketingImage aggregate from a dictionary of data and then
        calls the object's accept reject before
        returning a dictionary representation.
        """
        marketing_image = self.from_dict(data)
        marketing_image.reject()
        marketing_image_return_dict = self.to_dict(marketing_image)
        return marketing_image_return_dict

    def modify(self, data: Dict[str, Any]) -> Dict:
        """
        Reconstitutes a MarketingImage aggregate from a dictionary of data and then
        calls the object's modify method before
        returning a dictionary representation.
        """
        marketing_image = self.from_dict(data)
        marketing_image.modify()
        marketing_image_return_dict = self.to_dict(marketing_image)
        return marketing_image_return_dict

    def remove(self, data: Dict[str, Any]) -> Dict:
        """
        Reconstitutes a MarketingImage aggregate from a dictionary of data and then
        calls the object's remove method before
        returning a dictionary representation.
        """
        marketing_image = self.from_dict(data)
        marketing_image.remove()
        marketing_image_return_dict = self.to_dict(marketing_image)
        return marketing_image_return_dict
    
    def change_metadata(self, data: Dict[str, Any], description: str, keywords: dict) -> Dict:
        """
        Reconstitutes a MarketingImage aggregate from a dictionary of data and then
        calls the object's change_metadata method before
        returning a dictionary representation.
        """
        marketing_image = self.from_dict(data)
        description = ImageDescription.from_dict(data={"description": description}) if description is not None else None
        keywords = ImageKeywords.from_dict(data={"keywords": keywords}) if keywords is not None else None
        dimensions = ImageDimensions.from_dict(data=data["dimensions"]) if data.get("dimensions") is not None else None
        size = ImageSize.from_dict(data={"size": data["size"]}) if data.get("size") is not None else None
        url = ImageUrl.from_dict(data={"url": data["url"]}) if data.get("url") else None
        marketing_image.change_metadata(description=description, keywords=keywords, dimensions=dimensions, size=size, url=url)
        marketing_image_return_dict = self.to_dict(marketing_image)
        return marketing_image_return_dict