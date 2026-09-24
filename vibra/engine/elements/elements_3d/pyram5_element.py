
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_3d.hex8_element import Hexahedron8

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class Pyramid5(Hexahedron8):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):
        super().__init__(model, dof_per_node, nodes_per_element)
        
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    @property
    def corner_nodes_indices(self):
        return np.arange(5, dtype=int)


    def reorder_connect(self):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """
        self.connectivities = self.model.mesh.solids_connectivity[:, [4, 5, 6, 7, 8, 8, 8, 8]]