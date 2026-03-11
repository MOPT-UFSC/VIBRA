from functools import cached_property
from typing import Optional, Self

import numpy as np

from vibra.engine.analysis_info import AnalysisID

from .common_solution import Array1D, Array2D, CommonHarmonicSolution


class StructuralHarmonicSolution(CommonHarmonicSolution):
    analysis_id = AnalysisID.ACOUSTIC_HARMONIC

    def __init__(
        self,
        frequencies: Array1D,
        results: Array2D,
        displacement_dof: Array2D,
        status: Optional[np.ndarray[tuple[int], bool]] = None,
    ):
        self.displacement_dof: Array2D = self._immutable_array(displacement_dof)
        super().__init__(frequencies, results, status)

    @cached_property
    def results_reordered(self) -> Array2D:
        reordered = self.modal_shape[self.displacement_dof, :]
        return self._immutable_array(reordered)

    def get_row(self, row_index: int) -> Array1D:
        return self.results_reordered[row_index, :]

    def get_column(self, column_index: int) -> Array1D:
        return self.results_reordered[:, column_index]

    def __eq__(self, other: Self) -> bool:
        return all(
            [
                isinstance(other, StructuralHarmonicSolution),
                super().__eq__(other),
                np.allclose(self.displacement_dof, other.displacement_dof),
            ]
        )
