from .base_value_object import ValueObject


class ImageDimensions(ValueObject):
    """
    Represents the dimensions (width and height) of an image.
    """

    def __init__(self, width: int, height: int):
        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError("Image dimensions must be integers.")
        if width <= 0 or height <= 0:
            raise ValueError("Image dimensions must be positive.")
        self.width = width
        self.height = height

    def __eq__(self, other):
        if not isinstance(other, ImageDimensions):
            return False
        return self.width == other.width and self.height == other.height

    def __hash__(self):
        return hash((self.width, self.height))

    @classmethod
    def from_string(cls, dimensions: str):
        width, height = dimensions.split("x")
        return cls(width=int(width), height=int(height))
    
    def to_string(self):
        return f"{self.width}x{self.height}"
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(width=data["width"], height=data["height"])
    
    def to_dict(self):
        return {"width": self.width, "height": self.height}

    def __str__(self):
        return f"{self.width}x{self.height}"

    def __repr__(self):
        return f"ImageDimensions(width={self.width}, height={self.height})"
