from .base_value_object import ValueObject


class ImageUrl(ValueObject):
    """
    Represents the URL of an image.
    """

    def __init__(self, url: str):
        if not isinstance(url, str):
            raise ValueError("Image URL must be a string.")
        if not url:
            raise ValueError("Image URL cannot be empty.")
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, ImageUrl):
            return False
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)
    
    @classmethod
    def from_string(cls, url: str):
        return ImageUrl(url=url)
    
    def to_string(self):
        return self.url
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(url=data["url"])
    
    def to_dict(self):
        return {"url": self.url}

    def __str__(self):
        return self.url

    def __repr__(self):
        return f"ImageUrl(url={self.url})"