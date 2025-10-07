from .base_service import DrivingSideService
from typing import Dict, Any
from ..ports.generate_marketing_image_input_port import GenerateMarketingImageInputPort
from ..command_objects.base_command_object import Command
from ..command_objects.generate_marketing_image_command import GenerateMarketingImageCommand, GenerateMarketingImageData
from ..command_objects.edit_marketing_image_command import EditMarketingImageCommand
from ..command_objects.approve_marketing_image_command import ApproveMarketingImageCommand
from ..command_objects.reject_marketing_image_command import RejectMarketingImageCommand
from ..command_objects.remove_marketing_image_command import RemoveMarketingImageCommand
from ..command_objects.update_marketing_image_metadata_command import UpdateMarketingImageMetadataCommand


class GenerateMarketingImageDrivingService(
    DrivingSideService[Command], GenerateMarketingImageInputPort[Command]
):
    """
    Application service for handling marketing image requests from a driving adapter.
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
        self.source = "driving-side-service"

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
            case "generate":
                data = {
                    "request_id": request_data.get("request_id"),
                    "request_time": request_data.get("request_time"),
                    "requestor": request_data.get("requestor"),
                    "request_text": request_data.get("request_text"),
                    "image_min_dimensions": request_data.get("image_min_dimensions"),
                    "image_max_dimensions": request_data.get("image_max_dimensions"),
                    "mime_type": request_data.get("mime_type"),
                }

                command = GenerateMarketingImageCommand(
                    data=GenerateMarketingImageData(**data),
                    source=self.source,
                    command_prefix=self.command_prefix,
                )

            case "remove":
                command = RemoveMarketingImageCommand(data=request_data, source=self.source)

            case "change":
                # If image data or a new prompt is present, it's an edit, otherwise a metadata update.
                # This logic assumes that a request to change the image content will include
                # keys like 'image_data' or 'new_request_text'.
                if "image_data" in request_data or "new_request_text" in request_data:
                    command = EditMarketingImageCommand(data=request_data, source=self.source)
                else:
                    command = UpdateMarketingImageMetadataCommand(data=request_data, source=self.source)

            case "set_approval_status":
                approval_status = request_data.get("approval_status")
                if approval_status == "approved":
                    command = ApproveMarketingImageCommand(data=request_data, source=self.source)
                elif approval_status == "rejected":
                    command = RejectMarketingImageCommand(data=request_data, source=self.source)
                else:
                    raise ValueError(
                        "Invalid or missing 'approval_status' for request type"
                        f" '{request_type}'. Expected 'approved' or 'rejected'."
                )
            
            case _:
                raise ValueError(f"Invalid request type: {request_type}")

        command_handler_response = self.command_dispatcher.dispatch(command)

        return command_handler_response

        # return {"status": "success", "message": f"Command for request type '{request_type}' dispatched."}