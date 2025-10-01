from .base_value_object import ValueObject


class MimeType(ValueObject):
    """
    Represents the MIME type of an image (e.g., "image/jpeg", "image/png").
    """

    def __init__(self, mime_type: str):
        if not isinstance(mime_type, str):
            raise ValueError("MIME type must be a string.")
        if not mime_type:
            raise ValueError("MIME type cannot be empty.")
        self.mime_type = mime_type

    def __eq__(self, other):
        if not isinstance(other, MimeType):
            return False
        return self.mime_type == other.mime_type

    def __hash__(self):
        return hash(self.mime_type)

    @classmethod
    def from_string(cls, mime_type: str):
        return MimeType(mime_type=mime_type)
    
    def to_string(self):
        return self.mime_type
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(mime_type=data["mime_type"])
    
    def to_dict(self):
        return {"mime_type": self.mime_type}

    def __str__(self):
        return self.mime_type

    def __repr__(self):
        return f"MimeType(mime_type={self.mime_type})"
