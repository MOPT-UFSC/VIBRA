from typing import TYPE_CHECKING

from vibra.engine.elements.elements_1d.line2_element import LINE_2

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class ACT_LINE_2(LINE_2):

    def __init__(self, model: "Model", dof_per_node: int = 1):
        super().__init__(model, dof_per_node)

        self.model = model
        self.local_dof = np.arange(dof_per_node, dtype=int)

        self.connectivities = None
        self.element_label = "acoustic_line_2"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates


    def get_rows_and_cols_indices_1D(self, index: int):
        """
        This method returns, for a selected element, the row 
        and column indices for 1D element integration.
        
        index: int
            The element index.
        """

        dof = self.dof_per_node
        elem_nodes = self.connectivities[index, :]
        _elem_nodes = self.model.fluid_node_mapping[elem_nodes]
        dof_indices = dof * _elem_nodes + self.local_dof
        return dof_indices


    def get_rows_and_cols_indices_2D(self, connectivities: np.ndarray):
        """
        This method returns the row and column indices for 2D element 
        integration for all elements related to the connectivities.
        
        connectivities: np.ndarray
            A 2D array containing all element connectivities.
        """

        self.reorder_connect(connectivities)

        n_el = len(connectivities)
        dof, edof = self.dof_per_node, self.dof_per_element

        ind_dof = np.zeros((n_el, edof), dtype=int)

        for j in range(self.nodes_per_element):
            start = j * dof
            end = (j + 1) * dof
            elem_nodes = self.model.fluid_node_mapping[self.connectivities[:, j]]
            ind_dof[:, start : end] = dof * elem_nodes.reshape(-1, 1) + self.local_dof

        vect_indices = ind_dof.flatten()
        ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        ind_cols = (np.tile(ind_dof, edof)).flatten()

        return ind_rows, ind_cols