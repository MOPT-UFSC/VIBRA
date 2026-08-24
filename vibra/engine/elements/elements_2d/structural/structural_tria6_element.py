
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.tria6_element import TRIANGLE_6, get_local_coordinates

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class STRUCT_TRIANGLE_6(TRIANGLE_6):

    def __init__(self, model: "Model", dof_per_node: int = 3):
        super().__init__(model, dof_per_node)

        self.model = model

        self.connectivities = None
        self.element_label = "structural_triangular_6"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates

        self.define_integration_points(integration_points=6)
        self.process_shape_functions_and_derivatives()

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

        # integration loop
        for i in range(self.nint):

            # determinant of Jacobian for the i-th integration point
            det_jac = self.get_jacobian_determinant(i, coords)

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


    ## NOTE: to be removed

    def integrate_area_old(self, connectivities: np.ndarray):

        self.connectivities = connectivities
        
        # compute local coordinates for all elements
        local_coords = self.get_stacked_local_coordinates()

        # initialize variable
        dA = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrices of all elements
            JAC_stacked = self.dphi[i, :, :] @ local_coords

            # Jacobian determinants and inverses of all elements
            det_jacs, _ = self.get_detJAC_and_invJAC(JAC_stacked)

            dA +=  det_jacs * self.wps[i]

        return np.sum(dA)


    def integrate_normal_pressure_load_old(self, el_index: int, e_normal: np.ndarray,  normal_pressure: np.ndarray) -> np.ndarray:
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
        coords = self.nodal_coordinates[e_nodes, :]

        # nodal coordinates in the local CS
        coord_lcs = get_local_coordinates(coords)

        # initialize the shape functions matrix
        N = np.zeros((3, self.dof_per_element), dtype=float)

        # initialize the variable Fe
        Fe = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrix
            JAC = self.dphi[i, :, :] @ coord_lcs

            # determinant of Jacobian matrix
            det_JAC = self.get_detJAC(JAC)

            # populate the shape functions matrix
            N[0, 0::3] = self.phi[i, :, :]
            N[1, 1::3] = self.phi[i, :, :]
            N[2, 2::3] = self.phi[i, :, :]

            # the negative value of the normal is used to point the normal toward the interior of the domain.
            Fe += (N.T @ (-e_normal @ normal_pressure)) * (det_JAC * self.wps[i])

        return Fe


    def integrate_distributed_mass_old(self, el_index: int, distributed_mass: float) -> np.ndarray:
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
        coords = self.nodal_coordinates[e_nodes, :]

        # nodal coordinates in the local CS
        coord_lcs = get_local_coordinates(coords)

        # initialize the shape functions matrix
        N = np.zeros((3, self.dof_per_element), dtype=float)

        # initialize the variable Fe
        Me = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrix
            JAC = self.dphi[i, :, :] @ coord_lcs

            # determinant of Jacobian matrix
            det_JAC = self.get_detJAC(JAC)

            # populate the shape functions matrix
            N[0, 0::3] = self.phi[i, :, :]
            N[1, 1::3] = self.phi[i, :, :]
            N[2, 2::3] = self.phi[i, :, :]

            Me += (N.T @ N) * distributed_mass * (det_JAC * self.wps[i])

        return Me