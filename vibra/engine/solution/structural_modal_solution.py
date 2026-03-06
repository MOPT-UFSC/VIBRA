import numpy as np

from .common_solution import Array1D, Array2D, ModalSolution


class StructuralModalSolution(ModalSolution):
    def __init__(
        self,
        natural_frequencies: Array1D,
        modal_shape: Array2D,
        displacement_dof: Array2D,
    ):
        self.displacement_dof: Array2D = np.array(displacement_dof, copy=True)
        self.displacement_dof.setflags(write=False)
        super().__init__(natural_frequencies, modal_shape)
