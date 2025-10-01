from .base_value_object import ValueObject


class Checksum(ValueObject):
    """
    Represents the checksum of an image file.
    """

    def __init__(self, checksum: str):
        if not isinstance(checksum, str):
            raise ValueError("Checksum must be a string.")
        if not checksum:
            raise ValueError("Checksum cannot be empty.")
        self.checksum = checksum

    def __eq__(self, other):
        if not isinstance(other, Checksum):
            return False
        return self.checksum == other.checksum

    def __hash__(self):
        return hash(self.checksum)
    
    @classmethod
    def from_string(cls, checksum: str):
        return cls(checksum=checksum)
    
    def to_string(self) -> str:
        return self.checksum

    @classmethod
    def from_dict(cls, data: dict):
        return cls(checksum=data["checksum"])
    
    def to_dict(self) -> dict:
        return {"checksum": self.checksum}

    def __str__(self):
        return self.checksum

    def __repr__(self):
        return f"Checksum(checksum={self.checksum})"
