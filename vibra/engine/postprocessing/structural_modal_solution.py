from dataclasses import dataclass
from functools import cached_property

import numpy as np


@dataclass(frozen=True)
class StructuralModalSolution:
    natural_frequencies: np.ndarray[
        tuple[int, int],
        float | complex,
    ]
    modal_shape: np.ndarray[
        tuple[int, int],
        float | complex,
    ]
    displacement_dof: np.ndarray[
        tuple[int, int],
        float | complex,
    ]

    def __post_init__(self):
        # Copy the arrays and make them immutable
        self.natural_frequencies = self.natural_frequencies.copy()
        self.natural_frequencies.setflags(write=False)

        self.modal_shape = self.modal_shape.copy()
        self.modal_shape.setflags(write=False)

        self.displacement_dof = self.displacement_dof.copy()
        self.displacement_dof.setflags(write=False)

    @cached_property
    def iscomplex(self):
        return any(
            [
                np.iscomplex(self.natural_frequencies),
                np.iscomplex(self.modal_shape),
                np.iscomplex(self.displacement_dof),
            ]
        )

    @cached_property
    def number_of_modes(self):
        return len(self.natural_frequencies)
