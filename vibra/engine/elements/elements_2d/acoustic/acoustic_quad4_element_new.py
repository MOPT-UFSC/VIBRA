
from vibra.engine.elements.surface_elements import Element2D

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


def get_detJAC(JAC: np.ndarray) -> float:
    """
    This function computes the determinant of the Jacobian
    matrix in both stacked and non-stacked matrices form.

    Parameter
    ---------
    JAC: np.ndarray
        The Jacobian 2D or 3D matrix.
    
    Return
    ------
    det_jac: float
        The determinant of the Jacobian matrix.
    """
    if len(JAC.shape) == 3:
        det_jac = JAC[:, 0, 0] * JAC[:, 1, 1]  - JAC[:, 0, 1] * JAC[:, 1, 0]
        return det_jac.reshape(-1, 1, 1)

    else:
        det_jac = JAC[0, 0] * JAC[1, 1]  - JAC[0, 1] * JAC[1, 0]  
        return det_jac


def get_stacked_detJAC_and_invJAC(JAC: np.ndarray) -> np.ndarray:
    """
    This function computes the determinants and inverses
    of Jacobian matrices in stacked form.

    Parameters
    ----------
    JAC: np.array
        The stacked Jacobian matrices.

    Returns
    -------
    det_jacs: np.ndarray
        The stacked determinants of Jacobian matrices.

    inv_jacs: np.ndarray
        The stacked inverse of Jacobian matrices.

    """

    # determinant of the Jacobian matrix
    det_jacs = JAC[:, 0, 0] * JAC[:, 1, 1]  - JAC[:, 0, 1] * JAC[:, 1, 0] 
    det_jacs = det_jacs.reshape(-1, 1, 1)

    # the adjoint matrix AUJJ
    AUJJ = np.zeros((JAC.shape[0], 2, 2), dtype=float)

    AUJJ[:, 0, 0] =  JAC[:, 1, 1]
    AUJJ[:, 0, 1] = -JAC[:, 0, 1]
    AUJJ[:, 1, 0] = -JAC[:, 1, 0]
    AUJJ[:, 1, 1] =  JAC[:, 0, 0]

    # inverse of the Jacobian matrix
    inv_jacs = (1 / det_jacs) * AUJJ

    return det_jacs, inv_jacs


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
    
    XX1, XX2, XX3, XX4 = coords[:, 1]
    YY1, YY2, YY3, YY4 = coords[:, 2]
    ZZ1, ZZ2, ZZ3, ZZ4 = coords[:, 3]

    vec_12 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
    vec_13 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T
    vec_14 = np.array([XX4-XX1, YY4-YY1, ZZ4-ZZ1]).T

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

    coord_loc = np.array([[x1, y1],
                          [x2, y2],
                          [x3, y3],
                          [x4, y4]], dtype=float)

    return coord_loc


# def shapeFZ4(ssx, ttx):
#     """This function returns the shape functions and its derivatives."""

#     # shape functions
#     denominator = 4
#     phi = np.array([(1.+ssx)*(1.+ttx), 
#                     (1.-ssx)*(1.+ttx), 
#                     (1.-ssx)*(1.-ttx), 
#                     (1.+ssx)*(1.-ttx)], dtype=float).T / denominator

#     # derivatives of shape functions
#     dphi = np.zeros((2, 4), dtype=float)
#     dphi[0,:] =  np.array([(1.+ttx), -(1.+ttx), -(1.-ttx), (1.-ttx)])
#     dphi[1,:] =  np.array([(1.+ssx), (1.-ssx), -(1.-ssx), -(1.+ssx)])
#     dphi = dphi / denominator

#     return phi, dphi


# def get_detJAC(JAC: np.ndarray):
#     # Inverse Jacobian
#     detJAC = JAC[0, 0] * JAC[1, 1]  - JAC[0, 1] * JAC[1, 0]  
#     return detJAC


# def get_detJAC_3D(JAC: np.ndarray):
#     # Inverse Jacobian
#     detJAC = JAC[:, 0, 0] * JAC[:, 1, 1]  - JAC[:, 0, 1] * JAC[:, 1, 0]  
#     return detJAC.reshape(-1, 1, 1)


