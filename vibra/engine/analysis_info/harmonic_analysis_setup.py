from dataclasses import KW_ONLY, dataclass, replace
from typing import Literal, Self

import numpy as np
from pyparsing import Optional


class HarmonicAnalysisSetup:
    analysis_method: Literal["direct", "mode_superposition"] = "direct"
    global_damping: tuple[float, float, float] = (0.0, 0.0, 0.0)
    modes_number: None | int = None

    def replace(self, **changes) -> Self:
        return replace(self, **changes)

    def frequencies(self) -> np.ndarray: ...

    def as_dict(self) -> dict: ...


@dataclass
class IntervalHarmonicAnalysisSetup(HarmonicAnalysisSetup):
    f_min: int | float
    f_max: int | float
    f_step: int | float
    _: KW_ONLY
    analysis_method: Literal["direct", "mode_superposition"] = "direct"
    global_damping: None | tuple[float, ...] = None
    modes_number: None | int = None

    def frequencies(self):
        return np.arange(
            self.f_min,
            self.f_max + self.f_step,
            self.f_step,
        )

    def as_dict(self):
        data = {
            "f_min": self.f_min,
            "f_max": self.f_max,
            "f_step": self.f_step,
            "frequencies": self.frequencies(),
        }

        if self.global_damping is not None:
            data["global_damping"] = self.global_damping

        if self.modes_number is not None:
            data["modes_number"] = self.global_damping

        return data


@dataclass
class FrequenciesHarmonicAnalysisSetup(HarmonicAnalysisSetup):
    all_frequencies: np.ndarray[tuple[int], float]
    mask_frequencies: Optional[np.ndarray[tuple[int], bool]] = None
    _: KW_ONLY
    analysis_method: Literal["direct", "mode_superposition"] = "direct"
    global_damping: None | tuple[float, ...] = None
    modes_number: None | int = None

    def __post_init__(self):
        # cast everything to arrays and fill with ones if needed
        self.all_frequencies = np.array(self.all_frequencies)
        if self.mask_frequencies is not None:
            self.mask_frequencies = np.array(self.mask_frequencies, dtype=bool)
            assert self.all_frequencies.shape == self.mask_frequencies.shape

    def frequencies(self):
        return self.all_frequencies[self.mask_frequencies]

    def as_dict(self):
        data = {
            "f_min": self.f_min,
            "f_max": self.f_max,
            "f_step": self.f_step,
            "frequencies": self.frequencies(),
        }

        if self.global_damping is not None:
            data["global_damping"] = self.global_damping

        if self.modes_number is not None:
            data["modes_number"] = self.global_damping

        return data
