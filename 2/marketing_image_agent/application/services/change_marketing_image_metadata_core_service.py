from ...domain.entities.marketing_image_aggregate import MarketingImage
from ...domain.factories.marketing_image_aggregate_factory import MarketingImageAggregateFactory
from ..command_objects.change_marketing_image_metadata_command import ChangeMarketingImageMetadataCommand
from ..ports.marketing_image_repository_output_port import MarketingImageRepositoryOutputPort
from ..ports.domain_event_output_port import DomainEventOutputPort


class ChangeMarketingImageMetadataCoreService:
    def __init__(
        self,
        marketing_image_repository: MarketingImageRepositoryOutputPort,
        domain_event_prefix: str,
        domain_event_dispatcher: DomainEventOutputPort,
    ):
        self.aggregate_factory = MarketingImageAggregateFactory()
        self.aggregate_repository = marketing_image_repository
        self.domain_event_prefix = domain_event_prefix
        self.domain_event_dispatcher = domain_event_dispatcher

    def change_marketing_image_metadata(self, command: ChangeMarketingImageMetadataCommand) -> MarketingImage:
        command_data = command.data

        requestor = command_data["requestor"]
        request_id = command_data["request_id"]
        image_id = command_data["image_id"]
        print(f"Handling 'change marketing image metadata' command for Image: {image_id} with Request ID: {request_id}")

        marketing_image = self.aggregate_repository.retrieve_by_id(image_id)
        if not marketing_image:
            raise ValueError(f"Marketing image with ID {image_id} not found.")

        # Use the factory to apply changes. The factory will handle creating VOs.
        updated_marketing_image = self.aggregate_factory.change_metadata(
            data=self.aggregate_factory.to_dict(marketing_image),
            description=command_data.get("new_description"),
            keywords=command_data.get("new_keywords"),
            dimensions=command_data.get("new_dimensions"),
            size=command_data.get("new_size"),
            url=command_data.get("new_url"),
        )

        marketing_image_metadata_changed_event = updated_marketing_image.events_list[-1]
        changed_metadata = marketing_image_metadata_changed_event.data.copy()
        # Remove non-metadata fields from the response dictionary
        changed_metadata.pop("id", None)
        changed_metadata.pop("changed_at", None)
        changed_metadata.pop("changed_by", None)

        self.aggregate_repository.save(updated_marketing_image)
        print(f"Successfully changed metadata and saved marketing image with ID: {marketing_image.id}")

        self.domain_event_dispatcher.dispatch(domain_event=marketing_image_metadata_changed_event)
        
        return {
            "request_id": request_id,
            "requestor": requestor,
            "image_id": str(updated_marketing_image.id),
            "url": updated_marketing_image.url,
            "changed_metadata": changed_metadata
        }