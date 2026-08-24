
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
    
    X1, X2, X3, X4, X5, X6, X7, X8 = coords[:, 1]
    Y1, Y2, Y3, Y4, Y5, Y6, Y7, Y8 = coords[:, 2]
    Z1, Z2, Z3, Z4, Z5, Z6, Z7, Z8 = coords[:, 3]

    vec_12 = np.array([X2-X1, Y2-Y1, Z2-Z1]).T
    vec_13 = np.array([X3-X1, Y3-Y1, Z3-Z1]).T
    vec_14 = np.array([X4-X1, Y4-Y1, Z4-Z1]).T
    vec_15 = np.array([X5-X1, Y5-Y1, Z5-Z1]).T
    vec_16 = np.array([X6-X1, Y6-Y1, Z6-Z1]).T
    vec_17 = np.array([X7-X1, Y7-Y1, Z7-Z1]).T
    vec_18 = np.array([X8-X1, Y8-Y1, Z8-Z1]).T

    loc_x_axis = vec_12.copy()
    loc_z_axis = np.cross(loc_x_axis, vec_14)
    loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

    unit_x_axis = loc_x_axis / np.linalg.norm(loc_x_axis)
    unit_y_axis = loc_y_axis / np.linalg.norm(loc_y_axis)

    x1 = 0.
    x2 = np.dot(vec_12, unit_x_axis)
    x3 = np.dot(vec_13, unit_x_axis)
    x4 = np.dot(vec_14, unit_x_axis)
    x5 = np.dot(vec_15, unit_x_axis)
    x6 = np.dot(vec_16, unit_x_axis)
    x7 = np.dot(vec_17, unit_x_axis)
    x8 = np.dot(vec_18, unit_x_axis)

    y1 = 0.
    y2 = np.dot(vec_12, unit_y_axis)
    y3 = np.dot(vec_13, unit_y_axis)
    y4 = np.dot(vec_14, unit_y_axis)
    y5 = np.dot(vec_15, unit_y_axis)
    y6 = np.dot(vec_16, unit_y_axis)
    y7 = np.dot(vec_17, unit_y_axis)
    y8 = np.dot(vec_18, unit_y_axis)

    coord_loc = np.array([[x1, y1],
                          [x2, y2],
                          [x3, y3],
                          [x4, y4],
                          [x5, y5],
                          [x6, y6],
                          [x7, y7],
                          [x8, y8]], dtype=float)

    return coord_loc


