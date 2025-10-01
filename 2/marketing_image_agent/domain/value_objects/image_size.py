from .base_value_object import ValueObject


class ImageSize(ValueObject):
    """
    Represents the size of an image in bytes.
    """

    def __init__(self, size: int):
        if not isinstance(size, int):
            raise ValueError("Image size must be an integer.")
        if size <= 0:
            raise ValueError("Image size must be positive.")
        self.size = size

    def __eq__(self, other):
        if not isinstance(other, ImageSize):
            return False
        return self.size == other.size

    def __hash__(self):
        return hash(self.size)
    
    @classmethod
    def from_string(cls, size: str):
        return cls(size=int(size))
    
    def to_string(self):
        return str(self.size)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(size=data["size"]) # Integer
    
    def to_dict(self):
        return {"size": self.size}

    def __str__(self):
        return f"{self.size} bytes"

    def __repr__(self):
        return f"ImageSize(size={self.size})"
