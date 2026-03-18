from abc import ABC, abstractmethod
from dataclasses import replace
from enum import StrEnum, auto
from typing import Callable, ParamSpec, Self, TypeVar

import numpy as np

P = ParamSpec("P")
T = TypeVar("T")


class FrequencySpacing(StrEnum):
    USER_DEFINED = "user-defined"
    EQUALLY_DISTRIBUTED = "equally distributed"


class AnalysisMethod(StrEnum):
    DIRECT = auto()
    MODE_SUPERPOSITION = auto()


class HarmonicAnalysisSetup(ABC):
    f_min: float
    f_max: float
    f_size: float
    analysis_method: AnalysisMethod = AnalysisMethod.DIRECT
    global_damping: tuple[float, float, float] = (0.0, 0.0, 0.0)
    modes_number: None | int = None

    def replace(self, **changes) -> Self:
        return replace(self, **changes)

    def convert_to(self, cls: Callable[P, T], **kwargs: P.kwargs) -> T:
        # TODO: this type hints are not working very well, fix them manually
        if not isinstance(cls, HarmonicAnalysisSetup):
            raise ValueError('You can only convert to another subclass of "HarmonicAnalysisSetup"')

        kwargs.setdefault("analysis_method", self.analysis_method)
        kwargs.setdefault("global_damping", self.global_damping)
        kwargs.setdefault("modes_number", self.modes_number)
        return cls(**kwargs)

    def __iter__(self):
        yield from self.frequencies()

    def __len__(self):
        return self.f_size

    @abstractmethod
    def frequencies(self) -> np.ndarray: ...

    @abstractmethod
    def as_dict(self) -> dict: ...
