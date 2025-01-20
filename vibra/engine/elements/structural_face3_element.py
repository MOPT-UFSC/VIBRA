#fmt: off

import numpy as np

from vibra.engine.elements.surface_elements import Element2D
from numba import njit

def get_detJAC_and_invJAC(JAC: np.ndarray):
    """ """

    detJAC = JAC[0, 0] * JAC[1, 1] - JAC[0, 1] * JAC[1, 0]
    AUJJ = np.array([[ JAC[1, 1], -JAC[0, 1]], 
                     [-JAC[1, 0],  JAC[0, 0]]], dtype=float)

    return detJAC, (1 / detJAC) * AUJJ

def get_local_coordinates(nodal_coords: np.ndarray):

    x = nodal_coords[:, 0]
    y = nodal_coords[:, 1]
    z = nodal_coords[:, 2]

    # X vector
    v_x = np.array([x[1] - x[0], y[1] - y[0], z[1] - z[0]], dtype=float)
    v_x = v_x / np.linalg.norm(v_x)

    # Auxiliary vector
    v_a = np.array([x[2] - x[0], y[2] - y[0], z[2] - z[0]], dtype=float)
    v_a = v_a / np.linalg.norm(v_a)

    # Z vector
    v_z = np.cross(v_x, v_a)
    v_z /= np.linalg.norm(v_z)
    # v_z = np.array([v_x[1]*v_r[2] - v_x[2]*v_r[1], v_x[2]*v_r[0] - v_x[0]*v_r[2], v_x[0]*v_r[1] - v_x[1]*v_r[0]])
    # v_z = v_z / np.linalg.norm(v_z)

    # Y vector
    v_y = np.cross(v_z, v_x)
    v_y /= np.linalg.norm(v_y)
    # v_y = np.array([v_z[1] * v_x[2] - v_z[2] * v_x[1], v_z[2] * v_x[0] - v_z[0] * v_x[2], v_z[0] * v_x[1] - v_z[1] * v_x[0]])
    # v_y = v_y / np.linalg.norm(v_y)

    # Element area calculation
    area = np.linalg.norm(v_z) / 2

    # Direction cosines
    dir_cossines = np.array([v_x, v_y, v_z], dtype=float)

    # Transformation to local coordinate system
    # coords_lcs = np.column_stack((x, y, z)) @ dir_cossines.T
    coords_lcs = nodal_coords @ dir_cossines.T
    x_loc = coords_lcs[:, 0] - coords_lcs[0, 0]
    y_loc = coords_lcs[:, 1] - coords_lcs[0, 1]

    # Transformation matrix
    Tp = np.zeros((6, 6), dtype=float)
    T = np.zeros((18, 18), dtype=float)

    Tp[0:3, 0:3] = Tp[3:6, 3:6] = dir_cossines
    T[0:6, 0:6] = T[6:12, 6:12] = T[12:18, 12:18] = Tp

    return x_loc, y_loc, area, T

