from typing import TYPE_CHECKING

from vibra.engine.elements.line_elements import Element1D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class ACOUSTIC_1D_ELEMENT(Element1D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = ""
        self.connectivities = None

        self.dof_indexes_proc = self.dof_indexes_processor("acoustic")


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