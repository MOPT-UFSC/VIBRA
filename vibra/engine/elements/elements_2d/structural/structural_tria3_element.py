#fmt: off

from typing import TYPE_CHECKING

from vibra.engine.elements.surface_elements import Element2D
from vibra.engine.properties.material import Material

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np

np.set_printoptions(precision=18)#threshold=sys.maxsize)


def get_local_coordinates(nodal_coords: np.ndarray):

    x = nodal_coords[:, 0]
    y = nodal_coords[:, 1]
    z = nodal_coords[:, 2]

    # x vector
    v_x = np.array([x[1] - x[0], y[1] - y[0], z[1] - z[0]], dtype=float)

    # Auxiliary vector
    v_a = np.array([x[2] - x[0], y[2] - y[0], z[2] - z[0]], dtype=float)

    # z vector
    v_z = np.cross(v_x, v_a)

    # y vector
    v_y = np.cross(v_z, v_x)

    # Element area calculation
    area = np.linalg.norm(v_z) / 2

    if area == 0:
        return None, None, 0., None

    n_x = v_x / np.linalg.norm(v_x)
    n_y = v_y / np.linalg.norm(v_y)
    n_z = v_z / np.linalg.norm(v_z)

    # Direction cosines
    dir_cossines = np.array([n_x, n_y, n_z], dtype=float)

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

def get_batoz_constants(x_loc: np.ndarray, y_loc: np.ndarray):
    """
        Constants (Batoz) - shape: (4, 3)

                                    [pk0, pk1, pk2; 
                                     qk0, qk1, qk2; 
                                     rk0, rk1, rk2; 
                                     tk0, tk1, tk2]

    """

    # Useful constants
    x_12, x_23, x_31 = x_loc[0] - x_loc[1], x_loc[1] - x_loc[2], x_loc[2] - x_loc[0]
    y_12, y_23, y_31 = y_loc[0] - y_loc[1], y_loc[1] - y_loc[2], y_loc[2] - y_loc[0]
    l_12, l_23, l_31 = x_12**2 + y_12**2, x_23**2 + y_23**2, x_31**2 + y_31**2
    y_21, y_32, y_13 = y_loc[1] - y_loc[0], y_loc[2] - y_loc[1], y_loc[0] - y_loc[2]

    # # Derivative of element area with respect to local coordinates
    # dA = np.array([[-y_12 - y_31, y_31, y_12], [x_31 + x_12, -x_31, -x_12]])/2

    # # Derivative of constants with respect to local coordinates
    # dx_12, dx_23, dx_31 = np.array([1, -1, 0]), np.array([0, 1, -1]), np.array([-1, 0, 1])
    # dy_12, dy_23, dy_31 = np.array([1, -1, 0]), np.array([0, 1, -1]), np.array([-1, 0, 1])

    batoz_const = np.array([[    -6*x_23 / l_23,     -6*x_31 / l_31,     -6*x_12 / l_12],
                            [3*x_23*y_23 / l_23, 3*x_31*y_31 / l_31, 3*x_12*y_12 / l_12],
                            [  3*y_23**2 / l_23,   3*y_31**2 / l_31,   3*y_12**2 / l_12],
                            [    -6*y_23 / l_23,     -6*y_31 / l_31,     -6*y_12 / l_12]], dtype=float)

    return batoz_const


def get_batoz_shape_functions(r, s, batoz_const):

    N = len(r)

    pk0, pk1, pk2 = batoz_const[0, 0], batoz_const[0, 1], batoz_const[0, 2]
    qk0, qk1, qk2 = batoz_const[1, 0], batoz_const[1, 1], batoz_const[1, 2]
    rk0, rk1, rk2 = batoz_const[2, 0], batoz_const[2, 1], batoz_const[2, 2]
    tk0, tk1, tk2 = batoz_const[3, 0], batoz_const[3, 1], batoz_const[3, 2]

    # Initialization in numba format
    H_xr = np.zeros((9, N), dtype=float)
    H_yr = np.zeros((9, N), dtype=float)
    H_xs = np.zeros((9, N), dtype=float) 
    H_ys = np.zeros((9, N), dtype=float)

    # Loop over each integration point
    for ii in range(N):

        # Precompute repeated terms
        r_ii = r[ii]
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


