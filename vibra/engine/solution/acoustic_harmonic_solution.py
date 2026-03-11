from typing import Self

import numpy as np

from vibra.engine.analysis_info import AnalysisID

from .common_solution import CommonHarmonicSolution


# a lot more stuff will be implemented soon
class AcousticHarmonicSolution(CommonHarmonicSolution):
    analysis_id = AnalysisID.ACOUSTIC_HARMONIC

    def __eq__(self, other: Self) -> bool:
        return all(
            [
                isinstance(other, AcousticHarmonicSolution),
                super().__eq__(other),
            ]
        )
