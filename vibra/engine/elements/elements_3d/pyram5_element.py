
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_3d.solid_elements import Element3D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class Pyramid5(Element3D):

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
        return np.arange(5, dtype=int)


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
        self.phi_inv = self.inverse_of_trilinear_shape_functions()


    def inverse_of_trilinear_shape_functions(self):
        """
        This method returns the inverse of shape functions matrix N applied
        at integration points (Gauss-Legendre quadrature points).
        """
        N = self.phi
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

    def get_shape_functions_and_derivatives(self, xi: np.ndarray | float, eta: np.ndarray | float, zeta: np.ndarray | float):

        """
        This method returns the shape functions and its derivatives.
        
        Parameters
        ----------
        xi: np.ndarray
            The x coordinates of the integration points.
        
        eta: np.ndarray
            The y coordinates of the integration points.

        zeta: np.ndarray
            The z coordinates of the integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        if isinstance(xi, np.ndarray):
            Nz = xi.size
        else:
            Nz = 1

        ##NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015

        # define the shape functions (Atalla and Sgard, 2015, pg. 170)
        phi = np.zeros((Nz, self.nodes_per_element), dtype=float)

        phi[:, 0] = (1 / 4) * ((1 - xi) * (1 - eta) - (1 + zeta) / 2 + ((xi * eta) * (1 + zeta) / (2 * (1 - zeta))))      # ->      (-1.0, -1.0, -1.0)   Node 1
        phi[:, 1] = (1 / 4) * ((1 + xi) * (1 - eta) - (1 + zeta) / 2 - ((xi * eta) * (1 + zeta) / (2 * (1 - zeta))))      # ->      ( 1.0, -1.0, -1.0)   Node 2
        phi[:, 2] = (1 / 4) * ((1 + xi) * (1 + eta) - (1 + zeta) / 2 + ((xi * eta) * (1 + zeta) / (2 * (1 - zeta))))      # ->      ( 1.0,  1.0, -1.0)   Node 3
        phi[:, 3] = (1 / 4) * ((1 - xi) * (1 + eta) - (1 + zeta) / 2 - ((xi * eta) * (1 + zeta) / (2 * (1 - zeta))))      # ->      (-1.0,  1.0, -1.0)   Node 4
        phi[:, 4] = (1 / 2) * (1 + zeta)                                                                                  # ->      ( 0.0,  0.0,  1.0)   Node 5

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((Nz, 3, self.nodes_per_element), dtype=float)

        # dN / dxi
        dphi[:, 0, 0] = (1 / 4) * (-(1 - eta) + eta * (1 + zeta) / (2 * (1 - zeta))) 
        dphi[:, 0, 1] = (1 / 4) * (+(1 - eta) - eta * (1 + zeta) / (2 * (1 - zeta)))
        dphi[:, 0, 2] = (1 / 4) * (+(1 - eta) + eta * (1 + zeta) / (2 * (1 - zeta)))
        dphi[:, 0, 3] = (1 / 4) * (-(1 - eta) - eta * (1 + zeta) / (2 * (1 - zeta)))
        dphi[:, 0, 4] = 0

        # dN / deta
        dphi[:, 1, 0] = (1 / 4) * (-(1 - xi) + (xi * (1 + zeta) / (2 * (1 - zeta))))
        dphi[:, 1, 1] = (1 / 4) * (-(1 - xi) - (xi * (1 + zeta) / (2 * (1 - zeta))))
        dphi[:, 1, 2] = (1 / 4) * (+(1 - xi) + (xi * (1 + zeta) / (2 * (1 - zeta))))
        dphi[:, 1, 3] = (1 / 4) * (+(1 - xi) - (xi * (1 + zeta) / (2 * (1 - zeta))))
        dphi[:, 1, 4] =  0

        # dN / dzeta
        dphi[:, 2, 0] = (1 / 4) * (-(1 / 2) + (xi * eta) / ((1 - zeta)**2))
        dphi[:, 2, 1] = (1 / 4) * (-(1 / 2) - (xi * eta) / ((1 - zeta)**2))
        dphi[:, 2, 2] = (1 / 4) * (-(1 / 2) + (xi * eta) / ((1 - zeta)**2))
        dphi[:, 2, 3] = (1 / 4) * (-(1 / 2) - (xi * eta) / ((1 - zeta)**2))
        dphi[:, 2, 4] = (1 / 2) * zeta

        if Nz == 1:
            return phi[0, :], dphi[0, :, :]

        return phi, dphi


    def reorder_connect(self):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """
        self.connectivities = self.model.mesh.solids_connectivity[:, [4, 5, 6, 7, 8]]