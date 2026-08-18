
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.tria6_element import TRIANGLE_6, get_local_coordinates

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class STRUCT_TRIANGLE_6(TRIANGLE_6):

    def __init__(self, model: "Model", dof_per_node: int = 3):
        super().__init__(model, dof_per_node)

        self.model = model

        self.connectivities = None
        self.element_label = "structural_triangular_6"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def normal_pressure_load(self, e_normals: np.ndarray, normal_pressures: np.ndarray) -> np.ndarray:
        """ 
        This method computes the acoustic pressure loads over a surface.

        Parameters
        ----------
        e_normals: np.ndarray
            The stacked surface elements normals vectors.

        nodal_solution: np.ndarray
            The acoustic nodal_solution array.

        Returns
        -------
        acoustic_load: np.ndarray
            The acoustic presure loads integrated over a surface.
        """

        # # stack all elements nodal pressures 
        # pressures = np.array([normal_pressures @ np.ones() for node_ids in self.connectivities.T], dtype=complex)

        # stack the element normal pressures in format [n_el, DOFS_PER_ELEMENT, n_freq]
        # Pe = pressures.transpose(1, 0, 2)
        # Pe = normal_pressures.reshape(-1, 1, len(self.model.frequencies))
        Pe = normal_pressures.transpose(1, 0, 2)

        # compute local coordinates for all elements
        local_coords = self.get_stacked_local_coordinates()

        # initialize variable
        element_loads = 0.

        # Pn = Pe @ e_normals

        # integration loop
        for i in range(self.nint):

            # Jacobian matrices of all elements
            JAC_stacked = self.dphi[i, :, :] @ local_coords

            # Jacobian determinants and inverses of all elements
            det_jacs, _ = self.get_detJAC_and_invJAC(JAC_stacked)

            # shape functions
            N = np.zeros((3, self.dof_per_element), dtype=float)
            N[0, 0::3] = self.phi[i, :, :]
            N[1, 1::3] = self.phi[i, :, :]
            N[2, 2::3] = self.phi[i, :, :]

            element_loads +=  (N.T @ (e_normals @ Pe)) * (det_jacs * self.wps[i])

        total_dof = self.dof_per_node * len(self.nodal_coordinates)
        nodal_loads = np.zeros(total_dof, len(self.model.frequencies), dtype=complex)

        for elem_id, node_ids in enumerate(self.connectivities):
            nodal_loads[node_ids, :] += element_loads[elem_id, :, :]

        return nodal_loads
    

    def calculate_load_vector_for_normal_pressure_loading(self, el_index: int, e_normal: np.ndarray,  normal_pressure: np.ndarray) -> np.ndarray:
        """ 
        This method computes the elementary load vector.

        Parameters
        ----------
        el_index: int
            The element index.

        load: float, optional
            The load vector.

        Returns
        -------
        Fe: np.ndarray
            The elementary load vector.
        """

        # element nodes
        e_nodes = self.connectivities[el_index, :]

        # element nodal coordinates
        coords = self.nodal_coordinates[e_nodes, :]

        # nodal coordinates in the local CS
        coord_lcs = get_local_coordinates(coords)

        # reshape the normal pressures vector
        normal_pressure = normal_pressure.reshape(1, -1)

        # initialize the shape functions matrix
        N = np.zeros((3, self.dof_per_element), dtype=float)

        # initialize the variable Fe
        Fe = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrix
            JAC = self.dphi[i, :, :] @ coord_lcs

            # determinant of Jacobia matrix
            det_JAC = self.get_detJAC(JAC)

            # populate the shape functions matrix
            N[0, 0::3] = self.phi[i, :, :]
            N[1, 1::3] = self.phi[i, :, :]
            N[2, 2::3] = self.phi[i, :, :]

            # the negative value of the normal is used to point the normal toward the interior of the domain.
            Fe += (N.T @ (-e_normal @ normal_pressure)) * (det_JAC * self.wps[i])

        return Fe

    def element_indexes(self, index: int):
        node_ids = self.connectivities[index, :]
        element_dofs = self.dof_per_node * node_ids.reshape(-1, 1) + np.arange(self.dof_per_node, dtype=int)
        return element_dofs.flatten()
