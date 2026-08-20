
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.quad4_element import QUADRANGLE_4, get_local_coordinates

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class STRUCT_QUADRANGLE_4(QUADRANGLE_4):

    def __init__(self, model: "Model", dof_per_node: int = 3):
        super().__init__(model, dof_per_node)

        self.model = model

        self.connectivities = None
        self.element_label = "structural_quadrangle_4"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates


    def integrate_area(self, connectivities: np.ndarray):

        self.connectivities = connectivities
        
        # compute local coordinates for all elements
        local_coords = self.get_stacked_local_coordinates()

        # initialize variable
        dA = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrices of all elements
            JAC_stacked = self.dphi[i, :, :] @ local_coords

            # Jacobian determinants and inverses of all elements
            det_jacs, _ = self.get_detJAC_and_invJAC(JAC_stacked)

            dA +=  det_jacs * self.wps[i]

        return np.sum(dA)


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
    

    def integrate_normal_pressure_load(self, el_index: int, e_normal: np.ndarray,  normal_pressure: np.ndarray) -> np.ndarray:
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

    def integrate_distributed_load(self, el_index: int, distributed_load: np.ndarray) -> np.ndarray:
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

            Fe += (N.T @ distributed_load) * (det_JAC * self.wps[i])

        return Fe


    def integrate_distributed_mass(self, el_index: int, distributed_mass: float) -> np.ndarray:
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

        # initialize the shape functions matrix
        N = np.zeros((3, self.dof_per_element), dtype=float)

        # initialize the variable Fe
        Me = 0.

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

            Me += (N.T @ N) * distributed_mass * (det_JAC * self.wps[i])

        return Me


    def element_indexes_vector(self, index: int):
        node_ids = self.connectivities[index, :]
        element_dofs = self.dof_per_node * node_ids.reshape(-1, 1) + np.arange(self.dof_per_node, dtype=int)
        return element_dofs.flatten()


    def elements_indexes_matrix(self):

        dof, edof = self.dof_per_node, self.dof_per_element
        n_el = len(self.connectivities)

        local_dof = np.arange(dof, dtype=int)
        ind_dof = np.zeros((n_el, edof), dtype=int)

        for j in range(self.NODES_PER_ELEMENT):
            ind_dof[:, j*dof : (1 + j)*dof] = dof * self.connectivities[:, j+1].reshape(-1, 1) + local_dof

        vect_indices = ind_dof.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dof, edof)).flatten()

        return self.ind_rows, self.ind_cols