from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from vibra.engine.model import Model


class DOFIndexesProcessor:
    def __init__(self, model: "Model", domain: str, dof_per_node: int, nodes_per_element: int):

        self.model = model
        self.domain = domain
        self.dof_per_node = dof_per_node
        self.nodes_per_element = nodes_per_element
        self.dof_per_element = dof_per_node * nodes_per_element
        self.local_dof = np.arange(dof_per_node, dtype=int)


    @property
    def dofs_shift(self):
        return self.model.domains_processor.get_dofs_offset(self.domain)


    def get_rows_and_cols_indices_1D(
            self,
            index: int,
            connectivities: np.ndarray,
            ):
        """
        This method returns, for a selected element, the row 
        and column indices for 1D element integration.
        
        index: int
            The element index.
        """

        dof = self.dof_per_node
        elem_nodes = connectivities[index, :]
        _elem_nodes = self.model.get_mapped_nodes(elem_nodes, self.domain)

        dof_indices = dof * _elem_nodes.reshape(-1, 1) + self.local_dof + self.dofs_shift

        return dof_indices.flatten()


    def get_rows_and_cols_indices_2D(
            self,
            connectivities: np.ndarray,
            ):
        """
        This method returns the row and column indices for 2D element 
        integration for all elements related to the connectivities.
        
        connectivities: np.ndarray
            A 2D array containing all element connectivities.
        """

        dof = self.dof_per_node
        edof = self.dof_per_element

        n_el = len(connectivities)
        ind_dof = np.zeros((n_el, edof), dtype=int)

        for j in range(self.nodes_per_element):
            start = j * dof
            end = (j + 1) * dof
            _elem_nodes = self.model.get_mapped_nodes(connectivities[:, j], self.domain)
            ind_dof[:, start : end] = dof * _elem_nodes.reshape(-1, 1) + self.local_dof

        ind_dof += self.dofs_shift

        vect_indices = ind_dof.flatten()
        ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        ind_cols = (np.tile(ind_dof, edof)).flatten()

        return ind_rows, ind_cols


    def get_rows_and_cols_indices_3D(
            self,
            connectivities: np.ndarray,
            ):
        """ 
        This method processess the dof indices (rows and columns) 
        for assembly
        """

        # filter the acoustic elements connectivities
        element_ids = self.model.domains_processor.elements_of_domain.get(self.domain, [])
        reduced_connect = connectivities[element_ids, :]

        dof = self.dof_per_node
        edof = self.dof_per_element

        n_el = len(element_ids)
        ind_dof = np.zeros((n_el, edof), dtype=int)

        for j in range(self.nodes_per_element):
            start = j * dof
            end = (j + 1) * dof
            _elem_nodes = self.model.get_mapped_nodes(reduced_connect[:, j], self.domain)

            ind_dof[:, start : end] = dof * _elem_nodes.reshape(-1, 1) + self.local_dof

        ind_dof += self.dofs_shift

        vect_indices = ind_dof.flatten()
        ordered_dofs = np.unique(vect_indices)

        ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        ind_cols = (np.tile(ind_dof, edof)).flatten()

        return ind_rows, ind_cols, ordered_dofs