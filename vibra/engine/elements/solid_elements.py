
from vibra.engine.properties.material import Material

import numpy as np
from dataclasses import dataclass


class Element3D:
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
    

    def get_constitutive_model(self, material: Material, model_type="linear-isotropic"):
        """This methdo returns the material constitutive model."""

        rho = material.material_density
        vv = material.poisson_ratio
        E = material.elasticity_modulus

        if model_type == "linear-isotropic":
            # Constititive model - Linear isotropic material

            factor = E / ((1 + vv) * (1 - 2 * vv))
            nn = (1 - 2 * vv) / 2
            tt = 1 - vv

            const_law = np.array(
                [
                [tt, vv, vv,  0,  0,  0],
                [vv, tt, vv,  0,  0,  0],
                [vv, vv, tt,  0,  0,  0],
                [ 0,  0,  0, nn,  0,  0],
                [ 0,  0,  0,  0, nn,  0],
                [ 0,  0,  0,  0,  0, nn],
                ], 
                dtype=float)

            return factor * const_law, rho


    def get_detJAC_and_invJAC(self, JAC: np.ndarray):
        """
        This function computes the determinant and inverse
        of Jacobian matrix.

        Parameters
        ----------
        JAC: np.array
            The Jacobian matrices.

        Returns
        -------
        det_jac: np.ndarray
            The determinant of Jacobian matrix.

        inv_jac: np.ndarray
            The inverse of Jacobian matrix.
        """

        if len(JAC.shape) == 3:

            det_jac = (
                JAC[:, 0, 0] * JAC[:, 1, 1] * JAC[:, 2, 2]
                + JAC[:, 0, 1] * JAC[:, 1, 2] * JAC[:, 2, 0]
                + JAC[:, 0, 2] * JAC[:, 1, 0] * JAC[:, 2, 1]
            ) - (
                JAC[:, 2, 0] * JAC[:, 1, 1] * JAC[:, 0, 2]
                + JAC[:, 2, 1] * JAC[:, 1, 2] * JAC[:, 0, 0]
                + JAC[:, 2, 2] * JAC[:, 1, 0] * JAC[:, 0, 1]
            )
            det_jac = det_jac.reshape(-1, 1, 1)

            adj_matrix = np.zeros((det_jac.shape[0], 3, 3), dtype=float)
            adj_matrix[:, 0, 0] =  ((JAC[:, 1, 1] * JAC[:, 2, 2]) - (JAC[:, 2, 1] * JAC[:, 1, 2]))
            adj_matrix[:, 1, 0] = -((JAC[:, 1, 0] * JAC[:, 2, 2]) - (JAC[:, 1, 2] * JAC[:, 2, 0]))
            adj_matrix[:, 2, 0] =  ((JAC[:, 1, 0] * JAC[:, 2, 1]) - (JAC[:, 1, 1] * JAC[:, 2, 0]))
            adj_matrix[:, 0, 1] = -((JAC[:, 0, 1] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 1]))
            adj_matrix[:, 1, 1] =  ((JAC[:, 0, 0] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 0]))
            adj_matrix[:, 2, 1] = -((JAC[:, 0, 0] * JAC[:, 2, 1]) - (JAC[:, 0, 1] * JAC[:, 2, 0]))
            adj_matrix[:, 0, 2] =  ((JAC[:, 0, 1] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 1]))
            adj_matrix[:, 1, 2] = -((JAC[:, 0, 0] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 0]))
            adj_matrix[:, 2, 2] =  ((JAC[:, 0, 0] * JAC[:, 1, 1]) - (JAC[:, 0, 1] * JAC[:, 1, 0]))

        else:

            det_jac = (
                JAC[0, 0] * JAC[1, 1] * JAC[2, 2]
                + JAC[0, 1] * JAC[1, 2] * JAC[2, 0]
                + JAC[0, 2] * JAC[1, 0] * JAC[2, 1]
            ) - (
                JAC[2, 0] * JAC[1, 1] * JAC[0, 2]
                + JAC[2, 1] * JAC[1, 2] * JAC[0, 0]
                + JAC[2, 2] * JAC[1, 0] * JAC[0, 1]
            )

            adj_matrix = np.zeros((3, 3), dtype=float)
            adj_matrix[0, 0] =  ((JAC[1, 1] * JAC[2, 2]) - (JAC[2, 1] * JAC[1, 2]))
            adj_matrix[1, 0] = -((JAC[1, 0] * JAC[2, 2]) - (JAC[1, 2] * JAC[2, 0]))
            adj_matrix[2, 0] =  ((JAC[1, 0] * JAC[2, 1]) - (JAC[1, 1] * JAC[2, 0]))
            adj_matrix[0, 1] = -((JAC[0, 1] * JAC[2, 2]) - (JAC[0, 2] * JAC[2, 1]))
            adj_matrix[1, 1] =  ((JAC[0, 0] * JAC[2, 2]) - (JAC[0, 2] * JAC[2, 0]))
            adj_matrix[2, 1] = -((JAC[0, 0] * JAC[2, 1]) - (JAC[0, 1] * JAC[2, 0]))
            adj_matrix[0, 2] =  ((JAC[0, 1] * JAC[1, 2]) - (JAC[0, 2] * JAC[1, 1]))
            adj_matrix[1, 2] = -((JAC[0, 0] * JAC[1, 2]) - (JAC[0, 2] * JAC[1, 0]))
            adj_matrix[2, 2] =  ((JAC[0, 0] * JAC[1, 1]) - (JAC[0, 1] * JAC[1, 0]))

        return det_jac, (1 / det_jac) * adj_matrix