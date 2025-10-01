from abc import ABC, abstractmethod
from typing import Any, TypeVar, Tuple

from .base_output_port import BaseOutputPort

T = TypeVar("T")


class MarketingImageObjectStorageOutputPort(BaseOutputPort[T], ABC):
    """
    This class defines the interface for storing marketing images.
    """

    @abstractmethod
    def save_marketing_image_object(self, image_data: Any, file_name: str, content_type: str) -> Tuple[str, str]:
        """
        Saves the marketing image data to the object storage.

        Args:
            image_data: The image data to be saved.
            file_name: The name of the file to save the image as.
            content_type: The content type of the image.

        Returns:
            A tuple containing the URL to the saved image and its checksum.
        """
        pass

    @abstractmethod
    def retrieve_marketing_image_object(self, file_name: str) -> Any:
        """
        Retrieves the marketing image data from the object storage.

        Args:
            file_name: The name of the file to retrieve the image from.

        Returns:
            The image data.
        """
        pass

    @abstractmethod
    def remove_marketing_image_object(self, file_name: str) -> None:
        """
        Removes the marketing image data from the object storage.

        Args:
            file_name: The name of the file to delete the image from.
        """
        pass