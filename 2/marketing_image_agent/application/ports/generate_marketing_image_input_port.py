from abc import ABC, abstractmethod
from typing import Dict, Any, Generic, TypeVar

from .base_input_port import BaseInputPort

T = TypeVar("T")


class GenerateMarketingImageInputPort(BaseInputPort[T], ABC, Generic[T]):
    """
    Input port for handling marketing image generation requests.
    The concrete implementation of this interface - a driving service -
    takes a DTO from an infrastructure adapter (via an input port),
    maps it to a command, and dispatches the command using a dispatcher
    in the infrastructure layer (via an output port).
    """
 
    @abstractmethod
    def handle(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handles an incoming request by passing it to the driving service.

        Args:
            request_data: A dictionary containing the request data.
        """
        raise NotImplementedError
