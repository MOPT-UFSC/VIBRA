from abc import abstractmethod
from dataclasses import replace
from typing import Literal, Self

import numpy as np


class HarmonicAnalysisSetup:
    analysis_method: Literal["direct", "mode_superposition"] = "direct"
    global_damping: tuple[float, float, float] = (0.0, 0.0, 0.0)
    modes_number: None | int = None

    def __init__(self, *args, **kwargs):
        subclass_names = ", ".join([f"{cls.__module__}.{cls.__name__}" for cls in self.__class__.__subclasses__()])
        msg = "HarmonicAnalysisSetup can not be intantiated.\n"
        msg += f"Use one of the following classes instead: {subclass_names}"
        raise ValueError(msg)

    def replace(self, **changes) -> Self:
        return replace(self, **changes)

    @abstractmethod
    def frequencies(self) -> np.ndarray: ...

    @abstractmethod
    def as_dict(self) -> dict: ...
