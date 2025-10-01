from abc import ABC
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseOutputPort(ABC, Generic[T]):
    pass
