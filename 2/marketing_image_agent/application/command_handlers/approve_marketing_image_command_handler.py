from ..ports.command_input_port import CommandInputPort
from ..ports.command_output_port import CommandOutputPort
from ..services.approve_marketing_image_core_service import ApproveMarketingImageCoreService
from ..command_objects.approve_marketing_image_command import ApproveMarketingImageCommand


class ApproveMarketingImageCommandHandler(
    CommandInputPort[ApproveMarketingImageCommand]
):
    def __init__(
        self,
        core_service: ApproveMarketingImageCoreService,
        command_dispatcher: CommandOutputPort,
    ):
        self.core_service = core_service
        command_dispatcher.register(ApproveMarketingImageCommand, self)

    def handle(self, command: ApproveMarketingImageCommand):
        """Handles the ApproveMarketingImageCommand by calling the core service."""
        core_service_response = self.core_service.approve_marketing_image(command)
        return core_service_response