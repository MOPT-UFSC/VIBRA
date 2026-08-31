from typing import TYPE_CHECKING

from vibra.engine.elements.elements_1d.line_elements import Element1D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class ACOUSTIC_1D_ELEMENT(Element1D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.model = model
        self.element_label = ""
        self.connectivities = None

        self.dof_indexes_proc = self.dof_indexes_processor("acoustic")


    def stacked_matrices_NtN_and_BtB(self) -> np.ndarray:
        """
        This method processes all elementary matrices for mass source
        and returns them in the stacked array form.

        Returns
        -------
        Nt_N_stacked: np.ndarray
            The array containing the elementary stacked matrices int(Nt @ N, gamma_L).

        Bt_B_stacked: np.ndarray
            The array containing the elementary stacked matrices int(Bt @ B, gamma_L).
        """

        # local coordinates
        local_coords = self.get_stacked_local_coordinates()

        # initialize variables
        int1d_NtN = 0.
        int1d_BtB = 0.

        # integration loop for stiffness matrix
        for i in range(self.wps_K.size):

            # determinant of Jacobian
            det_jacs = self.dphi_K[i, :, :] @ local_coords

            # inverse of Jacobian
            inv_jacs = 1 / det_jacs

            # derivative of shape functions
            B = inv_jacs @ self.dphi_K[i, :, :]
            B_t = np.transpose(B, axes=(0, 2, 1))

            int1d_BtB += B_t @ B * (det_jacs * self.wps_K[i])

        # integration loop for mass matrix
        for i in range(self.wps_M.size):

            # determinant of Jacobian
            det_jacs = self.dphi_M[i, :, :] @ local_coords

            # shape functions
            N = self.phi_M[i, :, :]

            int1d_NtN += N.T @ N * (det_jacs * self.wps_M[i])

        return int1d_NtN, int1d_BtB


    def get_rows_and_cols_indices_1D(self, index: int):
        """
        This method returns, for a selected element, the row 
        and column indices for 1D element integration.
        
        index: int
            The element index.
        """

        return self.dof_indexes_proc.get_rows_and_cols_indices_1D(index, self.connectivities)


    def get_rows_and_cols_indices_2D(self, connectivities: np.ndarray):
        """
        This method returns the row and column indices for 2D element 
        integration for all elements related to the connectivities.
        
        connectivities: np.ndarray
            A 2D array containing all element connectivities.
        """

        self.reorder_connect(connectivities)

        return self.dof_indexes_proc.get_rows_and_cols_indices_2D(self.connectivities)