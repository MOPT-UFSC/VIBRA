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

        self.dof_indexes_proc = self.dof_indexes_processor(
            model,
            "acoustic",
            dof_per_node,
            self.nodes_per_element,
            )


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