import numpy as np


class Element1D:
    """
    This determines the attributes and methods
    that need to exist in EVERY element.
    """

    # Constants of the element
    NODES_PER_ELEMENT: int = 0
    DOF_PER_NODE: int = 0
    DOF_PER_ELEMENT: int = NODES_PER_ELEMENT * DOF_PER_NODE

    def elementary_matrices(self) -> tuple[np.ndarray]:
        raise NotImplementedError("The function elementary_matrices was not implemented")
