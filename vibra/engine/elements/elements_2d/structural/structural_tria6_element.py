
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.structural.structural_2d_element import STRUCTURAL_2D_ELEMENT
from vibra.engine.elements.elements_2d.tria6_element import TRIANGLE_6

if TYPE_CHECKING:
    from vibra.engine.model import Model


class STRUCT_TRIANGLE_6(STRUCTURAL_2D_ELEMENT, TRIANGLE_6):

    def __init__(self, model: "Model", dof_per_node: int = 3, nodes_per_element: int = 6):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = "structural_triangular_6"

        self.define_integration_points(integration_points=6)
        self.process_shape_functions_and_derivatives()


    # def get_N_matrix(self):
    #     N = np.zeros((self.nint, 3, self.dof_per_element), dtype=float)

    #     for i in range(self.nint):
    #         N[i, 0, 0::3] = self.phi[i, :, :]
    #         N[i, 1, 1::3] = self.phi[i, :, :]
    #         N[i, 2, 2::3] = self.phi[i, :, :]

    #     return N


    # def integrate_area(self, connectivities: np.ndarray):

    #     self.connectivities = connectivities

    #     # stack the element nodes coordinates for all elements
    #     coords = self.nodal_coordinates[[connect for connect in connectivities], 1:]

    #     # initialize variable
    #     dA = 0.

    #     # integration loop
    #     for i in range(self.nint):

    #         det_jacs = self.get_jacobian_determinant_2d(i, self.dphi, coords)

    #         # integrate all elementary areas
    #         dA += det_jacs * self.wps[i]

    #     return np.sum(dA)


    # def integrate_normal_pressure_load(self, el_index: int, e_normal: np.ndarray,  normal_pressure: np.ndarray) -> np.ndarray:
    #     """ 
    #     This method computes the elementary load vector.

    #     Parameters
    #     ----------
    #     el_index: int
    #         The element index.

    #     load: float, optional
    #         The load vector.

    #     Returns
    #     -------
    #     Fe: np.ndarray
    #         The elementary load vector.
    #     """

    #     # element nodes
    #     e_nodes = self.connectivities[el_index, :]

    #     # element nodal coordinates
    #     coords = self.nodal_coordinates[e_nodes, 1:]

    #     # initialize the variable Fe
    #     Fe = 0.

    #     # integration loop
    #     for i in range(self.nint):

    #         # determinant of Jacobian and normal vector for the i-th integration point
    #         det_jac, normal_vector, *_ = self.get_jacobian_determinant_2d(i, coords, self.dphi, return_vectors=True)

    #         # matrix of shape functions for all DOF
    #         N = self.N_matrix[i, :, :]

    #         # the negative value of the normal is used to point the normal toward the interior of the domain.
    #         Fe += (N.T @ (-normal_vector @ normal_pressure)) * (det_jac * self.wps[i])

    #     return Fe


    # def integrate_distributed_load(self, el_index: int, distributed_load: np.ndarray) -> np.ndarray:
    #     """ 
    #     This method computes the elementary load vector.

    #     Parameters
    #     ----------
    #     el_index: int
    #         The element index.

    #     distributed_load: float, optional
    #         The load vector.

    #     Returns
    #     -------
    #     Fe: np.ndarray
    #         The elementary load vector.
    #     """

    #     # element nodes
    #     e_nodes = self.connectivities[el_index, :]

    #     # element nodal coordinates
    #     coords = self.nodal_coordinates[e_nodes, 1:]

    #     # initialize the variable Fe
    #     Fe = 0.

    #     # integration loop
    #     for i in range(self.nint):

    #         # determinant of Jacobian for the i-th integration point
    #         det_jac = self.get_jacobian_determinant_2d(i, self.dphi, coords)

    #         # matrix of shape functions for all DOF
    #         N = self.N_matrix[i, :, :]

    #         Fe += (N.T @ distributed_load) * (det_jac * self.wps[i])

    #     return Fe


    # def integrate_distributed_mass(self, el_index: int, distributed_mass: float) -> np.ndarray:
    #     """ 
    #     This method computes the elementary load vector.

    #     Parameters
    #     ----------
    #     el_index: int
    #         The element index.

    #     distributed_mass: float
    #         The mass density in kg/m².

    #     Returns
    #     -------
    #     Me: np.ndarray
    #         The two-dimensional elementary consistent mass matrix.
    #     """

    #     # element nodes
    #     e_nodes = self.connectivities[el_index, :]

    #     # element nodal coordinates
    #     coords = self.nodal_coordinates[e_nodes, 1:]

    #     # initialize the variable Fe
    #     Me = 0.

    #     # integration loop
    #     for i in range(self.nint):

    #         # determinant of Jacobian for the i-th integration point
    #         det_jac = self.get_jacobian_determinant_2d(i, self.dphi, coords)

    #         # matrix of shape functions for all DOF
    #         N = self.N_matrix[i, :, :]

    #         Me += (N.T @ N) * distributed_mass * (det_jac * self.wps[i])

    #     return Me


    # def get_rows_and_cols_indices_1D(self, index: int):
    #     """
    #     This method returns, for a selected element, the row 
    #     and column indices for 1D element integration.
        
    #     index: int
    #         The element index.
    #     """

    #     return self.dof_indexes_proc.get_rows_and_cols_indices_1D(index, self.connectivities)


    # def get_rows_and_cols_indices_2D(self, connectivities: np.ndarray):
    #     """
    #     This method returns the row and column indices for 2D element 
    #     integration for all elements related to the connectivities.
        
    #     connectivities: np.ndarray
    #         A 2D array containing all element connectivities.
    #     """

    #     self.reorder_connect(connectivities)

    #     return self.dof_indexes_proc.get_rows_and_cols_indices_2D(self.connectivities)