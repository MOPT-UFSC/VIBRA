
from vibra.engine.elements.surface_elements import Element2D

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np

ones_31 = np.ones((3, 1), dtype=float)


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


def get_jacobian_determinant(JAC: np.ndarray) -> float:
    """
    This function computes the determinant of the Jacobian
    matrix.

    Parameter
    ---------
    JAC: np.ndarray
        The Jacobian matrix.
    
    Return
    ------
    det_jac: float
        The determinant of the Jacobian matrix.
    """
    det_jac = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  

    return det_jac


def get_stacked_jacobian_determinant(JAC: np.ndarray) -> float:
    """
    This function computes the determinant of the Jacobian
    matrix.

    Parameter
    ---------
    JAC: np.ndarray
        The Jacobian matrix.
    
    Return
    ------
    det_jac: float
        The determinant of the Jacobian matrix.
    """
    det_jac = JAC[:, 0, 0] * JAC[:, 1, 1]  - JAC[:, 0, 1] * JAC[:, 1, 0]  

    return det_jac.reshape(-1, 1, 1)


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

    det_jacs = JAC[:, 0, 0] * JAC[:, 1, 1]  - JAC[:, 0, 1] * JAC[:, 1, 0] 
    det_jacs = det_jacs.reshape(-1, 1, 1)

    # the adjoint matrix
    nel = JAC.shape[0]
    AUJJ = np.zeros((nel, 2, 2), dtype=float)

    AUJJ[:, 0, 0] =  JAC[:, 1, 1]
    AUJJ[:, 0, 1] = -JAC[:, 0, 1]
    AUJJ[:, 1, 0] = -JAC[:, 1, 0]
    AUJJ[:, 1, 1] =  JAC[:, 0, 0]

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


