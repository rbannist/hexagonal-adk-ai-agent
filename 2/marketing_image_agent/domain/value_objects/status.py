from enum import Enum
from .base_value_object import ValueObject


class StatusEnum(str, Enum):
    """
    Enumerates the possible states of an image in the workflow.
    """
    GENERATED = "GENERATED"
    REVIEWING = "REVIEWING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    REMOVED = "REMOVED"


class Status(ValueObject):
    """
    Represents the status of an image in the marketing image creation workflow.
    """

    def __init__(self, status: StatusEnum):
        if not isinstance(status, StatusEnum):
            raise ValueError("Status must be an StatusEnum.")
        self.status = status

    def __eq__(self, other):
        if not isinstance(other, Status):
            return False
        return self.status == other.status

    def __hash__(self):
        return hash(self.status)

    @classmethod
    def from_string(cls, status: str):
        try:
            status_enum = StatusEnum(status)
            return cls(status=status_enum)
        except ValueError:
            raise ValueError(f"Invalid status: {status}. "
                             f"Must be one of {', '.join(StatusEnum)}")

    def to_string(self):
        return self.status.value

    @classmethod
    def from_dict(cls, data: dict):
        try:
            status_enum = StatusEnum(data["status"])
            return cls(status=status_enum)
        except (KeyError, ValueError):
            raise ValueError(
                "Invalid data for Status. "
                "Expected a dictionary with a 'status' key "
                f"containing one of {', '.join(StatusEnum)}."
            )

    def to_dict(self):
        return {"status": self.status.value}

    def __str__(self):
        return self.status.value

    def __repr__(self):
        return f"Status(status={self.status.value})"

    def can_transition_to(self, new_status: StatusEnum) -> bool:
        """
        Checks if a transition to the new status is allowed based on a simple state machine.
        """
        if not isinstance(new_status, StatusEnum):
            raise ValueError("New status must be an StatusEnum.")

        if self.status == StatusEnum.GENERATED:
            return new_status in (StatusEnum.REVIEWING, StatusEnum.REMOVED)
        elif self.status == StatusEnum.REVIEWING:
            return new_status in (StatusEnum.ACCEPTED, StatusEnum.REJECTED, StatusEnum.REMOVED)
        elif self.status == StatusEnum.ACCEPTED:
            return new_status == StatusEnum.REMOVED
        elif self.status == StatusEnum.REJECTED:
            return new_status in (StatusEnum.GENERATED, StatusEnum.REMOVED)
        elif self.status == StatusEnum.REMOVED:
            return False  # Once removed, it cannot transition to any other state
        else:
            return False