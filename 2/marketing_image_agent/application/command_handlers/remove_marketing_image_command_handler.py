from ..ports.command_input_port import CommandInputPort
from ..ports.command_output_port import CommandOutputPort
from ..services.remove_marketing_image_core_service import RemoveMarketingImageCoreService
from ..command_objects.remove_marketing_image_command import RemoveMarketingImageCommand


class RemoveMarketingImageCommandHandler(
    CommandInputPort[RemoveMarketingImageCommand]
):
    def __init__(
        self,
        core_service: RemoveMarketingImageCoreService,
        command_dispatcher: CommandOutputPort,
    ):
        self.core_service = core_service
        command_dispatcher.register(RemoveMarketingImageCommand, self)

    def handle(self, command: RemoveMarketingImageCommand):
        """Handles the RemoveMarketingImageCommand by calling the core service."""
        core_service_response = self.core_service.remove_marketing_image(command)
        return core_service_response