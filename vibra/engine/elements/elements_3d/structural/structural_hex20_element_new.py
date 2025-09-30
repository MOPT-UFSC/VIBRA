import numpy as np

from vibra.engine.elements.solid_elements import Element3D
from vibra.engine.properties.material import Material

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model


def get_detJAC_and_invJAC(JAC: np.ndarray):
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


class STRUCT_HEXAHEDRON_20(Element3D):

    NODES_PER_ELEMENT = 20
    DOF_PER_NODE = 3
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivity = None
        self.element_label = "structural_hexahedron_20"

        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.solids_connectivity = self.model.mesh.solids_connectivity

        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.solids_connectivity)

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def define_integration_points(self, integration_points: int = 14):
        """ 
        This method defines the integration points and their
        weights for numerical integration.
        """

        if integration_points == 14:

            # Reference: https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_thry/thy_et1.html#a6e1b1lmm
            # Table 12.9 - Numerical Integration for 20-Node Brick (14-points rule)

            self.nint = 14
            a = 0.758786910639328
            b = 0.795822425754222

            w1 = 0.335180055401662
            w2 = 0.886426592797784

            self.num_int_data = np.array([  
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
            
            self.wps = self.num_int_data[:, -1].reshape(-1, 1, 1)

        elif integration_points == 27:

            # Reference: Zienkiewicz, O. C., Taylor, R. L. The Finite Element Method. Volume 1: The basis. Fifth edition. 2000.
            # See Table 9.1 from page 220 (n=3)

            self.nint = 27

            a = np.sqrt(3 / 5)

            w1 = (5**3) / (9**3)
            w2 = (5**2)*8 / (9**3)
            w3 = 5*(8**2) / (9**3)
            w4 = (8**3) / (9**3)

            self.num_int_data = np.array([  
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

            self.wps = self.num_int_data[:, -1].reshape(-1, 1, 1)


    def process_shape_functions_and_derivatives(self):
        """
        This method returns the shape functions and its derivatives
        for all integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        ## coordinates from integration points
        xi_1 = self.num_int_data[:, 0]
        xi_2 = self.num_int_data[:, 1]
        xi_3 = self.num_int_data[:, 2]

        self.phi, self.dphi = self.get_shape_functions_and_derivatives(xi_1, xi_2, xi_3)


    def get_shape_functions_and_derivatives(self, xi_1: np.ndarray|float, xi_2: np.ndarray|float, xi_3: np.ndarray|float):

        """
        This method returns the shape functions and its derivatives.
        
        Parameters
        ----------
        xi_1: np.ndarray
            The x coordinates of the integration points.
        
        xi_2: np.ndarray
            The y coordinates of the integration points.

        xi_3: np.ndarray
            The z coordinates of the integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        if isinstance(xi_1, np.ndarray):
            Nz = xi_1.size
        else:
            Nz = 1

        ##NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015

        # define the shape functions (Atalla and Sgard, 2015, pg. 171)
        phi = np.zeros((Nz, self.NODES_PER_ELEMENT), dtype=float)

        phi[:, 0] = (1 - xi_1) * (1 - xi_2) * (1 - xi_3) * (-xi_1 - xi_2 - xi_3 - 2) / 8      # ->      (-1.0, -1.0, -1.0)   Node 1
        phi[:, 1] = (1 + xi_1) * (1 - xi_2) * (1 - xi_3) * ( xi_1 - xi_2 - xi_3 - 2) / 8      # ->      ( 1.0, -1.0, -1.0)   Node 2
        phi[:, 2] = (1 + xi_1) * (1 + xi_2) * (1 - xi_3) * ( xi_1 + xi_2 - xi_3 - 2) / 8      # ->      ( 1.0,  1.0, -1.0)   Node 3
        phi[:, 3] = (1 - xi_1) * (1 + xi_2) * (1 - xi_3) * (-xi_1 + xi_2 - xi_3 - 2) / 8      # ->      (-1.0,  1.0, -1.0)   Node 4
        phi[:, 4] = (1 - xi_1) * (1 - xi_2) * (1 + xi_3) * (-xi_1 - xi_2 + xi_3 - 2) / 8      # ->      (-1.0, -1.0,  1.0)   Node 5
        phi[:, 5] = (1 + xi_1) * (1 - xi_2) * (1 + xi_3) * ( xi_1 - xi_2 + xi_3 - 2) / 8      # ->      ( 1.0, -1.0,  1.0)   Node 6
        phi[:, 6] = (1 + xi_1) * (1 + xi_2) * (1 + xi_3) * ( xi_1 + xi_2 + xi_3 - 2) / 8      # ->      ( 1.0,  1.0,  1.0)   Node 7
        phi[:, 7] = (1 - xi_1) * (1 + xi_2) * (1 + xi_3) * (-xi_1 + xi_2 + xi_3 - 2) / 8      # ->      (-1.0,  1.0,  1.0)   Node 8

        phi[:, 8 ] = (1 - xi_1**2) * (1 - xi_2) * (1 - xi_3) / 4                              # ->      ( 0.0, -1.0, -1.0)   Node 9
        phi[:, 9 ] = (1 + xi_1) * (1 - xi_2**2) * (1 - xi_3) / 4                              # ->      ( 1.0,  0.0, -1.0)   Node 10
        phi[:, 10] = (1 - xi_1**2) * (1 + xi_2) * (1 - xi_3) / 4                              # ->      ( 0.0,  1.0, -1.0)   Node 11
        phi[:, 11] = (1 - xi_1) * (1 - xi_2**2) * (1 - xi_3) / 4                              # ->      (-1.0,  0.0, -1.0)   Node 12
        phi[:, 12] = (1 - xi_1**2) * (1 - xi_2) * (1 + xi_3) / 4                              # ->      ( 0.0, -1.0,  1.0)   Node 17
        phi[:, 13] = (1 + xi_1) * (1 - xi_2**2) * (1 + xi_3) / 4                              # ->      ( 1.0,  0.0,  1.0)   Node 18
        phi[:, 14] = (1 - xi_1**2) * (1 + xi_2) * (1 + xi_3) / 4                              # ->      ( 0.0,  1.0,  1.0)   Node 19
        phi[:, 15] = (1 - xi_1) * (1 - xi_2**2) * (1 + xi_3) / 4                              # ->      (-1.0,  0.0,  1.0)   Node 20
        phi[:, 16] = (1 - xi_1) * (1 - xi_2) * (1 - xi_3**2) / 4                              # ->      (-1.0, -1.0,  0.0)   Node 13
        phi[:, 17] = (1 + xi_1) * (1 - xi_2) * (1 - xi_3**2) / 4                              # ->      ( 1.0, -1.0,  0.0)   Node 14
        phi[:, 18] = (1 + xi_1) * (1 + xi_2) * (1 - xi_3**2) / 4                              # ->      ( 1.0,  1.0,  0.0)   Node 15
        phi[:, 19] = (1 - xi_1) * (1 + xi_2) * (1 - xi_3**2) / 4                              # ->      (-1.0,  1.0,  0.0)   Node 16

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((Nz, 3, self.NODES_PER_ELEMENT), dtype=float)

        dphi[:, 0, 0 ] =  (1 - xi_2) * (1 - xi_3) * (2*xi_1 + xi_2 + xi_3 + 1) / 8
        dphi[:, 0, 1 ] =  (1 - xi_2) * (1 - xi_3) * (2*xi_1 - xi_2 - xi_3 - 1) / 8
        dphi[:, 0, 2 ] =  (1 + xi_2) * (1 - xi_3) * (2*xi_1 + xi_2 - xi_3 - 1) / 8
        dphi[:, 0, 3 ] =  (1 + xi_2) * (1 - xi_3) * (2*xi_1 - xi_2 + xi_3 + 1) / 8
        dphi[:, 0, 4 ] =  (1 - xi_2) * (1 + xi_3) * (2*xi_1 + xi_2 - xi_3 + 1) / 8
        dphi[:, 0, 5 ] =  (1 - xi_2) * (1 + xi_3) * (2*xi_1 - xi_2 + xi_3 - 1) / 8
        dphi[:, 0, 6 ] =  (1 + xi_2) * (1 + xi_3) * (2*xi_1 + xi_2 + xi_3 - 1) / 8
        dphi[:, 0, 7 ] =  (1 + xi_2) * (1 + xi_3) * (2*xi_1 - xi_2 - xi_3 + 1) / 8
        dphi[:, 0, 8 ] = (-2*xi_1) * (1 - xi_2) * (1 - xi_3) / 4
        dphi[:, 0, 9 ] = (1) * (1 - xi_2**2) * (1 - xi_3) / 4
        dphi[:, 0, 10] = (-2*xi_1) * (1 + xi_2) * (1 - xi_3) / 4
        dphi[:, 0, 11] = (-1) * (1 - xi_2**2) * (1 - xi_3) / 4
        dphi[:, 0, 12] = (-2*xi_1) * (1 - xi_2) * (1 + xi_3) / 4
        dphi[:, 0, 13] = (1) * (1 - xi_2**2) * (1 + xi_3) / 4
        dphi[:, 0, 14] = (-2*xi_1) * (1 + xi_2) * (1 + xi_3) / 4
        dphi[:, 0, 15] = (-1) * (1 - xi_2**2) * (1 + xi_3) / 4
        dphi[:, 0, 16] = (-1) * (1 - xi_2) * (1 - xi_3**2) / 4
        dphi[:, 0, 17] = (1) * (1 - xi_2) * (1 - xi_3**2) / 4
        dphi[:, 0, 18] = (1) * (1 + xi_2) * (1 - xi_3**2) / 4
        dphi[:, 0, 19] = (-1) * (1 + xi_2) * (1 - xi_3**2) / 4


        dphi[:, 1, 0 ] = (1 - xi_1) * (1 - xi_3) * ( xi_1 + 2*xi_2 + xi_3 + 1) / 8
        dphi[:, 1, 1 ] = (1 + xi_1) * (1 - xi_3) * (-xi_1 + 2*xi_2 + xi_3 + 1) / 8
        dphi[:, 1, 2 ] = (1 + xi_1) * (1 - xi_3) * ( xi_1 + 2*xi_2 - xi_3 - 1) / 8
        dphi[:, 1, 3 ] = (1 - xi_1) * (1 - xi_3) * (-xi_1 + 2*xi_2 - xi_3 - 1) / 8 
        dphi[:, 1, 4 ] = (1 - xi_1) * (1 + xi_3) * ( xi_1 + 2*xi_2 - xi_3 + 1) / 8
        dphi[:, 1, 5 ] = (1 + xi_1) * (1 + xi_3) * (-xi_1 + 2*xi_2 - xi_3 + 1) / 8
        dphi[:, 1, 6 ] = (1 + xi_1) * (1 + xi_3) * ( xi_1 + 2*xi_2 + xi_3 - 1) / 8
        dphi[:, 1, 7 ] = (1 - xi_1) * (1 + xi_3) * (-xi_1 + 2*xi_2 + xi_3 - 1) / 8
        dphi[:, 1, 8 ] = (1 - xi_1**2) * (-1) * (1 - xi_3) / 4
        dphi[:, 1, 9 ] = (1 + xi_1) * (-2*xi_2) * (1 - xi_3) / 4
        dphi[:, 1, 10] = (1 - xi_1**2) * (1) * (1 - xi_3) / 4
        dphi[:, 1, 11] = (1 - xi_1) * (-2*xi_2) * (1 - xi_3) / 4
        dphi[:, 1, 12] = (1 - xi_1**2) * (-1) * (1 + xi_3) / 4
        dphi[:, 1, 13] = (1 + xi_1) * (-2*xi_2) * (1 + xi_3) / 4
        dphi[:, 1, 14] = (1 - xi_1**2) * (1) * (1 + xi_3) / 4
        dphi[:, 1, 15] = (1 - xi_1) * (-2*xi_2) * (1 + xi_3) / 4
        dphi[:, 1, 16] = (1 - xi_1) * (-1) * (1 - xi_3**2) / 4
        dphi[:, 1, 17] = (1 + xi_1) * (-1) * (1 - xi_3**2) / 4
        dphi[:, 1, 18] = (1 + xi_1) * (1) * (1 - xi_3**2) / 4
        dphi[:, 1, 19] = (1 - xi_1) * (1) * (1 - xi_3**2) / 4

        dphi[:, 2, 0 ] = (1 - xi_1) * (1 - xi_2) * ( xi_1 + xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 1 ] = (1 + xi_1) * (1 - xi_2) * (-xi_1 + xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 2 ] = (1 + xi_1) * (1 + xi_2) * (-xi_1 - xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 3 ] = (1 - xi_1) * (1 + xi_2) * ( xi_1 - xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 4 ] = (1 - xi_1) * (1 - xi_2) * (-xi_1 - xi_2 + 2*xi_3 - 1) / 8
        dphi[:, 2, 5 ] = (1 + xi_1) * (1 - xi_2) * ( xi_1 - xi_2 + 2*xi_3 - 1) / 8 
        dphi[:, 2, 6 ] = (1 + xi_1) * (1 + xi_2) * ( xi_1 + xi_2 + 2*xi_3 - 1) / 8
        dphi[:, 2, 7 ] = (1 - xi_1) * (1 + xi_2) * (-xi_1 + xi_2 + 2*xi_3 - 1) / 8
        dphi[:, 2, 8 ] = (1 - xi_1**2) * (1 - xi_2) * (-1) / 4
        dphi[:, 2, 9 ] = (1 + xi_1) * (1 - xi_2**2) * (-1) / 4
        dphi[:, 2, 10] = (1 - xi_1**2) * (1 + xi_2) * (-1) / 4
        dphi[:, 2, 11] = (1 - xi_1) * (1 - xi_2**2) * (-1) / 4
        dphi[:, 2, 12] = (1 - xi_1**2) * (1 - xi_2) * (1) / 4
        dphi[:, 2, 13] = (1 + xi_1) * (1 - xi_2**2) * (1) / 4
        dphi[:, 2, 14] = (1 - xi_1**2) * (1 + xi_2) * (1) / 4
        dphi[:, 2, 15] = (1 - xi_1) * (1 - xi_2**2) * (1) / 4
        dphi[:, 2, 16] = (1 - xi_1) * (1 - xi_2) * (-2*xi_3) / 4
        dphi[:, 2, 17] = (1 + xi_1) * (1 - xi_2) * (-2*xi_3) / 4
        dphi[:, 2, 18] = (1 + xi_1) * (1 + xi_2) * (-2*xi_3) / 4
        dphi[:, 2, 19] = (1 - xi_1) * (1 + xi_2) * (-2*xi_3) / 4

        return phi, dphi


    def get_constitutive_model(self, material: Material, model_type="linear-isotropic"):
        """This methdo returns the material constitutive model."""

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

            return factor * const_law


    def elementary_matrices(self, el_index: int, material: Material):
        """This method returns elementary stiffness and mass matrices for HEXAHEDRON-20 nodes.
        ANSYS SOLID95 - Do not compare with new Ansys solid elements
        """

        rho = material.material_density
        const_mat = self.get_constitutive_model(material, model_type="linear-isotropic")

        # nodes from element
        elem_nodes = self.connectivity[el_index, 1:]

        # element nodal coords
        coords = self.nodal_coordinates[elem_nodes, 1:4]

        # Jacobian matrix
        JAC = self.dphi @ coords

        # Jacobian determinant and inverse
        detJAC, invJAC = get_detJAC_and_invJAC(JAC)

        # derivatives
        dphi_t = invJAC @ self.dphi

        B = np.zeros((self.nint, 6, self.DOF_PER_ELEMENT), dtype=float)
        B[:, 0, 0::3] = dphi_t[:, 0, :]
        B[:, 1, 1::3] = dphi_t[:, 1, :]
        B[:, 2, 2::3] = dphi_t[:, 2, :]
        B[:, 3, 0::3] = dphi_t[:, 1, :]
        B[:, 3, 1::3] = dphi_t[:, 0, :]
        B[:, 4, 0::3] = dphi_t[:, 2, :]
        B[:, 4, 2::3] = dphi_t[:, 0, :]
        B[:, 5, 1::3] = dphi_t[:, 2, :]
        B[:, 5, 2::3] = dphi_t[:, 1, :]

        N = np.zeros((self.nint, 3, self.DOF_PER_ELEMENT), dtype=float)
        N[:, 0, 0::3] = self.phi
        N[:, 1, 1::3] = self.phi
        N[:, 2, 2::3] = self.phi

        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            Ke += B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])
            Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i])

        return Ke, Me


    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        if self.solids_connectivity.shape[1] == self.NODES_PER_ELEMENT + 4:
            self.connectivity = self.solids_connectivity[
                :, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19]
            ]


    def generate_ind_rows_cols(self, reorder: bool = True):
        """ 
        This method processess the dof indices (rows and columns) 
        for assembly
        """

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.solids_connectivity[
                :, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]

        dof, edof = self.DOF_PER_NODE, self.DOF_PER_ELEMENT
        n_el = self.solids_connectivity.shape[0]
    
        # ind_dof = (
        #     np.array(
        #         [
        #             dof * self.connectivity[:, 1] - 1,
        #             dof * self.connectivity[:, 1],
        #             dof * self.connectivity[:, 1] + 1,
        #             dof * self.connectivity[:, 2] - 1,
        #             dof * self.connectivity[:, 2],
        #             dof * self.connectivity[:, 2] + 1,
        #             dof * self.connectivity[:, 3] - 1,
        #             dof * self.connectivity[:, 3],
        #             dof * self.connectivity[:, 3] + 1,
        #             dof * self.connectivity[:, 4] - 1,
        #             dof * self.connectivity[:, 4],
        #             dof * self.connectivity[:, 4] + 1,
        #             dof * self.connectivity[:, 5] - 1,
        #             dof * self.connectivity[:, 5],
        #             dof * self.connectivity[:, 5] + 1,
        #             dof * self.connectivity[:, 6] - 1,
        #             dof * self.connectivity[:, 6],
        #             dof * self.connectivity[:, 6] + 1,
        #             dof * self.connectivity[:, 7] - 1,
        #             dof * self.connectivity[:, 7],
        #             dof * self.connectivity[:, 7] + 1,
        #             dof * self.connectivity[:, 8] - 1,
        #             dof * self.connectivity[:, 8],
        #             dof * self.connectivity[:, 8] + 1,
        #             dof * self.connectivity[:, 9] - 1,
        #             dof * self.connectivity[:, 9],
        #             dof * self.connectivity[:, 9] + 1,
        #             dof * self.connectivity[:, 10] - 1,
        #             dof * self.connectivity[:, 10],
        #             dof * self.connectivity[:, 10] + 1,
        #             dof * self.connectivity[:, 11] - 1,
        #             dof * self.connectivity[:, 11],
        #             dof * self.connectivity[:, 11] + 1,
        #             dof * self.connectivity[:, 12] - 1,
        #             dof * self.connectivity[:, 12],
        #             dof * self.connectivity[:, 12] + 1,
        #             dof * self.connectivity[:, 13] - 1,
        #             dof * self.connectivity[:, 13],
        #             dof * self.connectivity[:, 13] + 1,
        #             dof * self.connectivity[:, 14] - 1,
        #             dof * self.connectivity[:, 14],
        #             dof * self.connectivity[:, 14] + 1,
        #             dof * self.connectivity[:, 15] - 1,
        #             dof * self.connectivity[:, 15],
        #             dof * self.connectivity[:, 15] + 1,
        #             dof * self.connectivity[:, 16] - 1,
        #             dof * self.connectivity[:, 16],
        #             dof * self.connectivity[:, 16] + 1,
        #             dof * self.connectivity[:, 17] - 1,
        #             dof * self.connectivity[:, 17],
        #             dof * self.connectivity[:, 17] + 1,
        #             dof * self.connectivity[:, 18] - 1,
        #             dof * self.connectivity[:, 18],
        #             dof * self.connectivity[:, 18] + 1,
        #             dof * self.connectivity[:, 19] - 1,
        #             dof * self.connectivity[:, 19],
        #             dof * self.connectivity[:, 19] + 1,
        #             dof * self.connectivity[:, 20] - 1,
        #             dof * self.connectivity[:, 20],
        #             dof * self.connectivity[:, 20] + 1,
        #         ],
        #         dtype=int,
        #     )
        #     + 1
        # ).T

        local_dof = np.arange(dof, dtype=int)
        ind_dof = np.zeros((n_el, edof), dtype=int)

        for j in range(self.NODES_PER_ELEMENT):
            ind_dof[:, j*dof : (1 + j)*dof] = dof * self.connectivity[:, j+1].reshape(-1, 1) + local_dof

        vect_indices = ind_dof.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dof, edof)).flatten()

        return self.ind_rows, self.ind_cols
