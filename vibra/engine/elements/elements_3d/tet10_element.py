
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_3d.solid_elements import Element3D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class TETRAHEDRON_10(Element3D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):

        self.model = model
        self.dof_per_node = dof_per_node
        self.nodes_per_element = nodes_per_element

        self.connectivities = None
        self.element_label = ""

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    @property
    def corner_nodes_indices(self):
        return np.arange(4, dtype=int)


    @property
    def midside_nodes_indices_map(self):
        return {
            4 : (0, 1),     # M -> (I, J)
            5 : (1, 2),     # N -> (J, K)
            6 : (2, 0),     # O -> (K, I)
            7 : (0, 3),     # P -> (I, L)
            8 : (1, 3),     # Q -> (J, L)
            9 : (2, 3),     # R -> (K, L)
            }


    def define_integration_points(self, integration_points: int=11):
        """ 
        This method defines the integration points and their
        weights for numerical integration.
        """
        self.nint = integration_points
        self.num_int_data = self.integration_points_data_for_tetrahedrons(integration_points)
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
        self.phi_K_trilinear = self.get_shape_functions_for_linear_stress_extrapolation(xi_1, xi_2, xi_3)
        self.phi_inv = self.inverse_of_trilinear_shape_functions()


    def inverse_of_trilinear_shape_functions(self):
        """
        This method returns the inverse of shape functions matrix N applied
        at integration points (Gauss-Legendre quadrature points).
        """
        N = self.phi_K_trilinear
        n_intp, n_nodes = N.shape

        if n_intp == n_nodes:
            # print("N_int = N_nodes")
            return np.linalg.inv(N)

        elif n_intp > n_nodes:
            # print("N_int > N_nodes")
            return np.linalg.inv(N.T @ N) @ N.T

        else:
            print("Not implemented stress extrapolation for N_int < N_nodes")
            return None


    def get_shape_functions_for_linear_stress_extrapolation(
            self, 
            xi_1: np.ndarray | float, 
            xi_2: np.ndarray | float, 
            xi_3: np.ndarray | float,
            ):

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
        """

        Nz = xi_1.size
    
        ##NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015

        # define the shape functions (Atalla and Sgard, 2015, pg. 170)
        phi = np.zeros((Nz, 4), dtype=float)

        # define isoparametric coordiante xi_4
        xi_4 = 1 - xi_1 - xi_2 - xi_3

        phi[:, 0] = xi_4      # ->      (0.0, 0.0, 0.0)   Node 1
        phi[:, 1] = xi_2      # ->      (0.0, 1.0, 0.0)   Node 2
        phi[:, 2] = xi_3      # ->      (0.0, 0.0, 1.0)   Node 3
        phi[:, 3] = xi_1      # ->      (1.0, 0.0, 0.0)   Node 4

        return phi


    def get_shape_functions_and_derivatives(self, xi_1: np.ndarray | float, xi_2: np.ndarray | float, xi_3: np.ndarray | float):

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

        # define the shape functions (Atalla and Sgard, 2015, pg. 170)
        phi = np.zeros((Nz, self.nodes_per_element), dtype=float)

        # define the isoparametric coordiante l4
        xi_4 = 1 - xi_1 - xi_2 - xi_3

        phi[:, 0] = (2 * xi_4 - 1) * xi_4       # ->      (0.0, 0.0, 0.0)   Node 1
        phi[:, 1] = (2 * xi_2 - 1) * xi_2       # ->      (0.0, 1.0, 0.0)   Node 2
        phi[:, 2] = (2 * xi_3 - 1) * xi_3       # ->      (0.0, 0.0, 1.0)   Node 3
        phi[:, 3] = (2 * xi_1 - 1) * xi_1       # ->      (1.0, 0.0, 0.0)   Node 4
        phi[:, 4] = 4 * xi_4 * xi_2             # ->      (0.0, 0.5, 0.0)   Node 5
        phi[:, 5] = 4 * xi_2 * xi_3             # ->      (0.0, 0.5, 0.5)   Node 6
        phi[:, 6] = 4 * xi_3 * xi_4             # ->      (0.0, 0.0, 0.5)   Node 7
        phi[:, 7] = 4 * xi_1 * xi_4             # ->      (0.5, 0.0, 0.0)   Node 8
        phi[:, 8] = 4 * xi_1 * xi_2             # ->      (0.5, 0.5, 0.0)   Node 9
        phi[:, 9] = 4 * xi_1 * xi_3             # ->      (0.5, 0.0, 0.5)   Node 10

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((Nz, 3, self.nodes_per_element), dtype=float)

        dphi[:, 0, 0] = -4 * xi_4 + 1
        dphi[:, 0, 1] =  0
        dphi[:, 0, 2] =  0
        dphi[:, 0, 3] =  4 * xi_1 - 1
        dphi[:, 0, 4] = -4 * xi_2
        dphi[:, 0, 5] =  0
        dphi[:, 0, 6] = -4 * xi_3
        dphi[:, 0, 7] =  4 * (xi_4 - xi_1)
        dphi[:, 0, 8] =  4 * xi_2
        dphi[:, 0, 9] =  4 * xi_3

        dphi[:, 1, 0] = -4 * xi_4 + 1
        dphi[:, 1, 1] =  4 * xi_2 - 1
        dphi[:, 1, 2] =  0
        dphi[:, 1, 3] =  0
        dphi[:, 1, 4] =  4 * (xi_4 - xi_2)
        dphi[:, 1, 5] =  4 * xi_3
        dphi[:, 1, 6] = -4 * xi_3
        dphi[:, 1, 7] = -4 * xi_1
        dphi[:, 1, 8] =  4 * xi_1
        dphi[:, 1, 9] =  0

        dphi[:, 2, 0] = -4 * xi_4 + 1
        dphi[:, 2, 1] =  0
        dphi[:, 2, 2] =  4 * xi_3 - 1
        dphi[:, 2, 3] =  0
        dphi[:, 2, 4] = -4 * xi_2
        dphi[:, 2, 5] =  4 * xi_2
        dphi[:, 2, 6] =  4 * (xi_4 - xi_3)
        dphi[:, 2, 7] = -4 * xi_1
        dphi[:, 2, 8] =  0
        dphi[:, 2, 9] =  4 * xi_1

        if Nz == 1:
            return phi[0, :, :], dphi[0, :, :]

        return phi, dphi


    def reorder_connect(self):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """
        self.connectivities = self.model.mesh.solids_connectivity[:, [6, 4, 5, 7, 10, 8, 9, 12, 11, 13]]