from typing import Dict, Any
from .base_value_object import ValueObject


class ImageGenerationParameters(ValueObject):
    """
    Represents the parameters used for image generation.
    """

    def __init__(self, parameters: Dict[str, Any]):
        if not isinstance(parameters, dict):
            raise ValueError("Image generation parameters must be a dictionary.")
        self.parameters = parameters

    def __eq__(self, other):
        if not isinstance(other, ImageGenerationParameters):
            return False
        return self.parameters == other.parameters

    def __hash__(self):
        return hash(tuple(sorted(self.parameters.items())))

    @classmethod
    def from_string(cls, parameters: str):
        param_dict = {}
        for param in parameters.split(","): # "key1:value1, key2:value2"
            key, value = param.strip().split(":")
            param_dict[key] = value
        return cls(parameters=param_dict)
    
    def to_string(self):
        return ", ".join([f"{k}:{v}" for k, v in self.parameters.items()])

    @classmethod
    def from_dict(cls, data: dict):
        return cls(parameters=data["parameters"])

    def to_dict(self):
        return {"parameters": self.parameters}

    def __str__(self):
        return str(self.parameters)

    def __repr__(self):
        return f"ImageGenerationParameters(parameters={self.parameters})"