class QUADRANGLE_8(Element2D):

    def __init__(self, model: "Model", dof_per_node: int):

        self.model = model

        self.nodes_per_element = 8
        self.dof_per_node = dof_per_node

        self.connectivities = None
        self.element_label = ""
        self.nodal_coordinates = self.model.mesh.nodal_coordinates

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
        phi = np.zeros((self.nint, 1, self.nodes_per_element), dtype=float)
        phi[:, 0, 0] = (1 - xi_1)*(1 - xi_2)*(-xi_1 - xi_2 - 1) / 4      # ->      (-1.0, -1.0)   Node 1
        phi[:, 0, 1] = (1 + xi_1)*(1 - xi_2)*( xi_1 - xi_2 - 1) / 4      # ->      ( 1.0, -1.0)   Node 2
        phi[:, 0, 2] = (1 + xi_1)*(1 + xi_2)*( xi_1 + xi_2 - 1) / 4      # ->      ( 1.0,  1.0)   Node 3
        phi[:, 0, 3] = (1 - xi_1)*(1 + xi_2)*(-xi_1 + xi_2 - 1) / 4      # ->      (-1.0,  1.0)   Node 4
        phi[:, 0, 4] = (1 - xi_1**2)*(1 - xi_2) / 2                      # ->      ( 0.0, -1.0)   Node 5
        phi[:, 0, 5] = (1 + xi_1)*(1 - xi_2**2) / 2                      # ->      ( 1.0,  0.0)   Node 6
        phi[:, 0, 6] = (1 - xi_1**2)*(1 + xi_2) / 2                      # ->      ( 0.0,  1.0)   Node 7
        phi[:, 0, 7] = (1 - xi_1)*(1 - xi_2**2) / 2                      # ->      (-1.0,  0.0)   Node 8

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((self.nint, 2, self.nodes_per_element), dtype=float)
        dphi[:, 0, 0] = (1 - xi_2)*(2*xi_1 + xi_2) / 4 
        dphi[:, 0, 1] = (1 - xi_2)*(2*xi_1 - xi_2) / 4
        dphi[:, 0, 2] = (1 + xi_2)*(2*xi_1 + xi_2) / 4
        dphi[:, 0, 3] = (1 + xi_2)*(2*xi_1 - xi_2) / 4
        dphi[:, 0, 4] = -(2*xi_1)*(1 - xi_2) / 2
        dphi[:, 0, 5] =  (1 - xi_2**2) / 2
        dphi[:, 0, 6] = -(2*xi_1)*(1 + xi_2) / 2
        dphi[:, 0, 7] = -(1 - xi_2**2) / 2

        dphi[:, 1, 0] = (1 - xi_1)*( xi_1 + 2*xi_2) / 4
        dphi[:, 1, 1] = (1 + xi_1)*(-xi_1 + 2*xi_2) / 4
        dphi[:, 1, 2] = (1 + xi_1)*( xi_1 + 2*xi_2) / 4
        dphi[:, 1, 3] = (1 - xi_1)*(-xi_1 + 2*xi_2) / 4
        dphi[:, 1, 4] = -(1 - xi_2**2) / 2
        dphi[:, 1, 5] = -(1 + xi_1)*(2*xi_2) / 2
        dphi[:, 1, 6] =  (1 - xi_2**2) / 2
        dphi[:, 1, 7] = -(1 - xi_1)*(2*xi_2) / 2

        self.phi = phi
        self.dphi = dphi


    def get_jacobian_determinant(self, int_point: int, coords: np.ndarray, return_vectors: bool = False):
        """
        This method evaluates the Jacobian determinant for the i-th integrarion point.
        
        Parameters
        ----------

        int_point: int
            The integration point to be evaluated.

        coords:  np.ndarray
            A three-dimensional coordinate matrix of the element. 

        return_vectors: bool, optional
            Use this argument to control when the normal unitary, g_xi and g_eta vectors are returned.

        Return
        ------
        det_jac: np.ndarray
            The Jacobian determinant at the i-th integration point.

        normal_vector: np.ndarray,  optional
            The unitary normal vectors at the i-th integration point
            (returned if the return_vectors argument is True).

        g_xi: np.ndarray,  optional
            The tangent vector in xi direction at the i-th integration point
            (returned if the return_vectors argument is True).

        g_eta: np.ndarray,  optional
            The tangent vector in eta direction at the i-th integration point
            (returned if the return_vectors argument is True).

        """

        # vectors tangent to the element's surface
        g_xi = self.dphi[int_point, 0, :] @ coords
        g_eta = self.dphi[int_point, 1, :] @ coords

        # normal vector for the i-th integration point
        normal_vector = np.cross(g_xi, g_eta).reshape(-1, 1)

        # determinant of Jacobian matrix
        det_jac = np.linalg.norm(normal_vector)

        if not return_vectors:
            return det_jac

        # normalize the element normal vector for the i-th integration point
        e_normal = normal_vector / det_jac

        return det_jac, e_normal, g_xi, g_eta


    def get_stacked_jacobian_determinant(self, int_point: int, coords: np.ndarray, return_vectors: bool = False):
        """
        This method evaluates the Jacobian determinant for the i-th integrarion point.
        
        Parameters
        ----------

        int_point: int
            The integration point to be evaluated.

        coords:  np.ndarray
            A three-dimensional coordinate matrix in which each plane contains
            the nodal coordinates of an element. 

        return_vectors: bool, optional
            Use this argument to control when the normal unitary, g_xi and g_eta vectors are returned.

        Return
        ------
        det_jac: np.ndarray
            A stacked vector with the Jacobian determinant of all elements evaluated
            at the i-th integration point.

        normal_vector: np.ndarray,  optional
            The unitary normal vectors at the i-th integration point for all elements
            (returned if the return_vectors argument is True).

        g_xi: np.ndarray,  optional
            The tangent vector in xi direction at the i-th integration point for all elements
            (returned if the return_vectors argument is True).

        g_eta: np.ndarray,  optional
            The tangent vector in eta direction at the i-th integration point for all elements
            (returned if the return_vectors argument is True).
        """

        # vectors tangent to the element's surface
        g_xi = self.dphi[int_point, 0, :] @ coords
        g_eta = self.dphi[int_point, 1, :] @ coords

        # compute the stacked normal vectors
        normal_vector = np.cross(g_xi, g_eta)

        # calculate the stacked Jacobian determinants
        det_jac = np.linalg.norm(normal_vector, axis=1)

        if not return_vectors:
            return det_jac

        # normalize the elements normal vectors for the i-th integration point
        e_normal = normal_vector / det_jac

        return det_jac, e_normal, g_xi, g_eta


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

        X5 = self.nodal_coordinates[self.connectivities[:, 4], 1]
        Y5 = self.nodal_coordinates[self.connectivities[:, 4], 2]
        Z5 = self.nodal_coordinates[self.connectivities[:, 4], 3]

        X6 = self.nodal_coordinates[self.connectivities[:, 5], 1]
        Y6 = self.nodal_coordinates[self.connectivities[:, 5], 2]
        Z6 = self.nodal_coordinates[self.connectivities[:, 5], 3]

        X7 = self.nodal_coordinates[self.connectivities[:, 6], 1]
        Y7 = self.nodal_coordinates[self.connectivities[:, 6], 2]
        Z7 = self.nodal_coordinates[self.connectivities[:, 6], 3]

        X8 = self.nodal_coordinates[self.connectivities[:, 7], 1]
        Y8 = self.nodal_coordinates[self.connectivities[:, 7], 2]
        Z8 = self.nodal_coordinates[self.connectivities[:, 7], 3]

        vec_12 = np.array([X2-X1, Y2-Y1, Z2-Z1]).T
        vec_13 = np.array([X3-X1, Y3-Y1, Z3-Z1]).T
        vec_14 = np.array([X4-X1, Y4-Y1, Z4-Z1]).T
        vec_15 = np.array([X5-X1, Y5-Y1, Z5-Z1]).T
        vec_16 = np.array([X6-X1, Y6-Y1, Z6-Z1]).T
        vec_17 = np.array([X7-X1, Y7-Y1, Z7-Z1]).T
        vec_18 = np.array([X8-X1, Y8-Y1, Z8-Z1]).T

        loc_x_axis = vec_12.copy()
        loc_z_axis = np.cross(loc_x_axis, vec_14, axis=1)
        loc_y_axis = np.cross(loc_z_axis, loc_x_axis, axis=1)

        nx = np.linalg.norm(loc_x_axis, axis=1).reshape(-1, 1, 1)
        ny = np.linalg.norm(loc_y_axis, axis=1).reshape(-1, 1, 1)

        unit_x_axis = loc_x_axis.reshape(-1, 1, 3) / nx
        unit_y_axis = loc_y_axis.reshape(-1, 1, 3) / ny

        unit_x_axis = unit_x_axis.reshape(-1, 3)
        unit_y_axis = unit_y_axis.reshape(-1, 3)

        x1 = 0.
        x2 = np.sum(vec_12 * unit_x_axis, axis=1)
        x3 = np.sum(vec_13 * unit_x_axis, axis=1)
        x4 = np.sum(vec_14 * unit_x_axis, axis=1)
        x5 = np.sum(vec_15 * unit_x_axis, axis=1)
        x6 = np.sum(vec_16 * unit_x_axis, axis=1)
        x7 = np.sum(vec_17 * unit_x_axis, axis=1)
        x8 = np.sum(vec_18 * unit_x_axis, axis=1)

        y1 = 0.
        y2 = np.sum(vec_12 * unit_y_axis, axis=1)
        y3 = np.sum(vec_13 * unit_y_axis, axis=1)
        y4 = np.sum(vec_14 * unit_y_axis, axis=1)
        y5 = np.sum(vec_15 * unit_y_axis, axis=1)
        y6 = np.sum(vec_16 * unit_y_axis, axis=1)
        y7 = np.sum(vec_17 * unit_y_axis, axis=1)
        y8 = np.sum(vec_18 * unit_y_axis, axis=1)

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
        coord_loc[:, 4, 0] = x5
        coord_loc[:, 4, 1] = y5
        coord_loc[:, 5, 0] = x6
        coord_loc[:, 5, 1] = y6
        coord_loc[:, 6, 0] = x7
        coord_loc[:, 6, 1] = y7
        coord_loc[:, 7, 0] = x8
        coord_loc[:, 7, 1] = y8

        return coord_loc


    def stacked_matrices_NtN(self) -> np.ndarray:
        """
        This method processes all elementary matrices and returns them
        in the stacked array form.

        Returns
        -------
        int2d_NtN: np.ndarray
            The array containing the stacked elementary matrices.
        """

        # compute local coordinates for all elements
        local_coords = self.get_stacked_local_coordinates()

        # initialize variable
        int2d_NtN = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrices of all elements
            JAC_stacked = self.dphi[i, :, :] @ local_coords

            # Jacobian determinants and inverses of all elements
            det_jacs = self.get_detJAC(JAC_stacked)

            # shape functions
            N = self.phi[i, :, :]

            int2d_NtN += N.T @ N * (det_jacs * self.wps[i])

        return int2d_NtN


    def stacked_matrices_NtN_and_BtB(self) -> np.ndarray:
        """
        This method processes all elementary matrices for mass source
        and returns them in the stacked array form.

        Returns
        -------
        Nt_N_stacked: np.ndarray
            The array containing the elementary stacked matrices int(Nt @ N, gamma_s).

        Bt_B_stacked: np.ndarray
            The array containing the elementary stacked matrices int(Bt @ B, gamma_s).
        """

        # compute local coordinates for all elements
        local_coords = self.get_stacked_local_coordinates()

        # initialize variables
        int2d_NtN = 0.
        int2d_BtB = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrices of all elements
            JAC_stacked = self.dphi[i, :, :] @ local_coords

            # Jacobian determinants and inverses of all elements
            det_jacs, inv_jacs = self.get_detJAC_and_invJAC(JAC_stacked)

            # shape functions
            N = self.phi[i, :, :]
            N_t = N.T

            # derivative of shape functions
            B = inv_jacs @ self.dphi[i, :, :]
            B_t = np.transpose(B, axes=(0, 2, 1))

            int2d_NtN += N_t @ N * (det_jacs * self.wps[i])
            int2d_BtB += B_t @ B * (det_jacs * self.wps[i])

        return int2d_NtN, int2d_BtB


    def reorder_connect(self, connect_face: np.ndarray):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivities = connect_face[:, [0, 1, 2, 3, 4, 5, 6, 7]]