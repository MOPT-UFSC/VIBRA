
from typing import TYPE_CHECKING

import numpy as np

from vibra.engine.elements.dof_indexes_processor import DOFIndexesProcessor
from vibra.engine.elements.element_data_processor import ElementDataProcessor
from vibra.engine.properties.material import Material

if TYPE_CHECKING:
    from vibra.engine.model import Model


class Element3D:

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):

        self.model = model
        self.dof_per_node = dof_per_node
        self.nodes_per_element = nodes_per_element
        self.local_dof = np.arange(dof_per_node, dtype=int)

        self.initialize()


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

        self.phi_inv: np.ndarray | None = None


    @property
    def dof_per_element(self):
        return self.dof_per_node * self.nodes_per_element


    def dof_indexes_processor(self, domain: str) -> DOFIndexesProcessor:
        return DOFIndexesProcessor(self.model, domain, self.dof_per_node, self.nodes_per_element)


    def element_data_processor(self, model: "Model", domain: str) -> ElementDataProcessor:
        return ElementDataProcessor(model, domain, self.dof_per_node, self.nodes_per_element)


    def elementary_matrices(self) -> tuple[np.ndarray]:
        raise NotImplementedError("The function elementary_matrices was not implemented")


    def reorder_connect(self):
        pass


    @property
    def midside_nodes_indices_map(self):
        return {}


    def get_constitutive_model(self, material: Material, model_type: str = "linear-isotropic"):
        """
        This method returns the material constitutive model.
        """
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

    def get_detJAC(self, JAC: np.ndarray):
        """
        This function computes the determinant of Jacobian matrix.

        Parameters
        ----------
        JAC: np.array
            The Jacobian matrices.

        Returns
        -------
        det_jac: np.ndarray
            The determinant of Jacobian matrix.

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

        return det_jac


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

        det_jac = self.get_detJAC(JAC)

        if len(JAC.shape) == 3:
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


    def integration_points_data_for_hexahedrons(self, integration_points: int):
        """
        This method defines the integration points and their respective
        weights for numerical integration.
        """
        # 8-node hexahedron integration rule (Atalla and Sgard, 2015, pg. 182)
        if integration_points == 8:

            a = 1 / np.sqrt(3)
            w1 = 1

            num_int_data = np.array([
                [-a, -a, -a, w1],
                [ a, -a, -a, w1],
                [ a,  a, -a, w1],
                [-a,  a, -a, w1],
                [-a, -a,  a, w1],
                [ a, -a,  a, w1],
                [ a,  a,  a, w1],
                [-a,  a,  a, w1],
                ], dtype=float)
            
        elif integration_points == 14:
            
            # Reference: https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_thry/thy_et1.html#a6e1b1lmm
            # Table 12.9 - Numerical Integration for 20-Node Brick (14-points rule)

            a = 0.758786910639328
            b = 0.795822425754222

            w1 = 0.335180055401662
            w2 = 0.886426592797784

            num_int_data = np.array([  
                [-a,  a,  a, w1],
                [ a,  a,  a, w1],
                [-a, -a,  a, w1],
                [ a, -a,  a, w1],
                [-a,  a, -a, w1],
                [ a,  a, -a, w1],
                [-a, -a, -a, w1],
                [ a, -a, -a, w1],
                [-b,  0,  0, w2],
                [ b,  0,  0, w2],
                [ 0, -b,  0, w2],
                [ 0,  b,  0, w2],
                [ 0,  0, -b, w2],
                [ 0,  0,  b, w2],
                ], dtype=float)

        elif integration_points == 27:

            # Reference: Zienkiewicz, O. C., Taylor, R. L. The Finite Element Method. Volume 1: The basis. Fifth edition. 2000.
            # See Table 9.1 from page 220 (n=3)

            a = np.sqrt(3 / 5)

            w1 = (5**3) / (9**3)
            w2 = (5**2)*8 / (9**3)
            w3 = 5*(8**2) / (9**3)
            w4 = (8**3) / (9**3)

            num_int_data = np.array([  
                [-a, -a, -a, w1],
                [ a, -a, -a, w1],
                [ a,  a, -a, w1],
                [-a,  a, -a, w1],
                [-a, -a,  a, w1],
                [ a, -a,  a, w1],
                [ a,  a,  a, w1],
                [-a,  a,  a, w1],
                [ 0, -a, -a, w2],
                [ a,  0, -a, w2],
                [ 0,  a, -a, w2],
                [-a,  0, -a, w2],
                [ 0, -a,  a, w2],
                [ a,  0,  a, w2],
                [ 0,  a,  a, w2],
                [-a,  0,  a, w2],
                [-a, -a,  0, w2],
                [ a, -a,  0, w2],
                [ a,  a,  0, w2],
                [-a,  a,  0, w2],
                [ 0,  0, -a, w3],
                [ 0, -a,  0, w3],
                [ a,  0,  0, w3],
                [ 0,  a,  0, w3],
                [-a,  0,  0, w3],
                [ 0,  0,  a, w3],
                [ 0,  0,  0, w4],
                ], dtype=float)
        
        return num_int_data
            

    def integration_points_data_for_tetrahedrons(self, integration_points: int):
        """ 
        This method defines the integration points and their respective
        weights for numerical integration.
        """

        # NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015
        # The numerical integration points and their respective weights for the 4-, 5-, and 15-point integration rules are found on pages 177 and 178.

        # 4-point integration rule for the quadratic tetrahedron element
        if integration_points == 4:

            a = (5 - np.sqrt(5)) / 20
            b = (5 + 3 * np.sqrt(5)) / 20

            w1 = 1/24

            num_int_data = np.array([
                [a, a, a, w1],
                [a, a, b, w1],
                [a, b, a, w1],
                [b, a, a, w1],
                ], dtype=float)

        # 5-point integration rule for the quadratic tetrahedron element
        elif integration_points == 5:

            a = 1/4
            b = 1/6
            c = 1/2

            w1 = -2/15
            w2 = 3/40

            num_int_data = np.array([
                [a, a, a, w1],
                [b, b, b, w2],
                [b, b, c, w2],
                [b, c, b, w2],
                [c, b, b, w2],
                ], dtype=float)

        # 11-point integration rule for the quadratic tetrahedron element
        elif integration_points == 11:

            # Reference: Table 12.8 from webpage https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_thry/thy_et1.html

            a = 1/4
            b = 0.0714285714285714
            c = 1 - 3*b
            d = 0.399403576166799
            e = 1/2 - d

            w1 = -0.013155555555555
            w2 = 0.007622222222222
            w3 = 0.024888888888888

            num_int_data = np.array([  
                [a, a, a, w1],
                [b, b, b, w2],
                [b, b, c, w2],
                [b, c, b, w2],
                [c, b, b, w2],
                [d, d, e, w3],
                [d, e, d, w3],
                [d, e, e, w3],
                [e, d, e, w3],
                [e, d, d, w3],
                [e, e, d, w3],
                ], dtype=float)

        # 15-point integration rule for the quadratic tetrahedron element
        elif integration_points == 15:

            a = 1 / 4
            b = (7 + np.sqrt(15)) / 34
            c = (7 - np.sqrt(15)) / 34
            d = (13 - 3 * np.sqrt(15)) / 34
            e = (13 + 3 * np.sqrt(15)) / 34
            f = (5 - np.sqrt(15)) / 20
            g = (5 + np.sqrt(15)) / 20

            w1 = 8 / 405
            w2 = (2665 - 14 * np.sqrt(15)) / 226800
            w3 = (2665 + 14 * np.sqrt(15)) / 226800
            w4 = 5 / 567

            num_int_data = np.array([  
                [a, a, a, w1],
                [b, b, b, w2],
                [b, b, d, w2],
                [b, d, b, w2],
                [d, b, b, w2],
                [c, c, c, w3],
                [c, c, e, w3],
                [c, e, c, w3],
                [e, c, c, w3],
                [f, f, g, w4],
                [f, g, f, w4],
                [g, f, f, w4],
                [f, g, g, w4],
                [g, f, g, w4],
                [g, g, f, w4],
                ], dtype=float)
            
        return num_int_data