def batoz_constants(x_loc: np.array, y_loc: np.array):
    """
        Constants (Batoz) - shape: (4, 3)

                                    [pk0, pk1, pk2; 
                                     qk0, qk1, qk2; 
                                     rk0, rk1, rk2; 
                                     tk0, tk1, tk2]

    """

    # Element area
    area = ((x_loc[2] - x_loc[0]) * (y_loc[0] - y_loc[1]) - (x_loc[0] - x_loc[1]) * (y_loc[2] - y_loc[0])) / 2

    # Useful constants
    x_12, x_23, x_31 = x_loc[0] - x_loc[1], x_loc[1] - x_loc[2], x_loc[2] - x_loc[0]
    y_12, y_23, y_31 = y_loc[0] - y_loc[1], y_loc[1] - y_loc[2], y_loc[2] - y_loc[0]
    l_12, l_23, l_31 = x_12**2 + y_12**2, x_23**2 + y_23**2, x_31**2 + y_31**2
    y_21, y_32, y_13 = y_loc[1] - y_loc[0], y_loc[2] - y_loc[1], y_loc[0] - y_loc[2]

    # Derivative of element area with respect to local coordinates
    dA = np.array([[-y_12 - y_31, y_31, y_12], [x_31 + x_12, -x_31, -x_12]])/2

    # Derivative of constants with respect to local coordinates
    dx_12, dx_23, dx_31 = np.array([1, -1, 0]), np.array([0, 1, -1]), np.array([-1, 0, 1])
    dy_12, dy_23, dy_31 = np.array([1, -1, 0]), np.array([0, 1, -1]), np.array([-1, 0, 1])

    batoz_const = np.array([[    -6*x_23 / l_23,     -6*x_31 / l_31,     -6*x_12 / l_12],
                            [3*x_23*y_23 / l_23, 3*x_31*y_31 / l_31, 3*x_12*y_12 / l_12],
                            [  3*y_23**2 / l_23,   3*y_31**2 / l_31,   3*y_12**2 / l_12],
                            [    -6*y_23 / l_23,     -6*y_31 / l_31,     -6*y_12 / l_12]], dtype=float)

    return batoz_const, area

@njit
def batoz_shape_functions(r, s, batoz_const):

    pk0, pk1, pk2 = batoz_const[0, 0], batoz_const[0, 1], batoz_const[0, 2]
    qk0, qk1, qk2 = batoz_const[1, 0], batoz_const[1, 1], batoz_const[1, 2]
    rk0, rk1, rk2 = batoz_const[2, 0], batoz_const[2, 1], batoz_const[2, 2]
    tk0, tk1, tk2 = batoz_const[3, 0], batoz_const[3, 1], batoz_const[3, 2]

    # Initialization in numba format
    H_xr = np.zeros((9, len(r)), dtype=float)
    H_yr = np.zeros((9, len(r)), dtype=float)
    H_xs = np.zeros((9, len(r)), dtype=float) 
    H_ys = np.zeros((9, len(r)), dtype=float)

    # Loop over each integration point
    for ii, r_ii in enumerate(r):

        # Precompute repeated terms
        s_ii = s[ii]
        r_2 = 1 - 2 * r_ii
        s_2 = 1 - 2 * s_ii

        # Derivatives of shape functions
        H_xr[:, ii] = np.array([pk2*r_2 + (pk1 - pk2)*s_ii,
                                qk2*r_2 - (qk1 + qk2)*s_ii,
                                -4 + 6*(r_ii + s_ii) + rk2*r_2 - s_ii*(rk1 + rk2),
                                -pk2*r_2 + s_ii*(pk0 + pk2),
                                qk2*r_2 - s_ii*(qk2 - qk0),
                                -2 + 6*r_ii + rk2*r_2 + s_ii*(rk0 - rk2),
                                -s_ii*(pk1 + pk0),
                                s_ii*(qk0 - qk1),
                                -s_ii*(rk1 - rk0)], dtype=float)

        H_yr[:, ii] = np.array([tk2*r_2 + s_ii*(tk1 - tk2),
                                1 + rk2*r_2 - s_ii*(rk1 + rk2),
                                -qk2*r_2 + s_ii*(qk1 + qk2),
                                -tk2*r_2 + s_ii*(tk0 + tk2),
                                -1 + rk2*r_2 + s_ii*(rk0 - rk2),
                                -qk2*r_2 - s_ii*(qk0 - qk2),
                                -s_ii*(tk0 + tk1),
                                s_ii*(rk0 - rk1),
                                -s_ii*(qk0 - qk1)], dtype=float)

        H_xs[:, ii] = np.array([-pk1*s_2 - r_ii*(pk2 - pk1),
                                qk1*s_2 - r_ii*(qk1 + qk2),
                                -4 + 6*(r_ii + s_ii) + rk1*s_2 - r_ii*(rk1 + rk2),
                                r_ii*(pk0 + pk2),
                                r_ii*(qk0 - qk2),
                                -r_ii*(rk2 - rk0),
                                pk1*s_2 - r_ii*(pk0 + pk1),
                                qk1*s_2 + r_ii*(qk0 - qk1),
                                -2 + 6*s_ii + rk1*s_2 + r_ii*(rk0 - rk1)], dtype=float)

        H_ys[:, ii] = np.array([-tk1*s_2 - r_ii*(tk2 - tk1),
                                1 + rk1*s_2 - r_ii*(rk1 + rk2),
                                -qk1*s_2 + r_ii*(qk1 + qk2),
                                r_ii*(tk0 + tk2),
                                r_ii*(rk0 - rk2),
                                -r_ii*(qk0 - qk2),
                                tk1*s_2 - r_ii*(tk0 + tk1),
                                -1 + rk1*s_2 + r_ii*(rk0 - rk1),
                                -qk1*s_2 - r_ii*(qk0 - qk1)], dtype=float)

    return H_xr, H_yr, H_xs, H_ys

