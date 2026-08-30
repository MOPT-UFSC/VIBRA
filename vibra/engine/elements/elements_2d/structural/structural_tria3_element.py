
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.structural.structural_2d_element import STRUCTURAL_2D_ELEMENT
from vibra.engine.elements.elements_2d.tria3_element import TRIANGLE_3

if TYPE_CHECKING:
    from vibra.engine.model import Model


class STRUCT_TRIANGLE_3(STRUCTURAL_2D_ELEMENT, TRIANGLE_3):

    def __init__(self, model: "Model", dof_per_node: int = 3, nodes_per_element: int = 3):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "structural_triangular_3"