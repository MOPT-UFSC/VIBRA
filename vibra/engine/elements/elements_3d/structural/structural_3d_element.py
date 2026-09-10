from typing import TYPE_CHECKING

from vibra.engine.elements.common.matrix_utils import get_3x3_matrix_inverse
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

        self.local_dof = np.arange(dof_per_node, dtype=int)


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
        jac = self.dphi @ coords

        # Jacobian determinant and inverse
        inv_jac, det_jac = get_3x3_matrix_inverse(jac)

        # derivatives
        dphi_t = inv_jac @ self.dphi

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
            return det_jac, B, coords

        return det_jac, B


    def process_detJAC_and_B_matrix2(self, element_ids: int):
        """
        This method computes and returns the matrix of shape functions 
        derivatives B and the determinant of the Jacobian matrix detJAC. 
        """

        reduced_connect = self.connectivities[element_ids, :]

        nel = len(reduced_connect)

        stacked_coords = np.zeros((nel, self.nodes_per_element, 3), dtype=float)
        for j in range(self.nodes_per_element):
            stacked_coords[:, j, :] = self.model.mesh.nodal_coordinates[reduced_connect[:, j], 1:4]

        # initialize the B matrix
        B = np.zeros((nel, self.nint, 6, self.dof_per_element), dtype=float)

        for i in range(self.nint):

            # Jacobian matrix
            jacs = self.dphi[i, :, :] @ stacked_coords

            # Jacobian determinant and inverse
            inv_jacs, _ = get_3x3_matrix_inverse(jacs)

            # derivatives
            dphi_t = inv_jacs @ self.dphi[i, :, :]

            B[:, i, 0, 0::3] = dphi_t[:, 0, :]
            B[:, i, 1, 1::3] = dphi_t[:, 1, :]
            B[:, i, 2, 2::3] = dphi_t[:, 2, :]
            B[:, i, 3, 0::3] = dphi_t[:, 1, :]
            B[:, i, 3, 1::3] = dphi_t[:, 0, :]
            B[:, i, 4, 0::3] = dphi_t[:, 2, :]
            B[:, i, 4, 2::3] = dphi_t[:, 0, :]
            B[:, i, 5, 1::3] = dphi_t[:, 2, :]
            B[:, i, 5, 2::3] = dphi_t[:, 1, :]

        return B


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
        const_mat, rho = self.get_constitutive_model(material.identifier, model_type="linear-isotropic")

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
        element_averaged: bool = False,
        extrapolate: bool = False,
        ):

        node_ids = self.connectivities[element_id, :]
        indices = self.model.get_dof_indices_from_nodes(node_ids, "structural")

        # define the element's solution matrix
        Ue = self.model.solution.structural_solution[indices.flatten(), :]

        # get the material ID of the element
        material = self.get_material(self.model.mesh.solids_connectivity[element_id, 1])

        # constitutive material law
        D, _ = self.get_constitutive_model(material.identifier, model_type="linear-isotropic")

        # get data to compute the stress
        _, B = self.process_detJAC_and_B_matrix(element_id)

        # calculate the nodal stress tensor
        element_stresses = D @ (B @ Ue)

        if extrapolate:
            extrapolated_stresses = self.phi_inv @ element_stresses.transpose(1, 0, 2)
            return extrapolated_stresses.transpose(1, 0, 2)

        if element_averaged:
            return np.average(element_stresses, axis=1)

        return element_stresses


    def process_stresses_at_integration_points_batched(
        self,
        element_ids : list[int],
        material: Material | None,
        extrapolate: bool = False,
        ):

        n_el = len(element_ids)
        n_freq = len(self.model.frequencies)

        _dof_indices_from_nodes = self.model.get_dof_indices_from_nodes(self.connectivities[element_ids, :].ravel(), "structural")

        # define the nodal solution matrix (batched)
        Ue_batch = self.model.solution.structural_solution[_dof_indices_from_nodes.ravel(), :].reshape(n_el, 1, self.dof_per_element, n_freq)

        # constitutive material law
        D, _ = self.get_constitutive_model(material.identifier, model_type="linear-isotropic")

        # get batched data to compute the elements stresses
        B_batch = self.process_detJAC_and_B_matrix2(element_ids)

        # calculate the nodal stress tensor (batched)
        elements_stresses = D @ (B_batch @ Ue_batch)

        if extrapolate:
            extrapolated_stresses = self.phi_inv @ elements_stresses.transpose(0, 2, 1, 3)
            return extrapolated_stresses.transpose(0, 2, 1, 3)

        return elements_stresses


    def generate_ind_rows_cols(self, reorder: bool = True):
        """This method processess the dof indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivities = self.model.mesh.solids_connectivity[:, 4:]

        dof_indexes = self.dof_indexes_processor("structural")

        return dof_indexes.get_rows_and_cols_indices_3D(self.connectivities)