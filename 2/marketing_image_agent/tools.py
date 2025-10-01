import os
import uuid
from typing import Dict, Optional, Literal
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime

from config import Container

class InputDataBaseClass(BaseModel):
    """
    A base class for input data models using Pydantic for validation.
    The 'request_type' field is used to discriminate between different input request types.
    """
    request_id: str
    request_type: Literal["generate", "change", "set_acceptance_status", "remove"]
    request_time: Optional[str] = None
    traceparent: Optional[str] = None
    tracestate: Optional[str] = None

class GenerateMarketingImageInputData(InputDataBaseClass):
    requestor: str
    request_text: str
    image_min_dimensions: Optional[Dict[str, int]] = None
    image_max_dimensions: Optional[Dict[str, int]] = None
    mime_type: Optional[str] = None

# class ChangeMarketingImageInputData(InputDataBaseClass):

# class SetMarketingImageAcceptanceStatusInputData(InputDataBaseClass):

# class RemoveMarketingImageInputData(InputDataBaseClass):


class MarketingImageGenerator:
    """A tool for generating marketing images."""

    def __init__(self, container: Container):
        """Initialises the MarketingImageGeneratorTool."""
        load_dotenv()

        self.container = container

        # Wire and instantiate services
        self.container.wire(
            modules=[
                __name__,
                ".application.services.generate_marketing_image_driving_service",
                "config",
            ]
        )

        # Eagerly instantiate handlers to register them
        self.container.generate_marketing_image_command_handler()
        self.container.marketing_image_generated_domain_event_handler()
        self.driving_service = self.container.generate_marketing_image_driving_service()

    def generate_image(self, prompt: str): # -> dict:
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

        result = self.driving_service.handle(generate_marketing_image_input_data.model_dump())
        print(result)
        return result