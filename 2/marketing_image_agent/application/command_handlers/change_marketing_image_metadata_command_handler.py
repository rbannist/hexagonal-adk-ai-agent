from ..ports.command_input_port import CommandInputPort
from ..ports.command_output_port import CommandOutputPort
from ..services.change_marketing_image_metadata_core_service import ChangeMarketingImageMetadataCoreService
from ..command_objects.change_marketing_image_metadata_command import ChangeMarketingImageMetadataCommand


class ChangeMarketingImageMetadataCommandHandler(
    CommandInputPort[ChangeMarketingImageMetadataCommand]
):
    def __init__(
        self,
        core_service: ChangeMarketingImageMetadataCoreService,
        command_dispatcher: CommandOutputPort,
    ):
        self.core_service = core_service
        command_dispatcher.register(ChangeMarketingImageMetadataCommand, self)

    def handle(self, command: ChangeMarketingImageMetadataCommand):
        """Handles the ChangeMarketingImageMetadataCommand by calling the core service."""
        core_service_response = self.core_service.change_marketing_image_metadata(command)
        return core_service_response