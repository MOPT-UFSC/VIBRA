from typing import TYPE_CHECKING

from vibra.engine.elements.elements_1d.line3_element import LINE_3

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class ACT_LINE_3(LINE_3):

    def __init__(self, model: "Model", dof_per_node: int = 1):
        super().__init__(model, dof_per_node)

        self.model = model

        self.connectivities = None
        self.element_label = "acoustic_line_3"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates


    def generate_ind_rows_cols(self, connectivities: np.ndarray):
        """
        This method processess the dof indices (rows and columns) 
        for assembly.

        Parameter
        ---------
        connectivities: np.ndarray
            An array containing the lines connectivities.
        """
        self.reorder_connect(connectivities)
        dof, edof = self.dof_per_node, self.dof_per_element

        ind_dof = dof * self.connectivities[:, :]
        ind_dof_flat = ind_dof.flatten()

        ind_rows = ((np.tile(ind_dof_flat, (edof,1))).T).flatten()
        ind_cols = (np.tile(ind_dof, edof)).flatten()

        return ind_rows, ind_cols