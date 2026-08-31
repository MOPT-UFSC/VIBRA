
from typing import TYPE_CHECKING

import numpy as np

from vibra.engine.elements.dof_indexes_processor import DOFIndexesProcessor
from vibra.engine.elements.element_data_processor import get_jacobian_determinant_2d

if TYPE_CHECKING:
    from vibra.engine.model import Model


class Element2D:

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):

        self.model = model
        self.dof_per_node = dof_per_node
        self.nodes_per_element = nodes_per_element

        self.initialize()
        self.local_dof = np.arange(dof_per_node, dtype=int)


    def initialize(self):

        self.nint: np.ndarray | None = None
        self.nint_M: np.ndarray | None = None
        self.nint_K: np.ndarray | None = None

        self.wps: np.ndarray | None = None
        self.wps_M: np.ndarray | None = None
        self.wps_K: np.ndarray | None = None

        self.phi: np.ndarray | None = None
        self.phi_M: np.ndarray | None = None
        self.phi_K: np.ndarray | None = None

        self.dphi: np.ndarray | None = None
        self.dphi_M: np.ndarray | None = None
        self.dphi_K: np.ndarray | None = None


    @property
    def dof_per_element(self):
        return self.dof_per_node * self.nodes_per_element


    @property
    def nodal_coordinates(self):
        return self.model.mesh.nodal_coordinates


    def dof_indexes_processor(self, domain: str) -> DOFIndexesProcessor:
        return DOFIndexesProcessor(self.model, domain, self.dof_per_node, self.nodes_per_element)


    def get_stacked_local_coordinates(self):
        pass


    def get_jacobian_determinant_2d(self, int_point: int, dphi: np.ndarray, coords: np.ndarray, return_vectors: bool = False):
        return get_jacobian_determinant_2d(int_point, dphi, coords, return_vectors=return_vectors)


    def elementary_matrices(self) -> tuple[np.ndarray]:
        raise NotImplementedError("The function elementary_matrices was not implemented")


    def reorder_connect(self, connectivities: np.ndarray):
        pass


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


    def integration_points_data_for_quadrangles(self, integration_points: int):
        """ 
        This method defines the integration points and their respective
        weights for the numerical integration processing.
        """
        if integration_points == 4:

            a = 1 / np.sqrt(3)
            w1 = 1

            num_int_data = np.array([
                [-a, -a, w1],
                [ a, -a, w1],
                [ a,  a, w1],
                [-a,  a, w1],
                ], dtype=float)

        elif integration_points == 9:

            a = np.sqrt(3/5)
            w1 = 25/81
            w2 = 40/81
            w3 = 64/81

            num_int_data = np.array([
                [-a, -a, w1],
                [ a, -a, w1],
                [ a,  a, w1],
                [-a,  a, w1],
                [ 0, -a, w2],
                [ a,  0, w2],
                [ 0,  a, w2],
                [-a,  0, w2],
                [ 0,  0, w3],
                ], dtype=float)

        elif integration_points == 16:

            a = np.sqrt((3 + 2*np.sqrt(6/5)) / 7)
            b = np.sqrt((3 - 2*np.sqrt(6/5)) / 7)

            w1 = 0.1210029932856020
            w2 = 0.4252933030106942
            w3 = 0.2268518518518519

            num_int_data = np.array([
                [-a, -a, w1],
                [-a,  a, w1],
                [ a,  a, w1],
                [ a, -a, w1],
                [-b, -b, w2],
                [-b,  b, w2],
                [ b,  b, w2],
                [ b, -b, w2],
                [-a, -b, w3],
                [-a,  b, w3],
                [ a, -b, w3],
                [ a,  b, w3],
                [-b, -a, w3],
                [-b,  a, w3],
                [ b,  a, w3],
                [ b, -a, w3],
                ], dtype=float)
            
        return num_int_data


    def integration_points_data_for_triangles(self, integration_points: int):
        """ 
        This method defines the integration points and their respective
        weights for the numerical integration processing.
        """

        if integration_points == 1:
            a = 1/3
            w1 = 1/2

            num_int_data = np.array([
                [a, w1]
                ], dtype=float)

        if integration_points == 3:
            a = 1/6
            b = 2/3
            w1 = 1/6

            num_int_data = np.array([
                [a, a, w1],
                [b, a, w1],
                [a, b, w1],
                ], dtype=float)

        elif integration_points == 4:
            a = 1/3
            b = 1/5
            c = 3/5
            w1 = -27/96
            w2 = 25/96

            num_int_data = np.array([
                [a, a, w1],
                [b, b, w2],
                [b, c, w2],
                [c, b, w2],
                ], dtype=float)

        elif integration_points == 6:
            a = 0.4459484909
            b = 0.091576213509771
            c = 1 - 2*a
            d = 1 - 2*b 
            w1 = 0.111690794839005
            w2 = 0.054975871827661

            num_int_data = np.array([
                [a, a, w1],
                [c, a, w1],
                [a, c, w1],
                [b, b, w2],
                [d, b, w2],
                [b, d, w2],
                ], dtype=float)

        elif integration_points == 7:
            a = 1/3
            b = (6 + np.sqrt(15)) / 21
            c = 4/7 - b
            d = 1 - 2 * b
            e = 1 - 2 * c
            w1 = 9 / 80
            w2 = (155 + np.sqrt(15)) / 2400
            w3 = (155 - np.sqrt(15)) / 2400

            num_int_data = np.array([
                [a, a, w1],
                [b, b, w2],
                [d, b, w2],
                [b, d, w2],
                [c, c, w3],
                [e, c, w3],
                [c, e, w3],
                ], dtype=float)

        return num_int_data