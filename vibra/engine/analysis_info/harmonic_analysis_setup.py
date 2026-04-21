from dataclasses import KW_ONLY, dataclass, field, fields
from functools import wraps
from typing import List, Optional

import numpy as np

from vibra.engine.analysis_info import AnalysisID, AnalysisMethod, FrequencySpacing


def ignore_extra_kwargs(cls):
    original_init = cls.__init__

    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        
        # expected fields of original dataclass
        expected_fields = {f.name for f in fields(cls)}

        # filter the unnecessary kwargs
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in expected_fields}

        original_init(self, *args, **filtered_kwargs)

    cls.__init__ = new_init
    return cls


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
            "frequency_spacing": self.frequency_spacing,
            "frequencies": self.get_frequencies(),
            "solution_steps_mask" : self.get_mask(),
            "global_damping": self.global_damping,
        }

        if self.frequency_spacing == FrequencySpacing.EQUALLY_DISTRIBUTED:
            data.update({
                "f_min": self.f_min,
                "f_max": self.f_max,
                "f_step": self.f_step,
                })

        if self.modes_number is not None:
            data["modes_number"] = self.modes_number

        return data