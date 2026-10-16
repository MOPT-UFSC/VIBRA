from typing import TYPE_CHECKING

from vibra.engine.elements.elements_1d.acoustic.acoustic_1d_element import Acoustic1DElement
from vibra.engine.elements.elements_1d.line3_element import Line3

if TYPE_CHECKING:
    from vibra.engine.model import Model


class AcousticLine3(Acoustic1DElement, Line3):

    def __init__(self, model: "Model", dof_per_node: int = 1, nodes_per_element: int = 3):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "acoustic_line_3"