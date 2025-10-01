from .base_value_object import ValueObject


class ImageDescription(ValueObject):
    """
    Represents the description of an image.
    """

    def __init__(self, description: str):
        if not isinstance(description, str):
            raise ValueError("Image description must be a string.")
        if not description:
            raise ValueError("Image description cannot be empty.")
        self.description = description

    def __eq__(self, other):
        if not isinstance(other, ImageDescription):
            return False
        return self.description == other.description

    def __hash__(self):
        return hash(self.description)

    @classmethod
    def from_string(cls, description: str):
        return ImageDescription(description=description)
    
    def to_string(self):
        return self.description

    @classmethod
    def from_dict(cls, data: dict):
        return cls(description=data["description"])
    
    def to_dict(self):
        return {"description": self.description}

    def __str__(self):
        return self.description

    def __repr__(self):
        return f"ImageDescription(description={self.description})"