def get_allman_constants(rho, thick, area, x_loc, y_loc):

    # Auxiliary constants
    x_12, x_23, x_31 = x_loc[0] - x_loc[1], x_loc[1] - x_loc[2], x_loc[2] - x_loc[0]
    y_12, y_23, y_31 = y_loc[0] - y_loc[1], y_loc[1] - y_loc[2], y_loc[2] - y_loc[0]
    y_21, y_32, y_13 = y_loc[1] - y_loc[0], y_loc[2] - y_loc[1], y_loc[0] - y_loc[2]

    # Precompute repeated terms
    x_12, x_23, x_31 = 0.5*x_12, 0.5*x_23, 0.5*x_31
    y_21, y_32, y_13 = -0.5*y_12, -0.5*y_23, -0.5*y_31
    # premult = rho * thick * area

    # Allman matrices
    Bw = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 1, 0, 0]], dtype=float)

    Bwa = np.array([[0, y_21, x_12, 0, -y_21, -x_12, 0, 0, 0],
                    [0, 0, 0, 0, y_32, x_23, 0, -y_32, -x_23],
                    [0, -y_13, -x_31, 0, 0, 0, 0, y_13, x_31],
                    [-1, -y_21, -x_12, 1, -y_21, -x_12, 0, 0, 0],
                    [0, 0, 0, -1, -y_32, -x_23, 1, -y_32, -x_23],
                    [1, -y_13, -x_31, 0, 0, 0, -1, -y_13, -x_31]], dtype=float)

    NN = (rho*thick*area/6) * np.array([[1.0, 0.5, 0.5],
                                        [0.5, 1.0, 0.5],
                                        [0.5, 0.5, 1.0]], dtype=float)

    NNa = (rho*thick*area/30) * np.array([[1, 0.5, 1, -1/6, 0, 1/6],
                                          [1, 1, 0.5, 1/6, -1/6, 0],
                                          [0.5, 1, 1, 0, 1/6, -1/6]], dtype=float)

    NaN = NNa.T
    NaNa = (rho*thick*area) * np.array([[  1/90,    1/180,   1/180,       0, -1/1260,  1/1260],
                                        [ 1/180,     1/90,   1/180,  1/1260,       0, -1/1260],
                                        [ 1/180,    1/180,    1/90, -1/1260,  1/1260,       0],
                                        [     0,   1/1260, -1/1260,   1/840, -1/2520, -1/2520],
                                        [-1/1260,       0,  1/1260, -1/2520,   1/840, -1/2520],
                                        [ 1/1260, -1/1260,       0, -1/2520, -1/2520,   1/840]], dtype=float)

    return Bw, Bwa, NN, NNa, NaN, NaNa


def get_detJAC_and_invJAC(JAC: np.ndarray):
    """ """

    detJAC = JAC[0, 0] * JAC[1, 1] - JAC[0, 1] * JAC[1, 0]
    AUJJ = np.array([[ JAC[1, 1], -JAC[0, 1]], 
                     [-JAC[1, 0],  JAC[0, 0]]], dtype=float)

    return detJAC, (1 / detJAC) * AUJJ


