import numpy as np

from vibra.engine.elements.solid_elements import Element3D
from vibra.engine.properties.material import Material

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model


class STRUCT_HEXAHEDRON_20(Element3D):

    NODES_PER_ELEMENT = 20
    DOF_PER_NODE = 3
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivity = None
        self.element_label = "structural_hexahedron_20"

        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.solids_connectivity = self.model.mesh.solids_connectivity

        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.solids_connectivity)

        self.define_integration_points_for_Ke()
        self.define_integration_points_for_Me()
        self.process_shape_functions_and_derivatives_for_Ke()
        self.process_shape_functions_and_derivatives_for_Me()


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


    def get_shape_functions_and_derivatives(self, xi_1: np.ndarray|float, xi_2: np.ndarray|float, xi_3: np.ndarray|float):

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

        if isinstance(xi_1, np.ndarray):
            Nz = xi_1.size
        else:
            Nz = 1

        ##NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015

        # define the shape functions (Atalla and Sgard, 2015, pg. 171)
        phi = np.zeros((Nz, self.NODES_PER_ELEMENT), dtype=float)

        phi[:, 0] = (1 - xi_1) * (1 - xi_2) * (1 - xi_3) * (-xi_1 - xi_2 - xi_3 - 2) / 8      # ->      (-1.0, -1.0, -1.0)   Node 1
        phi[:, 1] = (1 + xi_1) * (1 - xi_2) * (1 - xi_3) * ( xi_1 - xi_2 - xi_3 - 2) / 8      # ->      ( 1.0, -1.0, -1.0)   Node 2
        phi[:, 2] = (1 + xi_1) * (1 + xi_2) * (1 - xi_3) * ( xi_1 + xi_2 - xi_3 - 2) / 8      # ->      ( 1.0,  1.0, -1.0)   Node 3
        phi[:, 3] = (1 - xi_1) * (1 + xi_2) * (1 - xi_3) * (-xi_1 + xi_2 - xi_3 - 2) / 8      # ->      (-1.0,  1.0, -1.0)   Node 4
        phi[:, 4] = (1 - xi_1) * (1 - xi_2) * (1 + xi_3) * (-xi_1 - xi_2 + xi_3 - 2) / 8      # ->      (-1.0, -1.0,  1.0)   Node 5
        phi[:, 5] = (1 + xi_1) * (1 - xi_2) * (1 + xi_3) * ( xi_1 - xi_2 + xi_3 - 2) / 8      # ->      ( 1.0, -1.0,  1.0)   Node 6
        phi[:, 6] = (1 + xi_1) * (1 + xi_2) * (1 + xi_3) * ( xi_1 + xi_2 + xi_3 - 2) / 8      # ->      ( 1.0,  1.0,  1.0)   Node 7
        phi[:, 7] = (1 - xi_1) * (1 + xi_2) * (1 + xi_3) * (-xi_1 + xi_2 + xi_3 - 2) / 8      # ->      (-1.0,  1.0,  1.0)   Node 8

        phi[:, 8 ] = (1 - xi_1**2) * (1 - xi_2) * (1 - xi_3) / 4                              # ->      ( 0.0, -1.0, -1.0)   Node 9
        phi[:, 9 ] = (1 + xi_1) * (1 - xi_2**2) * (1 - xi_3) / 4                              # ->      ( 1.0,  0.0, -1.0)   Node 10
        phi[:, 10] = (1 - xi_1**2) * (1 + xi_2) * (1 - xi_3) / 4                              # ->      ( 0.0,  1.0, -1.0)   Node 11
        phi[:, 11] = (1 - xi_1) * (1 - xi_2**2) * (1 - xi_3) / 4                              # ->      (-1.0,  0.0, -1.0)   Node 12
        phi[:, 12] = (1 - xi_1**2) * (1 - xi_2) * (1 + xi_3) / 4                              # ->      ( 0.0, -1.0,  1.0)   Node 17
        phi[:, 13] = (1 + xi_1) * (1 - xi_2**2) * (1 + xi_3) / 4                              # ->      ( 1.0,  0.0,  1.0)   Node 18
        phi[:, 14] = (1 - xi_1**2) * (1 + xi_2) * (1 + xi_3) / 4                              # ->      ( 0.0,  1.0,  1.0)   Node 19
        phi[:, 15] = (1 - xi_1) * (1 - xi_2**2) * (1 + xi_3) / 4                              # ->      (-1.0,  0.0,  1.0)   Node 20
        phi[:, 16] = (1 - xi_1) * (1 - xi_2) * (1 - xi_3**2) / 4                              # ->      (-1.0, -1.0,  0.0)   Node 13
        phi[:, 17] = (1 + xi_1) * (1 - xi_2) * (1 - xi_3**2) / 4                              # ->      ( 1.0, -1.0,  0.0)   Node 14
        phi[:, 18] = (1 + xi_1) * (1 + xi_2) * (1 - xi_3**2) / 4                              # ->      ( 1.0,  1.0,  0.0)   Node 15
        phi[:, 19] = (1 - xi_1) * (1 + xi_2) * (1 - xi_3**2) / 4                              # ->      (-1.0,  1.0,  0.0)   Node 16

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((Nz, 3, self.NODES_PER_ELEMENT), dtype=float)

        dphi[:, 0, 0 ] =  (1 - xi_2) * (1 - xi_3) * (2*xi_1 + xi_2 + xi_3 + 1) / 8
        dphi[:, 0, 1 ] =  (1 - xi_2) * (1 - xi_3) * (2*xi_1 - xi_2 - xi_3 - 1) / 8
        dphi[:, 0, 2 ] =  (1 + xi_2) * (1 - xi_3) * (2*xi_1 + xi_2 - xi_3 - 1) / 8
        dphi[:, 0, 3 ] =  (1 + xi_2) * (1 - xi_3) * (2*xi_1 - xi_2 + xi_3 + 1) / 8
        dphi[:, 0, 4 ] =  (1 - xi_2) * (1 + xi_3) * (2*xi_1 + xi_2 - xi_3 + 1) / 8
        dphi[:, 0, 5 ] =  (1 - xi_2) * (1 + xi_3) * (2*xi_1 - xi_2 + xi_3 - 1) / 8
        dphi[:, 0, 6 ] =  (1 + xi_2) * (1 + xi_3) * (2*xi_1 + xi_2 + xi_3 - 1) / 8
        dphi[:, 0, 7 ] =  (1 + xi_2) * (1 + xi_3) * (2*xi_1 - xi_2 - xi_3 + 1) / 8
        dphi[:, 0, 8 ] = (-2*xi_1) * (1 - xi_2) * (1 - xi_3) / 4
        dphi[:, 0, 9 ] = (1) * (1 - xi_2**2) * (1 - xi_3) / 4
        dphi[:, 0, 10] = (-2*xi_1) * (1 + xi_2) * (1 - xi_3) / 4
        dphi[:, 0, 11] = (-1) * (1 - xi_2**2) * (1 - xi_3) / 4
        dphi[:, 0, 12] = (-2*xi_1) * (1 - xi_2) * (1 + xi_3) / 4
        dphi[:, 0, 13] = (1) * (1 - xi_2**2) * (1 + xi_3) / 4
        dphi[:, 0, 14] = (-2*xi_1) * (1 + xi_2) * (1 + xi_3) / 4
        dphi[:, 0, 15] = (-1) * (1 - xi_2**2) * (1 + xi_3) / 4
        dphi[:, 0, 16] = (-1) * (1 - xi_2) * (1 - xi_3**2) / 4
        dphi[:, 0, 17] = (1) * (1 - xi_2) * (1 - xi_3**2) / 4
        dphi[:, 0, 18] = (1) * (1 + xi_2) * (1 - xi_3**2) / 4
        dphi[:, 0, 19] = (-1) * (1 + xi_2) * (1 - xi_3**2) / 4


        dphi[:, 1, 0 ] = (1 - xi_1) * (1 - xi_3) * ( xi_1 + 2*xi_2 + xi_3 + 1) / 8
        dphi[:, 1, 1 ] = (1 + xi_1) * (1 - xi_3) * (-xi_1 + 2*xi_2 + xi_3 + 1) / 8
        dphi[:, 1, 2 ] = (1 + xi_1) * (1 - xi_3) * ( xi_1 + 2*xi_2 - xi_3 - 1) / 8
        dphi[:, 1, 3 ] = (1 - xi_1) * (1 - xi_3) * (-xi_1 + 2*xi_2 - xi_3 - 1) / 8 
        dphi[:, 1, 4 ] = (1 - xi_1) * (1 + xi_3) * ( xi_1 + 2*xi_2 - xi_3 + 1) / 8
        dphi[:, 1, 5 ] = (1 + xi_1) * (1 + xi_3) * (-xi_1 + 2*xi_2 - xi_3 + 1) / 8
        dphi[:, 1, 6 ] = (1 + xi_1) * (1 + xi_3) * ( xi_1 + 2*xi_2 + xi_3 - 1) / 8
        dphi[:, 1, 7 ] = (1 - xi_1) * (1 + xi_3) * (-xi_1 + 2*xi_2 + xi_3 - 1) / 8
        dphi[:, 1, 8 ] = (1 - xi_1**2) * (-1) * (1 - xi_3) / 4
        dphi[:, 1, 9 ] = (1 + xi_1) * (-2*xi_2) * (1 - xi_3) / 4
        dphi[:, 1, 10] = (1 - xi_1**2) * (1) * (1 - xi_3) / 4
        dphi[:, 1, 11] = (1 - xi_1) * (-2*xi_2) * (1 - xi_3) / 4
        dphi[:, 1, 12] = (1 - xi_1**2) * (-1) * (1 + xi_3) / 4
        dphi[:, 1, 13] = (1 + xi_1) * (-2*xi_2) * (1 + xi_3) / 4
        dphi[:, 1, 14] = (1 - xi_1**2) * (1) * (1 + xi_3) / 4
        dphi[:, 1, 15] = (1 - xi_1) * (-2*xi_2) * (1 + xi_3) / 4
        dphi[:, 1, 16] = (1 - xi_1) * (-1) * (1 - xi_3**2) / 4
        dphi[:, 1, 17] = (1 + xi_1) * (-1) * (1 - xi_3**2) / 4
        dphi[:, 1, 18] = (1 + xi_1) * (1) * (1 - xi_3**2) / 4
        dphi[:, 1, 19] = (1 - xi_1) * (1) * (1 - xi_3**2) / 4

        dphi[:, 2, 0 ] = (1 - xi_1) * (1 - xi_2) * ( xi_1 + xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 1 ] = (1 + xi_1) * (1 - xi_2) * (-xi_1 + xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 2 ] = (1 + xi_1) * (1 + xi_2) * (-xi_1 - xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 3 ] = (1 - xi_1) * (1 + xi_2) * ( xi_1 - xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 4 ] = (1 - xi_1) * (1 - xi_2) * (-xi_1 - xi_2 + 2*xi_3 - 1) / 8
        dphi[:, 2, 5 ] = (1 + xi_1) * (1 - xi_2) * ( xi_1 - xi_2 + 2*xi_3 - 1) / 8 
        dphi[:, 2, 6 ] = (1 + xi_1) * (1 + xi_2) * ( xi_1 + xi_2 + 2*xi_3 - 1) / 8
        dphi[:, 2, 7 ] = (1 - xi_1) * (1 + xi_2) * (-xi_1 + xi_2 + 2*xi_3 - 1) / 8
        dphi[:, 2, 8 ] = (1 - xi_1**2) * (1 - xi_2) * (-1) / 4
        dphi[:, 2, 9 ] = (1 + xi_1) * (1 - xi_2**2) * (-1) / 4
        dphi[:, 2, 10] = (1 - xi_1**2) * (1 + xi_2) * (-1) / 4
        dphi[:, 2, 11] = (1 - xi_1) * (1 - xi_2**2) * (-1) / 4
        dphi[:, 2, 12] = (1 - xi_1**2) * (1 - xi_2) * (1) / 4
        dphi[:, 2, 13] = (1 + xi_1) * (1 - xi_2**2) * (1) / 4
        dphi[:, 2, 14] = (1 - xi_1**2) * (1 + xi_2) * (1) / 4
        dphi[:, 2, 15] = (1 - xi_1) * (1 - xi_2**2) * (1) / 4
        dphi[:, 2, 16] = (1 - xi_1) * (1 - xi_2) * (-2*xi_3) / 4
        dphi[:, 2, 17] = (1 + xi_1) * (1 - xi_2) * (-2*xi_3) / 4
        dphi[:, 2, 18] = (1 + xi_1) * (1 + xi_2) * (-2*xi_3) / 4
        dphi[:, 2, 19] = (1 - xi_1) * (1 + xi_2) * (-2*xi_3) / 4

        return phi, dphi


    def elementary_matrices(self, element_id: int, material: Material):
        """This method returns elementary stiffness and mass matrices for HEXAHEDRON-20 nodes.
        ANSYS SOLID95 - Do not compare with new Ansys solid elements
        """

        const_mat, rho = self.get_constitutive_model(material, model_type="linear-isotropic")

        # nodes from element
        elem_nodes = self.connectivity[element_id, 1:]

        # element nodal coords
        coords = self.nodal_coordinates[elem_nodes, 1:4]

        # Jacobian matrix
        JAC_K = self.dphi_K @ coords
        JAC_M = self.dphi_M @ coords

        # Jacobian determinant and inverse
        detJAC_K, invJAC_K = self.get_detJAC_and_invJAC(JAC_K)
        detJAC_M, invJAC_M = self.get_detJAC_and_invJAC(JAC_M)

        # derivatives
        dphi_t = invJAC_K @ self.dphi_K

        B = np.zeros((self.nint_K, 6, self.DOF_PER_ELEMENT), dtype=float)
        B[:, 0, 0::3] = dphi_t[:, 0, :]
        B[:, 1, 1::3] = dphi_t[:, 1, :]
        B[:, 2, 2::3] = dphi_t[:, 2, :]
        B[:, 3, 0::3] = dphi_t[:, 1, :]
        B[:, 3, 1::3] = dphi_t[:, 0, :]
        B[:, 4, 0::3] = dphi_t[:, 2, :]
        B[:, 4, 2::3] = dphi_t[:, 0, :]
        B[:, 5, 1::3] = dphi_t[:, 2, :]
        B[:, 5, 2::3] = dphi_t[:, 1, :]

        N = np.zeros((self.nint_M, 3, self.DOF_PER_ELEMENT), dtype=float)
        N[:, 0, 0::3] = self.phi_M
        N[:, 1, 1::3] = self.phi_M
        N[:, 2, 2::3] = self.phi_M

        # integration loop
        Ke, Me = 0, 0
        
        for i in range(self.nint_K):
            Ke += B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC_K[i, :, :] * self.wps_K[i])

        for i in range(self.nint_M):
            Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC_M[i, :, :] * self.wps_M[i])

        # if self.nint_M >= self.nint_K:
        #     for i in range(self.nint_M):
        #         Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC_M[i, :, :] * self.wps_M[i])
        #         if i <= self.nint_K:
        #             Ke += B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC_K[i, :, :] * self.wps_K[i])

        # else:
        #     for i in range(self.nint_K):
        #         Ke += B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC_K[i, :, :] * self.wps_K[i])
        #         if i <= self.nint_M:
        #             Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC_M[i, :, :] * self.wps_M[i])

        return Ke, Me


    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        if self.solids_connectivity.shape[1] == self.NODES_PER_ELEMENT + 4:
            self.connectivity = self.solids_connectivity[
                :, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19]
            ]


    def generate_ind_rows_cols(self, reorder: bool = True):
        """ 
        This method processess the dof indices (rows and columns) 
        for assembly
        """

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.solids_connectivity[
                :, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]

        dof, edof = self.DOF_PER_NODE, self.DOF_PER_ELEMENT
        n_el = self.solids_connectivity.shape[0]
    
        local_dof = np.arange(dof, dtype=int)
        ind_dof = np.zeros((n_el, edof), dtype=int)

        for j in range(self.NODES_PER_ELEMENT):
            ind_dof[:, j*dof : (1 + j)*dof] = dof * self.connectivity[:, j+1].reshape(-1, 1) + local_dof

        vect_indices = ind_dof.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dof, edof)).flatten()

        return self.ind_rows, self.ind_cols
    
# fmt: on