@njit
def allman_constants(rho, thick, area, x_loc, y_loc):
# def allman_constants(rho, thick, area, x_12, x_23, x_31, y_12, y_23, y_31):

    # Useful constants
    x_12, x_23, x_31 = x_loc[0] - x_loc[1], x_loc[1] - x_loc[2], x_loc[2] - x_loc[0]
    y_12, y_23, y_31 = y_loc[0] - y_loc[1], y_loc[1] - y_loc[2], y_loc[2] - y_loc[0]
    y_21, y_32, y_13 = y_loc[1] - y_loc[0], y_loc[2] - y_loc[1], y_loc[0] - y_loc[2]

    # Precompute repeated terms
    x_12, x_23, x_31 = 0.5*x_12, 0.5*x_23, 0.5*x_31
    y_21, y_32, y_13 = -0.5*y_12, -0.5*y_23, -0.5*y_31
    premult = rho*thick*area

    # Allman matrices
    Bw = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 1, 0, 0]])

    Bwa = np.array([[0, y_21, x_12, 0, -y_21, -x_12, 0, 0, 0],
                    [0, 0, 0, 0, y_32, x_23, 0, -y_32, -x_23],
                    [0, -y_13, -x_31, 0, 0, 0, 0, y_13, x_31],
                    [-1, -y_21, -x_12, 1, -y_21, -x_12, 0, 0, 0],
                    [0, 0, 0, -1, -y_32, -x_23, 1, -y_32, -x_23],
                    [1, -y_13, -x_31, 0, 0, 0, -1, -y_13, -x_31]])

    NN = premult*(1/6)*np.array([[1.0, 0.5, 0.5],
                                 [0.5, 1.0, 0.5],
                                 [0.5, 0.5, 1.0]], dtype=float)

    NNa = premult*(1/30)*np.array([[1, 0.5, 1, -1/6, 0, 1/6],
                                   [1, 1, 0.5, 1/6, -1/6, 0],
                                   [0.5, 1, 1, 0, 1/6, -1/6]], dtype=float)

    NaN = NNa.T
    NaNa = premult*np.array([[1/90, 1/180, 1/180, 0, -1/1260, 1/1260],
                             [1/180, 1/90, 1/180, 1/1260, 0, -1/1260],
                             [1/180, 1/180, 1/90, -1/1260, 1/1260, 0],
                             [0, 1/1260, -1/1260, 1/840, -1/2520, -1/2520],
                             [-1/1260, 0, 1/1260, -1/2520, 1/840, -1/2520],
                             [1/1260, -1/1260, 0, -1/2520, -1/2520, 1/840]])

    return Bw, Bwa, NN, NNa, NaN, NaNa