def get_local_coordinates_old(coords):
    
    XX1, XX2, XX3, XX4 = coords[:, 1]
    YY1, YY2, YY3, YY4 = coords[:, 2]
    ZZ1, ZZ2, ZZ3, ZZ4 = coords[:, 3]

    vec13 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T
    vec14 = np.array([XX4-XX1, YY4-YY1, ZZ4-ZZ1]).T
    vec12 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T

    # Cosseno de direção
    XX = vec12/np.linalg.norm(vec12)
    vecZZ = np.cross(XX,vec14)
    ZZ = vecZZ/np.linalg.norm(vecZZ)
    vecYY = np.cross(ZZ,XX)
    YY = vecYY/np.linalg.norm(vecYY)
    COSDIR = np.array([XX,YY,ZZ]) 

    loc_x_axis = vec12.copy()
    loc_z_axis = np.cross(loc_x_axis, vec14)
    loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

    unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
    unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

    x1 = np.dot(vec13,unit_x_axis)
    x2 = np.dot(vec14,unit_x_axis)
    x3 = 0
    x4 = np.dot(vec12,unit_x_axis)
    y1 = np.dot(vec13,unit_y_axis)
    y2 = np.dot(vec14,unit_y_axis)
    y3 = 0
    y4 = np.dot(vec12,unit_y_axis)

    coord_loc = np.array([[x1, y1],
                          [x2, y2],
                          [x3, y3],
                          [x4, y4]], dtype=float)

    return coord_loc


