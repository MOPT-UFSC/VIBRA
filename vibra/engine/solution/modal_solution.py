from functools import cached_property
from typing import Generator, Iterator, Self, override

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
        if np.iscomplex(self.natural_frequencies).any():
            return True
        if self.structural_modal_shapes is not None and np.iscomplex(self.structural_modal_shapes).any():
            return True
        if self.acoustic_modal_shapes is not None and np.iscomplex(self.acoustic_modal_shapes).any():
            return True
        if self.coupled_modal_shapes is not None and np.iscomplex(self.coupled_modal_shapes).any():
            return True
        return False

    @cached_property
    def number_of_modes(self):
        return len(self.natural_frequencies)

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModalSolution):
            return False

        return all(
            [
                np.allclose(self.natural_frequencies, other.natural_frequencies),
                self._compare_optional_arrays(self.structural_modal_shapes, other.structural_modal_shapes),
                self._compare_optional_arrays(self.acoustic_modal_shapes, other.acoustic_modal_shapes),
                self._compare_optional_arrays(self.coupled_modal_shapes, other.coupled_modal_shapes),
                self._compare_optional_arrays(self.displacement_dof, other.displacement_dof),
            ]
        )
