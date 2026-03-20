import numpy as np

from vibra.engine.elements.solid_elements import Element3D
from vibra.engine.properties.material import Material

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

from vibra.engine.elements.elements_3d.structural.FEMSTHEX8_Bbar import matricesH8S_Bbar

class STRUCT_HEXAHEDRON_8(Element3D):

    NODES_PER_ELEMENT = 8
    DOF_PER_NODE = 3
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE
    LOCAL_DOF = np.arange(DOF_PER_NODE, dtype=int)

    dil_projector = np.array([1, 1, 1, 0, 0, 0], dtype=float).reshape(-1, 1)
    m_mt = dil_projector @ dil_projector.T


    def __init__(self, model: "Model"):

        self.model = model

        self.connectivity = None
        self.element_label = "structural_hexahedron_8"

        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.solids_connectivity = self.model.mesh.solids_connectivity

        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.solids_connectivity)

        self.define_integration_points()
        self.load_element_options()
        self.process_shape_functions_and_derivatives()


    @property
    def corner_nodes_indexes(self):
        indexes = np.arange(self.NODES_PER_ELEMENT, dtype=int)
        return indexes[:8]


    def load_element_options(self):
        """
        This method updates the extra shape functions state based on the model global properties.
        """
        self.extra_shape_function = False
        self.Bbar_formulation = False
        advanced_element_options = self.model.properties._get_property("advanced_element_options")
        if not isinstance(advanced_element_options, dict):
            return

        hex8_options = advanced_element_options.get("hex8", dict)
        if not isinstance(hex8_options, dict):
            return

        self.extra_shape_function = hex8_options.get("extra_shape_functions", False)
        self.Bbar_formulation = hex8_options.get("Bbar_formulation", False)


    def define_integration_points(self, integration_points: int = 8):
        """
        This method defines the integration points and their
        weights for numerical integration.
        """
        self.nint = integration_points
        self.num_int_data = self.integration_points_data_for_hexahedrons(integration_points)
        self.wps = self.num_int_data[:, -1].reshape(-1, 1, 1)


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
        N = self.phi[:, :self.NODES_PER_ELEMENT]
        n_intp, n_nodes = N.shape

        if n_intp == n_nodes:
            return np.linalg.inv(N)

        elif n_intp > n_nodes:
            return np.linalg.inv(N.T @ N) @ N.T

        else:
            return None


    def get_shape_functions_and_derivatives(
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

        if isinstance(xi_1, np.ndarray):
            Nz = xi_1.size
        else:
            Nz = 1

        ##NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015

        # define the shape functions (Atalla and Sgard, 2015, pg. 171)
        phi = np.zeros((Nz, self.NODES_PER_ELEMENT), dtype=float)

        phi[:, 0] = (1.0 - xi_1) * (1.0 - xi_2) * (1.0 - xi_3) / 8       # ->      (-1.0, -1.0, -1.0)   Node 1
        phi[:, 1] = (1.0 + xi_1) * (1.0 - xi_2) * (1.0 - xi_3) / 8       # ->      ( 1.0, -1.0, -1.0)   Node 2
        phi[:, 2] = (1.0 + xi_1) * (1.0 + xi_2) * (1.0 - xi_3) / 8       # ->      ( 1.0,  1.0, -1.0)   Node 3
        phi[:, 3] = (1.0 - xi_1) * (1.0 + xi_2) * (1.0 - xi_3) / 8       # ->      (-1.0,  1.0, -1.0)   Node 4
        phi[:, 4] = (1.0 - xi_1) * (1.0 - xi_2) * (1.0 + xi_3) / 8       # ->      (-1.0, -1.0,  1.0)   Node 5
        phi[:, 5] = (1.0 + xi_1) * (1.0 - xi_2) * (1.0 + xi_3) / 8       # ->      ( 1.0, -1.0,  1.0)   Node 6
        phi[:, 6] = (1.0 + xi_1) * (1.0 + xi_2) * (1.0 + xi_3) / 8       # ->      ( 1.0,  1.0,  1.0)   Node 7
        phi[:, 7] = (1.0 - xi_1) * (1.0 + xi_2) * (1.0 + xi_3) / 8       # ->      (-1.0,  1.0,  1.0)   Node 8

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((Nz, 3, self.NODES_PER_ELEMENT), dtype=float)

        dphi[:, 0, 0] = -(1.0 - xi_2) * (1.0 - xi_3) / 8
        dphi[:, 0, 1] =  (1.0 - xi_2) * (1.0 - xi_3) / 8
        dphi[:, 0, 2] =  (1.0 + xi_2) * (1.0 - xi_3) / 8
        dphi[:, 0, 3] = -(1.0 + xi_2) * (1.0 - xi_3) / 8
        dphi[:, 0, 4] = -(1.0 - xi_2) * (1.0 + xi_3) / 8
        dphi[:, 0, 5] =  (1.0 - xi_2) * (1.0 + xi_3) / 8
        dphi[:, 0, 6] =  (1.0 + xi_2) * (1.0 + xi_3) / 8
        dphi[:, 0, 7] = -(1.0 + xi_2) * (1.0 + xi_3) / 8

        dphi[:, 1, 0] = -(1.0 - xi_1) * (1.0 - xi_3) / 8
        dphi[:, 1, 1] = -(1.0 + xi_1) * (1.0 - xi_3) / 8
        dphi[:, 1, 2] =  (1.0 + xi_1) * (1.0 - xi_3) / 8
        dphi[:, 1, 3] =  (1.0 - xi_1) * (1.0 - xi_3) / 8
        dphi[:, 1, 4] = -(1.0 - xi_1) * (1.0 + xi_3) / 8
        dphi[:, 1, 5] = -(1.0 + xi_1) * (1.0 + xi_3) / 8
        dphi[:, 1, 6] =  (1.0 + xi_1) * (1.0 + xi_3) / 8
        dphi[:, 1, 7] =  (1.0 - xi_1) * (1.0 + xi_3) / 8

        dphi[:, 2, 0] = -(1.0 - xi_1) * (1.0 - xi_2) / 8
        dphi[:, 2, 1] = -(1.0 + xi_1) * (1.0 - xi_2) / 8
        dphi[:, 2, 2] = -(1.0 + xi_1) * (1.0 + xi_2) / 8
        dphi[:, 2, 3] = -(1.0 - xi_1) * (1.0 + xi_2) / 8
        dphi[:, 2, 4] =  (1.0 - xi_1) * (1.0 - xi_2) / 8
        dphi[:, 2, 5] =  (1.0 + xi_1) * (1.0 - xi_2) / 8
        dphi[:, 2, 6] =  (1.0 + xi_1) * (1.0 + xi_2) / 8
        dphi[:, 2, 7] =  (1.0 - xi_1) * (1.0 + xi_2) / 8

        if Nz == 1:
            return phi[0, :], dphi[0, :, :]

        return phi, dphi


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
        esf = 3 if self.extra_shape_function else 0
        return int(self.DOF_PER_NODE * esf)


    def process_detJAC_and_B_matrix(self, element_id: int):
        """
        This method computes and returns the matrix of shape functions 
        derivatives B and the determinant of the Jacobian matrix detJAC. 
        """

        # nodes from element
        elem_nodes = self.connectivity[element_id, 1:]

        # element nodal coords
        coords = self.nodal_coordinates[elem_nodes, 1:4]

        # Jacobian matrix
        JAC = self.dphi @ coords

        # Jacobian determinant and inverse
        detJAC, invJAC = self.get_detJAC_and_invJAC(JAC)

        # derivatives
        dphi_t = invJAC @ self.dphi

        # initialize the B matrix
        edof = self.DOF_PER_ELEMENT
        B = np.zeros((self.nint, 6, edof + self.extra_dofs), dtype=float)

        B[:, 0, 0:edof:3] = dphi_t[:, 0, :]
        B[:, 1, 1:edof:3] = dphi_t[:, 1, :]
        B[:, 2, 2:edof:3] = dphi_t[:, 2, :]
        B[:, 3, 0:edof:3] = dphi_t[:, 1, :]
        B[:, 3, 1:edof:3] = dphi_t[:, 0, :]
        B[:, 4, 0:edof:3] = dphi_t[:, 2, :]
        B[:, 4, 2:edof:3] = dphi_t[:, 0, :]
        B[:, 5, 1:edof:3] = dphi_t[:, 2, :]
        B[:, 5, 2:edof:3] = dphi_t[:, 1, :]

        if self.Bbar_formulation:
            # B-bar: compute B at centroid (0, 0, 0) and extract dilatational part

            # Jacobian matrix at the centroid (0, 0, 0)
            JAC_0 = self.dphi_0 @ coords

            # Jacobian determinant and inverse at the centroid
            detJAC_0, invJAC_0 = self.get_detJAC_and_invJAC(JAC_0)

            # derivatives in global coordinates variables
            dphi_t0 = invJAC_0 @ self.dphi_0
       
            # initialize the B0 matrix
            B0 = np.zeros((6, edof), dtype=float)

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
            Bbar_dil = (1/3) * self.m_mt @ B0
            # Bbar_dil = np.zeros((6, edof), dtype=float)
            # Bbar_dil[0, 0:edof:3] = dphi_t0[0, :] / 3
            # Bbar_dil[1, 0:edof:3] = dphi_t0[0, :] / 3
            # Bbar_dil[2, 0:edof:3] = dphi_t0[0, :] / 3
            # Bbar_dil[0, 1:edof:3] = dphi_t0[1, :] / 3
            # Bbar_dil[1, 1:edof:3] = dphi_t0[1, :] / 3
            # Bbar_dil[2, 1:edof:3] = dphi_t0[1, :] / 3
            # Bbar_dil[0, 2:edof:3] = dphi_t0[2, :] / 3
            # Bbar_dil[1, 2:edof:3] = dphi_t0[2, :] / 3
            # Bbar_dil[2, 2:edof:3] = dphi_t0[2, :] / 3


            # B_dil = (1/3) * m * m^T * B  extracts the volumetric part of B
            B_dil = (1/3) * self.m_mt @ B
            # B_dil = np.zeros((self.nint, 6, edof), dtype=float)
            # B_dil[:, 0, 0:edof:3] = dphi_t[:, 0, :] / 3
            # B_dil[:, 1, 0:edof:3] = dphi_t[:, 0, :] / 3
            # B_dil[:, 2, 0:edof:3] = dphi_t[:, 0, :] / 3
            # B_dil[:, 0, 1:edof:3] = dphi_t[:, 1, :] / 3
            # B_dil[:, 1, 1:edof:3] = dphi_t[:, 1, :] / 3
            # B_dil[:, 2, 1:edof:3] = dphi_t[:, 1, :] / 3
            # B_dil[:, 0, 2:edof:3] = dphi_t[:, 2, :] / 3
            # B_dil[:, 1, 2:edof:3] = dphi_t[:, 2, :] / 3
            # B_dil[:, 2, 2:edof:3] = dphi_t[:, 2, :] / 3

            # B-bar: replace dilatational part of B by centroid dilatational part
            # Bbar = B - B_dil(gauss_pt) + Bbar_dil(centroid)
            Bbar = B - B_dil + Bbar_dil

            return detJAC, Bbar

        elif self.extra_shape_function:

            #TODO: add reference
            # Zienkiewicz, O. C., Taylor, R. L. The Finite Element Method: Its Basis and Fundamentals. Seventh Edition. pg 271-275

            # Jacobian matrix at the centroid (0, 0, 0)
            JAC_0 = self.dphi_0 @ coords

            # Jacobian determinant and inverse at the centroid
            detJAC_0, invJAC_0 = self.get_detJAC_and_invJAC(JAC_0)
        
            # adjusted derivatives in global coordinates variables (satisfy the stress patch test)
            dphi_esf_t = (detJAC_0 / detJAC) * invJAC_0 @ self.dphi_esf

            B[:, 0, edof + 0::3] = dphi_esf_t[:, 0, :]
            B[:, 1, edof + 1::3] = dphi_esf_t[:, 1, :]
            B[:, 2, edof + 2::3] = dphi_esf_t[:, 2, :]
            B[:, 3, edof + 0::3] = dphi_esf_t[:, 1, :]
            B[:, 3, edof + 1::3] = dphi_esf_t[:, 0, :]
            B[:, 4, edof + 0::3] = dphi_esf_t[:, 2, :]
            B[:, 4, edof + 2::3] = dphi_esf_t[:, 0, :]
            B[:, 5, edof + 1::3] = dphi_esf_t[:, 2, :]
            B[:, 5, edof + 2::3] = dphi_esf_t[:, 1, :]

        return detJAC, B


    def elementary_matrices(self, element_id: int, material: Material):
        """This method returns elementary stiffness and mass matrices for 
        HEXAHEDRON-8 nodes (ANSYS SOLID45 w/o extra diplacements).
        """

        # get constitutive law matrix D and the material's density
        D, rho = self.get_constitutive_model(material, model_type="linear-isotropic")

        # process the determinant of Jacobian and the B matrix
        detJAC, B = self.process_detJAC_and_B_matrix(element_id)

        # initialize the matrix of shape functions N
        N = np.zeros((self.nint, 3, self.DOF_PER_ELEMENT), dtype=float)
        N[:, 0, 0::3] = self.phi
        N[:, 1, 1::3] = self.phi
        N[:, 2, 2::3] = self.phi

        # integration loop
        Ke, Me = 0., 0.
        for i in range(self.nint):
            Ke += B[i, :, :].T @ D @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])
            Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i])

        # condense the stiffness matrix Ke if the extra shape functions were enabled
        if self.extra_shape_function:
            Kuu = Ke[0 : self.DOF_PER_ELEMENT, 0 : self.DOF_PER_ELEMENT]
            Kua = Ke[0 : self.DOF_PER_ELEMENT, self.DOF_PER_ELEMENT :]
            Kau = Kua.T
            Kbb = Ke[self.DOF_PER_ELEMENT :, self.DOF_PER_ELEMENT :]

            Ke = Kuu - Kua @ np.linalg.inv(Kbb) @ Kau

        # # if element_id in [0]:
        # Ke_2, Me_2 = matricesH8S_Bbar(
        #     element_id, 
        #     self.nodal_coordinates, 
        #     self.connectivity, 
        #     material.elasticity_modulus,
        #     material.poisson_ratio, 
        #     material.material_density
        #     )

        # mask_Ke = Ke != 0
        # mask_Me = Me != 0

        # dif_Ke = 100 * np.max(np.abs(Ke[mask_Ke] - Ke_2[mask_Ke]) / (Ke[mask_Ke] + Ke_2[mask_Ke]))
        # dif_Me = 100 * np.max(np.abs(Me[mask_Me] - Me_2[mask_Me]) / (Me[mask_Me] + Me_2[mask_Me]))

        # print()
        # print(f"Maximum difference for Ke (#{element_id}): {dif_Ke} [%]")
        # print(f"Maximum difference for Me (#{element_id}): {dif_Me} [%]")

        return Ke, Me


    def get_data_to_compute_stresses(self, element_id: int, nodal_solution: np.ndarray, D: np.ndarray):

        # nodal solution
        Ue = nodal_solution

        # process the determinant of Jacobian and the B matrix
        detJAC, B = self.process_detJAC_and_B_matrix(element_id)

        if self.extra_shape_function:

            # initialize the stiffness matrix Ke
            Ke = 0.

            # integrate the stiffness matrix
            for i in range(self.nint):
                Ke += B[i, :, :].T @ D @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])

            Kau = Ke[self.DOF_PER_ELEMENT :, 0 : self.DOF_PER_ELEMENT]
            Kaa = Ke[self.DOF_PER_ELEMENT :, self.DOF_PER_ELEMENT :]

            # extra dofs results
            u_esf = -np.linalg.inv(Kaa) @ (Kau @ Ue)

            # extend element solution with extra dofs results
            Ue = np.append(Ue, u_esf, axis=0)

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
            node_ids = self.connectivity[element_id, 1:]

        if isinstance(nodal_solution, np.ndarray):
            Ue = nodal_solution

        elif isinstance(solution, np.ndarray):
            indexes = node_ids.reshape(-1, 1) * self.DOF_PER_NODE + self.LOCAL_DOF
            Ue = solution[indexes.flatten(), :]    

        else:
            return 0.

        if self.connectivity is None:
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


    def extrapolate_stresses_to_nodes(self, element_stresses: np.ndarray) -> np.ndarray:
        """
        This method extrapolates the nodal stresses from 
        the stresses calculated at the integration points.

        Parameters
        ----------
        element_stresses: np.ndarray
            The stresses calculate at integration points.

        """

        # Nf = element_stresses.shape[2]
        # nodal_stresses = np.zeros((self.NODES_PER_ELEMENT, 6, Nf), dtype=complex)

        # for i in range(6):
        #     nodal_stresses[:, i, :] = self.phi_inv @ element_stresses[:, i, :]

        nodal_stresses = self.phi_inv @ element_stresses
        # nodal_stresses = np.transpose(nodal_stresses, axes=(1, 0, 2))

        return nodal_stresses


    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        if self.solids_connectivity.shape[1] == self.NODES_PER_ELEMENT + 4:
            self.connectivity = self.solids_connectivity[:, [0, 4, 5, 6, 7, 8, 9, 10, 11]]


    def generate_ind_rows_cols(self, reorder: bool = True):
        """This method processess the dof indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.solids_connectivity[:, [0, 4, 5, 6, 7, 8, 9, 10, 11]]

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