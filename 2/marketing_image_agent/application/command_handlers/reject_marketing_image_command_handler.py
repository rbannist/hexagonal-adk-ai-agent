from ..ports.command_input_port import CommandInputPort
from ..ports.command_output_port import CommandOutputPort
from ..services.reject_marketing_image_core_service import RejectMarketingImageCoreService
from ..command_objects.reject_marketing_image_command import RejectMarketingImageCommand


class RejectMarketingImageCommandHandler(
    CommandInputPort[RejectMarketingImageCommand]
):
    def __init__(
        self,
        core_service: RejectMarketingImageCoreService,
        command_dispatcher: CommandOutputPort,
    ):
        self.core_service = core_service
        command_dispatcher.register(RejectMarketingImageCommand, self)

    def handle(self, command: RejectMarketingImageCommand):
        """Handles the RejectMarketingImageCommand by calling the core service."""
        core_service_response = self.core_service.reject_marketing_image(command)
        return core_service_response