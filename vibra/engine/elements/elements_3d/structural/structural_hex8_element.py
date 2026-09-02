from typing import TYPE_CHECKING

import numpy as np

from vibra.engine.elements.common.element_options import BbarDilatationalEvaluation, HEX8_structural
from vibra.engine.elements.common.matrix_tools import get_3x3_matrix_determinant, get_3x3_matrix_inverse
from vibra.engine.elements.elements_3d.hex8_element import Hexahedron8
from vibra.engine.elements.elements_3d.structural.flanagan_belytschko_formulation import (
    compute_hourglass_stiffness,
    get_B_analytic,
)
from vibra.engine.elements.elements_3d.structural.structural_3d_element import Structural3DElement
from vibra.engine.properties.material import Material

if TYPE_CHECKING:
    from vibra.engine.model import Model


class StructuralHexahedron4(Structural3DElement, Hexahedron8):

    def __init__(self, model: "Model", dof_per_node: int = 3, nodes_per_element: int = 8):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "structural_hexahedron_8"

        self.load_element_options()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()

        self.initialize()
        self.process_N_matrix()


    def initialize(self):
        self.aux_ones = np.ones(self.dof_per_element, dtype=float)
        dil_projector = np.array([1, 1, 1, 0, 0, 0], dtype=float).reshape(-1, 1)
        self.m_mt = dil_projector @ dil_projector.T


    def process_N_matrix(self):
        N = np.zeros((self.nint, 3, self.dof_per_element), dtype=float)

        for i in range(self.nint):
            N[i, 0, 0::3] = self.phi[i, :]
            N[i, 1, 1::3] = self.phi[i, :]
            N[i, 2, 2::3] = self.phi[i, :]

        self.N_matrix = N


    def load_element_options(self):
        """
        This method updates the extra shape functions state based on the model global properties.
        """

        self.element_options = HEX8_structural()
        self.static_condensation_required = False

        advanced_element_options = self.model.properties._get_property("advanced_element_options")
        if not isinstance(advanced_element_options, dict):
            return

        element_options = advanced_element_options.get("hex8")
        if isinstance(element_options, HEX8_structural):
            self.element_options = element_options

        self.static_condensation_required = element_options.extra_shape_functions or element_options.enhanced_assumed_strain


    def process_shape_functions_and_derivatives(self):
        """
        This method returns the shape functions and its derivatives
        for all integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        ## coordinates from integration points
        xi_1 = self.num_int_data[:, 0]
        xi_2 = self.num_int_data[:, 1]
        xi_3 = self.num_int_data[:, 2]

        self.phi, self.dphi = self.get_shape_functions_and_derivatives(xi_1, xi_2, xi_3)
        self.dphi_esf = self.get_shape_functions_derivatives_for_extra_shape_functions(xi_1, xi_2, xi_3)
        _, self.dphi_0 = self.get_shape_functions_and_derivatives(0, 0, 0)

        self.phi_inv = self.inverse_of_shape_functions()


    def inverse_of_shape_functions(self):
        """
        This method returns the inverse of shape functions matrix N applied
        at integration points (Gauss-Legendre quadrature points).
        """
        N = self.phi[:, :self.nodes_per_element]
        n_intp, n_nodes = N.shape

        if n_intp == n_nodes:
            return np.linalg.inv(N)

        elif n_intp > n_nodes:
            return np.linalg.inv(N.T @ N) @ N.T

        else:
            return None


    def get_shape_functions_derivatives_for_extra_shape_functions(
            self, 
            xi_1: np.ndarray | float, 
            xi_2: np.ndarray | float, 
            xi_3: np.ndarray | float,
            ):

        if isinstance(xi_1, np.ndarray):
            Nz = xi_1.size
        else:
            Nz = 1

        # NOTE: the extra shape functions
        # phi = np.zeros((Nz, 3), dtype=float)
        # phi_esf[:, 0] = (1.0 - xi_1**2)
        # phi_esf[:, 1] = (1.0 - xi_2**2)
        # phi_esf[:, 2] = (1.0 - xi_3**2)

        dphi_esf = np.zeros((Nz, 3, 3), dtype=float)
        dphi_esf[:, 0, 0] = -(2 * xi_1)
        dphi_esf[:, 1, 1] = -(2 * xi_2)
        dphi_esf[:, 2, 2] = -(2 * xi_3)

        return dphi_esf


    @property
    def extra_dofs(self):
        if self.element_options.extra_shape_functions:
            return int(3 * self.dof_per_node)

        elif self.element_options.enhanced_assumed_strain:
            return self.element_options.EAS_internal_dofs

        return 0


    def get_inverse_T0_matrix(self, J0: np.ndarray) -> np.ndarray:
        """
        This method returns the inverse transpose of the transformation matrix 
        T0 used to compute the shape functions derivative matrix B for 
        the enhanced assumed strain element formulation.

        Parameter
        ---------
        J0: np.ndarray
            The Jacobian evaluated at the element centre.

        """

        T0 = np.array(
            [
            [      J0[0, 0]**2,       J0[1, 0]**2,       J0[2, 0]**2,                     2*J0[0, 0]*J0[1, 0],                     2*J0[0, 0]*J0[2, 0],                     2*J0[1, 0]*J0[2, 0]],
            [      J0[0, 1]**2,       J0[1, 1]**2,       J0[2, 1]**2,                     2*J0[0, 1]*J0[1, 1],                     2*J0[0, 1]*J0[2, 1],                     2*J0[1, 1]*J0[2, 1]],
            [      J0[0, 2]**2,       J0[1, 2]**2,       J0[2, 2]**2,                     2*J0[0, 2]*J0[1, 2],                     2*J0[0, 2]*J0[2, 2],                     2*J0[1, 2]*J0[2, 2]],
            [J0[0, 0]*J0[0, 1], J0[1, 0]*J0[1, 1], J0[2, 0]*J0[2, 1], (J0[0, 0]*J0[1, 1] + J0[1, 0]*J0[0, 1]), (J0[0, 0]*J0[2, 1] + J0[2, 0]*J0[0, 1]), (J0[1, 0]*J0[2, 1] + J0[2, 0]*J0[1, 1])],
            [J0[0, 0]*J0[0, 2], J0[1, 0]*J0[1, 2], J0[2, 0]*J0[2, 2], (J0[0, 0]*J0[1, 2] + J0[1, 0]*J0[0, 2]), (J0[0, 0]*J0[2, 2] + J0[2, 0]*J0[0, 2]), (J0[1, 0]*J0[2, 2] + J0[2, 0]*J0[1, 2])],
            [J0[0, 1]*J0[0, 2], J0[1, 1]*J0[1, 2], J0[2, 1]*J0[2, 2], (J0[0, 1]*J0[1, 2] + J0[1, 1]*J0[0, 2]), (J0[0, 1]*J0[2, 2] + J0[2, 1]*J0[0, 2]), (J0[1, 1]*J0[2, 2] + J0[2, 1]*J0[1, 2])],
            ], dtype=float)
        
        return np.linalg.inv(T0)


    def get_interpolation_matrix_Mxi(self):
        """
        This method returns the interpolation matrix for the additional strain
        fields proposed by Andelfinger and Ramm.

        Reference: U. Andelfinger and E Ramm. EAS-Elements for Two-Dimensional, Three-Dimensional, 
        Plate and Shell Structures and Their Equivalence to HR-Elements. International Journal 
        for Numerical Methods in Engineering. Vol. 36. 1311–1337. 1993.

        """

        xi = self.num_int_data[:, 0]
        eta = self.num_int_data[:, 1]
        zeta = self.num_int_data[:, 2]

        M_xi = np.zeros((self.nint, 6, 30), dtype=float)

        # Alternative M_xi matrix

        M_xi[:, 0, 0] = xi
        M_xi[:, 1, 1] = eta
        M_xi[:, 2, 2] = zeta

        M_xi[:, 3, 3] = xi
        M_xi[:, 3, 4] = eta
        M_xi[:, 4, 5] = xi
        M_xi[:, 4, 6] = zeta
        M_xi[:, 5, 7] = eta
        M_xi[:, 5, 8] = zeta

        M_xi[:, 0, 9 ] = M_xi[:, 1, 9 ] = M_xi[:, 2, 9 ] = xi * eta
        M_xi[:, 0, 10] = M_xi[:, 1, 10] = M_xi[:, 2, 10] = eta * zeta
        M_xi[:, 0, 11] = M_xi[:, 1, 11] = M_xi[:, 2, 11] = xi * zeta

        M_xi[:, 0, 12] = xi * eta * zeta
        M_xi[:, 1, 12] = xi * eta * zeta
        M_xi[:, 2, 12] = xi * eta * zeta

        #NOTE: Matrix proposed by Andelfinger and Ramm

        # # Block 25~28
        # M_xi[:, 0, 0] = xi
        # M_xi[:, 1, 1] = eta
        # M_xi[:, 2, 2] = zeta

        # # Block 29~33
        # M_xi[:, 3, 3] = xi
        # M_xi[:, 3, 4] = eta
        # M_xi[:, 4, 5] = xi
        # M_xi[:, 4, 6] = zeta
        # M_xi[:, 5, 7] = eta
        # M_xi[:, 5, 8] = zeta

        # # Block 34~39
        # M_xi[:, 3, 9 ] = xi * zeta
        # M_xi[:, 3, 10] = eta * zeta
        # M_xi[:, 4, 11] = xi * eta
        # M_xi[:, 4, 12] = eta * zeta
        # M_xi[:, 5, 13] = xi * eta
        # M_xi[:, 5, 14] = xi * zeta

        # # Block 40~45
        # M_xi[:, 0, 15] = xi * eta
        # M_xi[:, 0, 16] = xi * zeta
        # M_xi[:, 1, 17] = xi * eta
        # M_xi[:, 1, 18] = eta * zeta
        # M_xi[:, 2, 19] = xi * zeta
        # M_xi[:, 2, 20] = eta * zeta

        # # Block 46~48
        # M_xi[:, 3, 21] = xi * eta
        # M_xi[:, 4, 22] = xi * zeta
        # M_xi[:, 5, 23] = eta * zeta

        # # Block 49~51
        # M_xi[:, 0, 24] = xi * eta * zeta
        # M_xi[:, 1, 25] = xi * eta * zeta
        # M_xi[:, 2, 26] = xi * eta * zeta

        # # Block 52~54
        # M_xi[:, 3, 27] = xi * eta * zeta
        # M_xi[:, 4, 28] = xi * eta * zeta
        # M_xi[:, 5, 29] = xi * eta * zeta

        last_col = self.element_options.EAS_internal_dofs

        return M_xi[:, :, :last_col]


    def process_detJAC_and_B_matrix(self, element_id: int):
        """
        This method computes and returns the matrix of shape functions 
        derivatives B and the determinant of the Jacobian matrix detJAC. 
        """

        # nodes from element
        elem_nodes = self.connectivities[element_id, :]

        # element nodal coords
        coords = self.model.mesh.nodal_coordinates[elem_nodes, 1:4]

        # Jacobian matrix
        jac = self.dphi @ coords

        # Jacobian determinant and inverse
        inv_jac, det_jac = get_3x3_matrix_inverse(jac)

        # derivatives
        dphi_t = inv_jac @ self.dphi

        # for validation purposes
        self.B_grad = np.sum(dphi_t * det_jac * self.wps, axis=0) / np.sum(det_jac * self.wps, axis=0)

        # initialize the B matrix
        edof = self.dof_per_element
        B = np.zeros((self.nint, 6, edof + self.extra_dofs), dtype=float)

        # fill the B matrix
        B[:, 0, 0:edof:3] = dphi_t[:, 0, :]
        B[:, 1, 1:edof:3] = dphi_t[:, 1, :]
        B[:, 2, 2:edof:3] = dphi_t[:, 2, :]
        B[:, 3, 0:edof:3] = dphi_t[:, 1, :]
        B[:, 3, 1:edof:3] = dphi_t[:, 0, :]
        B[:, 4, 0:edof:3] = dphi_t[:, 2, :]
        B[:, 4, 2:edof:3] = dphi_t[:, 0, :]
        B[:, 5, 1:edof:3] = dphi_t[:, 2, :]
        B[:, 5, 2:edof:3] = dphi_t[:, 1, :]

        if self.element_options.Bbar_formulation:

            # compute B using the generalized mean-dilatation formulation
            if self.element_options.Bbar_dilatational_evaluation == BbarDilatationalEvaluation.VOLUME_AVERAGED:

                # integrate the element volume
                elem_vol = np.sum(det_jac * self.wps, axis=0)
                
                # compute the volume-averaged B matrix
                B0 = np.sum((B * det_jac * self.wps), axis=0) / elem_vol

            # compute B at centroid (0, 0, 0)
            else:

                # Jacobian matrix at the centroid (0, 0, 0)
                jac_0 = self.dphi_0 @ coords

                # Jacobian determinant and inverse at the centroid
                inv_jac_0, det_jac_0 = get_3x3_matrix_inverse(jac_0)

                # derivatives in global coordinates variables
                dphi_t0 = inv_jac_0 @ self.dphi_0
        
                # initialize the B0 matrix that corresponds to the B matrix evaluated at the element centre
                B0 = np.zeros((6, edof), dtype=float)

                # fill the B0 matrix
                B0[0, 0:edof:3] = dphi_t0[0, :]
                B0[1, 1:edof:3] = dphi_t0[1, :]
                B0[2, 2:edof:3] = dphi_t0[2, :]
                B0[3, 0:edof:3] = dphi_t0[1, :]
                B0[3, 1:edof:3] = dphi_t0[0, :]
                B0[4, 0:edof:3] = dphi_t0[2, :]
                B0[4, 2:edof:3] = dphi_t0[0, :]
                B0[5, 1:edof:3] = dphi_t0[2, :]
                B0[5, 2:edof:3] = dphi_t0[1, :]

            # dilatational part of B at centroid: Bbar_dil = (1/3) m @ m^T B0
            B_bar_dil = (1/3) * self.m_mt @ B0

            # B_dil = (1/3) * m * m^T * B  extracts the volumetric part of B
            B_dil = (1/3) * self.m_mt @ B

            # B_dev is the deviatoric part of B (B-bar formulation replaces the dilatational part of B by its volume-averaged value)
            B_dev = B - B_dil

            # B-bar: replace dilatational part of B by centroid dilatational part
            B_bar = B_dev + B_bar_dil

            return det_jac, B_bar

        elif self.element_options.extra_shape_functions:

            #TODO: add reference
            # Zienkiewicz, O. C., Taylor, R. L. The Finite Element Method: Its Basis and Fundamentals. Seventh Edition. pg 271-275

            # Jacobian matrix at the centroid (0, 0, 0)
            jac_0 = self.dphi_0 @ coords

            # Jacobian determinant and inverse at the centroid
            inv_jac_0, det_jac0 = get_3x3_matrix_inverse(jac_0)
        
            # adjusted derivatives in global coordinates variables (satisfy the stress patch test)
            dphi_esf_t = (det_jac0 / det_jac) * inv_jac_0 @ self.dphi_esf

            # fill the B matrix with ESF-related derivatives
            B[:, 0, edof + 0::3] = dphi_esf_t[:, 0, :]
            B[:, 1, edof + 1::3] = dphi_esf_t[:, 1, :]
            B[:, 2, edof + 2::3] = dphi_esf_t[:, 2, :]
            B[:, 3, edof + 0::3] = dphi_esf_t[:, 1, :]
            B[:, 3, edof + 1::3] = dphi_esf_t[:, 0, :]
            B[:, 4, edof + 0::3] = dphi_esf_t[:, 2, :]
            B[:, 4, edof + 2::3] = dphi_esf_t[:, 0, :]
            B[:, 5, edof + 1::3] = dphi_esf_t[:, 2, :]
            B[:, 5, edof + 2::3] = dphi_esf_t[:, 1, :]

        elif self.element_options.enhanced_assumed_strain:

            # # Jacobian matrix at the centroid (0, 0, 0)
            jac_0 = self.dphi_0 @ coords

            # # integrate the element volume
            # e_vol = np.sum(det_jac * self.wps, axis=0)

            # Jacobian determinant and inverse at the centroid
            det_jac_0 = get_3x3_matrix_determinant(jac_0)

            # compute the inverse transpose T0 matrix
            inv_T0 = self.get_inverse_T0_matrix(jac_0)

            # compute the interpolation matrix M_xi
            M_xi = self.get_interpolation_matrix_Mxi()

            # extend the matrix of shape function derivatives B
            B[:, :, edof:] = (det_jac_0 / det_jac) * inv_T0.T @ M_xi

            # # evaluate the patch test
            # integral_patch_test = 0.
            # for i in range(self.nint):
            #     integral_patch_test += (detjac_0 / detjac[i, :, :]) * (inv_T0.T @ M_xi[i, :, :]) * (detjac[i, :, :] * self.wps[i])

            # if np.linalg.norm(integral_patch_test) > 1e-15:
            #     print(f"Patch test not satisfied for the element #{element_id}")

        return det_jac, B


    def get_B_matrix(self, dphi_t: np.ndarray):
        """ Assemble B matrix (6x24) from dphi_t (3x8).
        """
        if len(dphi_t.shape) == 2:
            B = np.zeros((6, self.dof_per_element), dtype=float)
            # fill the B matrix
            B[0, 0::3] = dphi_t[0, :]
            B[1, 1::3] = dphi_t[1, :]
            B[2, 2::3] = dphi_t[2, :]
            B[3, 0::3] = dphi_t[1, :]
            B[3, 1::3] = dphi_t[0, :]
            B[4, 0::3] = dphi_t[2, :]
            B[4, 2::3] = dphi_t[0, :]
            B[5, 1::3] = dphi_t[2, :]
            B[5, 2::3] = dphi_t[1, :]

        else:
            B = np.zeros((dphi_t.shape[0], 6, self.dof_per_element), dtype=float)

            # fill the B matrix
            B[:, 0, 0::3] = dphi_t[:, 0, :]
            B[:, 1, 1::3] = dphi_t[:, 1, :]
            B[:, 2, 2::3] = dphi_t[:, 2, :]
            B[:, 3, 0::3] = dphi_t[:, 1, :]
            B[:, 3, 1::3] = dphi_t[:, 0, :]
            B[:, 4, 0::3] = dphi_t[:, 2, :]
            B[:, 4, 2::3] = dphi_t[:, 0, :]
            B[:, 5, 1::3] = dphi_t[:, 2, :]
            B[:, 5, 2::3] = dphi_t[:, 1, :]

        return B


    def elementary_matrices(self, element_id: int, material: Material):
        """
        This method integrates the elementary stiffness and mass matrices
        for the structural linear hexahedron element.

        Parameters
        ----------
        element_id: int
            The element index.  
        
        material: Material
            An object of the material dataclass.

        Returns
        -------
        Ke: np.ndarray
            The elementary stiffness matrix.

        Me: np.ndarray
            The elementary mass matrix.

        """
        # get constitutive law matrix D and the material's density
        D, rho = self.get_constitutive_model(material, model_type="linear-isotropic")

        # process the determinant of Jacobian and the B matrix
        detJAC, B = self.process_detJAC_and_B_matrix(element_id)

        if self.element_options.reduced_integration:

            # the reduced element integration implies one integration 
            # point for the stiffness matrix and adopts the lumped mass matrix 

            # integrate the volume of the element
            e_vol = np.sum(detJAC * self.wps, axis=0)

            # calculate the nodal mass (total mass divided by element nodes)
            nodal_mass = (rho * e_vol[0]) / self.nodes_per_element

            # compute the lumped mass matrix
            Me = np.diag(self.aux_ones * nodal_mass)

            # nodes from element
            elem_nodes = self.connectivities[element_id, :]

            # element nodal coords
            coords = self.model.mesh.nodal_coordinates[elem_nodes, 1:4]

            # obtain the analytical B_mean and volume
            B_mean, V = get_B_analytic(coords)

            # equivalent to dphi_t
            dphi_t_an = B_mean / V                 

            # create the averaged B matrix
            B0 = self.get_B_matrix(dphi_t_an)
            
            # uniform strain stiffness
            K_unif = B0.T @ D @ B0 * V             

            #TODO: the hourglass stiffness compensation model must be improved

            # hourglass stabilization matrix K_hg
            K_hg = compute_hourglass_stiffness(K_unif, coords, dphi_t_an, material, e_vol[0])
            # K_hg = calcular_k_stab_corrigido(coords, material.elasticity_modulus, material.poisson_ratio, 0.1)
            # K_hg = matricesH8S_FB(element_id, self.model.mesh.nodal_coordinates, self.connectivities, material.elasticity_modulus, material.poisson_ratio, material.material_density, 0, kappa=0.125)

            ## PATCH TEST FOR ORTHOGONAL STABILIZATION ()
            
            # constant rotation about z-axis
            theta_z = 0.01
            u_rot = np.zeros(self.dof_per_element, dtype=float)
            
            u_rot[0::3] = -theta_z * coords[:, 1]
            u_rot[1::3] =  theta_z * coords[:, 0]
            u_rot[2::3] = 0

            fr_int = K_hg @ u_rot
            fr_residual = np.linalg.norm(fr_int)

            if fr_residual > 1e-6:
                print(f"Patch test failed for constat rotation at the element {element_id} - Residue: {fr_residual : '%.12e'}")

            # constant deformation epsilon_x
            e_def = 0.01
            u_def = np.zeros(self.dof_per_element, dtype=float)

            u_def[0::3] = e_def * coords[:, 0]
            u_def[1::3] = 0
            u_def[2::3] = 0

            fd_int = K_hg @ u_def
            fd_residual = np.linalg.norm(fd_int)

            if fd_residual > 1e-6:
                print(f"Patch test failed for constat deformation x at the element {element_id} - Residue: {fd_residual : '%.12e'}")

            if element_id == 0:
                print(K_hg[:4, :4])

            # add the correction matrix K_hg to penalizes the hourglasses modes
            # resultant from reduced integration
            Ke = K_unif + K_hg*1

        else:

            # initialize the matrix of shape functions N
            N = self.N_matrix

            # integration loop
            Ke, Me = 0., 0.
            for i in range(self.nint):
                Ke += B[i, :, :].T @ D @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])
                Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i])

            # static condensation of the elementary stiffness matrix Ke
            if self.static_condensation_required:
                Kuu = Ke[0 : self.dof_per_element, 0 : self.dof_per_element]
                Kua = Ke[0 : self.dof_per_element, self.dof_per_element :]
                Kau = Kua.T
                Kbb = Ke[self.dof_per_element :, self.dof_per_element :]

                Ke = Kuu - Kua @ np.linalg.inv(Kbb) @ Kau

        # # nodes from element
        # elem_nodes = self.connectivities[element_id, :]

        # # element nodal coords
        # coords = self.model.mesh.nodal_coordinates[elem_nodes, 1:4]


        # if element_id < 2:

        #     mask_Ke = Ke != 0
        #     mask_Me = Me != 0

        #     dif_Ke = 100 * np.max(np.abs(Ke[mask_Ke] - Ke_2[mask_Ke]) / (Ke[mask_Ke] + Ke_2[mask_Ke]))
        #     dif_Me = 100 * np.max(np.abs(Me[mask_Me] - Me_2[mask_Me]) / (Me[mask_Me] + Me_2[mask_Me]))

        #     print()
        #     print(f"Maximum difference for Ke (#{element_id}): {dif_Ke} [%]")
        #     print(f"Maximum difference for Me (#{element_id}): {dif_Me} [%]")

        # Ke = 0.5 * (Ke + Ke.T)
        # Me = 0.5 * (Me + Me.T)

        return Ke, Me


    def get_data_to_compute_stresses(self, element_id: int, nodal_solution: np.ndarray, D: np.ndarray):

        # nodal solution
        Ue = nodal_solution

        # process the determinant of Jacobian and the B matrix
        detJAC, B = self.process_detJAC_and_B_matrix(element_id)

        if self.static_condensation_required:

            # initialize the stiffness matrix Ke
            Ke = 0.

            # integrate the stiffness matrix
            for i in range(self.nint):
                Ke += B[i, :, :].T @ D @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])

            Kau = Ke[self.dof_per_element :, 0 : self.dof_per_element]
            Kaa = Ke[self.dof_per_element :, self.dof_per_element :]

            # extra dofs results
            alpha = -np.linalg.inv(Kaa) @ (Kau @ Ue)

            # extend element solution with extra dofs results
            Ue = np.append(Ue, alpha, axis=0)

        return B, Ue

 
    def process_stresses_at_integration_points(
        self,
        element_id : int,
        nodal_solution : np.ndarray | None = None,
        solution: np.ndarray | None = None,
        element_averaged: bool = False,
        **kwargs
        ):

        node_ids = kwargs.get("node_ids")

        if node_ids is None:
            node_ids = self.connectivities[element_id, :]

        if isinstance(nodal_solution, np.ndarray):
            Ue = nodal_solution

        elif isinstance(solution, np.ndarray):
            indices = node_ids.reshape(-1, 1) * self.dof_per_node + self.local_dof
            Ue = solution[indices.flatten(), :]    

        else:
            return 0.

        if self.connectivities is None:
            self.reorder_connect()

        # get the volume ID from element
        vol_id = self.model.mesh.solids_connectivity[element_id, 1]

        # get the material from element
        material = self.model.properties._get_property("material", volume=vol_id)
        if not isinstance(material, Material):
            return 0.

        D, _ = self.get_constitutive_model(material, model_type="linear-isotropic")

        # get data to compute the stress (with or without ESF)
        B, Ue = self.get_data_to_compute_stresses(element_id, Ue, D)

        # initialize the element stresses matrix
        element_stresses = np.zeros((6, self.nint, Ue.shape[1]), dtype=complex)

        # calculate the nodal stress tensor
        for i in range(self.nint):
            element_stresses[:, i, :] = D @ (B[i, :, :] @ Ue)

        if element_averaged:
            return np.average(element_stresses, axis=1)

        return element_stresses