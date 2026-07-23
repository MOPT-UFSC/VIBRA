from functools import cached_property
from typing import Generator, Optional, Self

import numpy as np

from vibra.engine import AnalysisID

from .common_solution import Array1D, Array2D, CommonSolution


class ModalSolution(CommonSolution):
    def __init__(
        self,
        analysis_id: AnalysisID,
        natural_frequencies: Array1D,
        modal_shapes: Array2D,
        complex_natural_frequencies: Optional[Array1D] = None,
        displacement_dof: Optional[Array2D] = None,
    ):
        self.analysis_id = analysis_id
        self.natural_frequencies = self._immutable_array(natural_frequencies)
        self.modal_shapes = self._immutable_array(modal_shapes)
        self.complex_natural_frequencies = self._optional_immutable_array(complex_natural_frequencies)
        self.displacement_dof = self._optional_immutable_array(displacement_dof)

        super().__init__()

    @cached_property
    def iscomplex(self):
        return np.iscomplex(self.natural_frequencies) or np.iscomplex(self.modal_shapes)

    @cached_property
    def number_of_modes(self):
        return len(self.natural_frequencies)

    @cached_property
    def nodal_displacements(self) -> Array2D:
        _nodal_displacements = self.modal_shapes[self.displacement_dof, :]
        return self._immutable_array(_nodal_displacements)

    def get_nodal_displacement_at_column(self, column_index: int) -> Array1D:
        return self.modal_shapes[self.displacement_dof, column_index].copy()

    def get_row(self, row_index: int) -> Array1D:
        return self.modal_shapes[row_index, :]

    def get_column(self, column_index: int) -> Array1D:
        return self.modal_shapes[:, column_index]

    def __iter__(self) -> Generator[tuple[float | complex, Array1D], None, None]:
        yield from zip(self.natural_frequencies, self.modal_shapes)

    def __eq__(self, other: Self) -> bool:
        match self.displacement_dof, other.displacement_dof:
            case np.ndarray(), np.ndarray() as a, b:
                cnf_equal = np.allclose(a, b)
            case None, None:
                cnf_equal = True
            case _, _:
                cnf_equal = False

        return all(
            [
                np.allclose(self.natural_frequencies, other.natural_frequencies),
                np.allclose(self.modal_shapes, other.modal_shapes),
                cnf_equal,
            ]
        )
