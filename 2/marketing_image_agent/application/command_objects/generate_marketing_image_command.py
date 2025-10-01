from typing import Any, Dict, Optional

from .base_command_object import Command


class ImageDimensions:
    """Represents image dimensions."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def to_dict(self) -> Dict[str, int]:
        """Converts the object to a dictionary."""
        return {"width": self.width, "height": self.height}


class GenerateMarketingImageData:
    """Represents the data payload for a GenerateMarketingImageCommand."""

    def __init__(
        self,
        request_id: str,
        requestor: str,
        request_text: str,
        image_min_dimensions: Optional[Dict[str, int]] = None,
        image_max_dimensions: Optional[Dict[str, int]] = None,
        mime_type: Optional[str] = None,
        **kwargs: Any,  # To ignore extra fields from the input dict
    ):
        self.request_id = request_id
        self.requestor = requestor
        self.request_text = request_text
        self.image_min_dimensions = (
            ImageDimensions(**image_min_dimensions) if isinstance(image_min_dimensions, dict) else image_min_dimensions
        )
        self.image_max_dimensions = (
            ImageDimensions(**image_max_dimensions) if isinstance(image_max_dimensions, dict) else image_max_dimensions
        )
        self.mime_type = mime_type

    def to_dict(self) -> Dict[str, Any]:
        """Converts the object to a dictionary for serialisation."""
        data = {
            "request_id": self.request_id,
            "requestor": self.requestor,
            "request_text": self.request_text,
            "image_min_dimensions": self.image_min_dimensions.to_dict() if self.image_min_dimensions else None,
            "image_max_dimensions": self.image_max_dimensions.to_dict() if self.image_max_dimensions else None,
            "mime_type": self.mime_type,
        }
        return {k: v for k, v in data.items() if v is not None}


class GenerateMarketingImageCommand(Command):
    """Command to generate a marketing image."""

    payload: GenerateMarketingImageData

    def __init__(
        self,
        data: GenerateMarketingImageData,
        source: str,
        command_prefix: str,
        version: str = "1.0",
        **kwargs,
    ):
        self.payload = data
        super().__init__(
            type=f"{command_prefix}.generate",
            data=self.payload.to_dict(),
            source=source,
            version=version,
            **kwargs,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GenerateMarketingImageCommand":
        command_data = data.copy()
        command_data.pop("type", None)
        command_data["data"] = GenerateMarketingImageData(**command_data["data"])
        return cls(**command_data)
