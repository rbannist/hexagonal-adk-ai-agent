import uuid
from typing import Dict, Optional, Literal, List
from pydantic import BaseModel
from datetime import datetime

from config import Container

class InputDataBaseClass(BaseModel):
    """
    A base class for input data models using Pydantic for validation.
    The 'request_type' field is used to discriminate between different input request types.
    """
    request_id: str
    request_type: Literal["generate", "change_metadata", "approval_status_change_request", "remove"]
    requestor: str
    request_time: Optional[str] = None
    traceparent: Optional[str] = None
    tracestate: Optional[str] = None

class GenerateMarketingImageInputData(InputDataBaseClass):
    request_type: Literal["generate"] = "generate"
    request_text: str
    image_min_dimensions: Optional[Dict[str, int]] = None
    image_max_dimensions: Optional[Dict[str, int]] = None
    mime_type: Optional[str] = None

class ChangeMarketingImageAttributesInputData(InputDataBaseClass):
    request_type: Literal["change_attributes"] = "change_attributes"
    image_id: str
    new_description: Optional[str] = None
    new_keywords: Optional[list[str]] = None
    new_dimensions: Optional[dict] = None
    new_url: Optional[str] = None
    new_size: Optional[int] = None

class ChangeMarketingImageApprovalStatusInputData(InputDataBaseClass):
    request_type: Literal["approval_status_change_request"] = "approval_status_change_request"
    image_id: str
    approval_status_request: Literal["approve", "reject"]

class RemoveMarketingImageInputData(InputDataBaseClass):
    request_type: Literal["remove"] = "remove"
    image_id: str


class MarketingImageTools:
    """A tool for handling all marketing image-related operations."""

    def __init__(self, container: Container):
        """Initialises the MarketingImageTools."""

        self.container = container

        # Wire and instantiate services
        self.container.wire(
            modules=[
                __name__,
                ".application.services.generate_marketing_image_driving_service",
                ".application.services.change_marketing_image_approval_status_driving_service",
                ".application.services.remove_marketing_image_driving_service",
                ".application.services.change_marketing_image_metadata_driving_service",
                "config",
            ]
        )

        # Eagerly instantiate handlers to register them
        self.container.generate_marketing_image_command_handler()
        self.container.approve_marketing_image_command_handler()
        self.container.reject_marketing_image_command_handler()
        self.container.remove_marketing_image_command_handler()
        self.container.change_marketing_image_metadata_command_handler()
        self.container.marketing_image_generated_domain_event_handler()
        self.container.marketing_image_approved_domain_event_handler()
        self.container.marketing_image_rejected_domain_event_handler()
        self.container.marketing_image_removed_domain_event_handler()
        self.container.marketing_image_metadata_changed_domain_event_handler()
        self.generate_marketing_image_driving_service = self.container.generate_marketing_image_driving_service()
        self.change_marketing_image_approval_status_driving_service = self.container.change_marketing_image_approval_status_driving_service()
        self.remove_marketing_image_driving_service = self.container.remove_marketing_image_driving_service()
        self.change_marketing_image_metadata_driving_service = self.container.change_marketing_image_metadata_driving_service()

    def generate_image(self, prompt: str) -> dict:
        """Generates a marketing image based on a text prompt."""
        input_data_dict = {
            "request_id": str(uuid.uuid4()),
            "request_time": str(datetime.now().isoformat()),
            "request_type": "generate",
            "requestor": str(uuid.uuid4()),
            "request_text": prompt,
            "image_min_dimensions": {"width": 1024, "height": 1024},
            "image_max_dimensions": {"width": 2048, "height": 2048},
            "mime_type": "image/png",
        }
        generate_marketing_image_input_data = GenerateMarketingImageInputData(**input_data_dict)

        result = self.generate_marketing_image_driving_service.handle(
            generate_marketing_image_input_data.model_dump()
        )
        print(result)
        return result

    def change_image_approval_status_request(self, image_id: str, status: Literal["approve", "reject"]) -> dict:
        """Requests an approval status change for a marketing image."""
        input_data_dict = {
            "request_id": str(uuid.uuid4()),
            "request_time": str(datetime.now().isoformat()),
            "request_type": "approval_status_change_request",
            "requestor": str(uuid.uuid4()),
            "image_id": image_id,
            "approval_status_request": status,
        }
        approval_status_change_request_input_data = ChangeMarketingImageApprovalStatusInputData(**input_data_dict)
        if status not in ["approve", "reject"]:
            raise ValueError("Invalid status. Must be 'approve' or 'reject'.")
        
        result = self.change_marketing_image_approval_status_driving_service.handle(approval_status_change_request_input_data.model_dump())
        return result

    def remove_image(self, image_id: str) -> dict:
        """Removes a marketing image."""
        input_data_dict = {
            "request_id": str(uuid.uuid4()),
            "request_time": str(datetime.now().isoformat()),
            "request_type": "remove",
            "requestor": str(uuid.uuid4()),
            "image_id": image_id,
        }
        remove_image_input_data = RemoveMarketingImageInputData(**input_data_dict)
        result = self.remove_marketing_image_driving_service.handle(remove_image_input_data.model_dump())
        return result

    def change_image_attributes(
        self,
        image_id: str,
        new_description: Optional[str] = None,
        new_keywords: Optional[List[str]] = None,
        new_dimensions: Optional[dict] = None,
        new_url: Optional[str] = None,
        new_size: Optional[int] = None,
    ) -> dict:
        """Changes the attributes of a marketing image."""
        input_data_dict = {
            "request_id": str(uuid.uuid4()), # This needs an implementation based on the session
            "request_time": str(datetime.now().isoformat()),
            "request_type": "change_attributes",
            "requestor": str(uuid.uuid4()), # This needs an implementation based on the session
            "image_id": image_id,
            "new_description": new_description,
            "new_keywords": new_keywords,
            "new_dimensions": new_dimensions,
            "new_url": new_url,
            "new_size": new_size,
        }
        # Filter out None values for optional fields before creating the Pydantic model
        filtered_input_data = {k: v for k, v in input_data_dict.items() if v is not None}
        change_attributes_input_data = ChangeMarketingImageAttributesInputData(**filtered_input_data)
        result = self.change_marketing_image_metadata_driving_service.handle(change_attributes_input_data.model_dump())
        return result