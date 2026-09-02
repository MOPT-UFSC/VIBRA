from copy import deepcopy
from functools import cached_property
from typing import Generator, Self

import numpy as np

from vibra.engine import AnalysisID
from vibra.utils.lazy_array import LazyArray

from .common_solution import CommonSolution


class HarmonicSolution(CommonSolution):
    def __init__(
        self,
        analysis_id: AnalysisID,
        frequencies: np.ndarray,
        structural_solution: np.ndarray | None = None,
        acoustic_solution: np.ndarray | None = None,
        coupled_solution: np.ndarray | None = None,
        status: np.ndarray | None = None,
        displacement_dof: np.ndarray | None = None,
    ):
        if all(i is None for i in [structural_solution, acoustic_solution, coupled_solution]):
            raise ValueError("Either structural_solution, acoustic_solution, or coupled_solution must be provided")

        self.analysis_id = analysis_id
        self.frequencies = self._immutable_array(frequencies)
        self.status = self._create_status(status)

        self.structural_solution: Array2D | None = self._optional_immutable_array(structural_solution)
        self.acoustic_solution: Array2D | None = self._optional_immutable_array(acoustic_solution)
        self.coupled_solution: Array2D | None = self._optional_immutable_array(coupled_solution)

        self.displacement_dof: Array2D | None = self._optional_immutable_array(displacement_dof)
        super().__init__()

    @cached_property
    def iscomplex(self) -> bool:
        if np.iscomplex(self.frequencies):
            return True

        if (self.structural_solution is not None) and np.iscomplex(self.structural_solution):
            return True

        if (self.acoustic_solution is not None) and np.iscomplex(self.acoustic_solution):
            return True

        if (self.coupled_solution is not None) and np.iscomplex(self.coupled_solution):
            return True

        return False

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

    def get_nodal_displacement_at_column(self, column_index: int) -> np.ndarray:
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

    def __iter__(self) -> Generator[tuple[float | complex, np.ndarray], None, None]:
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
