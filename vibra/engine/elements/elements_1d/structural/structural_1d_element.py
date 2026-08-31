from typing import TYPE_CHECKING

from vibra.engine.elements.line_elements import Element1D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class STRUCTURAL_1D_ELEMENT(Element1D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = ""
        self.connectivities = None

        self.process_N_matrix()
        self.dof_indexes_proc = self.dof_indexes_processor("structural")


    def process_N_matrix(self):
        N = np.zeros((self.nint_M, 3, self.dof_per_element), dtype=float)

        for i in range(self.nint_M):
            N[i, 0, 0::3] = self.phi_M[i, :]
            N[i, 1, 1::3] = self.phi_M[i, :]
            N[i, 2, 2::3] = self.phi_M[i, :]

        self.N_matrix = N


    def integrate_length(self, connectivities: np.ndarray):

        self.connectivities = connectivities

        # stack the element nodes coordinates for all elements
        coords = self.model.mesh.nodal_coordinates[[connect for connect in connectivities], 1:]

        # initialize variable
        dL = 0.

        # integration loop
        for i in range(self.nint_M):

            det_jacs = self.get_jacobian_determinant_1d(i, self.dphi_M, coords)

            # integrate all elementary areas
            dL += det_jacs * self.wps_M[i]

        return np.sum(dL)


    def integrate_distributed_load(self, el_index: int, distributed_load: np.ndarray) -> np.ndarray:
        """ 
        This method computes the elementary load vector.

        Parameters
        ----------
        el_index: int
            The element index.

        distributed_load: float, optional
            The load vector.

        Returns
        -------
        Fe: np.ndarray
            The elementary load vector.
        """

        # element nodes
        e_nodes = self.connectivities[el_index, :]

        # element nodal coordinates
        coords = self.model.mesh.nodal_coordinates[e_nodes, 1:]

        # initialize the variable Fe
        Fe = 0.

        # integration loop
        for i in range(self.nint_M):

            # determinant of Jacobian for the i-th integration point
            det_jac = self.get_jacobian_determinant_1d(i, self.dphi_M, coords)

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
        coords = self.model.mesh.nodal_coordinates[e_nodes, 1:]

        # initialize the variable Fe
        Me = 0.

        # integration loop
        for i in range(self.nint_M):

            # determinant of Jacobian for the i-th integration point
            det_jac = self.get_jacobian_determinant_1d(i, self.dphi_M, coords)

            # matrix of shape functions for all DOF
            N = self.N_matrix[i, :, :]

            Me += (N.T @ N) * distributed_mass * (det_jac * self.wps_M[i])

        return Me


    def get_rows_and_cols_indices_1D(self, index: int):
        """
        This method returns, for a selected element, the row 
        and column indices for 1D element integration.
        
        index: int
            The element index.
        """

        return self.dof_indexes_proc.get_rows_and_cols_indices_1D(index, self.connectivities)


    def get_rows_and_cols_indices_2D(self, connectivities: np.ndarray):
        """
        This method returns the row and column indices for 2D element 
        integration for all elements related to the connectivities.
        
        connectivities: np.ndarray
            A 2D array containing all element connectivities.
        """

        self.reorder_connect(connectivities)

        return self.dof_indexes_proc.get_rows_and_cols_indices_2D(self.connectivities)