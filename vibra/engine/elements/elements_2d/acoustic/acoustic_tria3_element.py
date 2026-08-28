
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_2d.tria3_element import TRIANGLE_3, get_local_coordinates

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class ACT_TRIANGLE_3(TRIANGLE_3):

    def __init__(self, model: "Model", dof_per_node: int = 1):
        super().__init__(model, dof_per_node)

        self.model = model
        self.local_dof = np.arange(dof_per_node, dtype=int)

        self.connectivities = None
        self.element_label = "acoustic_triangular_3"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates


    def load_vector(self, el_index: int, load: float = 1.0) -> np.ndarray:
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

        # element nodal coordinates
        coords = self.nodal_coordinates[self.connectivities[el_index, :], :]

        # nodal coordinates in the local CS
        coord_lcs = get_local_coordinates(coords)

        # initialize the variable Fe
        Fe = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrix
            JAC = self.dphi[i, :, :] @ coord_lcs

            # determinant of Jacobia matrix
            det_JAC = self.get_detJAC(JAC)

            # shape functions
            N = self.phi[i, :, :]

            Fe += load * N.T * (det_JAC * self.wps[i])

        return Fe


    def elementary_sound_power(self, e_connect: np.ndarray, P_e: np.ndarray, Vn_e: np.ndarray) -> np.ndarray:
        """ 
        This method computes the elementary load vector.

        Parameters
        ----------
        el_index: int
            The element index.

        P_e: np.ndarray
            The righ stacked vector (complex-conjugate of pressures).
    
        Vn_e: np.ndarray
            The left stacked vector (complex-conjugate of normal particle velocities).

        Returns
        -------
        We: np.ndarray
            The elementary sound power vector.
        """

        # element nodal coordinates
        coords = self.nodal_coordinates[e_connect, :]

        # nodal coordinates in the local CS
        local_coords = get_local_coordinates(coords)

        # initialize variable We
        We = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrices of all elements
            JAC = self.dphi[i, :, :] @ local_coords

            # determinant of Jacobian matrix
            det_jac = self.get_detJAC(JAC)

            # shape functions
            N = self.phi[i, :, :]

            We += P_e @ (N.T @ N) @ Vn_e * (det_jac * self.wps[i])

        return We.flatten()


    def acoustic_pressure_load(self, e_normals: np.ndarray, nodal_solution: np.ndarray) -> np.ndarray:
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

        # stack all elements nodal pressures 
        pressures = np.array([nodal_solution[node_ids, :] for node_ids in self.connectivities.T], dtype=complex)

        # stack the element nodal pressures in format [n_el, DOFS_PER_ELEMENT, n_freq]
        Pe = pressures.transpose(1, 0, 2)

        # compute local coordinates for all elements
        local_coords = self.get_stacked_local_coordinates()

        # initialize variable
        acoustic_load = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrices of all elements
            JAC_stacked = self.dphi[i, :, :] @ local_coords

            # Jacobian determinants and inverses of all elements
            det_jacs, _ = self.get_detJAC_and_invJAC(JAC_stacked)

            # shape functions
            N = self.phi[i, :, :]

            acoustic_load += np.sum(-e_normals @ (N @ Pe) * (det_jacs * self.wps[i]), axis=0)

        return acoustic_load


    def get_rows_and_cols_indices_1D(self, index: int):
        """
        This method returns, for a selected element, the row 
        and column indices for 1D element integration.
        
        index: int
            The element index.
        """

        dof = self.dof_per_node
        elem_nodes = self.connectivities[index, :]
        _elem_nodes = self.model.fluid_node_mapping[elem_nodes]
        dof_indices = dof * _elem_nodes + self.local_dof
        return dof_indices


    def get_rows_and_cols_indices_2D(self, connectivities: np.ndarray):
        """
        This method returns the row and column indices for 2D element 
        integration for all elements related to the connectivities.
        
        connectivities: np.ndarray
            A 2D array containing all element connectivities.
        """

        self.reorder_connect(connectivities)

        n_el = len(connectivities)
        dof, edof = self.dof_per_node, self.dof_per_element

        ind_dof = np.zeros((n_el, edof), dtype=int)

        for j in range(self.nodes_per_element):
            start = j * dof
            end = (j + 1) * dof
            elem_nodes = self.model.fluid_node_mapping[self.connectivities[:, j]]
            ind_dof[:, start : end] = dof * elem_nodes.reshape(-1, 1) + self.local_dof

        vect_indices = ind_dof.flatten()
        ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        ind_cols = (np.tile(ind_dof, edof)).flatten()

        return ind_rows, ind_cols