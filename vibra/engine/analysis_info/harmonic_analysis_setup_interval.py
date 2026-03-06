from dataclasses import KW_ONLY, dataclass
from typing import Literal

import numpy as np

from .harmonic_analysis_setup import HarmonicAnalysisSetup


@dataclass
class HarmonicAnalysisSetupInterval(HarmonicAnalysisSetup):
    f_min: int | float
    f_max: int | float
    f_step: int | float = 1
    _: KW_ONLY
    analysis_method: Literal["direct", "mode_superposition"] = "direct"
    global_damping: None | tuple[float, ...] = None
    modes_number: None | int = None

    @property
    def f_size(self):
        from math import ceil

        return ceil((self.f_max + self.f_step - self.f_min) / self.f_step)

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
