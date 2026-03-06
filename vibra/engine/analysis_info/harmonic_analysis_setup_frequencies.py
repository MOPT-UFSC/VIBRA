from dataclasses import KW_ONLY, dataclass
from typing import Literal, Optional

import numpy as np

from .harmonic_analysis_setup import HarmonicAnalysisSetup


@dataclass
class HarmonicAnalysisSetupFrequencies(HarmonicAnalysisSetup):
    all_frequencies: np.ndarray[tuple[int], float]
    mask_frequencies: Optional[np.ndarray[tuple[int], bool]] = None
    _: KW_ONLY
    analysis_method: Literal["direct", "mode_superposition"] = "direct"
    global_damping: tuple[float, float, float] = (0.0, 0.0, 0.0)
    modes_number: None | int = None

    def __post_init__(self):
        # cast everything to arrays and fill with ones if needed
        self.all_frequencies = np.array(self.all_frequencies)
        if self.mask_frequencies is not None:
            self.mask_frequencies = np.array(self.mask_frequencies, dtype=bool)
            assert self.all_frequencies.shape == self.mask_frequencies.shape
        assert self.all_frequencies.size > 0

    def get_mask(self):
        if self.mask_frequencies is None:
            return np.ones(self.f_size, dtype=bool)
        return self.mask_frequencies

    def frequencies(self):
        if self.mask_frequencies is None:
            return self.all_frequencies.copy()
        return self.all_frequencies[self.mask_frequencies].copy()

    @property
    def f_min(self):
        if self.mask_frequencies is None:
            return self.all_frequencies[0]
        return self.frequencies()[0]

    @property
    def f_max(self):
        if self.mask_frequencies is None:
            return self.all_frequencies[-1]
        return self.frequencies()[-1]

    @property
    def f_size(self):
        if self.mask_frequencies is None:
            return len(self.all_frequencies)
        return sum(self.mask_frequencies)

    def as_dict(self):
        data = {
            "frequency_spacing": "user-defined",
            "f_min": self.f_min,
            "f_max": self.f_max,
            "f_step": self.all_frequencies[1] - self.all_frequencies[0],
            "frequencies": self.all_frequencies,
            "solution_steps_mask": self.get_mask(),
        }

        if self.global_damping is not None:
            data["global_damping"] = self.global_damping

        if self.modes_number is not None:
            data["modes_number"] = self.global_damping

        return data
