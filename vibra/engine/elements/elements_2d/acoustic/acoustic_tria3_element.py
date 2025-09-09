
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
    
    XX1, XX2, XX3 = coords[:, 1]
    YY1, YY2, YY3 = coords[:, 2]
    ZZ1, ZZ2, ZZ3 = coords[:, 3]

    vec21 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
    vec31 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T

    loc_x_axis = vec21.copy()
    loc_z_axis = np.cross(loc_x_axis, vec31)
    loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

    unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
    unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

    x1 = 0. 
    x2 = np.dot(vec21,unit_x_axis)
    x3 = np.dot(vec31,unit_x_axis)
    y1 = 0.
    y2 = np.dot(vec21,unit_y_axis)
    y3 = np.dot(vec31,unit_y_axis)

    coord_loc = np.array([[x1, y1],
                          [x2, y2],
                          [x3, y3]], dtype=float)

    return coord_loc


class ACT_TRIANGLE_3(Element2D):

    NODES_PER_ELEMENT = 3
    DOFS_PER_NODE = 1
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOFS_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def initialize_variables(self):
        self.connectivities = None
        self.element_label = "acoustic_triangular_3"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates


    def define_integration_points(self):
        """ 
        Defines the integration points and their respective weights
        for the numerical integration processing.
        """
        self.nint = 3
        con1 = 1/6
        con2 = 2/3
        self.wps = 1/3
        self.pint = np.array([[con1, con1],
                              [con2, con1],
                              [con1, con2]], dtype=float)


    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """
        ## coordinates from integration points
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]

        ## shape functions
        phi = np.zeros((self.nint, 1, self.NODES_PER_ELEMENT), dtype=float)
        phi[:, 0, 0] = 1 - ssx - ttx
        phi[:, 0, 1] = ttx
        phi[:, 0, 2] = ssx
        # phi = np.array([1 - ssx - ttx, ttx, ssx], dtype=float).T

        ## shape functions derivatives
        dphi = np.array([[-1, 0, 1],
                         [-1, 1, 0]], dtype=float)

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
        det_jacs = get_detJAC(JAC_stacked)

        # initialize variable
        int2d_NtN = 0.

        # integration loop
        for i in range(self.nint):

            # shape functions
            N = self.phi[i, :, :]

            int2d_NtN += - (1 / 2) * N.T @ N * (det_jacs * self.wps)

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
        det_jacs, inv_jacs = get_stacked_detJAC_and_invJAC(JAC_stacked)

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

            int2d_NtN += - (1 / 2) * N_t @ N * (det_jacs * self.wps)
            int2d_BtB += - (1 / 2) * B_t @ B * (det_jacs * self.wps)

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
        det_jac = get_detJAC(JAC)

        # intialize variable
        Fe = 0.

        # integration loop
        for i in range(self.nint):

            # shape functions
            N = self.phi[i, :, :]

            Fe += -(1 / 2) * load * N.T * (det_jac * self.wps)

        return Fe


    def elementary_sound_power(self, e_connect: np.ndarray, L_sv: np.ndarray, R_sv: np.ndarray) -> np.ndarray:
        """ 
        This method computes the elementary load vector.

        Parameters
        ----------
        el_index: int
            The element index.

        L_sv: np.ndarray
            The left stacked vector (complex-conjugate of particle velocities).

        R_sv: np.ndarray
            The righ stacked vector (complex-conjugate of pressures).

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
        det_jac = get_detJAC(JAC)

        # intialize variable
        We = 0.

        # integration loop
        for i in range(self.nint):

            # shape functions
            N = self.phi[i, :, :]

            We += -(1 / 2) * L_sv @ (N.T @ N) @ R_sv * (det_jac * self.wps)

        return We.flatten()


    def reorder_connect(self, connect_face):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """

        self.connectivities = connect_face[:, [0, 1, 2]]


    def generate_ind_rows_cols(self, connect_face):
        """
        This method processess the dofs indices (rows and columns) 
        for assembly
        """

        self.reorder_connect(connect_face)
        dofs, edofs = self.DOFS_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs * self.connectivities[:, :]

        vect_indices = ind_dofs.flatten()
        ind_rows_face = ((np.tile(vect_indices, (edofs,1))).T).flatten()
        ind_cols_face = (np.tile(ind_dofs, edofs)).flatten()

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


def forceF3(ee, coord, connect_face, Vn=1):
    """ F3 matrices
    """
    #Check Connectivity -- Ansys = Gmsh

    ############## Definir plano de trabalho e adaptar coordenadas para tal plano
    XX1, YY1, ZZ1 = coord[connect_face[ee,0],1], coord[connect_face[ee,0],2], coord[connect_face[ee,0],3]
    XX2, YY2, ZZ2 = coord[connect_face[ee,1],1], coord[connect_face[ee,1],2], coord[connect_face[ee,1],3]
    XX3, YY3, ZZ3 = coord[connect_face[ee,2],1], coord[connect_face[ee,2],2], coord[connect_face[ee,2],3]

    vec21 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
    vec31 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T

    loc_x_axis = vec21.copy()
    loc_z_axis = np.cross(loc_x_axis, vec31)
    loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

    unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
    unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

    x1 = 0 
    x2 = np.dot(vec21,unit_x_axis)
    x3 = np.dot(vec31,unit_x_axis)
    y1 = 0 
    y2 = np.dot(vec21,unit_y_axis)
    y3 = np.dot(vec31,unit_y_axis)

    coord_loc = np.array([[x1, y1],
                            [x2, y2],
                            [x3, y3]])

    ################ Definir pontos de integração 2D
    nint = 3
    con1 = 1/6
    con2 = 2/3
    wps = 1/3
    pint = np.array([[con1, con1],
                        [con2, con1],
                        [con1, con2]])

    ######################## Inicio da integração na face
    Fe = np.zeros((3,1),dtype=complex)
    N = np.zeros((1,3))
    # integration
    for i in range(nint):
        ssx, ttx = pint[i, 0], pint[i, 1]
        phi, dphi = get_shape_functions_and_derivatives(ssx, ttx)
        #ie = connect_face[ee_face,1:]-1
        dxdy = dphi@coord_loc
        # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
        JAC = np.array([[dxdy[0,0], dxdy[0,1]],
                        [dxdy[1,0], dxdy[1,1]]], dtype=float)
        # print(f"forceF3: index - {ee} : k - {i} JAC {JAC}")
        #Inverse Jacobian
        detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  
        # N[0, :] = phi
        for iii in range(3):
            N[0,iii]=phi[iii]

        # print(f"forceF3: index - {ee} : k - {i} {N}")           
        Fe += -(1/2) * Vn * N.T * (detJAC * wps)

    return Fe


def impedanceZ3(ee, coord, connect_face, rho=1, impedance=1):
    """ Z3 matrices
    """
    #Check Connectivity -- Ansys = Gmsh

    ############## Definir plano de trabalho e adaptar coordenadas para tal plano
    XX1, YY1, ZZ1 = coord[connect_face[ee,0],1], coord[connect_face[ee,0],2], coord[connect_face[ee,0],3]
    XX2, YY2, ZZ2 = coord[connect_face[ee,1],1], coord[connect_face[ee,1],2], coord[connect_face[ee,1],3]
    XX3, YY3, ZZ3 = coord[connect_face[ee,2],1], coord[connect_face[ee,2],2], coord[connect_face[ee,2],3]

    vec21 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
    vec31 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T

    loc_x_axis = vec21.copy()
    loc_z_axis = np.cross(loc_x_axis, vec31)
    loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

    unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
    unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

    x1 = 0 
    x2 = np.dot(vec21,unit_x_axis)
    x3 = np.dot(vec31,unit_x_axis)
    y1 = 0 
    y2 = np.dot(vec21,unit_y_axis)
    y3 = np.dot(vec31,unit_y_axis)

    coord_loc = np.array([[x1, y1],
                            [x2, y2],
                            [x3, y3]])
    # print(f"matricesZ3: index - {ee} \n {coord_loc}")

    ################ Definir pontos de integração 2D
    nint = 3
    con1 = 1/6
    con2 = 2/3
    wps = 1/3
    pint = np.array([[con1, con1],
                        [con2, con1],
                        [con1, con2]])

    ######################## Inicio da integração na face
    Ze = np.zeros((3,3),dtype=complex)
    N = np.zeros((1,3))
    # integration
    for i in range(nint):
        ssx, ttx = pint[i, 0], pint[i, 1]
        phi, dphi = get_shape_functions_and_derivatives(ssx,ttx)
        #ie = connect_face[ee_face,1:]-1
        dxdy = dphi@coord_loc
        # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
        JAC = np.array([[dxdy[0,0], dxdy[0,1]],
                        [dxdy[1,0], dxdy[1,1]]], dtype=float) 
        #Inverse Jacobian
        detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]
        # print(f"matricesZ3: index - {ee} \n {coord_loc} {detJAC} -> {i}")

        for iii in range(3):
            N[0, iii] = phi[iii]
        
        # print(f"matricesZ3: index - {ee} k - {i} {N}")
        
        Ze += -(1/2) * (rho/impedance) * N.T@N * (detJAC * wps)

    return Ze