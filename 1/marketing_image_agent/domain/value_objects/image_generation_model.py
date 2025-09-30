from .base_value_object import ValueObject


class ImageGenerationModel(ValueObject):
    """
    Represents the AI model used to generate the image.
    """

    def __init__(self, model: str):
        if not isinstance(model, str):
            raise ValueError("Image generation model must be a string.")
        if not model:
            raise ValueError("Image generation model cannot be empty.")
        self.model = model

    def __eq__(self, other):
        if not isinstance(other, ImageGenerationModel):
            return False
        return self.model == other.model

    def __hash__(self):
        return hash(self.model)
    
    @classmethod
    def from_string(cls, model: str):
        return ImageGenerationModel(model=model)
    
    def to_string(self):
        return self.model

    @classmethod
    def from_dict(cls, data: dict):
        return cls(model=data["model"])
    
    def to_dict(self):
        return {"model": self.model}

    def __str__(self):
        return self.model

    def __repr__(self):
        return f"ImageGenerationModel(model={self.model})"
