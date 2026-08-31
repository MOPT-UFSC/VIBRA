
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_1d.line_elements import Element1D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


def get_local_coordinates(coords: np.ndarray) -> np.ndarray:
    """
    This funtion computes the local coordinates from global coordinates.

    Parameter
    ---------
    coords: np.ndarray
        An array containing the global coordinates to be converted.

    Returns
    -------
    coord_loc: np.ndarray
        The array of the stacked coordinates in the local coordinate system.
    """
    X1, X2, = coords[:, 1]
    Y1, Y2, = coords[:, 2]
    Z1, Z2, = coords[:, 3]

    vec_21 = np.array([X2-X1, Y2-Y1, Z2-Z1]).T

    coord_loc = np.zeros((2, 1), dtype=float)
    coord_loc[1, 0] = np.linalg.norm(vec_21)

    return coord_loc


class LINE_2(Element1D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):

        self.model = model
        self.dof_per_node = dof_per_node
        self.nodes_per_element = nodes_per_element

        self.connectivities = None
        self.element_label = ""
        self.nodal_coordinates = self.model.mesh.nodal_coordinates

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    @property
    def dof_per_element(self):
        return self.nodes_per_element * self.dof_per_node


    def define_integration_points(self):
        """ 
        Defines the integration points and their respective weights
        for the numerical integration processing.
        """
        self.nint_K = 2
        self.nint_M = 3
        self.wps_K = 1
        self.wps_M = 1
        con = 1 / np.sqrt(3)
        self.pint2 = np.array([-con, con], dtype=float)


    def get_shape_functions_and_derivatives(self, xi: np.ndarray):

        """
        This method returns the shape functions and its derivatives.
        
        Parameters
        ----------
        xi: np.ndarray
            The x coordinates of the integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        # shape functions
        phi = np.zeros((xi.size, 1, self.nodes_per_element), dtype=float)

        phi[:, 0, 0] = 0.5*(1 - xi)
        phi[:, 0, 1] = 0.5*(1 + xi)

        # shape functions derivatives
        dphi = np.zeros((xi.size, 1, self.nodes_per_element), dtype=float)

        dphi[:, 0, 0] = -0.5
        dphi[:, 0, 1] =  0.5

        return phi, dphi


    def get_integration_points_data(self, integration_points: int=3):
        """ 
        Defines the integration points and their respective weights
        for the numerical integration processing.
        """

        if integration_points == 1:
            p_int = np.array([0], dtype=float)
            wps = np.array([2], dtype=float)

        elif integration_points == 2:
            a = 1 / np.sqrt(3)
            p_int = np.array([-a, a], dtype=float)
            wps = np.array([1, 1], dtype=float)

        elif integration_points == 3:
            a = np.sqrt(15) / 5
            w1 = 5/9
            w2 = 8/9
            p_int = np.array([-a, a, 0.0], dtype=float)
            wps = np.array([w1, w1, w2], dtype=float)

        else:
            NotImplementedError(f"Non-implement integration points for {integration_points}.")
            return (None, None)

        return (p_int, wps.reshape(-1, 1, 1))


    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """
        # calculate the shape functions and derivatives for stiffness matrix
        pint_K, self.wps_K = self.get_integration_points_data(integration_points=self.nint_K)
        self.phi_K, self.dphi_K = self.get_shape_functions_and_derivatives(pint_K)

        # calculate the shape functions and derivatives for mass matrix
        pint_M, self.wps_M = self.get_integration_points_data(integration_points=self.nint_M)
        self.phi_M, self.dphi_M = self.get_shape_functions_and_derivatives(pint_M)


    def get_stacked_local_coordinates(self) -> np.ndarray:
        """
        This funtion computes the local coordinates from global coordinates.

        Parameter
        ---------
        coords: np.ndarray
            An array containing the global coordinates to be converted.

        Returns
        -------
        coord_loc: np.ndarray
            The array of the stacked coordinates in the local coordinate system.
        """
        X1 = self.nodal_coordinates[self.connectivities[:, 0], 1]
        Y1 = self.nodal_coordinates[self.connectivities[:, 0], 2]
        Z1 = self.nodal_coordinates[self.connectivities[:, 0], 3]

        X2 = self.nodal_coordinates[self.connectivities[:, 1], 1]
        Y2 = self.nodal_coordinates[self.connectivities[:, 1], 2]
        Z2 = self.nodal_coordinates[self.connectivities[:, 1], 3]

        nel = self.connectivities.shape[0]
        vec_21 = np.array([X2-X1, Y2-Y1, Z2-Z1]).T

        coord_loc = np.zeros((nel, 2, 1), dtype=float)
        coord_loc[:, 1, 0] = np.linalg.norm(vec_21, axis=1)

        return coord_loc


    def reorder_connect(self, connectivities: np.ndarray):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model.

        Parameter
        ---------
        connectivities: np.ndarray
            An array containing the lines connectivities.
        """
        self.connectivities = connectivities[:, [0, 1]]