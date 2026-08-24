from typing import TYPE_CHECKING

from vibra.engine.elements.elements_1d.line2_element import LINE_2, get_local_coordinates

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class STRUCT_LINE_2(LINE_2):

    def __init__(self, model: "Model", dof_per_node: int = 3):
        super().__init__(model, dof_per_node)

        self.model = model

        self.connectivities = None
        self.element_label = "structural_line_2"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.N_matrix = self.get_N_matrix()


    def get_N_matrix(self):
        N = np.zeros((self.nint_M, 3, self.dof_per_element), dtype=float)

        for i in range(self.nint_M):
            N[i, 0, 0::3] = self.phi_M[i, :, :]
            N[i, 1, 1::3] = self.phi_M[i, :, :]
            N[i, 2, 2::3] = self.phi_M[i, :, :]

        return N


    def integrate_length(self, connectivities: np.ndarray):

        self.connectivities = connectivities

        # stack the element nodes coordinates for all elements
        coords = self.nodal_coordinates[[connect for connect in connectivities], 1:]

        # initialize variable
        dL = 0.

        # integration loop
        for i in range(self.nint_M):

            det_jacs = self.get_stacked_jacobian_determinant(i, coords)

            # integrate all elementary areas
            dL += det_jacs * self.wps_M[i]

        return np.sum(dL)


    def get_jacobian_determinant(self, int_point: int, coords: np.ndarray):
        """
        This method evaluates the Jacobian determinant for the i-th integrarion point.
        
        Parameters
        ----------

        int_point: int
            The integration point to be evaluated.

        coords:  np.ndarray
            A three-dimensional coordinate matrix of the element. 

        Return
        ------
        det_jac: np.ndarray
            The Jacobian determinant at the i-th integration point.

        """

        # Jacobian matrix
        jac = self.dphi_M[int_point, 0, :] @ coords

        # determinant of Jacobian matrix
        det_jac = np.linalg.norm(jac).reshape(-1, 1)

        return det_jac


    def get_stacked_jacobian_determinant(self, int_point: int, coords: np.ndarray):
        """
        This method evaluates the Jacobian determinant for the i-th integrarion point.
        
        Parameters
        ----------

        int_point: int
            The integration point to be evaluated.

        coords:  np.ndarray
            A three-dimensional coordinate matrix in which each plane contains
            the nodal coordinates of an element. 

        Return
        ------
        det_jac: np.ndarray
            A stacked vector with the Jacobian determinant of all elements evaluated
            at the i-th integration point.

        """

        # stacked Jacobian matrix
        jac = self.dphi_M[int_point, 0, :] @ coords

        # calculate the stacked Jacobian determinants
        det_jac = np.linalg.norm(jac, axis=1)

        return det_jac


    def integrate_distributed_load(self, el_index: int, distributed_load: np.ndarray) -> np.ndarray:
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
        for i in range(self.nint_M):

            # determinant of Jacobian for the i-th integration point
            det_jac = self.get_jacobian_determinant(i, coords)

            # matrix of shape functions for all DOF
            N = self.N_matrix[i, :, :]

            Fe += (N.T @ distributed_load) * (det_jac * self.wps_M[i])

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
        for i in range(self.nint_M):

            # determinant of Jacobian for the i-th integration point
            det_jac = self.get_jacobian_determinant(i, coords)

            # matrix of shape functions for all DOF
            N = self.N_matrix[i, :, :]

            Me += (N.T @ N) * distributed_mass * (det_jac * self.wps_M[i])

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