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
        modal_shape: Array2D,
        complex_natural_frequencies: Optional[Array1D] = None,
        displacement_dof: Optional[Array2D] = None,
    ):
        self.analysis_id = analysis_id
        self.natural_frequencies = self._immutable_array(natural_frequencies)
        self.modal_shape = self._immutable_array(modal_shape)
        self.complex_natural_frequencies = self._optional_immutable_array(complex_natural_frequencies)
        self.displacement_dof = self._optional_immutable_array(displacement_dof)
        super().__init__()

    @cached_property
    def iscomplex(self):
        return np.iscomplex(self.natural_frequencies) or np.iscomplex(self.modal_shape)

    @cached_property
    def number_of_modes(self):
        return len(self.natural_frequencies)

    @cached_property
    def results_reordered(self) -> Array2D:
        reordered = self.modal_shape[self.displacement_dof, :]
        return self._immutable_array(reordered)

    def get_row(self, row_index: int) -> Array1D:
        return self.modal_shape[row_index, :]

    def get_column(self, column_index: int) -> Array1D:
        return self.modal_shape[:, column_index]

    def __iter__(self) -> Generator[tuple[float | complex, Array1D], None, None]:
        yield from zip(self.natural_frequencies, self.modal_shape)

    def __eq__(self, other: Self) -> bool:
        return all(
            [
                np.allclose(self.natural_frequencies, other.natural_frequencies),
                np.allclose(self.modal_shape, other.modal_shape),
                np.allclose(self.complex_natural_frequencies, other.complex_natural_frequencies),
            ]
        )
