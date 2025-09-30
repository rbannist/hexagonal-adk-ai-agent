import uuid

from .base_value_object import ValueObject


class ImageId(ValueObject):
    """
    Represents the unique identifier for an image.
    """

    def __init__(self, id: uuid.UUID):
        if not isinstance(id, uuid.UUID):
            raise ValueError("Image ID must be a UUID.")
        self.id = id

    def __eq__(self, other):
        if not isinstance(other, ImageId):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def from_string(cls, id: str):
        return ImageId(id=uuid.UUID(id))
    
    def to_string(self):
        return str(self.id)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(id=uuid.UUID(data["id"]))  # Convert str to UUID

    def to_dict(self):
        return {"id": str(self.id)}

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"ImageId(id={self.id})"
