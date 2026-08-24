
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

    XX1, XX2, XX3, XX4, XX5, XX6 = coords[:, 1]
    YY1, YY2, YY3, YY4, YY5, YY6 = coords[:, 2]
    ZZ1, ZZ2, ZZ3, ZZ4, ZZ5, ZZ6 = coords[:, 3]

    vec_12 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
    vec_13 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T
    vec_14 = np.array([XX4-XX1, YY4-YY1, ZZ4-ZZ1]).T
    vec_15 = np.array([XX5-XX1, YY5-YY1, ZZ5-ZZ1]).T
    vec_16 = np.array([XX6-XX1, YY6-YY1, ZZ6-ZZ1]).T

    loc_x_axis = vec_12.copy()
    loc_z_axis = np.cross(loc_x_axis, vec_13)   # ---> normal
    loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

    unit_x_axis = loc_x_axis / np.linalg.norm(loc_x_axis)
    unit_y_axis = loc_y_axis / np.linalg.norm(loc_y_axis)
    unit_z_axis = loc_z_axis / np.linalg.norm(loc_z_axis)  # noqa: F841

    x1 = 0.
    x2 = np.dot(vec_12, unit_x_axis)
    x3 = np.dot(vec_13, unit_x_axis)
    x4 = np.dot(vec_14, unit_x_axis)
    x5 = np.dot(vec_15, unit_x_axis)
    x6 = np.dot(vec_16, unit_x_axis)

    y1 = 0.
    y2 = np.dot(vec_12, unit_y_axis)
    y3 = np.dot(vec_13, unit_y_axis)
    y4 = np.dot(vec_14, unit_y_axis)
    y5 = np.dot(vec_15, unit_y_axis)
    y6 = np.dot(vec_16, unit_y_axis)

    coord_loc = np.array([[x1, y1],
                          [x2, y2],
                          [x3, y3],
                          [x4, y4],
                          [x5, y5],
                          [x6, y6]], dtype=float)

    return coord_loc


