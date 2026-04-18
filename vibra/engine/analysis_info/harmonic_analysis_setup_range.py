from dataclasses import KW_ONLY, dataclass
from typing import Optional

import numpy as np

from .harmonic_analysis_setup import AnalysisMethod, HarmonicAnalysisSetup


@dataclass
class HarmonicAnalysisSetupRange(HarmonicAnalysisSetup):
    f_min: float
    f_max: float
    f_step: float = 1
    _: KW_ONLY
    mask_frequencies: Optional[np.ndarray[tuple[int], bool]] = None
    analysis_method: AnalysisMethod = AnalysisMethod.DIRECT
    modes_number: int = 40
    sigma_factor: float = 0.01
    global_damping: tuple[float, float, float] = (0.0, 0.0, 0.0)

    @property
    def f_size(self):
        # TODO: Find an analytic expression to calculate this more efficiently
        return len(self.frequencies())

    def get_mask(self):
        if self.mask_frequencies is None:
            return np.ones(self.f_size, dtype=bool)
        return self.mask_frequencies

    def frequencies(self):
        frequencies = np.arange(
            self.f_min,
            self.f_max + self.f_step,
            self.f_step,
            dtype=float,
        )
        # TODO: This is unecessarily expensive, simplify it
        mask = frequencies <= self.f_max
        return frequencies[mask]

    def as_dict(self):
        data = {
            "frequency_spacing": "equally distributed",
            "f_min": self.f_min,
            "f_max": self.f_max,
            "f_step": self.f_step,
            "frequencies": self.frequencies(),
            "solution_steps_mask" : self.get_mask(),
            "global_damping": self.global_damping,
        }

        if self.modes_number is not None:
            data["modes_number"] = self.modes_number

        return data
