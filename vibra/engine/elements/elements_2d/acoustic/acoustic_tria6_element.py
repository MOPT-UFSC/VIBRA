
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.acoustic.acoustic_2d_element import ACOUSTIC_2D_ELEMENT
from vibra.engine.elements.elements_2d.tria6_element import TRIANGLE_6

if TYPE_CHECKING:
    from vibra.engine.model import Model


class ACT_TRIANGLE_6(ACOUSTIC_2D_ELEMENT, TRIANGLE_6):

    def __init__(self, model: "Model", dof_per_node: int = 1, nodes_per_element: int = 6):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "acoustic_triangular_6"