class TRIANGLE_6(Element2D):

    def __init__(self, model: "Model", dof_per_node: int):

        self.model = model

        self.nodes_per_element = 6
        self.dof_per_node = dof_per_node

        self.connectivities = None
        self.element_label = ""
        self.nodal_coordinates = self.model.mesh.nodal_coordinates

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    @property
    def dof_per_element(self):
        return self.nodes_per_element * self.dof_per_node


    def define_integration_points(self, integration_points: int = 6):
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
        ## coordinates from integration points
        xi_1 = self.num_int_data[:, 0]
        xi_2 = self.num_int_data[:, 1]

        ##NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015

        ## shape functions
        xi_3 = 1 - xi_1 - xi_2

        ## shape functions (Atalla and Sgard, 2015, pg. 173)
        phi = np.zeros((self.nint, 1, self.nodes_per_element), dtype=float)
        phi[:, 0, 0] = xi_1 * (2 * xi_1 - 1)
        phi[:, 0, 1] = xi_2 * (2 * xi_2 - 1)
        phi[:, 0, 2] = xi_3 * (2 * xi_3 - 1)
        phi[:, 0, 3] = 4 * xi_1 * xi_2
        phi[:, 0, 4] = 4 * xi_2 * xi_3
        phi[:, 0, 5] = 4 * xi_1 * xi_3

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((self.nint, 2, self.nodes_per_element), dtype=float)
        dphi[:, 0, 0] =  4 * xi_1 - 1
        dphi[:, 0, 1] =  0
        dphi[:, 0, 2] = -4 * xi_3 + 1
        dphi[:, 0, 3] =  4 * xi_2
        dphi[:, 0, 4] = -4 * xi_2
        dphi[:, 0, 5] =  4 * (xi_3 - xi_1)

        dphi[:, 1, 0] =  0
        dphi[:, 1, 1] =  4 * xi_2 - 1
        dphi[:, 1, 2] = -4 * xi_3 + 1
        dphi[:, 1, 3] =  4 * xi_1
        dphi[:, 1, 4] =  4 * (xi_3 - xi_2)
        dphi[:, 1, 5] = -4 * xi_1

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

        X5 = self.nodal_coordinates[self.connectivities[:, 4], 1]
        Y5 = self.nodal_coordinates[self.connectivities[:, 4], 2]
        Z5 = self.nodal_coordinates[self.connectivities[:, 4], 3]

        X6 = self.nodal_coordinates[self.connectivities[:, 5], 1]
        Y6 = self.nodal_coordinates[self.connectivities[:, 5], 2]
        Z6 = self.nodal_coordinates[self.connectivities[:, 5], 3]

        vec_12 = np.array([X2-X1, Y2-Y1, Z2-Z1]).T
        vec_13 = np.array([X3-X1, Y3-Y1, Z3-Z1]).T
        vec_14 = np.array([X4-X1, Y4-Y1, Z4-Z1]).T
        vec_15 = np.array([X5-X1, Y5-Y1, Z5-Z1]).T
        vec_16 = np.array([X6-X1, Y6-Y1, Z6-Z1]).T

        loc_x_axis = vec_12.copy()
        loc_z_axis = np.cross(loc_x_axis, vec_13, axis=1)   # ---> normal
        loc_y_axis = np.cross(loc_z_axis, loc_x_axis, axis=1)

        nx = np.linalg.norm(loc_x_axis, axis=1).reshape(-1, 1, 1)
        ny = np.linalg.norm(loc_y_axis, axis=1).reshape(-1, 1, 1)
        # nz = np.linalg.norm(loc_z_axis, axis=1).reshape(-1, 1, 1)

        unit_x_axis = loc_x_axis.reshape(-1, 1, 3) / nx
        unit_y_axis = loc_y_axis.reshape(-1, 1, 3) / ny
        # unit_z_axis = loc_z_axis.reshape(-1, 1, 3) / nz

        unit_x_axis = unit_x_axis.reshape(-1, 3)
        unit_y_axis = unit_y_axis.reshape(-1, 3)
        # unit_z_axis = unit_z_axis.reshape(-1, 3)

        x2 = np.sum(vec_12 * unit_x_axis, axis=1)
        x3 = np.sum(vec_13 * unit_x_axis, axis=1)
        x4 = np.sum(vec_14 * unit_x_axis, axis=1)
        x5 = np.sum(vec_15 * unit_x_axis, axis=1)
        x6 = np.sum(vec_16 * unit_x_axis, axis=1)

        y2 = np.sum(vec_12 * unit_y_axis, axis=1)
        y3 = np.sum(vec_13 * unit_y_axis, axis=1)
        y4 = np.sum(vec_14 * unit_y_axis, axis=1)
        y5 = np.sum(vec_15 * unit_y_axis, axis=1)
        y6 = np.sum(vec_16 * unit_y_axis, axis=1)

        nel = self.connectivities.shape[0]
        coord_loc = np.zeros((nel, self.nodes_per_element, 2), dtype=float)

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

        return coord_loc


    def get_jacobian_determinant(self, int_point: int, coords: np.ndarray, return_vectors: bool = False):

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


    def get_stacked_jacobian_determinant(self, int_point: int, coords: np.ndarray, return_normal_vector: bool = False):
        """
        This method evaluates the Jacobian determinant of the i-th integrarion point.
        
        Parameters
        ----------

        int_point: int
            The integration point to be evaluated.

        coords:  np.ndarray
            A three-dimensional coordinate matrix in which each plane 
            contains the nodal coordinates of an element. 

        return_normal_vector: bool, optional
            Use this argument to control when the normal vector is returned.

        Return
        ------
        det_jac: np.ndarray
            A stacked vector with the Jacobian determinant of all elements evaluated
            at the i-th integration point.

        normal_vector: np.ndarray
            The normalized normal vectors at the i-th integration point of all 
            elements that is returned if the return_normal_vector argument is True.
        """

        # vectors tangent to the element's surface
        g_xi = self.dphi[int_point, 0, :] @ coords
        g_eta = self.dphi[int_point, 1, :] @ coords

        # compute the stacked normal vectors
        normal_vector = np.cross(g_xi, g_eta)

        # calculate the stacked Jacobian determinants
        det_jac = np.linalg.norm(normal_vector, axis=1)

        if not return_normal_vector:
            return det_jac

        # normalize the elements normal vectors for the i-th integration point
        e_normal = normal_vector / det_jac

        return det_jac, e_normal 


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


    def reorder_connect(self, connectivities: np.ndarray):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """
        self.connectivities = connectivities[:, [1, 2, 0, 4, 5, 3]]
        # self.connectivities = connectivities[:, [0, 1, 2, 3, 4, 5]]


def get_shape_functions_and_derivatives(rrx: np.ndarray, ssx: np.ndarray):

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

    ## shape functions
    ttx = 1 - rrx - ssx
    phi = np.array([ttx*(2*ttx - 1), rrx*(2*rrx - 1), ssx*(2*ssx - 1), 4*rrx*ttx, 4*rrx*ssx, 4*ssx*ttx,], dtype=float).T

    ## shape functions derivatives
    dphi = np.array([[(-1)*(2*ttx-1) + ttx*(-2), 4*rrx-1,       0, 4*ttx + 4*rrx*(-1), 4*ssx,         4*ssx*(-1)],
                     [(-1)*(2*ttx-1) + ttx*(-2),       0, 4*ssx-1,         4*rrx*(-1), 4*rrx, 4*ttx + 4*ssx*(-1)]], dtype=float)

    return phi, dphi


# def excitation_F_base(self, ee, coord, connect_face, Vn=1):
#     """ F3 matrices
#     """
#     #Check Connectivity -- Ansys = Gmsh

