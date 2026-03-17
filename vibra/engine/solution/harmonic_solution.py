from functools import cached_property
from typing import Generator, Optional, Self

import numpy as np

from vibra.engine import AnalysisID

from .common_solution import Array1D, Array2D, CommonSolution


class HarmonicSolution(CommonSolution):
    def __init__(
        self,
        analysis_id: AnalysisID,
        frequencies: Array1D,
        results: Array2D,
        status: Optional[np.ndarray[tuple[int], bool]] = None,
        displacement_dof: Optional[Array2D] = None,
    ):
        self.analysis_id = analysis_id
        self.frequencies = self._immutable_array(frequencies)
        self.results = self._immutable_array(results)
        self.status = self._create_status(status)
        self.displacement_dof: Array2D = self._optional_immutable_array(displacement_dof)
        super().__init__()

    @cached_property
    def iscomplex(self):
        return np.iscomplex(self.frequencies) or np.iscomplex(self.results)

    @cached_property
    def number_of_frequencies(self):
        return len(self.number_of_frequencies)

    @cached_property
    def has_partial_solutions(self):
        return not all(self.status)

    @cached_property
    def results_reordered(self) -> Array2D:
        reordered = self.modal_shape[self.displacement_dof, :]
        return self._immutable_array(reordered)

    def get_row(self, row_index: int) -> Array1D:
        return self.results[row_index, :]

    def get_column(self, column_index: int) -> Array1D:
        return self.results[:, column_index]

    def _create_status(self, status: Optional[np.ndarray[tuple[int], bool]]):
        if status is None:
            return np.ones_like(self.frequencies, dtype=bool)
        return self._immutable_array(status)

    def __iter__(self) -> Generator[tuple[float | complex, Array1D], None, None]:
        yield from zip(self.frequencies, self.results)

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, HarmonicSolution):
            return False

        match self.displacement_dof, other.displacement_dof:
            case None, None:
                pass

            case None, _:
                return False

            case _, None:
                return False

            case _, _:
                if not np.allclose(self.displacement_dof, other.displacement_dof):
                    return False

        return all(
            [
                np.allclose(self.frequencies, other.frequencies),
                np.allclose(self.results, other.results),
                np.allclose(self.status, other.status),
            ]
        )
