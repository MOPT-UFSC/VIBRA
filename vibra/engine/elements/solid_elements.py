from dataclasses import dataclass

import numpy as np


class Element3D:
    """
    This determines the attributes and methods
    that need to exist in EVERY element.
    """

    # Constants of the element
    NODES_PER_ELEMENT: int = 0
    DOFS_PER_NODE: int = 0
    DOFS_PER_ELEMENT: int = NODES_PER_ELEMENT * DOFS_PER_NODE

    def elementary_matrices(self) -> tuple[np.ndarray]:
        raise NotImplementedError("The function elementary_matrices was not implemented")

    # def generate_ind_rows_cols(self):
    #     """
    #     Processes the indexes (rows and columns) of the element
    #     that will be used in the assembler.
    #     """
    #     self.reorder_connect()
    #     dofs, edofs = self.DOF_PER_NODE, self.DOFS_PER_ELEMENT
    #     ind_dofs = dofs * self.connectivity[:, 1:]

    #     vect_indices = ind_dofs.flatten()
    #     self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
    #     self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

    #     return self.ind_rows, self.ind_cols
