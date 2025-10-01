from typing import List
from .base_value_object import ValueObject


class ImageKeywords(ValueObject):
    """
    Represents the keywords associated with an image.
    """

    def __init__(self, keywords: List[str]):
        if not isinstance(keywords, list) or not all(
            isinstance(keyword, str) for keyword in keywords
        ):
            raise ValueError("Image keywords must be a list of strings.")
        self.keywords = keywords

    def __eq__(self, other):
        if not isinstance(other, ImageKeywords):
            return False
        return self.keywords == other.keywords

    def __hash__(self):
        return hash(tuple(self.keywords))
    
    @classmethod
    def from_string(cls, keywords: str):
        return cls(keywords=keywords.split(","))
    
    def to_string(self):
        return ", ".join(self.keywords)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(keywords=data["keywords"]) # List
    
    def to_dict(self):
        return {"keywords": self.keywords}

    def __str__(self):
        return ", ".join(self.keywords)

    def __repr__(self):
        return f"ImageKeywords(keywords={self.keywords})"
