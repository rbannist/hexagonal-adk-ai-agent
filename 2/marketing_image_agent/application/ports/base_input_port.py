from abc import ABC
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseInputPort(ABC, Generic[T]):
    pass
