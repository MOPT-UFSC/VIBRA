from typing import TYPE_CHECKING

from vibra.engine.elements.elements_3d.solid_elements import Element3D
from vibra.engine.properties.material import Material

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class Structural3DElement(Element3D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.element_label = ""
        self.connectivities = None
        self.dof_indexes_proc = self.dof_indexes_processor("structural")


    def process_N_matrix(self):
        N = np.zeros((self.nint, 3, self.dof_per_element), dtype=float)

        for i in range(self.nint):
            N[i, 0, 0::3] = self.phi[i, :]
            N[i, 1, 1::3] = self.phi[i, :]
            N[i, 2, 2::3] = self.phi[i, :]

        self.N_matrix = N


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
        JAC = self.dphi @ coords

        # Jacobian determinant and inverse
        detJAC, invJAC = self.get_detJAC_and_invJAC(JAC)

        # derivatives
        dphi_t = invJAC @ self.dphi
        
        # initialize the B matrix
        B = np.zeros((self.nint, 6, self.dof_per_element), dtype=float)

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
            return detJAC, B, coords

        return detJAC, B


    def elementary_matrices(self, element_id: int, material: Material):
        """
        This method integrates the elementary stiffness and mass matrices
        for the structural quadratic tetrahedron element.

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
        detJAC, B = self.process_detJAC_and_B_matrix(element_id)

        # matrix of shape functions N
        N = self.N_matrix

        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            Ke += B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])
            Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i])

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
        # nodal_stresses = np.zeros((self.nodes_per_element, 6, Nf), dtype=complex)

        # for i in range(6):
        #     nodal_stresses[:, i, :] = self.phi_inv @ element_stresses[:, i, :]

        # nodal_stresses = np.transpose(nodal_stresses, axes=(1, 0, 2))

        return self.phi_inv @ element_stresses


    def generate_ind_rows_cols(self, reorder: bool = True):
        """This method processess the dof indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivities = self.model.mesh.solids_connectivity[:, 4:]

        dof_indexes = self.dof_indexes_processor("structural")

        return dof_indexes.get_rows_and_cols_indices_3D(self.connectivities)