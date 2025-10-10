from ...domain.entities.marketing_image_aggregate import MarketingImage
from ...domain.factories.marketing_image_aggregate_factory import MarketingImageAggregateFactory
from ..command_objects.remove_marketing_image_command import RemoveMarketingImageCommand
from ..ports.marketing_image_repository_output_port import MarketingImageRepositoryOutputPort
from ..ports.marketing_image_object_storage_output_port import MarketingImageObjectStorageOutputPort
from ..ports.domain_event_output_port import DomainEventOutputPort


class RemoveMarketingImageCoreService:
    def __init__(
        self,
        marketing_image_repository: MarketingImageRepositoryOutputPort,
        marketing_image_object_storage: MarketingImageObjectStorageOutputPort,
        domain_event_prefix: str,
        domain_event_dispatcher: DomainEventOutputPort,
    ):
        self.aggregate_factory = MarketingImageAggregateFactory()
        self.aggregate_repository = marketing_image_repository
        self.object_storage = marketing_image_object_storage
        self.domain_event_prefix = domain_event_prefix
        self.domain_event_dispatcher = domain_event_dispatcher

    def remove_marketing_image(self, command: RemoveMarketingImageCommand) -> MarketingImage:
        command_data = command.data

        requestor = command_data["requestor"]
        request_id = command_data["request_id"]
        image_id = command_data["image_id"]
        print(f"Handling 'remove marketing image' command for Image: {image_id} with Request ID: {request_id}")

        marketing_image = self.aggregate_repository.retrieve_by_id(image_id)
        if not marketing_image:
            raise ValueError(f"Marketing image with ID {image_id} not found.")
        
        url = marketing_image.url.url
        file_name = url.split('/')[-1]
        
        object_storage_removal_result = self.object_storage.remove_marketing_image_object(file_name=file_name)
        if not object_storage_removal_result:
            raise ValueError(f"Image with file name {file_name} not found in object storage.")
        
        marketing_image.remove()

        # Get the most recent domain event before it's cleared by the remove method.
        marketing_image_removed_most_recent_domain_event = marketing_image.events_list[-1]

        self.aggregate_repository.remove(image_id)
        print(f"Successfully removed marketing image with ID: {marketing_image.id}")

        # Dispatch the most recent domain event using the dispatcher
        self.domain_event_dispatcher.dispatch(domain_event=marketing_image_removed_most_recent_domain_event)

        response = {
            "request_id": request_id,
            "requestor": requestor,
            "image_id": str(marketing_image.id),
            "url": marketing_image.url.url,
            "status": marketing_image.status.status.value,
        }
        
        return response