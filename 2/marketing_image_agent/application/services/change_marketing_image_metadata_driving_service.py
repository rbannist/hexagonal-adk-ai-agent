from .base_service import DrivingSideService
from typing import Dict, Any
from ..ports.change_marketing_image_metadata_input_port import ChangeMarketingImageMetadataInputPort
from ..command_objects.base_command_object import Command
from ..command_objects.change_marketing_image_metadata_command import ChangeMarketingImageMetadataCommand


class ChangeMarketingImageMetadataDrivingService(
    DrivingSideService[Command], ChangeMarketingImageMetadataInputPort[Command]
):
    """
    Application service for handling marketing image metadata change requests from a driving adapter.
    """

    def __init__(self, command_dispatcher, command_prefix: str):
        """
        Initialises the service with a command dispatcher.

        Args:
            command_dispatcher: An object with a 'dispatch' method that accepts a command.
            command_prefix: The prefix for command types.
        """
        self.command_dispatcher = command_dispatcher
        self.command_prefix = command_prefix
        self.source = "change-marketing-image-metadata-driving-side-service"

    def handle(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handles an incoming request by mapping it to a command and dispatching it.

        Args:
            request_data: A dictionary containing the request data, including the request type.

        Raises:
            ValueError: If the request type is invalid or missing, or if required data for a
                        specific request type is not present.
        """
        request_type = request_data.get("request_type")
        command: Command | None = None

        match request_type:
            case "change_attributes":
                command = ChangeMarketingImageMetadataCommand(
                    data=request_data,
                    source=self.source,
                    command_prefix=self.command_prefix,
                )
            case _:
                raise ValueError(f"Invalid request type: {request_type}")

        command_handler_response = self.command_dispatcher.dispatch(command)

        return command_handler_response