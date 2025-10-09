from typing import Dict, Any
from .base_command_object import Command


class ApproveMarketingImageData:
    """Represents the data payload for a ApproveMarketingImageCommand."""
    def __init__(
        self,
        request_id: str,
        request_time: str,
        requestor: str,
        image_id: str,
        approval_status_request: str,
        **kwargs: Any,  # To ignore extra fields from the input dict
    ):
        self.request_id = request_id
        self.request_time = request_time
        self.requestor = requestor
        self.image_id = image_id
        self.approval_status_request = approval_status_request

    def to_dict(self) -> Dict[str, Any]:
        """Converts the object to a dictionary for serialisation."""
        data = {
            "request_id": self.request_id,
            "request_time": self.request_time,
            "requestor": self.requestor,
            "image_id": self.image_id,
            "approval_status_request": self.approval_status_request,
        }
        return {k: v for k, v in data.items() if v is not None}


class ApproveMarketingImageCommand(Command):
    def __init__(
        self,
        data: Dict[str, Any],
        source: str,
        command_prefix: str,
        version: str = "1.0",
        **kwargs,
    ):
        super().__init__(
            type=f"{command_prefix}.approve",
            data=data,
            source=source,
            version=version,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApproveMarketingImageCommand":
        command_data = data.copy()
        command_data.pop("type", None)
        command_data["data"] = ApproveMarketingImageData(**command_data["data"])
        return cls(**command_data)