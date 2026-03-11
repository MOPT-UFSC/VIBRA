from functools import cached_property
from typing import Optional

from vibra.engine.analysis_info import AnalysisID

from .common_solution import Array1D, Array2D, CommonModalSolution


class StructuralModalSolution(CommonModalSolution):
    analysis_id = AnalysisID.STRUCTURAL_MODAL

    def __init__(
        self,
        natural_frequencies: Array1D,
        modal_shape: Array2D,
        displacement_dof: Array2D,
        complex_natural_frequencies: Optional[Array1D] = None,
    ):
        self.displacement_dof: Array2D = self._immutable_array(displacement_dof)
        super().__init__(
            natural_frequencies,
            modal_shape,
            complex_natural_frequencies=complex_natural_frequencies,
        )

    @cached_property
    def results_reordered(self) -> Array2D:
        reordered = self.modal_shape[self.displacement_dof, :]
        return self._immutable_array(reordered)

    def get_row(self, row_index: int) -> Array1D:
        return self.results_reordered[row_index, :]

    def get_column(self, column_index: int) -> Array1D:
        return self.results_reordered[:, column_index]
