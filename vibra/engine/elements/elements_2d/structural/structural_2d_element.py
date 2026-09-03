
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.surface_elements import Element2D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class Structural2DElement(Element2D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.local_dof = np.arange(dof_per_node, dtype=int)

        self.element_label = ""
        self.connectivities = None

        self.process_N_matrix()
        self.dof_indexes_proc = self.dof_indexes_processor("structural")


    def process_N_matrix(self):
        N = np.zeros((self.nint, 3, self.dof_per_element), dtype=float)

        for i in range(self.nint):
            N[i, 0, 0::3] = self.phi[i, :]
            N[i, 1, 1::3] = self.phi[i, :]
            N[i, 2, 2::3] = self.phi[i, :]

        self.N_matrix = N


    def integrate_area(self, connectivities: np.ndarray):

        self.connectivities = connectivities

        # stack the element nodes coordinates for all elements
        coords = self.model.mesh.nodal_coordinates[[connect for connect in connectivities], 1:]

        # initialize variable
        dA = 0.

        # integration loop
        for i in range(self.nint):

            # determinant of Jacobian for the i-th integration point
            det_jacs = self.get_jacobian_determinant_2d(self.dphi[i, :, :], coords)

            # integrate all elementary areas
            dA += det_jacs * self.wps[i]

        return np.sum(dA)


    def integrate_normal_pressure_load(self, el_index: int, element_pressures: np.ndarray) -> np.ndarray:
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
        coords = self.model.mesh.nodal_coordinates[e_nodes, 1:]

        # initialize the variable Fe
        Fe = 0.

        # integration loop
        for i in range(self.nint):

            # determinant of Jacobian and normal vector for the i-th integration point
            det_jac, normal_vector = self.get_jacobian_determinant_2d(self.dphi[i, :, :], coords, return_normal=True)

            # vector of shape functions (structural dofs)
            N = self.N_matrix[i, :, :]

            # vector of shape functions (acoustic dofs)
            N_act = self.phi[i, :].reshape(1, -1)

            #
            Pe = N_act @ element_pressures

            # the negative value of the normal is used to point the normal toward the interior of the domain.
            Fe += (N.T @ (-normal_vector @ Pe)) * (det_jac * self.wps[i])

        return Fe


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
        for i in range(self.nint):

            # determinant of Jacobian for the i-th integration point
            det_jac = self.get_jacobian_determinant_2d(self.dphi[i, :, :], coords)

            # matrix of shape functions for all DOF
            N = self.N_matrix[i, :, :]

            Fe += (N.T @ distributed_load) * (det_jac * self.wps[i])

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
        for i in range(self.nint):

            # determinant of Jacobian for the i-th integration point
            det_jac = self.get_jacobian_determinant_2d(self.dphi[i, :, :], coords)

            # matrix of shape functions for all DOF
            N = self.N_matrix[i, :, :]

            Me += (N.T @ N) * distributed_mass * (det_jac * self.wps[i])

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