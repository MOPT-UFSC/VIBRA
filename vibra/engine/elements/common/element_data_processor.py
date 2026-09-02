

from typing import TYPE_CHECKING

import numpy as np

from vibra.engine.elements.common.matrix_utils import get_2x2_matrix_inverse

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


def get_jacobian_determinant_2d(
        dphi: np.ndarray, 
        coords: np.ndarray, 
        return_normal: bool = False, 
        return_inverse: bool = False,
        ):
    """
    This method evaluates the Jacobian determinant for the i-th integration point.
    
    Parameters
    ----------
    coords:  np.ndarray
        A three-dimensional coordinate matrix of the element. 

    return_normal: bool, optional
        Use this argument to control when the element normal vector will be returned.

    return_inverse: bool, optional
        Use this argument to control when the inverse of Jacobian matrix will be returned.

    Return
    ------
    det_jac: np.ndarray
        The Jacobian determinant at the i-th integration point.

    return_normal: np.ndarray
        The unitary normal vectors at the i-th integration point.

    inv_jac: np.ndarray, optional
        The inverse of Jacobian matrix at the i-th integration point
        (returned if the return_inverse argument is True).

    """

    multiple_elements = len(coords.shape) == 3

    # vectors tangent to the element's surface
    g_xi = dphi[0, :] @ coords
    g_eta = dphi[1, :] @ coords

    # compute the normal vector(s) for the i-th integration point
    normal_vector = np.cross(g_xi, g_eta)

    # calculate the determinant of Jacobian and the normal vector z' for the i-th integration point
    if multiple_elements:
        det_jac = np.linalg.norm(normal_vector, axis=1).reshape(-1, 1, 1)
        e_3 = normal_vector.reshape(-1, 3, 1) / det_jac.reshape(-1, 1, 1)

    else:
        normal_vector = normal_vector.reshape(-1, 1)
        det_jac = np.linalg.norm(normal_vector)
        e_3 = normal_vector / det_jac

    if return_normal:
        return det_jac, e_3

    if not return_inverse:
        return det_jac

    # calculate the x' vector
    if multiple_elements:
        e_1 = g_xi.reshape(-1, 3, 1) / np.linalg.norm(g_xi).reshape(-1, 1, 1)
    else:
        e_1 = g_xi / np.linalg.norm(g_xi)

    # calculate the y' vector
    e_2 = np.cross(e_3, e_1, axis=1)

    # Jacobian matrix
    jac = dphi @ coords

    if multiple_elements:
        dir = np.zeros((coords.shape[0], 3, 2), dtype=float)
        dir[:, :, 0] = e_1.reshape(-1, 3)
        dir[:, :, 1] = e_2.reshape(-1, 3)
    else:
        dir = np.array([e_1, e_2], dtype=float).T

    # compute the plane Jacobian
    jac_2d = jac @ dir

    # finally, calculate the inverse of plane Jacobian
    inv_jac_2d, _ = get_2x2_matrix_inverse(jac_2d)

    return det_jac, inv_jac_2d


def get_jacobian_determinant_1d(dphi: np.ndarray, coords: np.ndarray):
    """
    This method evaluates the Jacobian determinant for the i-th integration point.
    
    Parameters
    ----------
    coords:  np.ndarray
        A three-dimensional coordinate matrix of the element. 

    Return
    ------
    det_jac: np.ndarray
        The Jacobian determinant at the i-th integration point.

    """

    multiple_elements = len(coords.shape) == 3

    # Jacobian matrix
    jac = dphi[0, :] @ coords

    # determinant of Jacobian matrix
    if multiple_elements:
        det_jac = np.linalg.norm(jac, axis=1)
    else:
        det_jac = np.linalg.norm(jac).reshape(-1, 1)

    return det_jac