from abc import ABC, abstractmethod
from typing import TypeVar

from .base_output_port import BaseOutputPort

T = TypeVar("T")


class MarketingImageImageGenerationOutputPort(BaseOutputPort[T], ABC):
    """
    This class defines the interface for generating marketing images (the actual bytes) using GenAI models.
    """
    @abstractmethod
    def generate_marketing_image(self, prompt: str, min_dimensions: dict = None, max_dimensions: dict = None, mime_type: str = None) -> dict:
        """
        Generates a marketing image using AI.

        Args:
            prompt: The prompt to generate the marketing image.
            min_dimensions: The minimum dimensions of the generated image.
            max_dimensions: The maximum dimensions of the generated image.
            mime_type: The MIME type of the generated image.

        Returns:
            image_data: The data/bytes of the generated marketing image.
            mime_type: The MIME type of the generated marketing image.
            generation_model: The name of the model used to generate the marketing image.
            image_dimensions: A dictionary containing the dimensions of the generated marketing image (height, width).
            generation_parameters: A dictionary containing the parameters used to generate the marketing image.
        """
        pass