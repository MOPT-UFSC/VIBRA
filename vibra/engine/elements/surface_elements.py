from dataclasses import dataclass

import numpy as np


class Element2D:
    """
    This determines the attributes and methods
    that need to exist in EVERY element.
    """

    # Constants of the element
    NODES_PER_ELEMENT: int = 0
    DOF_PER_NODE: int = 0
    DOF_PER_ELEMENT: int = NODES_PER_ELEMENT * DOF_PER_NODE

    def elementary_matrices(self) -> tuple[np.ndarray]:
        raise NotImplementedError("The function elementary_matrices was not implemented")


    def get_detJAC(self, JAC: np.ndarray) -> float:
        """
        This function computes the determinant of the Jacobian
        matrix in both stacked and non-stacked matrices form.

        Parameter
        ---------
        JAC: np.ndarray
            The Jacobian 2D or 3D matrix.
        
        Return
        ------
        det_jac: float
            The determinant of the Jacobian matrix.
        """
        if len(JAC.shape) == 3:
            det_jac = JAC[:, 0, 0] * JAC[:, 1, 1]  - JAC[:, 0, 1] * JAC[:, 1, 0]
            return det_jac.reshape(-1, 1, 1)

        else:
            det_jac = JAC[0, 0] * JAC[1, 1]  - JAC[0, 1] * JAC[1, 0]  
            return det_jac


    def get_detJAC_and_invJAC(self, JAC: np.ndarray) -> np.ndarray:
        """
        This function computes the determinants and inverses
        of Jacobian matrices in stacked form.

        Parameters
        ----------
        JAC: np.array
            The stacked Jacobian matrices.

        Returns
        -------
        det_jacs: np.ndarray
            The stacked determinants of Jacobian matrices.

        inv_jacs: np.ndarray
            The stacked inverse of Jacobian matrices.

        """

        # determinant of the Jacobian matrix
        det_jacs = JAC[:, 0, 0] * JAC[:, 1, 1]  - JAC[:, 0, 1] * JAC[:, 1, 0] 
        det_jacs = det_jacs.reshape(-1, 1, 1)

        # the adjoint matrix AUJJ
        AUJJ = np.zeros((JAC.shape[0], 2, 2), dtype=float)

        AUJJ[:, 0, 0] =  JAC[:, 1, 1]
        AUJJ[:, 0, 1] = -JAC[:, 0, 1]
        AUJJ[:, 1, 0] = -JAC[:, 1, 0]
        AUJJ[:, 1, 1] =  JAC[:, 0, 0]

        # inverse of the Jacobian matrix
        inv_jacs = (1 / det_jacs) * AUJJ

        return det_jacs, inv_jacs