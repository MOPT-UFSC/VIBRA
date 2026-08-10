
from vibra.engine.elements.surface_elements import Element2D

from typing import TYPE_CHECKING
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
    
    XX1, XX2, XX3 = coords[:, 1]
    YY1, YY2, YY3 = coords[:, 2]
    ZZ1, ZZ2, ZZ3 = coords[:, 3]

    vec_12 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
    vec_13 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T

    loc_x_axis = vec_12.copy()
    loc_z_axis = np.cross(loc_x_axis, vec_13)
    loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

    unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
    unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

    x1 = 0. 
    x2 = np.dot(vec_12,unit_x_axis)
    x3 = np.dot(vec_13,unit_x_axis)
    y1 = 0.
    y2 = np.dot(vec_12,unit_y_axis)
    y3 = np.dot(vec_13,unit_y_axis)

    coord_loc = np.array([[x1, y1],
                          [x2, y2],
                          [x3, y3]], dtype=float)

    return coord_loc


class ACT_TRIANGLE_3(Element2D):

    NODES_PER_ELEMENT = 3
    DOF_PER_NODE = 1
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivities = None
        self.element_label = "acoustic_triangular_3"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def define_integration_points(self, integration_points: int = 3):
        """ 
        Defines the integration points and their respective weights
        for the numerical integration processing.
        """
        self.nint = integration_points
        self.num_int_data = self.integration_points_data_for_triangles(integration_points)
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

        # define coordiante l4
        xi_3 = 1 - xi_1 - xi_2

        ## shape functions (Atalla and Sgard, 2015, pg. 173)
        phi = np.zeros((self.nint, 1, self.NODES_PER_ELEMENT), dtype=float)
        phi[:, 0, 0] = xi_1      # ->      (1.0, 0.0)   Node 1
        phi[:, 0, 1] = xi_2      # ->      (0.0, 1.0)   Node 2
        phi[:, 0, 2] = xi_3      # ->      (0.0, 0.0)   Node 3

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((2, self.NODES_PER_ELEMENT), dtype=float)
        dphi[0, 0] = 1
        dphi[0, 1] = 0
        dphi[0, 2] = -1

        dphi[1, 0] = 0
        dphi[1, 1] = 1
        dphi[1, 2] = -1

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

        vec_21 = np.array([X2-X1, Y2-Y1, Z2-Z1]).T
        vec_31 = np.array([X3-X1, Y3-Y1, Z3-Z1]).T

        loc_x_axis = vec_21.copy()
        loc_z_axis = np.cross(loc_x_axis, vec_31, axis=1)
        loc_y_axis = np.cross(loc_z_axis, loc_x_axis, axis=1)

        nx = np.linalg.norm(loc_x_axis, axis=1).reshape(-1, 1, 1)
        ny = np.linalg.norm(loc_y_axis, axis=1).reshape(-1, 1, 1)

        unit_x_axis = loc_x_axis.reshape(-1, 1, 3) / nx
        unit_y_axis = loc_y_axis.reshape(-1, 1, 3) / ny

        unit_x_axis = unit_x_axis.reshape(-1, 3)
        unit_y_axis = unit_y_axis.reshape(-1, 3)

        x2 = np.sum(vec_21 * unit_x_axis, axis=1)
        x3 = np.sum(vec_31 * unit_x_axis, axis=1)

        y2 = np.sum(vec_21 * unit_y_axis, axis=1)
        y3 = np.sum(vec_31 * unit_y_axis, axis=1)

        nel = self.connectivities.shape[0]
        coord_loc = np.zeros((nel, 3, 2), dtype=float)

        coord_loc[:, 1, 0] = x2
        coord_loc[:, 1, 1] = y2
        coord_loc[:, 2, 0] = x3
        coord_loc[:, 2, 1] = y3

        return coord_loc


    def get_stacked_element_face_normals(self) -> np.ndarray:
        """
        This method processes the stacked element face normals.
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

        P2P1 = np.array([X2-X1, Y2-Y1, Z2-Z1]).T
        P3P1 = np.array([X3-X1, Y3-Y1, Z3-Z1]).T

        cross = np.cross(P2P1, P3P1, axis=1)
        norm_cross = np.linalg.norm(cross, axis=1)

        norm_cross = norm_cross.reshape(-1, 1, 1)
        cross = cross.reshape(-1, 1, 3)
        
        normals = cross / norm_cross

        return normals


    def stacked_matrices_NtN(self) -> np.ndarray:
        """
        This method processes all elementary matrices and returns them
        in the stacked array form.

        Returns
        -------
        int2d_NtN: np.ndarray
            The array containing the stacked elementary matrices.
        """

        # NOTE: the shape functions' derivatives are constant for all
        # integration points; this is why the Jacobian matrix-related
        # calculations are being performed out of the integration loop.

        # compute local coordinates for all elements
        local_coords = self.get_stacked_local_coordinates()

        # Jacobian matrices of all elements
        JAC_stacked = self.dphi @ local_coords

        # Jacobian determinants and inverses of all elements
        det_jacs = self.get_detJAC(JAC_stacked)

        # initialize variable
        int2d_NtN = 0.

        # integration loop
        for i in range(self.nint):

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

        # NOTE: the shape functions' derivatives are constant for all
        # integration points; this is why the Jacobian matrix-related
        # calculations are being performed out of the integration loop.

        # compute local coordinates for all elements
        local_coords = self.get_stacked_local_coordinates()

        # Jacobian matrices of all elements
        JAC_stacked = self.dphi @ local_coords

        # Jacobian determinants and inverses of all elements
        det_jacs, inv_jacs = self.get_detJAC_and_invJAC(JAC_stacked)

        # derivative of shape functions
        B = inv_jacs @ self.dphi
        B_t = np.transpose(B, axes=(0, 2, 1))

        # initialize variables
        int2d_NtN = 0.
        int2d_BtB = 0.

        # integration loop
        for i in range(self.nint):

            # shape functions
            N = self.phi[i, :, :]
            N_t = N.T

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

        # NOTE: the shape functions' derivatives are constant for all
        # integration points; this is why the Jacobian matrix-related
        # calculations are being performed out of the integration loop.

        # element nodal coordinates
        coords = self.nodal_coordinates[self.connectivities[el_index, :], :]

        # nodal coordinates in the local CS
        coord_lcs = get_local_coordinates(coords)

        # Jacobian matrix
        JAC = self.dphi @ coord_lcs

        # determinant of Jacobia matrix
        det_jac = self.get_detJAC(JAC)

        # initialize the variable Fe
        Fe = 0.

        # integration loop
        for i in range(self.nint):

            # shape functions
            N = self.phi[i, :, :]

            Fe += load * N.T * (det_jac * self.wps[i])

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

        # NOTE: the shape functions' derivatives are constant for all
        # integration points; this is why the Jacobian matrix-related
        # calculations are being performed out of the integration loop.

        # element nodal coordinates
        coords = self.nodal_coordinates[e_connect, :]

        # nodal coordinates in the local CS
        coord_lcs = get_local_coordinates(coords)

        # Jacobian matrix
        JAC = self.dphi @ coord_lcs

        # determinant of Jacobia matrix
        det_jac = self.get_detJAC(JAC)

        # initialize the variable We
        We = 0.

        # integration loop
        for i in range(self.nint):

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

        # NOTE: the shape functions' derivatives are constant for all
        # integration points; this is why the Jacobian matrix-related
        # calculations are being performed out of the integration loop.

        # compute local coordinates for all elements
        local_coords = self.get_stacked_local_coordinates()

        # Jacobian matrices of all elements
        JAC_stacked = self.dphi @ local_coords

        # Jacobian determinants and inverses of all elements
        det_jacs = self.get_detJAC(JAC_stacked)

        # initialize variable
        acoustic_load = 0.

        # integration loop
        for i in range(self.nint):

            # shape functions
            N = self.phi[i, :, :]

            acoustic_load += np.sum(-e_normals @ (N @ Pe) * (det_jacs * self.wps[i]), axis=0)

        return acoustic_load


    def reorder_connect(self, connect_face):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """

        self.connectivities = connect_face[:, [0, 1, 2]]


    def generate_ind_rows_cols(self, connect_face):
        """
        This method processess the dof indices (rows and columns) 
        for assembly
        """

        self.reorder_connect(connect_face)
        dof, edof = self.DOF_PER_NODE, self.DOF_PER_ELEMENT
        ind_dof = dof * self.connectivities[:, :]

        vect_indices = ind_dof.flatten()
        ind_rows_face = ((np.tile(vect_indices, (edof,1))).T).flatten()
        ind_cols_face = (np.tile(ind_dof, edof)).flatten()

        return ind_rows_face, ind_cols_face


def get_shape_functions_and_derivatives(ssx: np.ndarray, ttx: np.ndarray):

    """
    This function returns the shape functions and its derivatives.

    Parameters
    ----------
    ssx: np.ndarray
        The x coordinates of the integration points.

    ttx: np.ndarray
        The y coordinates of the integration points.

    Returns
    -------
    phi: np.ndarray
        The shape functions evaluated in the integration points.

    dphi: np.ndarray
        The shape functions derivatives.
    """

    # shape functions
    phi = np.array([1 - ssx - ttx, ttx, ssx], dtype=float).T

    # shape functions derivatives
    dphi = np.array([[-1, 0, 1],
                     [-1, 1, 0]], dtype=float)

    return phi, dphi