#     ############## Definir plano de trabalho e adaptar coordenadas para tal plano
#     XX1, YY1, ZZ1 = coord[connect_face[ee,0],1], coord[connect_face[ee,0],2], coord[connect_face[ee,0],3]
#     XX2, YY2, ZZ2 = coord[connect_face[ee,1],1], coord[connect_face[ee,1],2], coord[connect_face[ee,1],3]
#     XX3, YY3, ZZ3 = coord[connect_face[ee,2],1], coord[connect_face[ee,2],2], coord[connect_face[ee,2],3]

#     vec21 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
#     vec31 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T

#     loc_x_axis = vec21.copy()
#     loc_z_axis = np.cross(loc_x_axis, vec31)
#     loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

#     unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
#     unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

#     x1 = 0 
#     x2 = np.dot(vec21,unit_x_axis)
#     x3 = np.dot(vec31,unit_x_axis)
#     y1 = 0 
#     y2 = np.dot(vec21,unit_y_axis)
#     y3 = np.dot(vec31,unit_y_axis)

#     coord_loc = np.array([[x1, y1],
#                             [x2, y2],
#                             [x3, y3]])

#     ################ Definir pontos de integração 2D
#     nint = 3
#     con1 = 1/6
#     con2 = 2/3
#     wps = 1/3
#     pint = np.array([[con1, con1],
#                         [con2, con1],
#                         [con1, con2]])

#     ######################## Inicio da integração na face
#     Fe = np.zeros((3,1),dtype=complex)
#     N = np.zeros((1,3))
#     # integration
#     for i in range(nint):
#         ssx, ttx = pint[i, 0], pint[i, 1]
#         phi, dphi = get_shape_functions_and_derivatives(ssx, ttx)
#         #ie = connect_face[ee_face,1:]-1
#         dxdy = dphi@coord_loc
#         # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
#         JAC = np.array([[dxdy[0,0], dxdy[0,1]],
#                         [dxdy[1,0], dxdy[1,1]]], dtype=float)
#         # print(f"forceF3: index - {ee} : k - {i} JAC {JAC}")
#         #Inverse Jacobian
#         detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  
#         # N[0, :] = phi
#         for iii in range(3):
#             N[0,iii]=phi[iii]

#         # print(f"forceF3: index - {ee} : k - {i} {N}")           
#         Fe += -(1/2) * Vn * N.T * (detJAC * wps)

#     return Fe


# def matrices_Z_base(ee, coord, connect_face, rho=1, impedance=1):
#     """ Z3 matrices
#     """
#     #Check Connectivity -- Ansys = Gmsh

#     ############## Definir plano de trabalho e adaptar coordenadas para tal plano
#     XX1, YY1, ZZ1 = coord[connect_face[ee,0],1], coord[connect_face[ee,0],2], coord[connect_face[ee,0],3]
#     XX2, YY2, ZZ2 = coord[connect_face[ee,1],1], coord[connect_face[ee,1],2], coord[connect_face[ee,1],3]
#     XX3, YY3, ZZ3 = coord[connect_face[ee,2],1], coord[connect_face[ee,2],2], coord[connect_face[ee,2],3]

#     vec21 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
#     vec31 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T

#     loc_x_axis = vec21.copy()
#     loc_z_axis = np.cross(loc_x_axis, vec31)
#     loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

#     unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
#     unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

#     x1 = 0 
#     x2 = np.dot(vec21,unit_x_axis)
#     x3 = np.dot(vec31,unit_x_axis)
#     y1 = 0 
#     y2 = np.dot(vec21,unit_y_axis)
#     y3 = np.dot(vec31,unit_y_axis)

#     coord_loc = np.array([[x1, y1],
#                             [x2, y2],
#                             [x3, y3]])

#     ################ Definir pontos de integração 2D
#     nint = 3
#     con1 = 1/6
#     con2 = 2/3
#     wps = 1/3
#     pint = np.array([[con1, con1],
#                         [con2, con1],
#                         [con1, con2]])

#     ######################## Inicio da integração na face
#     Ze = np.zeros((3,3),dtype=complex)
#     N = np.zeros((1,3))

#     # integration
#     for i in range(nint):

#         ssx, ttx = pint[i, 0], pint[i, 1]
#         phi, dphi = get_shape_functions_and_derivatives(ssx,ttx)

#         #ie = connect_face[ee_face,1:]-1
#         dxdy = dphi@coord_loc

#         # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
#         JAC = np.array([[dxdy[0,0], dxdy[0,1]],
#                         [dxdy[1,0], dxdy[1,1]]], dtype=float) 

#         #Inverse Jacobian
#         detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]

#         for iii in range(3):
#             N[0, iii] = phi[iii]
        
