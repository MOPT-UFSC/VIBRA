

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from vibra.engine.model import Model


class ElementDataProcessor:
    def __init__(self, model: "Model", domain: str, dof_per_node: int, nodes_per_element: int):
        self.model = model
        self.domain = domain
        self.dof_per_node = dof_per_node
        self.nodes_per_element = nodes_per_element
        self.dof_per_element = dof_per_node * nodes_per_element


    def get_stacked_nodal_coords(self, connectivities: np.ndarray) -> np.ndarray:
        """
        This method returns the nodal coordinates of all elements in form 
        of a 3D matrix. Each plane of this matrix contains the nodal 
        coordiantes from all nodes relative to the i-th element.

        Returns
        -------
        stacked_coords: np.ndarray
            A tridimensional matrix containing the nodal 
            coordinates of all elements.

        """

        # filter the elements connectivities
        element_ids = self.model.elements_per_domain.get(self.domain, [])
        reduced_connect = connectivities[element_ids, :]

        nel = len(reduced_connect)

        stacked_coords = np.zeros((nel, self.dof_per_element, 3), dtype=float)
        for j in range(self.dof_per_element):
            stacked_coords[:, j, :] = self.model.mesh.nodal_coordinates[reduced_connect[:, j], 1:4]

        return stacked_coords