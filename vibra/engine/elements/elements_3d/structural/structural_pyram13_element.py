from typing import TYPE_CHECKING

from vibra.engine.elements.elements_3d.pyram5_element import Pyramid5
from vibra.engine.elements.elements_3d.structural.structural_3d_element import Structural3DElement

if TYPE_CHECKING:
    from vibra.engine.model import Model


class StructuralPyramid5(Structural3DElement, Pyramid5):

    def __init__(self, model: "Model", dof_per_node: int = 3, nodes_per_element: int = 5):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "structural_pyramid_5"

        self.define_integration_points(4)
        self.process_shape_functions_and_derivatives()
        self.process_N_matrix()