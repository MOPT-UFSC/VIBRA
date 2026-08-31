
from typing import TYPE_CHECKING

from vibra.engine.elements.surface_elements import Element2D

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
        The array of coordinates in the local coordinate system.
    """
    
    X1, X2, X3, X4 = coords[:, 1]
    Y1, Y2, Y3, Y4 = coords[:, 2]
    Z1, Z2, Z3, Z4 = coords[:, 3]

    vec_12 = np.array([X2-X1, Y2-Y1, Z2-Z1]).T
    vec_13 = np.array([X3-X1, Y3-Y1, Z3-Z1]).T
    vec_14 = np.array([X4-X1, Y4-Y1, Z4-Z1]).T

    loc_x_axis = vec_12.copy()
    loc_z_axis = np.cross(loc_x_axis, vec_14)
    loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

    unit_x_axis = loc_x_axis / np.linalg.norm(loc_x_axis)
    unit_y_axis = loc_y_axis / np.linalg.norm(loc_y_axis)

    x1 = np.dot(vec_13, unit_x_axis)
    x2 = np.dot(vec_14, unit_x_axis)
    x3 = 0.
    x4 = np.dot(vec_12, unit_x_axis)

    y1 = np.dot(vec_13, unit_y_axis)
    y2 = np.dot(vec_14, unit_y_axis)
    y3 = 0.
    y4 = np.dot(vec_12, unit_y_axis)

    # x1 = 0.
    # x2 = np.dot(vec_12, unit_x_axis)
    # x3 = np.dot(vec_13, unit_x_axis)
    # x4 = np.dot(vec_14, unit_x_axis)

    # y1 = 0.
    # y2 = np.dot(vec_12, unit_y_axis)
    # y3 = np.dot(vec_13, unit_y_axis)
    # y4 = np.dot(vec_14, unit_y_axis)

    coord_loc = np.array([[x1, y1],
                          [x2, y2],
                          [x3, y3],
                          [x4, y4]], dtype=float)

    return coord_loc


class QUADRANGLE_4(Element2D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):

        self.model = model
        self.dof_per_node = dof_per_node
        self.nodes_per_element = nodes_per_element

        self.connectivities = None
        self.element_label = ""

        self.local_dof = np.arange(dof_per_node, dtype=int)

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    @property
    def dof_per_element(self):
        return self.nodes_per_element * self.dof_per_node


    def define_integration_points(self, integration_points: int = 4):
        """ 
        Defines the integration points and their respective weights
        for the numerical integration processing.
        """
        self.nint = integration_points
        self.num_int_data = self.integration_points_data_for_quadrangles(integration_points)
        self.wps = self.num_int_data[:, -1].reshape(-1, 1, 1)


    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """

        ##NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015

        ## coordinates from integration points
        xi_1 = self.num_int_data[:, 0]
        xi_2 = self.num_int_data[:, 1]

        ## shape functions (Atalla and Sgard, 2015, pg. 174)
        phi = np.zeros((self.nint, self.nodes_per_element), dtype=float)
        phi[:, 0] = (1 - xi_1)*(1 - xi_2) / 4      # ->      (-1.0, -1.0)   Node 1
        phi[:, 1] = (1 + xi_1)*(1 - xi_2) / 4      # ->      ( 1.0, -1.0)   Node 2
        phi[:, 2] = (1 + xi_1)*(1 + xi_2) / 4      # ->      ( 1.0,  1.0)   Node 3
        phi[:, 3] = (1 - xi_1)*(1 + xi_2) / 4      # ->      (-1.0,  1.0)   Node 4

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((self.nint, 2, self.nodes_per_element), dtype=float)
        dphi[:, 0, 0] = -(1 - xi_2) / 4 
        dphi[:, 0, 1] =  (1 - xi_2) / 4
        dphi[:, 0, 2] =  (1 + xi_2) / 4
        dphi[:, 0, 3] = -(1 + xi_2) / 4

        dphi[:, 1, 0] = -(1 - xi_1) / 4
        dphi[:, 1, 1] = -(1 + xi_1) / 4
        dphi[:, 1, 2] =  (1 + xi_1) / 4
        dphi[:, 1, 3] =  (1 - xi_1) / 4

        self.phi = phi
        self.dphi = dphi


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
        
        X3 = self.nodal_coordinates[self.connectivities[:, 2], 1]
        Y3 = self.nodal_coordinates[self.connectivities[:, 2], 2]
        Z3 = self.nodal_coordinates[self.connectivities[:, 2], 3]

        X4 = self.nodal_coordinates[self.connectivities[:, 3], 1]
        Y4 = self.nodal_coordinates[self.connectivities[:, 3], 2]
        Z4 = self.nodal_coordinates[self.connectivities[:, 3], 3]

        vec_12 = np.array([X2-X1, Y2-Y1, Z2-Z1]).T
        vec_13 = np.array([X3-X1, Y3-Y1, Z3-Z1]).T
        vec_14 = np.array([X4-X1, Y4-Y1, Z4-Z1]).T

        loc_x_axis = vec_12.copy()
        loc_z_axis = np.cross(loc_x_axis, vec_14, axis=1)
        loc_y_axis = np.cross(loc_z_axis, loc_x_axis, axis=1)

        nx = np.linalg.norm(loc_x_axis, axis=1).reshape(-1, 1, 1)
        ny = np.linalg.norm(loc_y_axis, axis=1).reshape(-1, 1, 1)

        unit_x_axis = loc_x_axis.reshape(-1, 1, 3) / nx
        unit_y_axis = loc_y_axis.reshape(-1, 1, 3) / ny

        unit_x_axis = unit_x_axis.reshape(-1, 3)
        unit_y_axis = unit_y_axis.reshape(-1, 3)

        x1 = np.sum(vec_13 * unit_x_axis, axis=1)
        x2 = np.sum(vec_14 * unit_x_axis, axis=1)
        x3 = 0.
        x4 = np.sum(vec_12 * unit_x_axis, axis=1)

        y1 = np.sum(vec_13 * unit_y_axis, axis=1)
        y2 = np.sum(vec_14 * unit_y_axis, axis=1)
        y3 = 0.
        y4 = np.sum(vec_12 * unit_y_axis, axis=1)

        # x1 = 0.
        # x2 = np.sum(vec_12 * unit_x_axis, axis=1)
        # x3 = np.sum(vec_13 * unit_x_axis, axis=1)
        # x4 = np.sum(vec_14 * unit_x_axis, axis=1)

        # y1 = 0.
        # y2 = np.sum(vec_12 * unit_y_axis, axis=1)
        # y3 = np.sum(vec_13 * unit_y_axis, axis=1)
        # y4 = np.sum(vec_14 * unit_y_axis, axis=1)

        nel = self.connectivities.shape[0]
        coord_loc = np.zeros((nel, self.nodes_per_element, 2), dtype=float)

        coord_loc[:, 0, 0] = x1
        coord_loc[:, 0, 1] = y1
        coord_loc[:, 1, 0] = x2
        coord_loc[:, 1, 1] = y2
        coord_loc[:, 2, 0] = x3
        coord_loc[:, 2, 1] = y3
        coord_loc[:, 3, 0] = x4
        coord_loc[:, 3, 1] = y4

        return coord_loc


    def reorder_connect(self, connect_face: np.ndarray):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivities = connect_face[:, [0, 1, 2, 3]]