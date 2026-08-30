from typing import TYPE_CHECKING

import numpy as np

from vibra.engine.elements.dof_indexes_processor import DOFIndexesProcessor
from vibra.engine.elements.element_data_processor import get_jacobian_determinant_1d

if TYPE_CHECKING:
    from vibra.engine.model import Model


class Element1D:
    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):
        self.model = model
        self.dof_per_node = dof_per_node
        self.nodes_per_element = nodes_per_element

        self.initialize()


    def initialize(self):
        self.nint = None
        self.nint_M = None
        self.nint_K = None

        self.wps = None
        self.wps_M = None
        self.wps_K = None

        self.phi = None
        self.phi_M = None
        self.phi_K = None

        self.dphi = None
        self.dphi_M = None
        self.dphi_K = None


    @property
    def dof_per_element(self):
        return self.dof_per_node * self.nodes_per_element


    def dof_indexes_processor(self, model: "Model",  domain: str) -> DOFIndexesProcessor:
        return DOFIndexesProcessor(model, domain, self.dof_per_node, self.nodes_per_element)


    def reorder_connect(self, connectivities: np.ndarray):
        pass


    def elementary_matrices(self) -> tuple[np.ndarray]:
        raise NotImplementedError("The function elementary_matrices was not implemented")


    def get_jacobian_determinant_1d(self, int_point: int, dphi: np.ndarray, coords: np.ndarray):
        return get_jacobian_determinant_1d(int_point, dphi, coords)