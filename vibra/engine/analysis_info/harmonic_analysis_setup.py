from abc import ABC, abstractmethod
from dataclasses import field, replace
from typing import Callable, List, Optional, ParamSpec, Self, TypeVar

import numpy as np

from .analysis_enums import AnalysisMethod
from vibra.engine.analysis_info import AnalysisID

P = ParamSpec("P")
T = TypeVar("T")


class HarmonicAnalysisSetup(ABC):
    analysis_id: int = AnalysisID.NO_ANALYSIS
    frequency_spacing: str = "user-defined"
    analysis_method: AnalysisMethod = AnalysisMethod.DIRECT
    f_min: float | None = None
    f_max: float | None = None
    f_size: float | None = None
    frequencies: Optional[np.ndarray[tuple[int], float]] = None
    solution_steps_mask: List[bool] = field(default_factory=list)
    global_damping: tuple[float, float, float] = (0.0, 0.0, 0.0)
    modes_number: int = 40
    sigma_factor: float = 0.01
    # mask_frequencies: np.ndarray[tuple[int], bool] | None

    def replace(self, **changes) -> Self:
        return replace(self, **changes)

    def convert_to(self, cls: Callable[P, T], **kwargs: P.kwargs) -> T:
        # TODO: this type hints are not working very well, fix them manually
        if not issubclass(cls, HarmonicAnalysisSetup):
            raise ValueError('You can only convert to another subclass of "HarmonicAnalysisSetup"')

        kwargs.setdefault("analysis_method", self.analysis_method)
        kwargs.setdefault("global_damping", self.global_damping)
        kwargs.setdefault("modes_number", self.modes_number)
        kwargs.setdefault("sigma_factor", self.sigma_factor)
        return cls(**kwargs)

    def __iter__(self):
        yield from self.frequencies()

    def __len__(self):
        return self.f_size

    @abstractmethod
    def get_frequencies(self) -> np.ndarray: ...

    @abstractmethod
    def as_dict(self) -> dict: ...
