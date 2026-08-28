
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

    def __init__(self, model: "Model", dof_per_node: int):

        self.model = model

        self.nodes_per_element = 4
        self.dof_per_node = dof_per_node

        self.connectivities = None
        self.element_label = ""
        self.nodal_coordinates = self.model.mesh.nodal_coordinates

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
        phi = np.zeros((self.nint, 1, self.nodes_per_element), dtype=float)
        phi[:, 0, 0] = (1 - xi_1)*(1 - xi_2) / 4      # ->      (-1.0, -1.0)   Node 1
        phi[:, 0, 1] = (1 + xi_1)*(1 - xi_2) / 4      # ->      ( 1.0, -1.0)   Node 2
        phi[:, 0, 2] = (1 + xi_1)*(1 + xi_2) / 4      # ->      ( 1.0,  1.0)   Node 3
        phi[:, 0, 3] = (1 - xi_1)*(1 + xi_2) / 4      # ->      (-1.0,  1.0)   Node 4

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


    def load_vector(self, el_index: int, load: float = 1.0) -> np.ndarray:
        """ 
        This method computes the elementary load vector.

        Parameters
        ----------
        el_index: int
            The element index.

        load: float, optional
            The load vector.

        Returns
        -------
        Fe: np.ndarray
            The elementary load vector.
        """

        # element nodal coordinates
        coords = self.nodal_coordinates[self.connectivities[el_index, :], :]

        # nodal coordinates in the local CS
        coord_lcs = get_local_coordinates(coords)

        # initialize the variable Fe
        Fe = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrix
            JAC = self.dphi[i, :, :] @ coord_lcs

            # determinant of Jacobia matrix
            det_JAC = self.get_detJAC(JAC)

            # shape functions
            N = self.phi[i, :, :]

            Fe += load * N.T * (det_JAC * self.wps[i])

        return Fe


    def elementary_sound_power(self, e_connect: np.ndarray, P_e: np.ndarray, Vn_e: np.ndarray) -> np.ndarray:
        """ 
        This method computes the elementary load vector.

        Parameters
        ----------
        el_index: int
            The element index.

        P_e: np.ndarray
            The righ stacked vector (complex-conjugate of pressures).
    
        Vn_e: np.ndarray
            The left stacked vector (complex-conjugate of normal particle velocities).

        Returns
        -------
        We: np.ndarray
            The elementary sound power vector.
        """

        # element nodal coordinates
        coords = self.nodal_coordinates[e_connect, :]

        # nodal coordinates in the local CS
        local_coords = get_local_coordinates(coords)

        # initialize the variable We
        We = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrices of all elements
            JAC = self.dphi[i, :, :] @ local_coords

            # determinant of Jacobian matrix
            det_jac = self.get_detJAC(JAC)

            # shape functions
            N = self.phi[i, :, :]

            We += P_e @ (N.T @ N) @ Vn_e * (det_jac * self.wps[i])

        return We.flatten()


    def acoustic_pressure_load(self, e_normals: np.ndarray, nodal_solution: np.ndarray) -> np.ndarray:
        """ 
        This method computes the acoustic pressure loads over a surface.

        Parameters
        ----------
        e_normals: np.ndarray
            The stacked surface elements normals vectors.

        nodal_solution: np.ndarray
            The acoustic nodal_solution array.

        Returns
        -------
        acoustic_load: np.ndarray
            The acoustic presure loads integrated over a surface.
        """

        # stack all elements nodal pressures 
        pressures = np.array([nodal_solution[node_ids, :] for node_ids in self.connectivities.T], dtype=complex)

        # stack the element nodal pressures in format [n_el, DOFS_PER_ELEMENT, n_freq]
        Pe = pressures.transpose(1, 0, 2)

        # compute local coordinates for all elements
        local_coords = self.get_stacked_local_coordinates()

        # initialize variable
        acoustic_load = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrices of all elements
            JAC_stacked = self.dphi[i, :, :] @ local_coords

            # Jacobian determinants and inverses of all elements
            det_jacs, _ = self.get_detJAC_and_invJAC(JAC_stacked)

            # shape functions
            N = self.phi[i, :, :]

            acoustic_load += np.sum(-e_normals @ (N @ Pe) * (det_jacs * self.wps[i]), axis=0)

        return acoustic_load


    def reorder_connect(self, connect_face: np.ndarray):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivities = connect_face[:, [0, 1, 2, 3]]