class STRUCT_TRIANGLE_3(Element2D):

    NODES_PER_ELEMENT = 3
    DOF_PER_NODE = 6
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivity = None
        self.element_label = "structural_triangular_3"

        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.faces_connectivity = self.model.mesh.faces_connectivity

        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = self.faces_connectivity.shape[0]

        self.local_dof = np.arange(self.DOF_PER_NODE, dtype=int)

        self.define_integration_points_for_bending()
        self.define_integration_points_for_membrane()
        self.process_shape_functions_and_derivatives_for_membrane()


    def define_integration_points_for_bending(self):
        """ This method computes the integration points for the bending effects. """

        # integration points
        self.nint_bend = 3

        # Integration points
        self.pint_bend = np.array([ [1/2, 1/2], 
                                    [  0, 1/2], 
                                    [1/2,   0] ], dtype=float)

        self.weight_bend = (1/3) ** 2

    def define_integration_points_for_membrane(self):
        """ This method computes the integration points for the membrane effects. """

        # integration points
        self.nint_memb = 3

        # Integration points
        self.pint_memb = np.array([ [1/6, 1/6], 
                                    [4/6, 1/6], 
                                    [1/6, 4/6] ], dtype=float)

        self.weight_memb = 1 / 3

    def process_shape_functions_and_derivatives_for_bending(self, x_loc: np.ndarray, y_loc: np.ndarray):
        """ This method computes the shape functions and their
            derivatives for bending effects over all integration points.
        """

        batoz_cte = get_batoz_constants(x_loc, y_loc)

        r = np.repeat(self.pint_bend[:, 0], self.nint_bend)
        s = np.repeat(self.pint_bend[:, 1], self.nint_bend)

        # Batoz shape functions
        H_xr, H_yr, H_xs, H_ys = get_batoz_shape_functions(r, s, batoz_cte)

        return np.stack([H_xr, H_yr, H_xs, H_ys], axis=0)

    def process_shape_functions_and_derivatives_for_membrane(self):
        """ This method computes the shape functions and their
            derivatives for membrane effects over all integration points.
        """

        r = self.pint_memb[:, 0]
        s = self.pint_memb[:, 1]

        # Shape functions for each integration point
        self.phi_memb = np.column_stack((1 - r - s, r, s))

        # Derivatives of shape functions
        self.dphi_memb = np.array([ [-1, -1], 
                                    [ 1,  0], 
                                    [ 0,  1] ], dtype=float)

    def get_constitutive_model(self, material: Material, t: float, model_type="linear-isotropic"):
        """This methdo returns the material constitutive model."""

        self.material = material
        E = self.material.elasticity_modulus
        nu = self.material.poisson_ratio
        rho = self.material.material_density

        if model_type == "linear-isotropic":

            # Constititive model - Linear isotropic material

            # Elasticity matrix - bending
            Db = ((E * t ** 3) / (12 * (1 - nu ** 2))) * np.array([[ 1, nu, 0],
                                                                   [nu,  1, 0],
                                                                   [ 0,  0, (1 - nu) / 2]], dtype=float)

            # Elasticity matrix - membrane
            Dm = (E / (1 - nu ** 2)) * np.array([[ 1, nu, 0],
                                                 [nu,  1, 0],
                                                 [ 0,  0, (1 - nu) / 2]], dtype=float)

            return Db, Dm, rho

    def elementary_matrices(self, el_index: int, material: Material, t: float):
        """This method returns elementary stiffness and mass matrices for TRIANGLE-3 nodes.

        """

        Ke = np.zeros([self.DOF_PER_ELEMENT, self.DOF_PER_ELEMENT], dtype=float)
        Me = np.zeros([self.DOF_PER_ELEMENT, self.DOF_PER_ELEMENT], dtype=float)

        ie = self.connectivity[el_index, 1:]
        nodal_coords = self.nodal_coordinates[ie, 1:4]
        x_loc, y_loc, area, T = get_local_coordinates(nodal_coords)

        if area == 0:
            message = f"The element #{el_index} has invalid connectivity.\n"
            message += f"Connectivity: {ie}\n"
            print(message)
            return Ke, Me

        H = self.process_shape_functions_and_derivatives_for_bending(x_loc, y_loc)

        Db, Dm, rho = self.get_constitutive_model(material, t, model_type="linear-isotropic")

        # Processing the bending matrices
        b_11 =  (y_loc[2] - y_loc[0]) * H[0] + (y_loc[0] - y_loc[1]) * H[2]
        b_12 = -(x_loc[2] - x_loc[0]) * H[1] - (x_loc[0] - x_loc[1]) * H[3]
        b_13 = -(x_loc[2] - x_loc[0]) * H[0] - (x_loc[0] - x_loc[1]) * H[2] + (y_loc[2] - y_loc[0]) * H[1] + (y_loc[0] - y_loc[1]) * H[3]

        # Deformation matrix
        B = (1 / (2 * area)) * np.array([b_11, b_12, b_13], dtype=float)

        # Numerical integration
        K_bend = area * self.weight_bend * np.sum((np.einsum('nmp,mqp->nqp', np.einsum('mnp,nq->mqp', np.swapaxes(B, 1, 0), Db), B)), axis=2)

        # TODO: update the numerical integration
        # K_bend = 0.
        # for i in range(self.nint_bend**2):
        #     K_bend += area * B[:,:, i].T @ Db @ B[:, :, i] * self.weight_bend

        # Allman (1996) mass matrix
        Bw, Bwa, NN, NNa, NaN, NaNa = get_allman_constants(rho, t, area, x_loc, y_loc)
        M_bend = Bw.T @ (NN @ Bw + NNa @ Bwa) + Bwa.T @ (NaN @ Bw + NaNa @ Bwa)

        # Processing the membrane matrices

        # Jacobian matrix
        JAC = np.array([[x_loc[1] - x_loc[0], y_loc[1] - y_loc[0]], 
                        [x_loc[2] - x_loc[0], y_loc[2] - y_loc[0]]], dtype=float)

        detJAC, invJAC = get_detJAC_and_invJAC(JAC)
        dphi_t = invJAC @ self.dphi_memb.T

        # Element deformation matrix
        B = np.array([[dphi_t[0, 0],            0, dphi_t[0, 1],            0, dphi_t[0, 2],            0],
                      [           0, dphi_t[1, 0],            0, dphi_t[1, 1],            0, dphi_t[1, 2]],
                      [dphi_t[1, 0], dphi_t[0, 0], dphi_t[1, 1], dphi_t[0, 1], dphi_t[1, 2], dphi_t[0, 2]]], dtype=float)
        
        # B = np.array([[dphi_t[0, 0],            0, dphi_t[1, 0]],
        #               [           0, dphi_t[1, 0], dphi_t[0, 0]],
        #               [dphi_t[0, 1],            0, dphi_t[1, 1]],
        #               [           0, dphi_t[1, 1], dphi_t[0, 1]],
        #               [dphi_t[0, 2],            0, dphi_t[1, 2]],
        #               [           0, dphi_t[1, 2], dphi_t[0, 2]]], dtype=float).T

        # B = np.zeros((self.nint_memb, self.DOF_PER_NODE), dtype=float)
        # B[0, 0::2] = B[2, 1::2] = dphi_t[0, :]
        # B[1, 1::2] = B[2, 0::2] = dphi_t[1, :]

        # Element membrane stiffness matrix
        K_memb = 0.5 * detJAC * t * B.T @ Dm @ B

        N = np.zeros((self.nint_memb, 2, self.DOF_PER_NODE))
        N[:, 0, 0::2] = self.phi_memb
        N[:, 1, 1::2] = self.phi_memb

        M_memb = 0.
        for i in range(self.nint_memb):
            M_memb += 0.5 * rho * t * N[i, :, :].T @ N[i, :, :] * (detJAC * self.weight_memb)

        # # Product N.T @ N for each integration point
        # NTN = np.einsum('nij,njk->nik', N.transpose(0, 2, 1), N)

        # # Element membrane mass matrix
        # M_memb = 0.5 * self.weight_memb * detJAC * rho * t * NTN.sum(axis=0)

        # Indexing bend to global element matrices
        index = [2, 3, 4, 8, 9, 10, 14, 15, 16]
        Ke[np.ix_(index, index)] = K_bend
        Me[np.ix_(index, index)] = M_bend

        # Indexing membrane to global element matrices
        index = [0, 1, 6, 7, 12, 13]
        Ke[np.ix_(index, index)] = K_memb
        Me[np.ix_(index, index)] = M_memb

        # Indexing drilling dof
        index = [5, 11, 17]
        Ke[np.ix_(index, index)] = 1e-5  # drill
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
        # B = np.zeros((self.nint, 6, self.DOF_PER_ELEMENT), dtype=float)
        # N = np.zeros((self.nint, 3, self.DOF_PER_ELEMENT), dtype=float)
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
        if self.faces_connectivity.shape[1] == self.NODES_PER_ELEMENT + 4:
            self.connectivity = self.faces_connectivity[:, [0, 4, 5, 6]]


    def generate_ind_rows_cols(self, reorder: bool = True):
        """ 
        This method processess the dof indices (rows and columns) 
        for assembly
        """

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.faces_connectivity[:, [0, 4, 5, 6]]

        dof, edof = self.DOF_PER_NODE, self.DOF_PER_ELEMENT
        n_el = self.faces_connectivity.shape[0]

        local_dof = np.arange(dof, dtype=int)
        ind_dof = np.zeros((n_el, edof), dtype=int)

        for j in range(self.NODES_PER_ELEMENT):
            ind_dof[:, j*dof : (1 + j)*dof] = dof * self.connectivity[:, j+1].reshape(-1, 1) + local_dof

        vect_indices = ind_dof.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dof, edof)).flatten()

        # ind_dof = (
        #     np.array([  dof * self.connectivity[:, 1] + 0,
        #                 dof * self.connectivity[:, 1] + 1,
        #                 dof * self.connectivity[:, 1] + 2,
        #                 dof * self.connectivity[:, 1] + 3,
        #                 dof * self.connectivity[:, 1] + 4,
        #                 dof * self.connectivity[:, 1] + 5,
        #                 dof * self.connectivity[:, 2] + 0,
        #                 dof * self.connectivity[:, 2] + 1,
        #                 dof * self.connectivity[:, 2] + 2,
        #                 dof * self.connectivity[:, 2] + 3,
        #                 dof * self.connectivity[:, 2] + 4,
        #                 dof * self.connectivity[:, 2] + 5,
        #                 dof * self.connectivity[:, 3] + 0,
        #                 dof * self.connectivity[:, 3] + 1,
        #                 dof * self.connectivity[:, 3] + 2,
        #                 dof * self.connectivity[:, 3] + 3,
        #                 dof * self.connectivity[:, 3] + 4,
        #                 dof * self.connectivity[:, 3] + 5  ], dtype=int)).T

        # vect_indices = ind_dof.flatten()
        # self.ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        # self.ind_cols = (np.tile(ind_dof, (1, edof))).flatten()

        # linhas = np.tile(vect_indices, (edof, 1)).T
        # colunas = (np.tile(ind_dof, (1, edof))).reshape(-1, self.DOF_PER_ELEMENT)

        # np.savetxt("linhas.dat", linhas, delimiter=",", fmt="%i")
        # np.savetxt("colunas.dat", colunas, delimiter=",", fmt="%i")

        return self.ind_rows, self.ind_cols


    def force_vector(self, element_id: int, **kwargs):#, line_pressure, pressure, normpress, e_nodes_load, e_nodes_pressure, e_elems_normpress, n_unit_elem, **kwargs):

        distributed_line_load = kwargs.get("distributed_line_load", None) 
        line_connectivity = kwargs.get("line_connectivity", None)

        distributed_area_load = kwargs.get("distributed_area_load", None) 
        area_connectivity = kwargs.get("area_connectivity", None)

        normal_pressure_load = kwargs.get("normal_pressure_load", None)
        normal_unit_vector = kwargs.get("normal_unit_vector", None)

        loads = np.zeros(int(self.DOF_PER_ELEMENT / 2), dtype=float)

        # Local coordinate system definition
        node_ids = self.connectivity[element_id, 1:]
        nodal_coords = self.nodal_coordinates[node_ids, 1:]
        x_loc, y_loc, *_ = get_local_coordinates(nodal_coords)

        if distributed_line_load is not None:
            e_nodes_load = line_connectivity

            ## LOAD - LINE PRESSURE
            # if np.count_nonzero(e_nodes_load) >= 2:

            # Line integration points
            num = np.sqrt(3 / 5) / 2
            if e_nodes_load[0] == 1 and e_nodes_load[1] == 1:

                dx_dst = x_loc[1] - x_loc[0]
                dy_dst = y_loc[1] - y_loc[0]
                coord_int = np.array([[0.5-num,     0.5, 0.5+num], 
                                      [      0,       0,       0]], dtype=float)

            elif e_nodes_load[0] == 1 and e_nodes_load[2] == 1:

                dx_dst = x_loc[2] - x_loc[0]
                dy_dst = y_loc[2] - y_loc[0]
                coord_int = np.array([[      0,       0,       0], 
                                      [0.5-num,     0.5, 0.5+num]], dtype=float)

            else:

                dx_dst = x_loc[2] - x_loc[1]
                dy_dst = y_loc[2] - y_loc[1]
                coord_int = np.array([[0.5-num, 0.5, 0.5+num], 
                                      [0.5-num, 0.5, 0.5+num]], dtype=float)
                
            weights = np.array([5, 8, 5], dtype=float) / 18

            # Determinant of the Jacobian
            det_J = np.sqrt(dx_dst**2 + dy_dst**2)

            # Numerical integration
            for i, weight in enumerate(weights):

                # Coordinates of integration points
                r = coord_int[0, i]
                s = coord_int[1, i]

                # Shape functions
                N = np.array([[1 - r - s,         0,         0, r, 0, 0, s, 0, 0],
                              [        0, 1 - r - s,         0, 0, r, 0, 0, s, 0],
                              [        0,         0, 1 - r - s, 0, 0, r, 0, 0, s]], dtype=float)

                # Load vector
                loads += det_J * weight * N.T @ distributed_line_load


        if distributed_area_load is not None:
            e_nodes_pressure = area_connectivity

            ## PRESSURE
            if np.count_nonzero(e_nodes_pressure) == 3:

                # Integration points
                r = 1 / 3
                s = 1 / 3

                # Jacobian
                J = np.array([[x_loc[1] - x_loc[0], y_loc[1] - y_loc[0]], 
                              [x_loc[2] - x_loc[0], y_loc[2] - y_loc[0]]], dtype=float)

                # Determinant of the Jacobian
                det_J = np.linalg.det(J)

                # Shape functions
                N = np.array([[1 - r - s,         0,         0, r, 0, 0, s, 0, 0],
                              [        0, 1 - r - s,         0, 0, r, 0, 0, s, 0],
                              [        0,         0, 1 - r - s, 0, 0, r, 0, 0, s]], dtype=float)

                # Pressure vector
                loads += 0.5 * det_J * N.T @ distributed_area_load

        if normal_pressure_load is not None:

            e_elems_normpress = area_connectivity

            ## NORMAL PRESSURE
            if e_elems_normpress == 1:

                # Integration points
                r = 1 / 3
                s = 1 / 3

                # Jacobian
                J = np.array([[x_loc[1] - x_loc[0], y_loc[1] - y_loc[0]], 
                              [x_loc[2] - x_loc[0], y_loc[2] - y_loc[0]]], dtype=float)

                # Determinant of the Jacobian
                det_J = np.linalg.det(J)

                # Shape functions
                N = np.array([[1 - r - s,         0,         0, r, 0, 0, s, 0, 0],
                              [        0, 1 - r - s,         0, 0, r, 0, 0, s, 0],
                              [        0,         0, 1 - r - s, 0, 0, r, 0, 0, s]], dtype=float)

                # Normal pressure vector
                loads += 0.5 * det_J * N.T @ (normal_pressure_load * normal_unit_vector)

        force_indexes = [0, 1, 2, 6, 7, 8, 12, 13, 14]

        F_elem = np.zeros(self.DOF_PER_ELEMENT, dtype=float)
        F_elem[force_indexes] = loads

        return F_elem

    def process_forces_for_distributed_load_over_line(self, connect: np.ndarray, active_nodes: list, distributed_load: np.ndarray):

        # Local coordinate system definition
        nodal_coords = self.nodal_coordinates[connect, 1:]
        x_loc, y_loc, *_ = get_local_coordinates(nodal_coords)

        # Line integration points
        num = np.sqrt(3 / 5) / 2

        if active_nodes == [1, 1, 0]:
            dx_dst = x_loc[1] - x_loc[0]
            dy_dst = y_loc[1] - y_loc[0]
            coord_int = np.array([[0.5-num,     0.5, 0.5+num], 
                                  [      0,       0,       0]], dtype=float)

        elif active_nodes == [1, 0, 1]:
            dx_dst = x_loc[2] - x_loc[0]
            dy_dst = y_loc[2] - y_loc[0]
            coord_int = np.array([[      0,       0,       0], 
                                  [0.5-num,     0.5, 0.5+num]], dtype=float)

        else:
            dx_dst = x_loc[2] - x_loc[1]
            dy_dst = y_loc[2] - y_loc[1]
            coord_int = np.array([[0.5-num, 0.5, 0.5+num], 
                                  [0.5-num, 0.5, 0.5+num]], dtype=float)

        weights = np.array([5, 8, 5], dtype=float) / 18

        # Determinant of the Jacobian
        det_J = np.sqrt(dx_dst**2 + dy_dst**2)

        loads = 0.
        # Numerical integration
        for i, weight in enumerate(weights):

            # Coordinates of integration points
            r = coord_int[0, i]
            s = coord_int[1, i]

            # Shape functions
            N = np.array([[1 - r - s,         0,         0, r, 0, 0, s, 0, 0],
                          [        0, 1 - r - s,         0, 0, r, 0, 0, s, 0],
                          [        0,         0, 1 - r - s, 0, 0, r, 0, 0, s]], dtype=float)

            # Load vector
            loads += det_J * weight * N.T @ distributed_load

        force_indexes = [0, 1, 2, 6, 7, 8, 12, 13, 14]

        number_of_frequencies = distributed_load.shape[1]
        F_elem = np.zeros((self.DOF_PER_ELEMENT, number_of_frequencies), dtype=complex)
        F_elem[force_indexes, :] = loads

        g_dof = self.DOF_PER_NODE * connect.reshape(-1, 1) + self.local_dof

        return g_dof.flatten(), F_elem

    def process_forces_for_distributed_load_over_area(self, connect: np.ndarray, distributed_load: np.ndarray):

        # Local coordinate system definition
        nodal_coords = self.nodal_coordinates[connect, 1:]
        x_loc, y_loc, *_ = get_local_coordinates(nodal_coords)

        # Integration points
        r = 1 / 3
        s = 1 / 3

        # Jacobian
        J = np.array([[x_loc[1] - x_loc[0], y_loc[1] - y_loc[0]], 
                      [x_loc[2] - x_loc[0], y_loc[2] - y_loc[0]]], dtype=float)

        # Determinant of the Jacobian
        det_J = np.linalg.det(J)

        # Shape functions
        N = np.array([[1 - r - s,         0,         0, r, 0, 0, s, 0, 0],
                      [        0, 1 - r - s,         0, 0, r, 0, 0, s, 0],
                      [        0,         0, 1 - r - s, 0, 0, r, 0, 0, s]], dtype=float)

        # Pressure vector
        loads = 0.5 * det_J * N.T @ distributed_load

        force_indexes = [0, 1, 2, 6, 7, 8, 12, 13, 14]

        number_of_frequencies = distributed_load.shape[1]
        F_elem = np.zeros((self.DOF_PER_ELEMENT, number_of_frequencies), dtype=complex)
        F_elem[force_indexes, :] = loads

        g_dof = self.DOF_PER_NODE * connect.reshape(-1, 1) + self.local_dof

        return g_dof.flatten(), F_elem

    def process_forces_for_normal_pressure_load(self, connect: np.ndarray, normal_pressure_load: np.ndarray):

        # Local coordinate system definition
        nodal_coords = self.nodal_coordinates[connect, 1:]
        normal_unit_vector = self.model.mesh.get_element_face_normal(connect)

        number_of_frequencies = normal_pressure_load.shape[1]
        F_elem = np.zeros((self.DOF_PER_ELEMENT, number_of_frequencies), dtype=complex)

        if normal_unit_vector is None:
            return F_elem

        x_loc, y_loc, *_ = get_local_coordinates(nodal_coords)

        # Integration points
        r = 1 / 3
        s = 1 / 3

        # Jacobian
        J = np.array([[x_loc[1] - x_loc[0], y_loc[1] - y_loc[0]], 
                      [x_loc[2] - x_loc[0], y_loc[2] - y_loc[0]]], dtype=float)

        # Determinant of the Jacobian
        det_J = np.linalg.det(J)

        # Shape functions
        N = np.array([[1 - r - s,         0,         0, r, 0, 0, s, 0, 0],
                      [        0, 1 - r - s,         0, 0, r, 0, 0, s, 0],
                      [        0,         0, 1 - r - s, 0, 0, r, 0, 0, s]], dtype=float)

        # Normal pressure vector
        loads = 0.5 * det_J * N.T @ (normal_unit_vector.reshape(-1, 1) @ normal_pressure_load)

        force_indexes = [0, 1, 2, 6, 7, 8, 12, 13, 14]
        F_elem[force_indexes, :] = loads

        g_dof = self.DOF_PER_NODE * connect.reshape(-1, 1) + self.local_dof

        return g_dof.flatten(), F_elem