class ACT_FACE_3(Element2D):
    #
    NODES_PER_ELEMENT = 3
    DOFS_PER_NODE = 1
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOFS_PER_NODE


    def __init__(self, model: "Model"):

        self.model = model
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def initialize_variables(self):
        """ """
        self.element_label = "acoustic_triangular_3"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connectivity = self.model.mesh.solids_connectivity
        self.faces_connectivity = self.model.mesh.faces_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity)


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
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        #
        self.phi, self.dphi = get_shape_functions_and_derivatives(ssx, ttx)


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

        X1 = self.nodal_coordinates[self.connect_face[:, 0], 1]
        Y1 = self.nodal_coordinates[self.connect_face[:, 0], 2]
        Z1 = self.nodal_coordinates[self.connect_face[:, 0], 3]

        X2 = self.nodal_coordinates[self.connect_face[:, 1], 1]
        Y2 = self.nodal_coordinates[self.connect_face[:, 1], 2]
        Z2 = self.nodal_coordinates[self.connect_face[:, 1], 3]
        
        X3 = self.nodal_coordinates[self.connect_face[:, 2], 1]
        Y3 = self.nodal_coordinates[self.connect_face[:, 2], 2]
        Z3 = self.nodal_coordinates[self.connect_face[:, 2], 3]

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

        nel = self.connect_face.shape[0]
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

        X1 = self.nodal_coordinates[self.connect_face[:, 0], 1]
        Y1 = self.nodal_coordinates[self.connect_face[:, 0], 2]
        Z1 = self.nodal_coordinates[self.connect_face[:, 0], 3]

        X2 = self.nodal_coordinates[self.connect_face[:, 1], 1]
        Y2 = self.nodal_coordinates[self.connect_face[:, 1], 2]
        Z2 = self.nodal_coordinates[self.connect_face[:, 1], 3]
        
        X3 = self.nodal_coordinates[self.connect_face[:, 2], 1]
        Y3 = self.nodal_coordinates[self.connect_face[:, 2], 2]
        Z3 = self.nodal_coordinates[self.connect_face[:, 2], 3]

        P2P1 = np.array([X2-X1, Y2-Y1, Z2-Z1]).T
        P3P1 = np.array([X3-X1, Y3-Y1, Z3-Z1]).T

        cross = np.cross(P2P1, P3P1, axis=1)
        norm_cross = np.linalg.norm(cross, axis=1)

        norm_cross = norm_cross.reshape(-1, 1, 1)
        cross = cross.reshape(-1, 1, 3)
        
        normals = cross / norm_cross

        return normals


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

        nel = self.connect_face.shape[0]
        aux_ones = np.ones((nel, 1, 1), dtype=float)

        local_coords = self.get_stacked_local_coordinates()
        JAC_3d = (self.dphi * aux_ones) @ local_coords

        det_jacs, inv_jacs = get_stacked_detJAC_and_invJAC(JAC_3d)
        dphi_t = inv_jacs @ (aux_ones * self.dphi)

        # shape functions
        N = self.phi

        # derivative of shape functions
        B = dphi_t
        B_t = np.transpose(B, axes=(0, 2, 1))

        int2d_NtN = - (1/2) * N.T @ N * (det_jacs * self.wps)
        int2d_BtB = - (1/2) * B_t @ B * (det_jacs * self.wps)

        return int2d_NtN, int2d_BtB


    def damping_matrix_Ce(self, el_index: int, rho: float = 1.0, impedance: float = 1.0) -> np.ndarray:
        """ 
        This method computes the elementary impedance matrix.

        Parameters
        ----------
        el_index: int
            The element index.

        rho: float, optional
            The fluid density in kg/m³.

        impedance: float, optional
            The specific impedance in kg/m².s.

        Returns
        -------
        Ze: np.ndarray
            The elementary impedance matrix.
        """

        ie = self.connect_face[el_index, :]
        coords = self.nodal_coordinates[ie, :]
        coord_loc = get_local_coordinates(coords)

        JAC = self.dphi @ coord_loc
        detJAC = get_jacobian_determinant(JAC)

        # N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        # N[:, 0, :] = self.phi

        # Ze = 0.
        # for i in range(self.nint):
        #     Ze += -(1/2) * (rho/impedance) * N[i, :, :].T @ N[i, :, :] * (detJAC*self.wps)
        #     # print(f"matrices_Z: index - {el_index} k - {i} {N[i, :, :]}")

        N = self.phi
        Ze = - (1/2) * (rho / impedance) * N.T @ N * (detJAC * self.wps)

        return Ze


    def stacked_damping_matrices_Ce(self, rho: float = 1, impedance: float = 1) -> np.ndarray:
        """
        This method processes all impedance-related elementary matrices and returns them
        in the stacked array form.

        Parameters
        ----------
        rho: float, optional
            The fluid density in kg/m³.
        
        impedance: float, optional
            The specific impedance in kg/m²s.

        Returns
        -------
        Ze_stacked: np.ndarray
            The array containing the stacked elementary matrices.
        """

        int2d_NtN = self.stacked_matrices_NtN()
        Ze_stacked = (rho / impedance) * int2d_NtN

        return Ze_stacked


    def stacked_matrices_NtN(self) -> np.ndarray:
        """
        This method processes all elementary matrices and returns them
        in the stacked array form.

        Returns
        -------
        int2d_NtN: np.ndarray
            The array containing the stacked elementary matrices.
        """

        nel = self.connect_face.shape[0]
        aux_ones = np.ones((nel, 1, 1), dtype=float)

        local_coords = self.get_stacked_local_coordinates()
        JAC_3d = (self.dphi * aux_ones) @ local_coords
        det_jacs = get_stacked_jacobian_determinant(JAC_3d)

        # shape functions
        N = self.phi

        int2d_NtN = - (1/2) * N.T @ N * (det_jacs * self.wps)

        return int2d_NtN


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

        ie = self.connect_face[el_index, :]
        coords = self.nodal_coordinates[ie, :]
        coord_loc = get_local_coordinates(coords)

        JAC = self.dphi @ coord_loc
        det_jac = get_jacobian_determinant(JAC)

        # N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        # N[:, 0, :] = self.phi

        # Fe = 0.
        # for i in range(self.nint):            
        #     Fe += -(1/2) * load * N[i, :, :].T * (det_jac * self.wps)

        N = self.phi
        Fe = - (1/2) * load * (N @ ones_31) * (det_jac * self.wps)

        return Fe


    def surface_integrator(self, e_connect: np.ndarray, sound_intensity: np.ndarray) -> np.ndarray:
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

        # e_connect = self.connect_face[el_index, :]
        coords = self.nodal_coordinates[e_connect, :]
        coord_loc = get_local_coordinates(coords)

        JAC = self.dphi @ coord_loc
        det_jac = get_jacobian_determinant(JAC)

        # N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        # N[:, 0, :] = self.phi

        # Fe = 0.
        # for i in range(self.nint):            
        #     Fe += -(1/2) * load * N[i, :, :].T * (det_jac * self.wps)

        N = self.phi
        Fe = - (1/2) * (N @ sound_intensity) * (det_jac * self.wps)

        return Fe


    def elementary_sound_power_from_sound_intensity(self, e_connect: np.ndarray, sound_intensity: np.ndarray) -> np.ndarray:
        """ 
        This method computes the elementary load vector.

        Parameters
        ----------
        el_index: int
            The element index.

        sound_intensity: np.ndarray, optional
            The sound intensity vector.

        Returns
        -------
        Fe: np.ndarray
            The elementary sound power.
        """

        coords = self.nodal_coordinates[e_connect, :]
        coord_loc = get_local_coordinates(coords)

        JAC = self.dphi @ coord_loc
        det_jac = get_jacobian_determinant(JAC)

        N = self.phi

        Fe = - (1/2) * (N @ sound_intensity) * (det_jac * self.wps)

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
        Ce: np.ndarray
            The elementary sound power vector.
        """

        coords = self.nodal_coordinates[e_connect, :]
        coord_loc = get_local_coordinates(coords)

        JAC = self.dphi @ coord_loc
        det_jac = get_jacobian_determinant(JAC)

        N = self.phi
        Ce = - (1/2) * L_sv @ (N.T @ N) @ R_sv * (det_jac * self.wps)

        return Ce.flatten()


    def reorder_connect(self, connect_face):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """

        self.connect_face = connect_face[:, [0, 1, 2]]


    def generate_ind_rows_cols(self, connect_face):
        """
        This method processess the dofs indices (rows and columns) 
        for assembly
        """

        self.reorder_connect(connect_face)
        dofs, edofs = self.DOFS_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs * self.connect_face[:, :]

        vect_indices = ind_dofs.flatten()
        ind_rows_face = ((np.tile(vect_indices, (edofs,1))).T).flatten()
        ind_cols_face = (np.tile(ind_dofs, edofs)).flatten()

        return ind_rows_face, ind_cols_face


    def excitation_F_base(self, ee, Vn=1):
        """ F3 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        coord = self.nodal_coordinates
        connect_face = self.connect_face

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


    def matrices_Z_base(self, ee, rho=1, impedance=1):
        """ Z3 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        coord = self.nodal_coordinates
        connect_face = self.connect_face

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