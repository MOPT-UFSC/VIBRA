
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.structural.structural_2d_element import Structural2DElement
from vibra.engine.elements.elements_2d.tria6_element import Triangle_6

if TYPE_CHECKING:
    from vibra.engine.model import Model


class StructTriangle_6(Structural2DElement, Triangle_6):

    def __init__(self, model: "Model", dof_per_node: int = 3, nodes_per_element: int = 6):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "structural_triangular_6"

        self.define_integration_points(integration_points=6)
        self.process_shape_functions_and_derivatives()