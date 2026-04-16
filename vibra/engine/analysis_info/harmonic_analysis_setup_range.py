from dataclasses import KW_ONLY, dataclass

import numpy as np

from .harmonic_analysis_setup import AnalysisMethod, HarmonicAnalysisSetup


@dataclass
class HarmonicAnalysisSetupRange(HarmonicAnalysisSetup):
    f_min: float
    f_max: float
    f_step: float = 1
    _: KW_ONLY
    analysis_method: AnalysisMethod = AnalysisMethod.DIRECT
    global_damping: tuple[float, float, float] = (0.0, 0.0, 0.0)
    modes_number: int = 40
    sigma_factor: float = 0.01

    @property
    def f_size(self):
        from math import ceil

        return ceil((self.f_max + self.f_step - self.f_min) / self.f_step)

    def frequencies(self):
        return np.arange(
            self.f_min,
            self.f_max + self.f_step,
            self.f_step,
            dtype=float,
        )

    def as_dict(self):
        data = {
            "frequency_spacing": "equally distributed",
            "f_min": self.f_min,
            "f_max": self.f_max,
            "f_step": self.f_step,
            "frequencies": self.frequencies(),
            "solution_steps_mask": np.ones(self.f_size, dtype=bool),
            "global_damping": self.global_damping,
        }

        if self.modes_number is not None:
            data["modes_number"] = self.modes_number

        return data
