from dataclasses import KW_ONLY, dataclass, field, fields
from typing import List, Optional

import numpy as np

from vibra.engine.analysis_info import AnalysisID, AnalysisMethod, FrequencySpacing
from vibra.utils.dataclass_utils import ignore_extra_kwargs


@ignore_extra_kwargs
@dataclass
class HarmonicAnalysisSetup:
    _: KW_ONLY
    analysis_id: int = AnalysisID.NO_ANALYSIS
    frequency_spacing: str = FrequencySpacing.USER_DEFINED
    f_min: float | None = None
    f_max: float | None = None
    f_step: float | None = None
    frequencies: Optional[np.ndarray[tuple[int], float]] = None
    solution_steps_mask: List[bool] = field(default_factory=list)
    analysis_method: AnalysisMethod = AnalysisMethod.DIRECT
    modes_number: int = 40
    sigma_factor: float = 0.01
    global_damping: tuple[float, float, float] = (0.0, 0.0, 0.0)

    @property
    def f_size(self):
        # TODO: Find an analytic expression to calculate this more efficiently
        return len(self.get_frequencies())

    def get_mask(self):
        if self.solution_steps_mask:
            return np.array(self.solution_steps_mask, dtype=bool)
        return np.ones(self.f_size, dtype=bool)

    def get_frequencies(self):
        if self.frequency_spacing == FrequencySpacing.USER_DEFINED:
            return self.frequencies

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
            "analysis_method": self.analysis_method,
            "frequency_spacing": self.frequency_spacing,
            "frequencies": self.get_frequencies(),
            "solution_steps_mask": self.get_mask(),
            "global_damping": self.global_damping,
        }

        if self.frequency_spacing == FrequencySpacing.EQUALLY_DISTRIBUTED:
            data.update(
                {
                    "f_min": self.f_min,
                    "f_max": self.f_max,
                    "f_step": self.f_step,
                }
            )

        if self.analysis_method == AnalysisMethod.MODE_SUPERPOSITION:
            data.update(
                {
                    "modes_number": self.modes_number,
                    "sigma_factor": self.sigma_factor,
                }
            )

        return data
