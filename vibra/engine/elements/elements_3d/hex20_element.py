
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_3d.solid_elements import Element3D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class HEXAHEDRON_20(Element3D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):

        self.model = model
        self.dof_per_node = dof_per_node
        self.nodes_per_element = nodes_per_element

        self.connectivities = None
        self.element_label = ""


    @property
    def corner_nodes_indices(self):
        return np.arange(8, dtype=int)


    @property
    def midside_nodes_indices_map(self):
        return {
            8 : (0, 1),      # Q -> (I, J)
            9 : (1, 2),      # R -> (J, K)
            10 : (2, 3),     # S -> (K, L)
            11 : (3, 4),     # T -> (L, I)
            12 : (4, 5),     # U -> (M, N)
            13 : (5, 6),     # V -> (N, O)
            14 : (6, 7),     # W -> (O, P)
            15 : (7, 4),     # X -> (P, M)
            16 : (4, 0),     # Y -> (M, I)
            17 : (5, 1),     # Z -> (N, J)
            18 : (6, 2),     # A -> (O, K)
            19 : (7, 3),     # B -> (P, L)
            }


    def define_integration_points(self, integration_points: int = 27):
        """ 
        This method defines the integration points and their
        weights for numerical integration.
        """
        self.nint = integration_points
        self.num_int_data = self.integration_points_data_for_hexahedrons(integration_points)
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
        phi = np.zeros((Nz, self.nodes_per_element), dtype=float)

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
        dphi = np.zeros((Nz, 3, self.nodes_per_element), dtype=float)

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

        if Nz == 1:
            return phi[0, :, :], dphi[0, :, :]

        return phi, dphi


    def reorder_connect(self):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """
        self.connectivities = self.model.mesh.solids_connectivity[
                :, [4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19]
            ]