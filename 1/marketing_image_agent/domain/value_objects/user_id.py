import uuid

from .base_value_object import ValueObject


class UserId(ValueObject):
    """
    Represents the unique identifier for a user.
    """

    def __init__(self, user_id: uuid.UUID):
        if not isinstance(user_id, uuid.UUID):
            raise ValueError("User ID must be a UUID.")
        self.user_id = user_id

    def __eq__(self, other):
        if not isinstance(other, UserId):
            return False
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)

    @classmethod
    def from_string(cls, user_id: str):
        return UserId(user_id=uuid.UUID(user_id))
    
    def to_string(self):
        return str(self.user_id)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(user_id=uuid.UUID(data["user_id"]))  # Convert str to UUID
    
    def to_dict(self):
        return {"user_id": str(self.user_id)}

    def __str__(self):
        return str(self.user_id)

    def __repr__(self):
        return f"UserId(user_id={self.user_id})"


class CreatedBy(UserId):
    """
    Represents the user who created an entity.
    """
    pass
