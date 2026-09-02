from functools import cached_property
from typing import Generator, Self, Iterator

import numpy as np

from vibra.engine import AnalysisID

from .common_solution import CommonSolution


class ModalSolution(CommonSolution):
    def __init__(
        self,
        analysis_id: AnalysisID,
        natural_frequencies: np.ndarray,
        structural_modal_shapes: np.ndarray | None = None,
        acoustic_modal_shapes: np.ndarray | None = None,
        coupled_modal_shapes: np.ndarray | None = None,
        complex_natural_frequencies: np.ndarray | None = None,
        displacement_dof: np.ndarray | None = None,
    ):
        if all(i is None for i in [structural_modal_shapes, acoustic_modal_shapes, coupled_modal_shapes]):
            raise ValueError("Either structural_modal_shapes, acoustic_modal_shapes, or coupled_modal_shapes must be provided")

        self.analysis_id = analysis_id
        self.natural_frequencies = self._immutable_array(natural_frequencies)
        
        self.structural_modal_shapes: np.ndarray | None = self._optional_immutable_array(structural_modal_shapes)
        self.acoustic_modal_shapes: np.ndarray | None = self._optional_immutable_array(acoustic_modal_shapes)
        self.coupled_modal_shapes: np.ndarray | None = self._optional_immutable_array(coupled_modal_shapes)

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
    def nodal_displacements(self) -> np.ndarray:
        _nodal_displacements = self.modal_shapes[self.displacement_dof, :]
        return self._immutable_array(_nodal_displacements)

    def get_nodal_displacement_at_column(self, column_index: int) -> np.ndarray:
        return self.modal_shapes[self.displacement_dof, column_index].copy()

    def get_row(self, row_index: int) -> np.ndarray:
        return self.modal_shapes[row_index, :]

    def get_column(self, column_index: int) -> np.ndarray:
        return self.modal_shapes[:, column_index]

    def __iter__(self) -> Iterator[tuple[float | complex, np.ndarray]]:
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
