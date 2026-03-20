from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Self

from enum import StrEnum, auto


class GroupLabel(StrEnum):
    STRUCTURAL = auto()
    ACOUSTIC = auto()


@dataclass()
class Property(ABC):
    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @abstractmethod
    def get_group_label(self) -> GroupLabel: ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self: ...
