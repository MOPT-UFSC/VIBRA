from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Self


@dataclass()
class Property(ABC):
    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self: ...
