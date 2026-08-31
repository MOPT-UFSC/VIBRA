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
        self.local_dof = np.arange(dof_per_node, dtype=int)


    def initialize(self):

        self.nint: np.ndarray | None = None
        self.nint_M: np.ndarray | None = None
        self.nint_K: np.ndarray | None = None

        self.wps: np.ndarray | None = None
        self.wps_M: np.ndarray | None = None
        self.wps_K: np.ndarray | None = None

        self.phi: np.ndarray | None = None
        self.phi_M: np.ndarray | None = None
        self.phi_K: np.ndarray | None = None

        self.dphi: np.ndarray | None = None
        self.dphi_M: np.ndarray | None = None
        self.dphi_K: np.ndarray | None = None


    @property
    def dof_per_element(self):
        return self.dof_per_node * self.nodes_per_element


    def dof_indexes_processor(self, domain: str) -> DOFIndexesProcessor:
        return DOFIndexesProcessor(self.model, domain, self.dof_per_node, self.nodes_per_element)


    def reorder_connect(self, connectivities: np.ndarray):
        pass


    def elementary_matrices(self) -> tuple[np.ndarray]:
        raise NotImplementedError("The function elementary_matrices was not implemented")


    def get_jacobian_determinant_1d(self, int_point: int, dphi: np.ndarray, coords: np.ndarray):
        return get_jacobian_determinant_1d(int_point, dphi, coords)