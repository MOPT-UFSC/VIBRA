from typing import TYPE_CHECKING

import numpy as np

from vibra.engine.elements.elements_3d.hex20_element import Hexahedron20
from vibra.engine.elements.elements_3d.structural.structural_3d_element import Structural3DElement
from vibra.engine.properties.material import Material

if TYPE_CHECKING:
    from vibra.engine.model import Model


class StructHexahedron20(Structural3DElement, Hexahedron20):

    def __init__(self, model: "Model", dof_per_node: int = 3, nodes_per_element: int = 20):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "structural_hexahedron_20"

        self.define_integration_points_for_Ke()
        self.define_integration_points_for_Me()
        self.process_shape_functions_and_derivatives_for_Ke()
        self.process_shape_functions_and_derivatives_for_Me()
        self.process_N_matrix()


    def process_N_matrix(self):
        N = np.zeros((self.nint_M, 3, self.dof_per_element), dtype=float)

        for i in range(self.nint_M):
            N[i, 0, 0::3] = self.phi_M[i, :]
            N[i, 1, 1::3] = self.phi_M[i, :]
            N[i, 2, 2::3] = self.phi_M[i, :]

        self.N_matrix = N


    def define_integration_points_for_Ke(self, integration_points: int = 8):
        """
        This method defines the integration points and their
        weights for numerical integration.
        """
        self.nint_K = integration_points
        self.num_int_data_K = self.integration_points_data_for_hexahedrons(integration_points)
        self.wps_K = self.num_int_data_K[:, -1].reshape(-1, 1, 1)


    def define_integration_points_for_Me(self, integration_points: int = 14):
        """
        This method defines the integration points and their
        weights for numerical integration.
        """
        self.nint_M = integration_points
        self.num_int_data_M = self.integration_points_data_for_hexahedrons(integration_points)
        self.wps_M = self.num_int_data_M[:, -1].reshape(-1, 1, 1)

        print(self.nint_M)


    def process_shape_functions_and_derivatives_for_Ke(self):
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
        xi_1 = self.num_int_data_K[:, 0]
        xi_2 = self.num_int_data_K[:, 1]
        xi_3 = self.num_int_data_K[:, 2]

        self.phi_K, self.dphi_K = self.get_shape_functions_and_derivatives(xi_1, xi_2, xi_3)
        self.phi_K_trilinear = self.get_shape_functions_for_linear_stress_extrapolation(xi_1, xi_2, xi_3)
        self.phi_inv = self.inverse_of_trilinear_shape_functions()


    def inverse_of_trilinear_shape_functions(self):
        """
        This method returns the inverse of shape functions matrix N applied
        at integration points (Gauss-Legendre quadrature points).
        """
        N = self.phi_K_trilinear
        n_intp, n_nodes = N.shape

        if n_intp == n_nodes:
            # print("N_int = N_nodes")
            return np.linalg.inv(N)

        elif n_intp > n_nodes:
            # print("N_int > N_nodes")
            return np.linalg.inv(N.T @ N) @ N.T

        else:
            print("Not implemented stress extrapolation for N_int < N_nodes")
            return None


    def process_shape_functions_and_derivatives_for_Me(self):
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
        xi_1 = self.num_int_data_M[:, 0]
        xi_2 = self.num_int_data_M[:, 1]
        xi_3 = self.num_int_data_M[:, 2]

        self.phi_M, self.dphi_M = self.get_shape_functions_and_derivatives(xi_1, xi_2, xi_3)


    def get_shape_functions_for_linear_stress_extrapolation(
            self, 
            xi_1: np.ndarray | float, 
            xi_2: np.ndarray | float, 
            xi_3: np.ndarray | float,
            ):

        """
        This method returns the shape functions and its derivatives.
        
        Parameters
        ----------
        xi_1: np.ndarray
            The x coordinates of the integration points.
        
        xi_2: np.ndarray
            The y coordinates of the integration points.

        xi_3: np.ndarray
            The z coordinates of the integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        Nz = xi_1.size

        ##NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015

        # define the shape functions (Atalla and Sgard, 2015, pg. 171)
        phi = np.zeros((Nz, 8), dtype=float)

        phi[:, 0] = (1.0 - xi_1) * (1.0 - xi_2) * (1.0 - xi_3) / 8       # ->      (-1.0, -1.0, -1.0)   Node 1
        phi[:, 1] = (1.0 + xi_1) * (1.0 - xi_2) * (1.0 - xi_3) / 8       # ->      ( 1.0, -1.0, -1.0)   Node 2
        phi[:, 2] = (1.0 + xi_1) * (1.0 + xi_2) * (1.0 - xi_3) / 8       # ->      ( 1.0,  1.0, -1.0)   Node 3
        phi[:, 3] = (1.0 - xi_1) * (1.0 + xi_2) * (1.0 - xi_3) / 8       # ->      (-1.0,  1.0, -1.0)   Node 4
        phi[:, 4] = (1.0 - xi_1) * (1.0 - xi_2) * (1.0 + xi_3) / 8       # ->      (-1.0, -1.0,  1.0)   Node 5
        phi[:, 5] = (1.0 + xi_1) * (1.0 - xi_2) * (1.0 + xi_3) / 8       # ->      ( 1.0, -1.0,  1.0)   Node 6
        phi[:, 6] = (1.0 + xi_1) * (1.0 + xi_2) * (1.0 + xi_3) / 8       # ->      ( 1.0,  1.0,  1.0)   Node 7
        phi[:, 7] = (1.0 - xi_1) * (1.0 + xi_2) * (1.0 + xi_3) / 8       # ->      (-1.0,  1.0,  1.0)   Node 8

        return phi


    def process_detJAC_and_B_matrix(self, element_id: int, return_coords: bool=False):
        """
        This method computes and returns the matrix of shape functions 
        derivatives B and the determinant of the Jacobian matrix detJAC. 
        """

        # nodes from element
        elem_nodes = self.connectivities[element_id, :]

        # element nodal coords
        coords = self.model.mesh.nodal_coordinates[elem_nodes, 1:4]

        # Jacobian matrix
        JAC_K = self.dphi_K @ coords

        # Jacobian determinant and inverse
        detJAC_K, invJAC_K = self.get_detJAC_and_invJAC(JAC_K)

        # derivatives
        dphi_t = invJAC_K @ self.dphi_K

        # initialize the B matrix
        B = np.zeros((self.nint_K, 6, self.dof_per_element), dtype=float)

        B[:, 0, 0::3] = dphi_t[:, 0, :]
        B[:, 1, 1::3] = dphi_t[:, 1, :]
        B[:, 2, 2::3] = dphi_t[:, 2, :]
        B[:, 3, 0::3] = dphi_t[:, 1, :]
        B[:, 3, 1::3] = dphi_t[:, 0, :]
        B[:, 4, 0::3] = dphi_t[:, 2, :]
        B[:, 4, 2::3] = dphi_t[:, 0, :]
        B[:, 5, 1::3] = dphi_t[:, 2, :]
        B[:, 5, 2::3] = dphi_t[:, 1, :]

        if return_coords:
            return detJAC_K, B, coords

        return detJAC_K, B


    def elementary_matrices(self, element_id: int, material: Material):
        """
        This method integrates the elementary stiffness and mass matrices
        for the structural quadratic hexahedron element.

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
        const_mat, rho = self.get_constitutive_model(material, model_type="linear-isotropic")

        # process the determinant of Jacobian and the B matrix  
        detJAC_K, B, coords = self.process_detJAC_and_B_matrix(element_id, return_coords=True)

        # Jacobian matrix
        JAC_M = self.dphi_M @ coords

        # Jacobian determinant and inverse
        detJAC_M = self.get_detJAC(JAC_M)

        # matrix of shape functions N
        N = self.N_matrix

        # integration loop
        Ke, Me = 0, 0

        for i in range(self.nint_K):
            Ke += B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC_K[i, :, :] * self.wps_K[i])

        for i in range(self.nint_M):
            Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC_M[i, :, :] * self.wps_M[i])

        return Ke, Me

 
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

        # get data to compute the stress
        _, B = self.process_detJAC_and_B_matrix(element_id)

        # initialize the element stresses matrix
        element_stresses = np.zeros((6, self.nint_K, Ue.shape[1]), dtype=complex)

        # calculate the nodal stress tensor
        for i in range(self.nint_K):
            element_stresses[:, i, :] = D @ (B[i, :, :] @ Ue)

        if element_averaged:
            return np.average(element_stresses, axis=1)

        return element_stresses