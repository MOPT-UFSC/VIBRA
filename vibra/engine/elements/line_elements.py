from typing import TYPE_CHECKING

import numpy as np

from vibra.engine.elements.dof_indexes_processor import DOFIndexesProcessor

if TYPE_CHECKING:
    from vibra.engine.model import Model

class Element1D:
    """
    This determines the attributes and methods
    that need to exist in EVERY element.
    """

    # Constants of the element
    NODES_PER_ELEMENT: int = 0
    DOF_PER_NODE: int = 0
    DOF_PER_ELEMENT: int = NODES_PER_ELEMENT * DOF_PER_NODE


    def dof_indexes_processor(self, 
            model: "Model",
            domain: str,
            dof_per_node: int,
            nodes_per_element: int,
            ) -> DOFIndexesProcessor:
        return DOFIndexesProcessor(model, domain, dof_per_node, nodes_per_element)


    def elementary_matrices(self) -> tuple[np.ndarray]:
        raise NotImplementedError("The function elementary_matrices was not implemented")
