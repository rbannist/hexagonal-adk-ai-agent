import uuid
from typing import List, Optional

from .base_entity import AggregateRoot

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
from ..value_objects.timestamp import CreatedAt, LastModifiedAt
from ..value_objects.mime_type import MimeType
from ..value_objects.checksum import Checksum

from ..events.marketing_image_generated_event import MarketingImageGeneratedEvent
from ..events.marketing_image_modified_event import MarketingImageModifiedEvent
from ..events.marketing_image_approved_event import MarketingImageApprovedEvent
from ..events.marketing_image_rejected_event import MarketingImageRejectedEvent
from ..events.marketing_image_removed_event import MarketingImageRemovedEvent
from ..events.marketing_image_metadata_changed_event import MarketingImageMetadataChangedEvent


class MarketingImage(AggregateRoot):
    """
    Represents an aggregate root for an AI-generated marketing image.
    This aggregate stores metadata about the image, with the actual image data
    expected to be stored externally - e.g. in a cloud storage bucket).
    """

    def __init__(
        self,
        id: Optional[ImageId] = None,
        url: Optional[ImageUrl] = None,
        description: Optional[ImageDescription] = None,
        keywords: Optional[ImageKeywords] = None,
        generation_model: Optional[ImageGenerationModel] = None,
        generation_parameters: Optional[ImageGenerationParameters] = None,
        dimensions: Optional[ImageDimensions] = None,
        status: Optional[Status] = None,
        size: Optional[ImageSize] = None,
        mime_type: Optional[MimeType] = None,
        checksum: Optional[Checksum] = None,
        created_by: Optional[CreatedBy] = None,
        created_at: Optional[CreatedAt] = None,
        last_modified_at: Optional[LastModifiedAt] = None,
        events_list: Optional[List[dict]] = None,
    ):
        super().__init__(id if id is not None else ImageId(uuid.uuid4()))
        self.url: Optional[ImageUrl] = url
        self.description: Optional[ImageDescription] = description
        self.keywords: Optional[ImageKeywords] = keywords
        self.generation_model: Optional[ImageGenerationModel] = generation_model
        self.generation_parameters: Optional[ImageGenerationParameters] = (generation_parameters)
        self.dimensions: Optional[ImageDimensions] = dimensions
        self.status: Optional[Status] = status
        self.size: Optional[ImageSize] = size
        self.mime_type: Optional[MimeType] = mime_type
        self.checksum: Optional[Checksum] = checksum
        self.created_by: Optional[CreatedBy] = created_by
        self.created_at: Optional[CreatedAt] = created_at
        self.last_modified_at: Optional[LastModifiedAt] = last_modified_at
        self.events_list: List[
                MarketingImageGeneratedEvent
            | MarketingImageModifiedEvent
            | MarketingImageApprovedEvent
            | MarketingImageRejectedEvent
            | MarketingImageRemovedEvent
            | MarketingImageMetadataChangedEvent
        ] = events_list if events_list is not None else []

        self.status = status if status is not None else Status.from_string("GENERATED")

    def generate(self):
        self.status = Status.from_string("GENERATED")
        self.created_at = CreatedAt.now()
        self.last_modified_at = self.created_at
        self.add_domain_event(
            MarketingImageGeneratedEvent(
                id=str(self.id),
                url=self.url.url,
                description=self.description.description,
                keywords=self.keywords.keywords,
                generation_model=self.generation_model.model,
                generation_parameters=self.generation_parameters.parameters,
                dimensions=self.dimensions.to_dict(),
                size=self.size.size,
                mime_type=self.mime_type.mime_type,
                checksum=self.checksum.checksum,
                created_by=str(self.created_by.user_id),
                created_at=self.created_at.to_string(),
                last_modified_at=self.last_modified_at.to_string(),
            )
        )

    def approve(self):
        """
        Marks the marketing image as approved.
        """
        self.status = Status.from_string("APPROVED")
        self.last_modified_at = LastModifiedAt.now()
        self.add_domain_event(
            MarketingImageApprovedEvent(
                id=str(self.id),
                url=self.url.url,
                checksum=self.checksum.checksum,
                created_at=self.created_at.to_string() if self.created_at else None,
                last_modified_at=self.last_modified_at.to_string(),
            )
        )

    def reject(self):
        """
        Marks the marketing image as rejected.
        """
        self.status = Status.from_string("REJECTED")
        self.last_modified_at = LastModifiedAt.now()
        self.add_domain_event(
            MarketingImageRejectedEvent(
                id=str(self.id),
                url=self.url.url,
                checksum=self.checksum.checksum,
                created_at=self.created_at.to_string() if self.created_at else None,
                last_modified_at=self.last_modified_at.to_string(),
            )
        )

    def modify(self):
        """
        Updates the marketing image details.
        """
        self.status = Status.from_string("REVIEWING")
        self.last_modified_at = LastModifiedAt.now()
        self.add_domain_event(
            MarketingImageModifiedEvent(
                id=str(self.id),
                url=self.url.url,
                description=self.description.description,
                keywords=self.keywords.keywords,
                generation_model=self.generation_model.model,
                generation_parameters=self.generation_parameters.parameters,
                dimensions=self.dimensions.to_dict(),
                size=self.size.size,
                mime_type=self.mime_type.mime_type,
                checksum=self.checksum.checksum,
                created_at=self.created_at.to_string() if self.created_at else None,
                last_modified_at=self.last_modified_at.to_string(),
            )
        )

    def remove(self):
        """
        Removes the marketing image.
        """
        self.status = Status.from_string("REMOVED")
        self.last_modified_at = LastModifiedAt.now()
        self.add_domain_event(
            MarketingImageRemovedEvent(
                id=str(self.id),
                url=self.url.url,
                size=self.size.size,
                checksum=self.checksum.checksum,
                created_at=self.created_at.to_string() if self.created_at else None,
                last_modified_at=self.last_modified_at.to_string(),
            )
        )

    def change_metadata(
        self,
        description: Optional[ImageDescription] = None,
        keywords: Optional[ImageKeywords] = None,
        dimensions: Optional[ImageDimensions] = None,
        size: Optional[ImageSize] = None,
        url: Optional[ImageUrl] = None,
    ):
        if description is not None:
            self.description = description
        if keywords is not None:
            self.keywords = keywords
        if dimensions is not None:
            self.dimensions = dimensions
        if size is not None:
            self.size = size
        if url is not None:
            self.url = url
        self.last_modified_at = LastModifiedAt.now()
        self.add_domain_event(
            MarketingImageMetadataChangedEvent(
                id=str(self.id),
                url=self.url.url,
                description=self.description.description,
                keywords=self.keywords.keywords,
                dimensions=self.dimensions.to_dict(),
                size=self.size.size,
                created_at=self.created_at.to_string() if self.created_at else None,
                last_modified_at=self.last_modified_at.to_string(),
            )
        )