from functools import cached_property

from .common_solution import Array1D, Array2D, CommonModalSolution


class StructuralModalSolution(CommonModalSolution):
    def __init__(
        self,
        natural_frequencies: Array1D,
        modal_shape: Array2D,
        displacement_dof: Array2D,
    ):
        self.displacement_dof: Array2D = self._immutable_array(displacement_dof)
        super().__init__(natural_frequencies, modal_shape)

    @cached_property
    def results_reordered(self) -> Array2D:
        reordered = self.modal_shape[self.displacement_dof, :]
        return self._immutable_array(reordered)

    def get_row(self, row_index: int) -> Array1D:
        return self.results_reordered[row_index, :]

    def get_column(self, column_index: int) -> Array1D:
        return self.results_reordered[:, column_index]
