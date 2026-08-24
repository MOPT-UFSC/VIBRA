
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.tria3_element import TRIANGLE_3, get_local_coordinates

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class STRUCT_TRIANGLE_3(TRIANGLE_3):

    def __init__(self, model: "Model", dof_per_node: int = 3):
        super().__init__(model, dof_per_node)

        self.model = model

        self.connectivities = None
        self.element_label = "structural_triangular_3"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates

        self.N_matrix = self.get_N_matrix()


    def get_N_matrix(self):
        N = np.zeros((self.nint, 3, self.dof_per_element), dtype=float)

        for i in range(self.nint):
            N[i, 0, 0::3] = self.phi[i, :, :]
            N[i, 1, 1::3] = self.phi[i, :, :]
            N[i, 2, 2::3] = self.phi[i, :, :]

        return N


    def integrate_area(self, connectivities: np.ndarray):

        self.connectivities = connectivities

        # stack the element nodes coordinates for all elements
        coords = self.nodal_coordinates[[connect for connect in connectivities], 1:]

        # initialize variable
        dA = 0.

        # integration loop
        for i in range(self.nint):

            det_jacs = self.get_stacked_jacobian_determinant(i, coords)

            # integrate all elementary areas
            dA += det_jacs * self.wps[i]

        return np.sum(dA)


    def integrate_normal_pressure_load(self, el_index: int, e_normal: np.ndarray,  normal_pressure: np.ndarray) -> np.ndarray:
        """ 
        This method computes the elementary load vector.

        Parameters
        ----------
        el_index: int
            The element index.

        load: float, optional
            The load vector.

        Returns
        -------
        Fe: np.ndarray
            The elementary load vector.
        """

        # element nodes
        e_nodes = self.connectivities[el_index, :]

        # element nodal coordinates
        coords = self.nodal_coordinates[e_nodes, 1:]

        # initialize the variable Fe
        Fe = 0.

        # integration loop
        for i in range(self.nint):

            # determinant of Jacobian and normal vector for the i-th integration point
            det_jac, normal_vector, *_ = self.get_jacobian_determinant(i, coords, return_vectors=True)

            # matrix of shape functions for all DOF
            N = self.N_matrix[i, :, :]

            # the negative value of the normal is used to point the normal toward the interior of the domain.
            Fe += (N.T @ (-normal_vector @ normal_pressure)) * (det_jac * self.wps[i])

        return Fe


    def integrate_distributed_load(
            self, 
            el_index: int, 
            distributed_load: np.ndarray, 
            h_ecc: float = 0.0,
            load_vector: np.ndarray | float = 0.0,
            ) -> np.ndarray:
        """ 
        This method computes the elementary load vector.

        Parameters
        ----------
        el_index: int
            The element index.

        load: float, optional
            The load vector.

        Returns
        -------
        Fe: np.ndarray
            The elementary load vector.
        """

        # element nodes
        e_nodes = self.connectivities[el_index, :]

        # element nodal coordinates
        coords = self.nodal_coordinates[e_nodes, 1:]

        # initialize the variable Fe
        Fe = 0.
        Fe_moment = 0.

        # integration loop
        for i in range(self.nint):

            # determinant of Jacobian for the i-th integration point
            det_jac, normal_vector, g_xi, g_eta = self.get_jacobian_determinant(i, coords, return_vectors=True)

            # matrix of shape functions for all DOF
            N = self.N_matrix[i, :, :]

            Fe += (N.T @ distributed_load) * (det_jac * self.wps[i])

            # normal to surface load vector
            # normal_qvector = np.dot(load_vector, normal_vector) * normal_vector
            normal_qvector = (distributed_load.T @ normal_vector) @ normal_vector.T

            # tangent to surface load vector
            tangent_qvector = distributed_load.T - normal_qvector

            # compute moments
            dN_deta =  self.dphi[i, 1, :].reshape(-1, 1, 1)
            dN_dxi =  self.dphi[i, 0, :].reshape(-1, 1, 1)
            moment_xi  = np.sum(np.cross(g_xi, tangent_qvector) * h_ecc * dN_deta, axis=0)
            moment_eta = np.sum(np.cross(g_eta, tangent_qvector) * h_ecc * dN_dxi, axis=0)
            
            # load due the moments
            Fe_moment += ((moment_xi - moment_eta) / det_jac) * self.wps * 0.5

        return Fe


    def integrate_distributed_mass(self, el_index: int, distributed_mass: float) -> np.ndarray:
        """ 
        This method computes the elementary load vector.

        Parameters
        ----------
        el_index: int
            The element index.

        distributed_mass: float
            The mass density in kg/m².

        Returns
        -------
        Me: np.ndarray
            The two-dimensional elementary consistent mass matrix.
        """

        # element nodes
        e_nodes = self.connectivities[el_index, :]

        # element nodal coordinates
        coords = self.nodal_coordinates[e_nodes, 1:]

        # initialize the variable Fe
        Me = 0.

        # integration loop
        for i in range(self.nint):

            # determinant of Jacobian for the i-th integration point
            det_jac = self.get_jacobian_determinant(i, coords)

            # matrix of shape functions for all DOF
            N = self.N_matrix[i, :, :]

            Me += (N.T @ N) * distributed_mass * (det_jac * self.wps[i])

        return Me


    def get_load_indexes(self, index: int) -> np.ndarray:
        """
        Returns the load vector degrees of freedom indexes of an element.

        Parameter
        ---------
        index: int
            The element index of interest to compute the DOF indexes.

        """
        element_nodes = self.connectivities[index, :].reshape(-1, 1)
        element_dofs = self.dof_per_node * element_nodes + np.arange(self.dof_per_node, dtype=int)
        return element_dofs.flatten()


    def get_element_rows_and_columns_indexes(self):
        """
        Returns the element rows and columns degrees of freedom indexes of an element.
        """
        n_el = len(self.connectivities)
        dof, edof = self.dof_per_node, self.dof_per_element

        local_dof = np.arange(dof, dtype=int)
        ind_dof = np.zeros((n_el, edof), dtype=int)

        for j in range(self.nodes_per_element):
            start = j * dof
            end = (1 + j) * dof
            ind_dof[:, start : end] = dof * self.connectivities[:, j].reshape(-1, 1) + local_dof

        vect_indices = ind_dof.flatten()
        ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        ind_cols = (np.tile(ind_dof, edof)).flatten()

        return ind_rows, ind_cols