from typing import TYPE_CHECKING

from vibra.engine.elements.elements_1d.line3_element import Line3
from vibra.engine.elements.elements_1d.structural.structural_1d_element import Structural1DElement

if TYPE_CHECKING:
    from vibra.engine.model import Model


class StructuralLine3(Structural1DElement, Line3):

    def __init__(self, model: "Model", dof_per_node: int = 3, nodes_per_element: int = 3):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "structural_line_3"