def elementary_matrices(nodal_coords: np.ndarray):
    """ For validation purposes.
    """

    E = 2e11
    nu = 0.3
    rho = 7850
    t = 0.012

    # Constititive model - Linear isotropic material

    # Elasticity matrix - bending
    Db = ((E * t ** 3) / (12 * (1 - nu ** 2))) * np.array([[ 1, nu, 0],
                                                           [nu,  1, 0],
                                                           [ 0,  0, (1 - nu) / 2]], dtype=float)

    # Elasticity matrix - membrane
    Dm = (E / (1 - nu ** 2)) * np.array([[ 1, nu, 0],
                                         [nu,  1, 0],
                                         [ 0,  0, (1 - nu) / 2]], dtype=float)

    # integration points
    nint_bend = 3

    # Integration points
    pint_bend = np.array([  [1/2, 1/2], 
                            [  0, 1/2], 
                            [1/2,   0]  ], dtype=float)

    weight_bend = (1/3) ** 2

    # integration points
    nint_memb = 3

    # Integration points
    pint_memb = np.array([  [1/6, 1/6], 
                            [4/6, 1/6], 
                            [1/6, 4/6]  ], dtype=float)
    
    weight_memb = 1 / 3

    #
    x_loc, y_loc, area, T = get_local_coordinates(nodal_coords)
    batoz_cte = get_batoz_constants(x_loc, y_loc)

    r = np.repeat(pint_bend[:, 0], nint_bend)
    s = np.repeat(pint_bend[:, 1], nint_bend)

    # Batoz shape functions
    H_xr, H_yr, H_xs, H_ys = get_batoz_shape_functions(r, s, batoz_cte)

    H = np.stack([H_xr, H_yr, H_xs, H_ys], axis=0)

    # Processing the bending matrices

    b_11 =  (y_loc[2] - y_loc[0]) * H[0] + (y_loc[0] - y_loc[1]) * H[2]
    b_12 = -(x_loc[2] - x_loc[0]) * H[1] - (x_loc[0] - x_loc[1]) * H[3]
    b_13 = -(x_loc[2] - x_loc[0]) * H[0] - (x_loc[0] - x_loc[1]) * H[2] + (y_loc[2] - y_loc[0]) * H[1] + (y_loc[0] - y_loc[1]) * H[3]

    # Deformation matrix
    B = (1 / (2 * area)) * np.array([b_11, b_12, b_13], dtype=float)

    # Numerical integration
    K_bend = area * weight_bend * np.sum((np.einsum('nmp,mqp->nqp', np.einsum('mnp,nq->mqp', np.swapaxes(B, 1, 0), Db), B)), axis=2)

    # Allman (1996) mass matrix
    Bw, Bwa, NN, NNa, NaN, NaNa = get_allman_constants(rho, t, area, x_loc, y_loc)
    M_bend = Bw.T @ (NN @ Bw + NNa @ Bwa) + Bwa.T @ (NaN @ Bw + NaNa @ Bwa)
    # M_bend = Bw.T @ NN @ Bw + Bw.T @ NNa @ Bwa + Bwa.T @ NaN @ Bw + Bwa.T @ NaNa @ Bwa

    Ke = np.zeros([18, 18], dtype=float)
    Me = np.zeros([18, 18], dtype=float)

    # Indexing to global element matrices
    index = [2, 3, 4, 8, 9, 10, 14, 15, 16]
    Ke[np.ix_(index, index)] = K_bend
    Me[np.ix_(index, index)] = M_bend

    np.savetxt("K_bend_Vibra.dat", K_bend, delimiter=",")
    np.savetxt("M_bend_Vibra.dat", M_bend, delimiter=",")

    # Processing the membrane matrices
    r = pint_memb[:, 0]
    s = pint_memb[:, 1]

    # Shape functions for each integration point
    phi_memb = np.column_stack((1 - r - s, r, s))

    # Derivatives of shape functions
    dphi_memb = np.array([  [-1, -1], 
                            [ 1,  0], 
                            [ 0,  1]  ], dtype=float)

    # Jacobian matrix
    JAC = np.array([[x_loc[1] - x_loc[0], y_loc[1] - y_loc[0]], 
                    [x_loc[2] - x_loc[0], y_loc[2] - y_loc[0]]], dtype=float)

    detJAC, invJAC = get_detJAC_and_invJAC(JAC)
    dphi_t = (invJAC @ dphi_memb.T).T

    # print(JAC)
    # print(detJAC)
    # print(invJAC)
    # print(dphi_t)

    # Element deformation matrix
    B = np.array([[dphi_t[0, 0],            0, dphi_t[1, 0],            0, dphi_t[2, 0],            0],
                  [           0, dphi_t[0, 1],            0, dphi_t[1, 1],            0, dphi_t[2, 1]],
                  [dphi_t[0, 1], dphi_t[0, 0], dphi_t[1, 1], dphi_t[1, 0], dphi_t[2, 1], dphi_t[2, 0]]], dtype=float)

    # Element membrane stiffness matrix
    K_memb = 0.5 * detJAC * t * B.T @ Dm @ B

    # print(K_memb)

    N = np.zeros((nint_memb, 2, 6))
    N[:, 0, ::2] = phi_memb
    N[:, 1, 1::2] = phi_memb

    # Product N.T @ N for each integration point
    NTN = np.einsum('nij,njk->nik', N.transpose(0, 2, 1), N)

    # Element membrane mass matrix
    M_memb = 0.5 * weight_memb * detJAC * rho * t * NTN.sum(axis=0)

    # N = np.zeros((self.nint_memb, 2, self.DOF_PER_ELEMENT), dtype=float)
    # N[:, 0, 0::6] = self.phi_memb 
    # N[:, 1, 1::6] = self.phi_memb

    # M_memb = 0.
    # for i in range(self.nint_memb):
    #     M_memb += 0.5 * rho * t * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.weight_memb)

    np.savetxt("K_memb_Vibra.dat", K_memb, delimiter=",")
    np.savetxt("M_memb_Vibra.dat", M_memb, delimiter=",")

    # Indexing to global element matrices
    index = [0, 1, 6, 7, 12, 13]
    Ke[np.ix_(index, index)] = K_memb
    Me[np.ix_(index, index)] = M_memb

    np.savetxt("M_memb_Vibra.dat", M_memb, delimiter=",")
    np.savetxt("K_memb_Vibra.dat", K_memb, delimiter=",")

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


