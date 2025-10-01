from ..ports.command_input_port import CommandInputPort
from ..ports.command_output_port import CommandOutputPort
from ..services.generate_marketing_image_core_service import GenerateMarketingImageCoreService
from ..command_objects.generate_marketing_image_command import GenerateMarketingImageCommand


class GenerateMarketingImageCommandHandler(
    CommandInputPort[GenerateMarketingImageCommand]
):
    def __init__(
        self,
        core_service: GenerateMarketingImageCoreService,
        command_dispatcher: CommandOutputPort,
    ):
        self.core_service = core_service
        command_dispatcher.register(GenerateMarketingImageCommand, self)

    def handle(self, command: GenerateMarketingImageCommand):
        """Handles the GenerateMarketingImageCommand by calling the core service."""
        core_service_response = self.core_service.generate_marketing_image(command)
        return core_service_response