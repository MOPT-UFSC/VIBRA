import numpy as np

from vibra.engine.elements.solid_elements import Element3D
from vibra.engine.properties.material import Material

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

class STRUCT_HEXAHEDRON_8(Element3D):

    NODES_PER_ELEMENT = 8
    DOF_PER_NODE = 3
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE
    LOCAL_DOF = np.arange(DOF_PER_NODE, dtype=int)

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivity = None
        self.element_label = "structural_hexahedron_8"

        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.solids_connectivity = self.model.mesh.solids_connectivity

        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.solids_connectivity)

        self.define_integration_points()
        self.load_extra_shape_function_state()
        self.process_shape_functions_and_derivatives()


    def load_extra_shape_function_state(self):
        """
        This method updates the extra shape functions state based on the model global properties.
        """
        self.extra_shape_function = False
        advanced_element_options = self.model.properties._get_property("advanced_element_options")
        if not isinstance(advanced_element_options, dict):
            return
        
        hex8_options = advanced_element_options.get("hex8", dict)
        if not isinstance(hex8_options, dict):
            return

        self.extra_shape_function = hex8_options.get("extra_shape_functions")


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

        esf = 3 if self.extra_shape_function else 0
        phi = np.zeros((Nz, self.NODES_PER_ELEMENT + esf), dtype=float)

        phi[:, 0] = (1.0 - xi_1) * (1.0 - xi_2) * (1.0 - xi_3) / 8       # ->      (-1.0, -1.0, -1.0)   Node 1
        phi[:, 1] = (1.0 + xi_1) * (1.0 - xi_2) * (1.0 - xi_3) / 8       # ->      ( 1.0, -1.0, -1.0)   Node 2
        phi[:, 2] = (1.0 + xi_1) * (1.0 + xi_2) * (1.0 - xi_3) / 8       # ->      ( 1.0,  1.0, -1.0)   Node 3
        phi[:, 3] = (1.0 - xi_1) * (1.0 + xi_2) * (1.0 - xi_3) / 8       # ->      (-1.0,  1.0, -1.0)   Node 4
        phi[:, 4] = (1.0 - xi_1) * (1.0 - xi_2) * (1.0 + xi_3) / 8       # ->      (-1.0, -1.0,  1.0)   Node 5
        phi[:, 5] = (1.0 + xi_1) * (1.0 - xi_2) * (1.0 + xi_3) / 8       # ->      ( 1.0, -1.0,  1.0)   Node 6
        phi[:, 6] = (1.0 + xi_1) * (1.0 + xi_2) * (1.0 + xi_3) / 8       # ->      ( 1.0,  1.0,  1.0)   Node 7
        phi[:, 7] = (1.0 - xi_1) * (1.0 + xi_2) * (1.0 + xi_3) / 8       # ->      (-1.0,  1.0,  1.0)   Node 8

        if esf:
            phi[:, 8] = (1.0 - xi_1**2)                                  # ->      ( 0.0,  1.0,  1.0)   Node 8
            phi[:, 9] = (1.0 - xi_2**2)                                  # ->      ( 1.0,  0.0,  1.0)   Node 9
            phi[:, 10] = (1.0 - xi_3**2)                                 # ->      ( 1.0,  1.0,  0.0)   Node 10

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((self.nint, 3, self.NODES_PER_ELEMENT + esf), dtype=float)

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

        if esf:
            dphi[:, 0, 8] = -(2 * xi_1)
            dphi[:, 1, 9] = -(2 * xi_2)
            dphi[:, 2, 10] = -(2 * xi_3)

        if Nz == 1:
            return phi[0, :], dphi[0, :, :]

        return phi, dphi


    @property
    def extra_dofs(self):
        esf = 3 if self.extra_shape_function else 0
        return int(self.DOF_PER_NODE * esf)


    @property
    def local_coordinates(self):
        """
        """
        ## calculation points (Atalla and Sgard, 2015, pg. 170)
        local_coords = np.array([ 
            [-1.0, -1.0, -1.0],      # ->      (-1.0, -1.0, -1.0)   Node 1
            [ 1.0, -1.0, -1.0],      # ->      ( 1.0, -1.0, -1.0)   Node 2
            [ 1.0,  1.0, -1.0],      # ->      ( 1.0,  1.0, -1.0)   Node 3
            [-1.0,  1.0, -1.0],      # ->      (-1.0,  1.0, -1.0)   Node 4
            [-1.0, -1.0,  1.0],      # ->      (-1.0, -1.0,  1.0)   Node 5
            [ 1.0, -1.0,  1.0],      # ->      ( 1.0, -1.0,  1.0)   Node 6
            [ 1.0,  1.0,  1.0],      # ->      ( 1.0,  1.0,  1.0)   Node 7
            [-1.0,  1.0,  1.0],      # ->      (-1.0,  1.0,  1.0)   Node 8
            ], dtype=float)

        return local_coords


    def elementary_matrices(self, el_index: int, material: Material):
        """This method returns elementary stiffness and mass matrices for HEXAHEDRON-8 nodes.
        ANSYS SOLID45 w/o extra diplacements (very simple)
        """

        const_mat, rho = self.get_constitutive_model(material, model_type="linear-isotropic")

        # nodes from element
        elem_nodes = self.connectivity[el_index, 1:]

        # element nodal coords
        coords = self.nodal_coordinates[elem_nodes, 1:4]

        # Jacobian matrix
        JAC = self.dphi[:, :, :self.NODES_PER_ELEMENT] @ coords

        # Jacobian determinant and inverse
        detJAC, invJAC = self.get_detJAC_and_invJAC(JAC)

        # derivatives
        dphi_t = invJAC @ self.dphi

        B = np.zeros((self.nint, 6, self.DOF_PER_ELEMENT + self.extra_dofs), dtype=float)
        B[:, 0, 0::3] = dphi_t[:, 0, :]
        B[:, 1, 1::3] = dphi_t[:, 1, :]
        B[:, 2, 2::3] = dphi_t[:, 2, :]
        B[:, 3, 0::3] = dphi_t[:, 1, :]
        B[:, 3, 1::3] = dphi_t[:, 0, :]
        B[:, 4, 0::3] = dphi_t[:, 2, :]
        B[:, 4, 2::3] = dphi_t[:, 0, :]
        B[:, 5, 1::3] = dphi_t[:, 2, :]
        B[:, 5, 2::3] = dphi_t[:, 1, :]

        N = np.zeros((self.nint, 3, self.DOF_PER_ELEMENT), dtype=float)
        N[:, 0, 0::3] = self.phi[:, :self.NODES_PER_ELEMENT]
        N[:, 1, 1::3] = self.phi[:, :self.NODES_PER_ELEMENT]
        N[:, 2, 2::3] = self.phi[:, :self.NODES_PER_ELEMENT]

        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            Ke += B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])
            Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i])

        # condense the stiffness matrix Ke if the extra shape functions were enabled
        if self.extra_dofs:
            Kaa = Ke[0 : self.DOF_PER_ELEMENT, 0 : self.DOF_PER_ELEMENT]
            Kab = Ke[0 : self.DOF_PER_ELEMENT, self.DOF_PER_ELEMENT :]
            Kba = Kab.T
            # Kba = Ke[self.DOF_PER_ELEMENT :, 0 : self.DOF_PER_ELEMENT]
            Kbb = Ke[self.DOF_PER_ELEMENT :, self.DOF_PER_ELEMENT :]

            Ke = Kaa - Kab @ np.linalg.inv(Kbb) @ Kba

        return Ke, Me


    def get_data_to_compute_stresses(self, element_id: int, nodal_solution: np.ndarray, const_mat: np.ndarray):

        # nodal solution
        Ue = nodal_solution

        # nodes from element
        elem_nodes = self.connectivity[element_id, 1:]

        # element nodal coords
        coords = self.nodal_coordinates[elem_nodes, 1:4]

        # Jacobian matrix
        JAC = self.dphi[:, :, :self.NODES_PER_ELEMENT] @ coords

        # Jacobian determinant and inverse
        detJAC, invJAC = self.get_detJAC_and_invJAC(JAC)

        # derivatives
        dphi_t = invJAC @ self.dphi

        B = np.zeros((self.nint, 6, self.DOF_PER_ELEMENT + self.extra_dofs), dtype=float)
        B[:, 0, 0::3] = dphi_t[:, 0, :]
        B[:, 1, 1::3] = dphi_t[:, 1, :]
        B[:, 2, 2::3] = dphi_t[:, 2, :]
        B[:, 3, 0::3] = dphi_t[:, 1, :]
        B[:, 3, 1::3] = dphi_t[:, 0, :]
        B[:, 4, 0::3] = dphi_t[:, 2, :]
        B[:, 4, 2::3] = dphi_t[:, 0, :]
        B[:, 5, 1::3] = dphi_t[:, 2, :]
        B[:, 5, 2::3] = dphi_t[:, 1, :]

        if self.extra_dofs:

            # initialize the stiffness matrix Ke
            Ke = 0.

            # integrate the stiffness matrix
            for i in range(self.nint):
                Ke += B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])

            Kab = Ke[0 : self.DOF_PER_ELEMENT, self.DOF_PER_ELEMENT :]
            Kba = Kab.T
            Kbb = Ke[self.DOF_PER_ELEMENT :, self.DOF_PER_ELEMENT :]

            a = -np.linalg.inv(Kbb) @ (Kba @ Ue)

            # compute the extended nodal results
            Ue = np.append(Ue, a, axis=0)

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

        const_mat, _ = self.get_constitutive_model(material, model_type="linear-isotropic")

        # get data to compute the stress (with or without ESF)
        B, Ue = self.get_data_to_compute_stresses(element_id, Ue, const_mat)

        # initialize the element stresses matrix
        element_stresses = np.zeros((6, self.nint, Ue.shape[1]), dtype=complex)

        # calculate the nodal stress tensor
        for i in range(self.nint):
            element_stresses[:, i, :] = const_mat @ (B[i, :, :] @ Ue)

        if element_averaged:
            return np.average(element_stresses, axis=0)

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