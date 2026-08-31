from collections.abc import Generator
from copy import deepcopy
from functools import cached_property
from typing import Self

import numpy as np

from vibra.engine.analysis_info import AnalysisSetup
from vibra.utils.lazy_array import LazyArray

from .common_solution import Array1D, Array2D, CommonSolution


class HarmonicSolution(CommonSolution):
    def __init__(
        self,
        analysis_setup: AnalysisSetup,
        frequencies: Array1D,
        nodal_solution: Array2D,
        status: np.ndarray[tuple[int], bool] | None = None,
        displacement_dof: Array2D | None = None,
    ):
        self.analysis_setup = deepcopy(analysis_setup)
        self.frequencies = self._immutable_array(frequencies)
        self.nodal_solution: Array2D = self._immutable_array(nodal_solution)  # pyright: ignore[reportAttributeAccessIssue]
        self.status = self._create_status(status)
        self.displacement_dof: Array2D | None = self._optional_immutable_array(displacement_dof)  # pyright: ignore[reportAttributeAccessIssue]
        super().__init__()

    @cached_property
    def iscomplex(self):
        return np.iscomplex(self.frequencies) or np.iscomplex(self.nodal_solution)

    @cached_property
    def number_of_frequencies(self):
        return len(self.number_of_frequencies)

    @cached_property
    def has_partial_solutions(self):
        return not all(self.status)

    @cached_property
    def nodal_displacements(self) -> Array2D:
        _nodal_displacements = self.nodal_solution[self.displacement_dof, :]
        return self._immutable_array(_nodal_displacements)

    def get_nodal_displacement_at_column(self, column_index: int) -> Array1D:
        return self.nodal_solution[self.displacement_dof, column_index].copy()

    def copy(self):
        return deepcopy(self)

    def get_row(self, row_index: int) -> Array1D:
        return self.nodal_solution[row_index, :]

    def get_column(self, column_index: int) -> Array1D:
        return self.nodal_solution[:, column_index]

    def _create_status(self, status: np.ndarray[tuple[int], bool] | None):
        if status is None:
            return np.ones_like(self.frequencies, dtype=bool)
        return self._immutable_array(status)

    def __iter__(self) -> Generator[tuple[float | complex, Array1D]]:
        yield from zip(self.frequencies, self.nodal_solution)

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, HarmonicSolution):
            return False

        match self.displacement_dof, other.displacement_dof:
            case np.ndarray() | LazyArray(), np.ndarray() | LazyArray():
                dofs_equal = np.allclose(self.displacement_dof, other.displacement_dof)
            case None, None:
                dofs_equal = True
            case _, _:
                dofs_equal = False

        return all(
            [
                dofs_equal,
                np.allclose(self.frequencies, other.frequencies),
                np.allclose(self.nodal_solution, other.nodal_solution),
                np.allclose(self.status, other.status),
            ]
        )
