
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.quad8_element import Quadrangle8
from vibra.engine.elements.elements_2d.structural.structural_2d_element import Structural2DElement

if TYPE_CHECKING:
    from vibra.engine.model import Model


class StructQuadrangle8(Structural2DElement, Quadrangle8):

    def __init__(self, model: "Model", dof_per_node: int = 3, nodes_per_element: int = 8):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "structural_quadrangle_8"