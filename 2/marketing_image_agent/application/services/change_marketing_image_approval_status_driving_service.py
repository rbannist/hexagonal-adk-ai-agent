from .base_service import DrivingSideService
from typing import Dict, Any
from ..ports.change_marketing_image_approval_status_input_port import ChangeMarketingImageApprovalStatusInputPort
from ..command_objects.base_command_object import Command
from ..command_objects.approve_marketing_image_command import ApproveMarketingImageCommand
from ..command_objects.reject_marketing_image_command import RejectMarketingImageCommand


class ChangeMarketingImageApprovalStatusDrivingService(
    DrivingSideService[Command], ChangeMarketingImageApprovalStatusInputPort[Command]
):
    """
    Application service for handling marketing image approval status change requests from a driving adapter.
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
        self.source = "change-marketing-image-approval-status-driving-side-service"

    def handle(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handles an incoming request by mapping it to commands and dispatching them.

        Args:
            request_data: A dictionary containing the request data, including the request type.

        Raises:
            ValueError: If the request type is invalid or missing, or if required data for a
                        specific request type is not present.
        """
        request_type = request_data.get("request_type")
        command: Command | None = None

        match request_type:
            case "approval_status_change_request":
                approval_status_request = request_data.get("approval_status_request")
                if approval_status_request == "approve":
                    command = ApproveMarketingImageCommand(
                        data=request_data,
                        source=self.source,
                        command_prefix=self.command_prefix
                    )
                elif approval_status_request == "reject":
                    command = RejectMarketingImageCommand(
                        data=request_data,
                        source=self.source,
                        command_prefix=self.command_prefix
                    )
                else:
                    raise ValueError(
                        "Invalid or missing 'approval_status_request' for request type"
                        f" '{request_type}'. Expected 'approve' or 'reject'."
                )
            case _:
                raise ValueError(f"Invalid request type: {request_type}")

        command_handler_response = self.command_dispatcher.dispatch(command)

        return command_handler_response