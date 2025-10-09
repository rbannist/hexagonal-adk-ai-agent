from ...domain.entities.marketing_image_aggregate import MarketingImage
from ...domain.factories.marketing_image_aggregate_factory import MarketingImageAggregateFactory
from ..command_objects.reject_marketing_image_command import RejectMarketingImageCommand
from ..ports.marketing_image_repository_output_port import MarketingImageRepositoryOutputPort
from ..ports.domain_event_output_port import DomainEventOutputPort


class RejectMarketingImageCoreService:
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

    def reject_marketing_image(self, command: RejectMarketingImageCommand) -> MarketingImage:
        command_data = command.data

        requestor = command_data["requestor"]
        request_id = command_data["request_id"]
        image_id = command_data["image_id"]
        print(f"Handling 'reject marketing image' command for Image: {image_id} with Request ID: {request_id}")

        marketing_image = self.aggregate_repository.retrieve_by_id(image_id)
        if not marketing_image:
            raise ValueError(f"Marketing image with ID {image_id} not found.")

        marketing_image.reject()

        # Get the most recent domain event before it's cleared by the save method.
        marketing_image_rejected_most_recent_domain_event = marketing_image.events_list[-1]

        self.aggregate_repository.save(marketing_image)
        print(f"Successfully rejected and saved marketing image with ID: {marketing_image.id}")

        # Dispatch the most recent domain event using the dispatcher
        self.domain_event_dispatcher.dispatch(domain_event=marketing_image_rejected_most_recent_domain_event)
        
        response = {
            "request_id": request_id,
            "requestor": requestor,
            "image_id": str(marketing_image.id),
            "url": marketing_image.url.url,
            "status": marketing_image.status.status.value,
        }

        return response