class ACT_QUADRANGLE_4(Element2D):

    NODES_PER_ELEMENT = 4
    DOF_PER_NODE = 1
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivities = None
        self.element_label = "acoustic_triangular_3"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def define_integration_points(self, integration_points: int = 4):
        """ 
        Defines the integration points and their respective weights
        for the numerical integration processing.
        """
        if integration_points == 4:
            self.nint = 4
            a = 1 / np.sqrt(3)
            w1 = 1

            self.pint = np.array([[-a, -a],
                                  [ a, -a],
                                  [ a,  a],
                                  [-a,  a]], dtype=float)

            self.wps = 2 * np.array([w1, w1, w1, w1], dtype=float).reshape(-1, 1, 1)
        
        elif integration_points == 9:
            self.nint = 9
            a = np.sqrt(3/5)
            w1 = 25/81
            w2 = 40/81
            w3 = 64/81

            self.pint = np.array([[-a, -a],
                                  [ a, -a],
                                  [ a,  a],
                                  [-a,  a],
                                  [ 0, -a],
                                  [ a,  0],
                                  [ 0,  a],
                                  [-a,  0],
                                  [ 0,  0]], dtype=float)

            self.wps = 2 * np.array([w1, w1, w1, w1, w2, w2, w2, w2, w3], dtype=float).reshape(-1, 1, 1)

        else:
            self.nint = 16
            a = np.sqrt((3 + 2*np.sqrt(6/5)) / 7)
            b = np.sqrt((3 - 2*np.sqrt(6/5)) / 7)

            w1 = 0.1210029932856020
            w2 = 0.4252933030106942
            w3 = 0.2268518518518519

            self.pint = np.array([[-a, -a],
                                  [-a,  a],
                                  [ a,  a],
                                  [ a, -a],
                                  [-b, -b],
                                  [-b,  b],
                                  [ b,  b],
                                  [ b, -b],
                                  [-a, -b],
                                  [-a,  b],
                                  [ a, -b],
                                  [ a,  b],
                                  [-b, -a],
                                  [-b,  a],
                                  [ b,  a],
                                  [ b, -a]], dtype=float)

            self.wps = 2 * np.array([w1, w1, w1, w1, 
                                     w2, w2, w2, w2, 
                                     w3, w3, w3, w3,
                                     w3, w3, w3, w3], dtype=float).reshape(-1, 1, 1)


    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """

        ##NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015

        ## coordinates from integration points
        xi_1 = self.pint[:, 0]
        xi_2 = self.pint[:, 1]

        ## shape functions (Atalla and Sgard, 2015, pg. 174)
        phi = np.zeros((self.nint, 1, self.NODES_PER_ELEMENT), dtype=float)
        phi[:, 0, 0] = (1 - xi_1)*(1 - xi_2) / 4      # ->      (-1.0, -1.0)   Node 1
        phi[:, 0, 1] = (1 + xi_1)*(1 - xi_2) / 4      # ->      ( 1.0, -1.0)   Node 2
        phi[:, 0, 2] = (1 + xi_1)*(1 + xi_2) / 4      # ->      ( 1.0,  1.0)   Node 3
        phi[:, 0, 3] = (1 - xi_1)*(1 + xi_2) / 4      # ->      (-1.0,  1.0)   Node 4

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((self.nint, self.pint.shape[1], self.NODES_PER_ELEMENT), dtype=float)
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

        nel = self.connectivities.shape[0]
        coord_loc = np.zeros((nel, 4, 2), dtype=float)

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
            det_jacs = get_detJAC(JAC_stacked)

            # shape functions
            N = self.phi[i, :, :]

            int2d_NtN += (1 / 2) * N.T @ N * (det_jacs * self.wps[i])

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
            det_jacs, inv_jacs = get_stacked_detJAC_and_invJAC(JAC_stacked)

            # shape functions
            N = self.phi[i, :, :]
            N_t = N.T

            # derivative of shape functions
            B = inv_jacs @ self.dphi[i, :, :]
            B_t = np.transpose(B, axes=(0, 2, 1))

            int2d_NtN += (1 / 2) * N_t @ N * (det_jacs * self.wps[i])
            int2d_BtB += (1 / 2) * B_t @ B * (det_jacs * self.wps[i])

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

        # intialize variable
        Fe = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrix
            JAC = self.dphi[i, :, :] @ coord_lcs

            # determinant of Jacobia matrix
            det_JAC = get_detJAC(JAC)

            # shape functions
            N = self.phi[i, :, :]

            Fe += (1 / 2) * load * N.T * (det_JAC * self.wps[i])

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

        # intialize variable
        We = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrices of all elements
            JAC = self.dphi[i, :, :] @ local_coords

            # determinant of Jacobian matrix
            det_jac = get_detJAC(JAC)

            # shape functions
            N = self.phi[i, :, :]

            We += (1 / 2) * P_e @ (N.T @ N) @ Vn_e * (det_jac * self.wps[i])

        return We.flatten()


    # def matrices_Z(self, el_index, rho=1, impedance=1):
    #     """ Z matrices
    #     """

    #     # element nodal coordiantes
    #     nodal_coords = self.nodal_coordinates[self.connectivities[el_index, :], :]

    #     # nodal coordiantes in the local CS
    #     coord_loc = get_local_coordinates(nodal_coords)

    #     # Jacobian matrix
    #     JAC = self.dphi @ coord_loc
        
    #     # determinant of the Jacobian matrix
    #     detJAC = get_detJAC(JAC)
        
    #     # intialize the variable Ze
    #     Ze = 0.

    #     # integration loop
    #     for i in range(self.nint):
    #         N = self.phi[i, 0, :]
    #         Ze += -(rho / impedance) * N.T @ N * (detJAC[i, :, :]*self.wps)

    #     return Ze


    # def excitation_F(self, el_index, Vn=1):
    #     """ F matrices
    #     """

    #     # element nodal coordiantes
    #     nodal_coords = self.nodal_coordinates[self.connectivities[el_index, :], :]

    #     # nodal coordiantes in the local CS
    #     coord_loc = get_local_coordinates(nodal_coords)

    #     # Jacobian matrix
    #     JAC = self.dphi @ coord_loc
        
    #     # determinant of the Jacobian matrix
    #     detJAC = get_detJAC(JAC)

    #     # initialize the variable Fe
    #     Fe = 0.

    #     # integration loop
    #     for i in range(self.nint):
    #         N = self.phi[i, 0, :]  
    #         Fe += -(1/4) * Vn * N.T * (detJAC[i, :, :] * self.wps)

    #     return Fe


    def reorder_connect(self, connect_face: np.ndarray):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivities = connect_face[:, [0, 1, 2, 3]]


    def generate_ind_rows_cols(self, connect_face):
        """ This method processess the dof indices (rows and columns) for assembly"""

        self.reorder_connect(connect_face)
        dof, edof = self.DOF_PER_NODE, self.DOF_PER_ELEMENT
        ind_dof = dof * self.connectivities[:, :]

        vect_indices = ind_dof.flatten()
        ind_rows_face = ((np.tile(vect_indices, (edof,1))).T).flatten()
        ind_cols_face = (np.tile(ind_dof, edof)).flatten()

        return ind_rows_face, ind_cols_face


    def excitation_F_base(self, ee, Vn=1):
        """ F4 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        coord = self.nodal_coordinates
        connect_face = self.connectivities

        ############## Definir plano de trabalho e adaptar coordenadas para tal plano
        XX1, YY1, ZZ1 = coord[connect_face[ee,0],1], coord[connect_face[ee,0],2], coord[connect_face[ee,0],3]
        XX2, YY2, ZZ2 = coord[connect_face[ee,1],1], coord[connect_face[ee,1],2], coord[connect_face[ee,1],3]
        XX3, YY3, ZZ3 = coord[connect_face[ee,2],1], coord[connect_face[ee,2],2], coord[connect_face[ee,2],3]
        XX4, YY4, ZZ4 = coord[connect_face[ee,3],1], coord[connect_face[ee,3],2], coord[connect_face[ee,3],3]

        vec13 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T
        vec14 = np.array([XX4-XX1, YY4-YY1, ZZ4-ZZ1]).T
        vec12 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T

        #Cosseno de direção
        XX = vec12/np.linalg.norm(vec12)
        vecZZ = np.cross(XX,vec14)
        ZZ = vecZZ/np.linalg.norm(vecZZ)
        vecYY = np.cross(ZZ,XX)
        YY = vecYY/np.linalg.norm(vecYY)
        COSDIR = np.array([XX,YY,ZZ]) 

        loc_x_axis = vec12.copy()
        loc_z_axis = np.cross(loc_x_axis, vec14)
        loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

        unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
        unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

        x1 = np.dot(vec13,unit_x_axis)
        x2 = np.dot(vec14,unit_x_axis)
        x3 = 0
        x4 = np.dot(vec12,unit_x_axis)
        y1 = np.dot(vec13,unit_y_axis)
        y2 = np.dot(vec14,unit_y_axis)
        y3 = 0
        y4 = np.dot(vec12,unit_y_axis)

        coord_loc = np.array([[x1, y1],
                              [x2, y2],
                              [x3, y3],
                              [x4, y4]])
        
        # print(f"base: {coord_loc}")

        ################ Definir pontos de integração 2D
        nint, con, wps = 4, 1/np.sqrt(3), 1
        pint = np.array([[ con,  con],
                         [-con,  con],
                         [-con, -con],
                         [ con, -con]])

        ######################## Inicio da integração na face
        # Fe = np.zeros((4,1),dtype=complex)
        Fe = 0.
        N = np.zeros((1,4))
        # integration
        for i in range(nint):
            ssx, ttx = pint[i, 0], pint[i, 1]
            phi, dphi = shapeFZ4(ssx,ttx)
            #ie = connect_face[ee_face,1:]-1
            dxdy = dphi@coord_loc
            # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
            JAC = np.array([[dxdy[0,0], dxdy[0,1]],
                            [dxdy[1,0], dxdy[1,1]]], dtype=float) 
            #Inverse Jacobian
            detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  

            for iii in range(4):
                N[0,iii]=phi[iii]
            
            Fe += -(1/4) * Vn * N.T * (detJAC * wps)
            # print(f"base detJAC: {detJAC}")     

        return Fe

    def matrices_Z_base(self, ee, rho=1, impedance=1):
        """ Z4 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        coord = self.nodal_coordinates
        connect_face = self.connectivities

        ############## Definir plano de trabalho e adaptar coordenadas para tal plano
        XX1, YY1, ZZ1 = coord[connect_face[ee,0],1], coord[connect_face[ee,0],2], coord[connect_face[ee,0],3]
        XX2, YY2, ZZ2 = coord[connect_face[ee,1],1], coord[connect_face[ee,1],2], coord[connect_face[ee,1],3]
        XX3, YY3, ZZ3 = coord[connect_face[ee,2],1], coord[connect_face[ee,2],2], coord[connect_face[ee,2],3]
        XX4, YY4, ZZ4 = coord[connect_face[ee,3],1], coord[connect_face[ee,3],2], coord[connect_face[ee,3],3]

        vec13 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T
        vec14 = np.array([XX4-XX1, YY4-YY1, ZZ4-ZZ1]).T
        vec12 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T

        #Cosseno de direção
        XX = vec12/np.linalg.norm(vec12)
        vecZZ = np.cross(XX,vec14)
        ZZ = vecZZ/np.linalg.norm(vecZZ)
        vecYY = np.cross(ZZ,XX)
        YY = vecYY/np.linalg.norm(vecYY)
        COSDIR = np.array([XX,YY,ZZ])

        loc_x_axis = vec12.copy()
        loc_z_axis = np.cross(loc_x_axis, vec14)
        loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

        unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
        unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

        x1 = np.dot(vec13,unit_x_axis)
        x2 = np.dot(vec14,unit_x_axis)
        x3 = 0
        x4 = np.dot(vec12,unit_x_axis)
        y1 = np.dot(vec13,unit_y_axis)
        y2 = np.dot(vec14,unit_y_axis)
        y3 = 0
        y4 = np.dot(vec12,unit_y_axis)

        coord_loc = np.array([[x1, y1],
                              [x2, y2],
                              [x3, y3],
                              [x4, y4]])

        ################ Definir pontos de integração 2D
        nint, con, wps = 4, 1/np.sqrt(3), 1
        pint = np.array([[ con,  con],
                         [-con,  con],
                         [-con, -con],
                         [ con, -con]])

        ######################## Inicio da integração na face
        Area = 0
        Ze = 0.
        # Ze = np.zeros((4,4),dtype=complex)
        N = np.zeros((1,4))
        # integration
        for i in range(nint):
            ssx, ttx = pint[i, 0], pint[i, 1]
            phi, dphi = shapeFZ4(ssx,ttx)
            #ie = connect_face[ee_face,1:]-1
            dxdy = dphi@coord_loc
            # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
            JAC = np.array([[dxdy[0,0], dxdy[0,1]],
                            [dxdy[1,0], dxdy[1,1]]], dtype=float) 
            #Inverse Jacobian
            detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  

            for iii in range(4):
                N[0,iii]=phi[iii]
            
            Ze += -(rho/impedance) * N.T@N * (detJAC * wps)

        return Ze