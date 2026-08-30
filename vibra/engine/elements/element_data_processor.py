

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


def get_jacobian_determinant_2d(int_point: int, dphi: np.ndarray, coords: np.ndarray, return_vectors: bool = False):
    """
    This method evaluates the Jacobian determinant for the i-th integrarion point.
    
    Parameters
    ----------

    int_point: int
        The integration point to be evaluated.

    coords:  np.ndarray
        A three-dimensional coordinate matrix of the element. 

    return_vectors: bool, optional
        Use this argument to control when the normal unitary, g_xi and g_eta vectors are returned.

    Return
    ------
    det_jac: np.ndarray
        The Jacobian determinant at the i-th integration point.

    normal_vector: np.ndarray,  optional
        The unitary normal vectors at the i-th integration point
        (returned if the return_vectors argument is True).

    g_xi: np.ndarray,  optional
        The tangent vector in xi direction at the i-th integration point
        (returned if the return_vectors argument is True).

    g_eta: np.ndarray,  optional
        The tangent vector in eta direction at the i-th integration point
        (returned if the return_vectors argument is True).

    """

    multiple_elements = len(coords.shape) == 3

    # vectors tangent to the element's surface
    g_xi = dphi[int_point, 0, :] @ coords
    g_eta = dphi[int_point, 1, :] @ coords

    # compute the normal vector(s) for the i-th integration point
    normal_vector = np.cross(g_xi, g_eta)

    # determinant of Jacobian matrix
    if multiple_elements:
        det_jac = np.linalg.norm(normal_vector, axis=1).reshape(-1, 1, 1)
    else:
        normal_vector = normal_vector.reshape(-1, 1)
        det_jac = np.linalg.norm(normal_vector)

    if not return_vectors:
        return det_jac

    # normalize the element(s) normal vector(s) for the i-th integration point
    if multiple_elements:
        e_normal = normal_vector.reshape(-1, 3, 1) / det_jac.reshape(-1, 1, 1)
    else:
        e_normal = normal_vector / det_jac

    return det_jac, e_normal, g_xi, g_eta


def get_jacobian_determinant_1d(int_point: int, dphi: np.ndarray, coords: np.ndarray):
    """
    This method evaluates the Jacobian determinant for the i-th integrarion point.
    
    Parameters
    ----------

    int_point: int
        The integration point to be evaluated.

    coords:  np.ndarray
        A three-dimensional coordinate matrix of the element. 

    Return
    ------
    det_jac: np.ndarray
        The Jacobian determinant at the i-th integration point.

    """

    multiple_elements = len(coords.shape) == 3

    # Jacobian matrix
    jac = dphi[int_point, 0, :] @ coords

    # determinant of Jacobian matrix
    if multiple_elements:
        det_jac = np.linalg.norm(jac, axis=1)
    else:
        det_jac = np.linalg.norm(jac).reshape(-1, 1)

    return det_jac