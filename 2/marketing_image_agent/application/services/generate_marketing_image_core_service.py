import uuid
from datetime import datetime

from ...domain.entities.marketing_image_aggregate import MarketingImage
from ...domain.factories.marketing_image_aggregate_factory import MarketingImageAggregateFactory
from ..command_objects.generate_marketing_image_command import GenerateMarketingImageCommand
from ..ports.marketing_image_repository_output_port import MarketingImageRepositoryOutputPort
from ..ports.marketing_image_object_storage_output_port import MarketingImageObjectStorageOutputPort
from ..ports.generate_marketing_image_genai_output_port import MarketingImageImageGenerationOutputPort
from ..ports.domain_event_output_port import DomainEventOutputPort


class GenerateMarketingImageCoreService:
    def __init__(
        self,
        marketing_image_repository: MarketingImageRepositoryOutputPort,
        marketing_image_object_storage: MarketingImageObjectStorageOutputPort,
        marketing_image_genai_generator: MarketingImageImageGenerationOutputPort,
        domain_event_prefix: str,
        domain_event_dispatcher: DomainEventOutputPort,
    ):
        self.aggregate_factory = MarketingImageAggregateFactory()
        self.aggregate_repository = marketing_image_repository
        self.object_storage = marketing_image_object_storage
        self.genai_image_generator = marketing_image_genai_generator
        self.domain_event_prefix = domain_event_prefix
        self.domain_event_dispatcher = domain_event_dispatcher

    def generate_marketing_image(self, command: GenerateMarketingImageCommand) -> MarketingImage:
        command_data = command.data

        request_id = command_data["request_id"]
        print(f"Handling command with Request ID: {request_id}")
        request_text = command_data["request_text"]
        
        image_min_dimensions = command_data["image_min_dimensions"]
        image_max_dimensions = command_data["image_max_dimensions"]
        mime_type = command_data["mime_type"]

        image_generation_prompt = f"{request_text}"
        print(f"Image generation prompt: {image_generation_prompt}")

        generated_marketing_image = self.genai_image_generator.generate_marketing_image(prompt=image_generation_prompt, min_dimensions=image_min_dimensions, max_dimensions=image_max_dimensions, mime_type=mime_type)
        
        image_file_name = f"{request_id}.png"
        generated_image_bytes = generated_marketing_image["image_data"]
        generated_image_dimensions = generated_marketing_image["image_dimensions"]
        generated_image_mime_type = generated_marketing_image["mime_type"]
        generated_image_model = generated_marketing_image["generation_model"]
        generated_image_height = generated_image_dimensions["height"]
        generated_image_width = generated_image_dimensions["width"]
        generated_image_generation_parameters = generated_marketing_image["generation_parameters"]
        generated_image_size = len(generated_image_bytes)

        storage_saved_image_url, storage_saved_image_checksum = self.object_storage.save_marketing_image_object(image_data=generated_image_bytes, file_name=image_file_name, content_type=generated_image_mime_type, fixed_key_metadata={"content_type":generated_image_mime_type}, custom_metadata={"key1":"value1"})

        marketing_image_dict = self.aggregate_factory.generate(
            {
                "url": storage_saved_image_url,
                "description": image_generation_prompt,
                "keywords": ["retail"],
                "generation_model": generated_image_model,
                "generation_parameters": generated_image_generation_parameters,
                "dimensions": {"width": generated_image_width, "height": generated_image_height},
                "status": "GENERATED",
                "size": generated_image_size,
                "mime_type": generated_image_mime_type,
                "checksum": storage_saved_image_checksum,
                "created_by": str(uuid.uuid4()),
                "created_at": str(datetime.now().isoformat()),
                "last_modified_at": str(datetime.now().isoformat()),
            }
        )

        marketing_image = self.aggregate_factory.from_dict(marketing_image_dict)

        # Get the most recent domain event before it's cleared by the save method.
        marketing_image_generated_most_recent_domain_event = marketing_image.events_list[-1]

        self.aggregate_repository.save(marketing_image)
        print(f"Successfully generated and saved marketing image with ID: {marketing_image.id}")

        # Dispatch the most recent domain event using the dispatcher
        self.domain_event_dispatcher.dispatch(domain_event=marketing_image_generated_most_recent_domain_event)
        
        response = {
            "id": marketing_image_dict.get("id"),
            "url": marketing_image_dict.get("url"),
        }
        
        return response