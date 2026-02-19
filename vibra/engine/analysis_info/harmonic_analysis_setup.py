from dataclasses import dataclass, replace
from typing import Literal

import numpy as np


@dataclass
class HarmonicAnalysisSetup:
    f_min: int | float
    f_max: int | float
    f_step: int | float
    analysis_method: Literal["direct", "mode_superposition"] = "direct"
    global_damping: None | tuple[float, ...] = None
    modes_number: None | int = None

    @property
    def frequencies(self):
        return np.arange(
            self.f_min,
            self.f_max + self.f_step,
            self.f_step,
        )

    def replace(self, **changes):
        return replace(self, **changes)

    def as_dict(self):
        data = {
            "f_min": self.f_min,
            "f_max": self.f_max,
            "f_step": self.f_step,
            "frequencies": self.frequencies,
        }

        if self.global_damping is not None:
            data["global_damping"] = self.global_damping

        if self.modes_number is not None:
            data["modes_number"] = self.global_damping

        return data
