
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_3d.hex20_element import Hexahedron20

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class Pyramid13(Hexahedron20):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    @property
    def corner_nodes_indices(self):
        return np.arange(5, dtype=int)


    @property
    def midside_nodes_indices_map(self):
        return {
            5 : (0, 1),     # N -> (I, J)
            6 : (1, 2),     # O -> (J, K)
            7 : (2, 3),     # P -> (K, L)
            8 : (3, 0),     # Q -> (L, I)
            9 : (0, 4),     # R -> (I, M)
            10 : (1, 4),    # S -> (J, M)
            11 : (2, 4),    # T -> (K, M)
            12 : (3, 4),    # U -> (L, M)
            }


    def reorder_connect(self):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """

        # GMSH nodes ordering -> [0, 1, 2, 3, 4, 5, 8, 10, 6, 7, 9, 11, 12]
        self.connectivities = self.model.mesh.solids_connectivity[
            :, [4, 5, 6, 7, 8, 8, 8, 8, 9, 12, 14, 10, 8, 8, 8, 8, 11, 13, 15, 16]
            ]