#         Ze += -(1/2) * (rho/impedance) * N.T@N * (detJAC * wps)

#     return Ze
    

# def shapeF6(r,s):
#     """ Shape Functions and Derivatives TRIA6
#     """
#     #
#     t = 1 - r - s
#     phi = np.array([t*(2*t-1), r*(2*r-1), s*(2*s-1), 4*r*t, 4*r*s, 4*s*t])
#     #
#     dphi = np.array([[(-1)*(2*t-1)+t*(-2), 4*r-1,     0, 4*t + 4*r*(-1), 4*s,       4*s*(-1)],
#                      [(-1)*(2*t-1)+t*(-2),     0, 4*s-1,       4*r*(-1), 4*r, 4*t + 4*s*(-1)]], dtype=float)
#     #
#     return phi, dphi

# def forceF6(ee, coord, connect_face, c_0, rho, Vn):
#     """ F4 matrices
#     """
#     #Check Connectivity -- Ansys = Gmsh

#     ############## Definir plano de trabalho e adaptar coordenadas para tal plano
#     # Três primeiros nós da conectividade: vértices
#     XX1, YY1, ZZ1 = coord[connect_face[ee,1-1],1], coord[connect_face[ee,1-1],2], coord[connect_face[ee,1-1],3]
#     XX2, YY2, ZZ2 = coord[connect_face[ee,2-1],1], coord[connect_face[ee,2-1],2], coord[connect_face[ee,2-1],3]
#     XX3, YY3, ZZ3 = coord[connect_face[ee,3-1],1], coord[connect_face[ee,3-1],2], coord[connect_face[ee,3-1],3]
#     #
#     XX4, YY4, ZZ4 = coord[connect_face[ee,4-1],1], coord[connect_face[ee,4-1],2], coord[connect_face[ee,4-1],3]
#     XX5, YY5, ZZ5 = coord[connect_face[ee,5-1],1], coord[connect_face[ee,5-1],2], coord[connect_face[ee,5-1],3]
#     XX6, YY6, ZZ6 = coord[connect_face[ee,6-1],1], coord[connect_face[ee,6-1],2], coord[connect_face[ee,6-1],3]    

#     vec21 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
#     vec31 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T
#     #
#     vec41 = np.array([XX4-XX1, YY4-YY1, ZZ4-ZZ1]).T
#     vec51 = np.array([XX5-XX1, YY5-YY1, ZZ5-ZZ1]).T
#     vec61 = np.array([XX6-XX1, YY6-YY1, ZZ6-ZZ1]).T

#     loc_x_axis = vec21.copy()
#     loc_z_axis = np.cross(loc_x_axis, vec31)   # ---> normal
#     loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

#     unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
#     unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)
#     unit_z_axis = loc_z_axis/np.linalg.norm(loc_z_axis)

#     x1 = 0 
#     x2 = np.dot(vec21,unit_x_axis)
#     x3 = np.dot(vec31,unit_x_axis)
#     x4 = np.dot(vec41,unit_x_axis)
#     x5 = np.dot(vec51,unit_x_axis)
#     x6 = np.dot(vec61,unit_x_axis)
#     y1 = 0 
#     y2 = np.dot(vec21,unit_y_axis)
#     y3 = np.dot(vec31,unit_y_axis)
#     y4 = np.dot(vec41,unit_y_axis)
#     y5 = np.dot(vec51,unit_y_axis)
#     y6 = np.dot(vec61,unit_y_axis)

#     coord_loc = np.array([[x1, y1],
#                           [x2, y2],
#                           [x3, y3],
#                           [x4, y4],
#                           [x5, y5],
#                           [x6, y6],])

#     ################ Definir pontos de integração 2D
#     nint = 3
#     con1 = 1/6
#     con2 = 2/3
#     wps = 1/3
#     pint = np.array([[con1, con1],
#                      [con2, con1],
#                      [con1, con2]], dtype=float)
    
#     # nint = 1
#     # con = 1/3
#     # wps = 1
#     # pint = np.array([[con, con]])

#     ######################## Inicio da integração na face
#     Fe = np.zeros((6,1),dtype=complex)
#     N = np.zeros((1,6))
#     # integration
#     for i in range(nint):
#         ssx, ttx = pint[i, 0], pint[i, 1]
#         phi, dphi = shapeF6(ssx,ttx)
#         #ie = connect_face[ee_face,1:]-1
#         dxdy = dphi@coord_loc
#         # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
#         JAC = np.array([[dxdy[0,0], dxdy[0,1]],
#                         [dxdy[1,0], dxdy[1,1]]], dtype=float) 
#         #Inverse Jacobian
#         detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]

#         for iii in range(6):
#             N[0,iii]=phi[iii]
        
#         Fe += -(1/2)*Vn*N.T*(detJAC*wps)

#     return Fe