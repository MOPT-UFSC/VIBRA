
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.acoustic.acoustic_2d_element import Acoustic2DElement
from vibra.engine.elements.elements_2d.quad4_element import Quadrangle4

if TYPE_CHECKING:
    from vibra.engine.model import Model


class AcousticQuadrangle4(Acoustic2DElement, Quadrangle4):

    def __init__(self, model: "Model", dof_per_node: int = 1, nodes_per_element: int = 4):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "acoustic_quadrangular_4"