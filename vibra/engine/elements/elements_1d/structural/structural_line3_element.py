from typing import TYPE_CHECKING

from vibra.engine.elements.elements_1d.line3_element import LINE_3, get_local_coordinates

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class STRUCT_LINE_3(LINE_3):

    def __init__(self, model: "Model", dof_per_node: int = 3):
        super().__init__(model, dof_per_node)

        self.model = model

        self.connectivities = None
        self.element_label = "structural_line_3"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates


    def integrate_length(self, connectivities: np.ndarray):

        self.connectivities = connectivities
        
        # compute local coordinates for all elements
        coords_lcs = self.get_stacked_local_coordinates()

        # initialize variable
        dL = 0.

        # integration loop
        for i in range(self.nint_M):

            # calculate the Jacobian
            jacs = self.dphi_M[i, :, :] @ coords_lcs

            # calculate the determinant of the Jacobian
            det_jacs = np.abs(jacs)

            dL += (det_jacs * self.wps_M[i])    

        return np.sum(dL)


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
        coords = self.nodal_coordinates[e_nodes, :]

        # nodal coordinates in the local CS
        coord_lcs = get_local_coordinates(coords)

        # initialize the shape functions matrix
        N = np.zeros((3, self.dof_per_element), dtype=float)

        # initialize the variable Fe
        Fe = 0.

        # integration loop
        for i in range(self.nint_M):

            # Jacobian matrix
            JAC = self.dphi_M[i, :, :] @ coord_lcs

            # determinant of Jacobia matrix
            det_JAC = np.abs(JAC)

            # populate the shape functions matrix
            N[0, 0::3] = self.phi_M[i, :, :]
            N[1, 1::3] = self.phi_M[i, :, :]
            N[2, 2::3] = self.phi_M[i, :, :]

            Fe += (N.T @ distributed_load) * (det_JAC * self.wps_M[i])

        return Fe


    def integrate_distributed_mass(self, el_index: int, distributed_mass: float) -> np.ndarray:
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
        for i in range(self.nint_M):

            # determinant of Jacobia matrix
            det_jacs_M = self.dphi_M[i, :, :] @ coord_lcs

            # populate the shape functions matrix
            N[0, 0::3] = self.phi_M[i, :, :]
            N[1, 1::3] = self.phi_M[i, :, :]
            N[2, 2::3] = self.phi_M[i, :, :]

            Me += (N.T @ N) * distributed_mass * (det_jacs_M * self.wps_M[i])

        return Me


    def get_load_indexes(self, index: int):
        node_ids = self.connectivities[index, :]
        element_dofs = self.dof_per_node * node_ids.reshape(-1, 1) + np.arange(self.dof_per_node, dtype=int)
        return element_dofs.flatten()


    def get_element_rows_and_columns_indexes(self):

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