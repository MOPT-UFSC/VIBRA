from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)
