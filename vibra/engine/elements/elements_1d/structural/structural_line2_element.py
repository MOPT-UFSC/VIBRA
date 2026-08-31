from typing import TYPE_CHECKING

from vibra.engine.elements.elements_1d.line2_element import Line2
from vibra.engine.elements.elements_1d.structural.structural_1d_element import Structural1DElement

if TYPE_CHECKING:
    from vibra.engine.model import Model


class StructLine2(Structural1DElement, Line2):

    def __init__(self, model: "Model", dof_per_node: int = 3, nodes_per_element: int = 2):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "structural_line_2"