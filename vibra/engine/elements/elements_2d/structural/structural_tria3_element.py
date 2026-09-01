
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.structural.structural_2d_element import Structural2DElement
from vibra.engine.elements.elements_2d.tria3_element import Triangle_3

if TYPE_CHECKING:
    from vibra.engine.model import Model


class StructuralTriangle3(Structural2DElement, Triangle_3):

    def __init__(self, model: "Model", dof_per_node: int = 3, nodes_per_element: int = 3):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "structural_triangular_3"