class STRUCT_FACE_3(Element2D):

    NODES_PER_ELEMENT = 3
    DOF_PER_NODE = 6
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model):
        self.model = model
        self.initialize_variables()
        self.define_integration_points_for_bending()
        self.define_integration_points_for_membrane()
        # self.process_shape_functions_and_derivatives()
        self.process_shape_functions_and_derivatives_for_membrane()

    def initialize_variables(self):
        """ """
        self.element_label = "structural_triangular_3"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connectivity = self.model.mesh.faces_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity)

    def define_integration_points_for_bending(self):
        """ """

        # integration points
        self.nint_bend = 3

        # Integration points
        self.pint_bend = np.array([ [1/2, 1/2], 
                                    [  0, 1/2], 
                                    [1/2,   0] ], dtype=float)

        self.weight_bend = (1/3) ** 2

    def define_integration_points_for_membrane(self):
        """ """
        # integration points
        self.nint_memb = 3

        # Integration points
        self.pint_memb = np.array([ [1/6, 1/6], 
                                    [4/6, 1/6], 
                                    [1/6, 4/6] ], dtype=float)
        
        self.weight_memb = 1 / 3

    def process_shape_functions_and_derivatives_for_bending(self, x_loc: np.ndarray, y_loc: np.ndarray):
        """ This method processes the shape functions and their
            derivatives for all integration points.
        """

        batoz_cte, area = batoz_constants(x_loc, y_loc)

        r = np.repeat(self.pint_bend[:, 0], self.nint_bend)
        s = np.repeat(self.pint_bend[:, 1], self.nint_bend)

        # Batoz shape functions
        H_xr, H_yr, H_xs, H_ys = batoz_shape_functions(r, s, batoz_cte)

        return np.stack([H_xr, H_yr, H_xs, H_ys], axis=0)

    def process_shape_functions_and_derivatives_for_membrane(self):
        """ This method processes the shape functions and their
            derivatives for all integration points.
        """

        r = self.pint_memb[:, 0]
        s = self.pint_memb[:, 1]

        # Shape functions for each integration point
        self.phi_memb = np.column_stack((1 - r - s, r, s), dtype=float)

        # Derivatives of shape functions
        self.dphi_memb = np.array([ [-1, -1], 
                                    [ 1,  0], 
                                    [ 0,  1] ], dtype=float)

    def get_constitutive_model(self, el_index, model_type="linear-isotropic"):
        """This methdo returns the material constitutive model."""
        self.material = self.model.properties.get_material(element=el_index)
        E = self.material.young_modulus
        nu = self.material.poisson_ratio
        rho = self.material.density
        t = self.model.mesh.surface_thickness
        # print(self.material.density, self.material.young_modulus, self.material.poisson_ratio)

        if model_type == "linear-isotropic":

            # Constititive model - Linear isotropic material

            # Elasticity matrix - bending
            Db = (E * t ** 3 / (12 * (1 - nu ** 2))) * np.array([[ 1, nu, 0],
                                                                 [nu,  1, 0],
                                                                 [ 0,  0, (1 - nu) / 2]], dtype=float)
            # Elasticity matrix - membrane
            Dm = (E / (1 - nu ** 2)) * np.array([[ 1, nu, 0],
                                                 [nu,  1, 0],
                                                 [ 0,  0, (1 - nu) / 2]], dtype=float)

            return Db, Dm, rho

    def elementary_matrices(self, el_index):
        """This method returns elementary stiffness and mass matrices for HEXAHEDRON-8 nodes.
        ANSYS SOLID45 w/o extra diplacements (very simple)
        """

        #
        ie = self.connectivity[el_index, 1:]
        Db, Dm, rho = self.get_constitutive_model(ie, model_type="linear-isotropic")
        t = self.model.mesh.face_element_thickness[el_index]["surface_thickness"]
        #
        nodal_coords = self.nodal_coordinates[ie, 1:4]
        x_loc, y_loc, area, T = get_local_coordinates(nodal_coords)
        H = self.process_shape_functions_and_derivatives_for_bending(x_loc, y_loc)

        # Processing the bending matrices
        
        # Deformation matrix
        B = (1 / (2 * area)) * np.array([    (y_loc[2] - y_loc[0]) * H[0] + (y_loc[0] - y_loc[1]) * H[2],
                                            -(x_loc[2] - x_loc[0]) * H[1] - (x_loc[0] - x_loc[1]) * H[3],
                                            -(x_loc[2] - x_loc[0]) * H[0] - (x_loc[0] - x_loc[1]) * H[2] + (y_loc[2] - y_loc[0]) * H[1] + (y_loc[0] - y_loc[1]) * H[3]], dtype=float)

        # Numerical integration
        K_bend = area * self.weight_bend * np.sum((np.einsum('nmp,mqp->nqp', np.einsum('mnp,nq->mqp', np.swapaxes(B, 1, 0), Db), B)), axis=2)

        # Allman (1996) mass matrix
        Bw, Bwa, NN, NNa, NaN, NaNa = allman_constants(rho, t, area, x_loc, y_loc)
        M_bend = Bw.T @ (NN @ Bw + NNa @ Bwa) + Bwa.T @ (NaN @ Bw + NaNa @ Bwa)
        # M_bend = Bw.T @ NN @ Bw + Bw.T @ NNa @ Bwa + Bwa.T @ NaN @ Bw + Bwa.T @ NaNa @ Bwa

        # Indexing to global element matrices
        index = [2, 3, 4, 8, 9, 10, 14, 15, 16]
        Ke[np.ix_(index, index)] = K_bend
        Me[np.ix_(index, index)] = M_bend

        # Processing the membrane matrices

        # Jacobian matrix
        JAC = np.array([[x_loc[1] - x_loc[0], y_loc[1] - y_loc[0]], 
                        [x_loc[2] - x_loc[0], y_loc[2] - y_loc[0]]], dtype=float)

        detJAC, invJAC = get_detJAC_and_invJAC(JAC)
        dphi_t = (invJAC @ self.dphi_memb.T).T

        # Element deformation matrix
        B = np.array([  [dphi_t[0, 0], 0, dphi_t[1, 0], 0, dphi_t[2, 0], 0],
                        [0, dphi_t[0, 1], 0, dphi_t[1, 1], 0, dphi_t[2, 1]],
                        [dphi_t[0, 1], dphi_t[0, 0], dphi_t[1, 1], dphi_t[1, 0], dphi_t[2, 1], dphi_t[2, 0]]  ], dtype=float)

        # Element membrane stiffness matrix
        K_memb = 0.5 * detJAC * t * B.T @ Dm @ B

        N = np.zeros((self.nint_memb, 2, self.DOFS_PER_ELEMENT), dtype=float)
        N[:, 0, 0::2] = self.phi_memb 
        N[:, 1, 1::2] = self.phi_memb

        # # Product N.T @ N for each integration point
        # NTN = np.einsum('nij,njk->nik', N.transpose(0, 2, 1), N)

        # # Element membrane mass matrix
        # M_memb = 0.5 * weight * detJAC * rho * t * NTN.sum(axis=0)

        M_memb = 0.
        for i in range(self.nint_memb):
            M_memb += 0.5 * rho * t * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.weight_memb)

        #
        Ke = np.zeros([self.DOFS_PER_ELEMENT, self.DOFS_PER_ELEMENT], dtype=float)
        Me = np.zeros([self.DOFS_PER_ELEMENT, self.DOFS_PER_ELEMENT], dtype=float)

        # Indexing to global element matrices
        index = [0, 1, 6, 7, 12, 13]
        Ke[np.ix_(index, index)] = K_memb
        Me[np.ix_(index, index)] = M_memb

        # DRILLING DOF

        # Insertion of drilling dof
        index = [5, 11, 17]
        # drill = np.max(np.diagonal(K_elem))/1000
        # drill = np.min(np.diag(K_bend))
        drill = 1e-5
        Ke[np.ix_(index, index)] = drill
        Me[np.ix_(index, index)] = 1e-18

        # TRANSFORMATION TO GLOBAL COORDINATE SYSTEM
        Ke_gcs = T.T @ Ke @ T
        Me_gcs = T.T @ Me @ T

        return Ke_gcs, Me_gcs

        # #
        # JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        # detJAC, invJAC = get_detJAC_and_invJAC(JAC)
        # dphi_t = invJAC @ self.dphi
        # #
        # B = np.zeros((self.nint, 6, self.DOFS_PER_ELEMENT), dtype=float)
        # N = np.zeros((self.nint, 3, self.DOFS_PER_ELEMENT), dtype=float)
        # #
        # B[:, 0, 0::3] = dphi_t[:, 0, :]
        # B[:, 1, 1::3] = dphi_t[:, 1, :]
        # B[:, 2, 2::3] = dphi_t[:, 2, :]
        # B[:, 3, 0::3] = dphi_t[:, 1, :]
        # B[:, 3, 1::3] = dphi_t[:, 0, :]
        # B[:, 4, 0::3] = dphi_t[:, 2, :]
        # B[:, 4, 2::3] = dphi_t[:, 0, :]
        # B[:, 5, 1::3] = dphi_t[:, 2, :]
        # B[:, 5, 2::3] = dphi_t[:, 1, :]
        # #
        # N[:, 0, 0::3] = self.phi
        # N[:, 1, 1::3] = self.phi
        # N[:, 2, 2::3] = self.phi
        # #
        # # integration loop
        # Ke, Me = 0, 0
        # for i in range(self.nint):
        #     Ke += B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC[i, :, :] * self.wps)
        #     Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps)
        # #
        # return Ke, Me

    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivity = self.connectivity[:, [0, 4, 5, 6, 7, 8, 9, 10, 11]]

    def generate_ind_rows_cols(self):
        """This method processess the dofs indices (rows and columns) for assembly"""

        self.reorder_connect()
        dofs, edofs = self.DOF_PER_NODE, self.DOFS_PER_ELEMENT

        ind_dofs = (
            np.array(
                [
                    dofs * self.connectivity[:, 1] - 1,
                    dofs * self.connectivity[:, 1],
                    dofs * self.connectivity[:, 1] + 1,
                    dofs * self.connectivity[:, 2] - 1,
                    dofs * self.connectivity[:, 2],
                    dofs * self.connectivity[:, 2] + 1,
                    dofs * self.connectivity[:, 3] - 1,
                    dofs * self.connectivity[:, 3],
                    dofs * self.connectivity[:, 3] + 1,
                    dofs * self.connectivity[:, 4] - 1,
                    dofs * self.connectivity[:, 4],
                    dofs * self.connectivity[:, 4] + 1,
                    dofs * self.connectivity[:, 5] - 1,
                    dofs * self.connectivity[:, 5],
                    dofs * self.connectivity[:, 5] + 1,
                    dofs * self.connectivity[:, 6] - 1,
                    dofs * self.connectivity[:, 6],
                    dofs * self.connectivity[:, 6] + 1,
                    dofs * self.connectivity[:, 7] - 1,
                    dofs * self.connectivity[:, 7],
                    dofs * self.connectivity[:, 7] + 1,
                    dofs * self.connectivity[:, 8] - 1,
                    dofs * self.connectivity[:, 8],
                    dofs * self.connectivity[:, 8] + 1,
                ],
                dtype=int,
            )
            + 1
        ).T

        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

        return self.ind_rows, self.ind_cols

#fmt: on

if __name__ == "__main__":

    nodal_coords = np.array([[1.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0],
                             [0.0, 0.0, 1.0]], dtype=float)

    x_loc, y_loc, T = get_local_coordinates(nodal_coords)

    print(f"=> x coordinates (lcs): {x_loc}")
    print(f"=> y coordinates (lcs): {y_loc}")
