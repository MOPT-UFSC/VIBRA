
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_3d.solid_elements import Element3D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import logging

import numpy as np


class ACOUSTIC_3D_ELEMENT(Element3D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):
        super().__init__(model, dof_per_node, nodes_per_element)

        self.element_label = ""
        self.connectivities = None
        self.dof_indexes_proc = self.dof_indexes_processor("acoustic")


    def elementary_matrices(self, el_index: int) -> tuple[np.ndarray, np.ndarray]:
        """
        This method computes the elementary mass and stiffness matrices.

        Parameter
        ---------
        el_index: int
            Corresponds to the solid element index.

        Returns
        -------
        Ke: np.ndarray
            The elementary stiffness matrix.

        Me: np.ndarray
            The elementary mass matrix.
        """

        # nodes from element
        elem_nodes = self.connectivities[el_index, :]

        # element nodal coords
        coords = self.model.mesh.nodal_coordinates[elem_nodes, 1:4]

        # initializing variables
        Ke, Me = 0., 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrix
            JAC = self.dphi[i, :, :] @ coords

            # Jacobian determinant and inverse
            detJAC, invJAC = self.get_detJAC_and_invJAC(JAC)

            # shape functions
            N = self.phi[i, :].reshape(1, -1)

            # derivative of shape functions
            B = invJAC @ self.dphi[i, :, :]

            Ke += B.T @ B * (detJAC * self.wps[i])
            Me += N.T @ N * (detJAC * self.wps[i])

        # if el_index == 0:
        #     np.savetxt("Me_base.dat", Me, fmt="%.16e", delimiter=",")
        #     np.savetxt("Ke_base.dat", Ke, fmt="%.16e", delimiter=",")

        return Ke, Me


    def stacked_elementary_matrices_NtN_BtB(self):
        """
        This method computes all mass and stiffness matrices in
        stacked form performing a loop between the integration 
        points.

        Returns
        -------
        Ke: np.ndarray
            The elementary stiffness stacked matrices.

        Me: np.ndarray
            The elementary mass stacked matrices.
        """

        # proces the stacked nodal coordinates
        element_data_proc = self.element_data_processor(self.model, "acoustic")
        stacked_coords = element_data_proc.get_stacked_nodal_coords(self.connectivities)

        # initialize variables
        int2d_BtB = 0.
        int2d_NtN = 0.

        # integration loop
        for i in range(self.nint):

            progress = int(25 + 55*(i / self.nint))
            logging.info(f"Processing the elementary matrices data... [{progress}/100]")

            # Jacobian matrices of all elements
            JAC_stacked = self.dphi[i, :, :] @ stacked_coords

            # Jacobian determinants and inverses of all elements
            det_jacs, inv_jacs = self.get_detJAC_and_invJAC(JAC_stacked)

            # shape functions
            N = self.phi[i, :]
            N_t = N.T

            # derivative of shape functions
            B = inv_jacs @ self.dphi[i, :, :]
            B_t = np.transpose(B, axes=(0, 2, 1))

            int2d_BtB += B_t @ B * (det_jacs * self.wps[i])
            int2d_NtN += N_t @ N * (det_jacs * self.wps[i])

        return int2d_BtB, int2d_NtN


    def generate_ind_rows_cols(self, reorder: bool = True):
        """This method processess the dof indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivities = self.model.mesh.solids_connectivity[:, 4:]

        dof_indexes = self.dof_indexes_processor("acoustic")

        return dof_indexes.get_rows_and_cols_indices_3D(self.connectivities)