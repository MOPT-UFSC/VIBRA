from typing import TYPE_CHECKING

from vibra.engine.elements.elements_3d.structural.structural_3d_element import STRUCTURAL_3D_ELEMENT
from vibra.engine.elements.elements_3d.tet10_element import TETRAHEDRON_10

if TYPE_CHECKING:
    from vibra.engine.model import Model


class STRUCT_TETRAHEDRON_10(STRUCTURAL_3D_ELEMENT, TETRAHEDRON_10):

    def __init__(self, model: "Model", dof_per_node: int = 3, nodes_per_element: int = 10):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "structural_tetrahedron_10"

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()
        self.process_N_matrix()