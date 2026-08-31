
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.acoustic.acoustic_2d_element import ACOUSTIC_2D_ELEMENT
from vibra.engine.elements.elements_2d.quad8_element import QUADRANGLE_8

if TYPE_CHECKING:
    from vibra.engine.model import Model


class ACT_QUADRANGLE_8(ACOUSTIC_2D_ELEMENT, QUADRANGLE_8):

    def __init__(self, model: "Model", dof_per_node: int = 1, nodes_per_element: int = 8):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "acoustic_quadrangular_8"