#fmt: on

if __name__ == "__main__":
    

    nodal_coords = np.array([[1.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0],
                             [0.0, 0.0, 1.0]], dtype=float)

    # nodal_coords = np.array([[0.0, 0.0, 0.0],
    #                          [1.0, 0.0, 0.0],
    #                          [0.0, 1.0, 0.0]], dtype=float)

    # nodal_coords = np.array([[0.0, 0.0, 0.0],
    #                          [0.5, 0.0, 0.0],
    #                          [0.0, 0.5, 0.0]], dtype=float)

    # nodal_coords = np.array([[0.5, 0.0, 0.0],
    #                          [0.5, 0.5, 0.0],
    #                          [0.0, 0.5, 0.0]], dtype=float)

    # x_loc, y_loc, area, T = get_local_coordinates(nodal_coords)

    # print(f"=> x coordinates (lcs): {x_loc}")
    # print(f"=> y coordinates (lcs): {y_loc}")
    # print(f"element area: {area} [m²]")

    # Ke, Me = elementary_matrices(nodal_coords)
    # np.savetxt("Ke_Vibra.dat", Ke, delimiter=",")
    # np.savetxt("Me_Vibra.dat", Me, delimiter=",")

    # Ke_ref = np.loadtxt(PROJECT_DIR / "validation\data\structural\shell_element\dkt_cst\Ke_ref.dat", delimiter=",")
    # Me_ref = np.loadtxt(PROJECT_DIR / "validation\data\structural\shell_element\dkt_cst\Me_ref.dat", delimiter=",")

    # diff_K = np.abs(Ke - Ke_ref)
    # diff_M = np.abs(Me - Me_ref)

    # print(f"Max. diff_K: {np.sum(diff_K)}")
    # print(f"Max. diff_M: {np.sum(diff_M)}")

    # np.savetxt("diff_K.dat", diff_K, delimiter=",")
    # np.savetxt("diff_M.dat", diff_M, delimiter=",")

    # K_bend_ref = np.loadtxt(PROJECT_DIR / "validation\data\structural\shell_element\dkt_cst\K_bend_ref.dat", delimiter=",")
    # M_bend_ref = np.loadtxt(PROJECT_DIR / "validation\data\structural\shell_element\dkt_cst\M_bend_ref.dat", delimiter=",")

    # K_memb_ref = np.loadtxt(PROJECT_DIR / "validation\data\structural\shell_element\dkt_cst\K_memb_ref.dat", delimiter=",")
    # M_memb_ref = np.loadtxt(PROJECT_DIR / "validation\data\structural\shell_element\dkt_cst\M_memb_ref.dat", delimiter=",")

    # K_bend_Vibra = np.loadtxt(PROJECT_DIR / "K_bend_Vibra.dat", delimiter=",")
    # M_bend_Vibra = np.loadtxt(PROJECT_DIR / "M_bend_Vibra.dat", delimiter=",")

    # K_memb_Vibra = np.loadtxt(PROJECT_DIR / "K_memb_Vibra.dat", delimiter=",")
    # M_memb_Vibra = np.loadtxt(PROJECT_DIR / "M_memb_Vibra.dat", delimiter=",")

    # diff_K_bend = np.abs(K_bend_ref - K_bend_Vibra)
    # diff_M_bend = np.abs(M_bend_ref - M_bend_Vibra)

    # diff_K_memb = np.abs(K_memb_ref - K_memb_Vibra)
    # diff_M_memb = np.abs(M_memb_ref - M_memb_Vibra)

    # print(np.max(diff_K_bend))
    # print(np.max(diff_M_bend))

    # print(np.max(diff_K_memb))
    # print(np.max(diff_M_memb))