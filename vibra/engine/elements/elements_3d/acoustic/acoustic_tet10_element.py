# fmt: off

from vibra.engine.elements.solid_elements import Element3D

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


def get_detJAC_and_invJAC(JAC: np.ndarray):
    """
    This function computes the determinant and inverse
    of Jacobian matrix.

    Parameters
    ----------
    JAC: np.array
        The Jacobian matrices.

    Returns
    -------
    det_jac: np.ndarray
        The determinant of Jacobian matrix.

    inv_jac: np.ndarray
        The inverse of Jacobian matrix.
    """

    if len(JAC.shape) == 3:

        det_jac = (
              JAC[:, 0, 0] * JAC[:, 1, 1] * JAC[:, 2, 2]
            + JAC[:, 0, 1] * JAC[:, 1, 2] * JAC[:, 2, 0]
            + JAC[:, 0, 2] * JAC[:, 1, 0] * JAC[:, 2, 1]
        ) - (
              JAC[:, 2, 0] * JAC[:, 1, 1] * JAC[:, 0, 2]
            + JAC[:, 2, 1] * JAC[:, 1, 2] * JAC[:, 0, 0]
            + JAC[:, 2, 2] * JAC[:, 1, 0] * JAC[:, 0, 1]
        )
        det_jac = det_jac.reshape(-1, 1, 1)

        adj_matrix = np.zeros((det_jac.shape[0], 3, 3), dtype=float)
        adj_matrix[:, 0, 0] =  ((JAC[:, 1, 1] * JAC[:, 2, 2]) - (JAC[:, 2, 1] * JAC[:, 1, 2]))
        adj_matrix[:, 1, 0] = -((JAC[:, 1, 0] * JAC[:, 2, 2]) - (JAC[:, 1, 2] * JAC[:, 2, 0]))
        adj_matrix[:, 2, 0] =  ((JAC[:, 1, 0] * JAC[:, 2, 1]) - (JAC[:, 1, 1] * JAC[:, 2, 0]))
        adj_matrix[:, 0, 1] = -((JAC[:, 0, 1] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 1]))
        adj_matrix[:, 1, 1] =  ((JAC[:, 0, 0] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 0]))
        adj_matrix[:, 2, 1] = -((JAC[:, 0, 0] * JAC[:, 2, 1]) - (JAC[:, 0, 1] * JAC[:, 2, 0]))
        adj_matrix[:, 0, 2] =  ((JAC[:, 0, 1] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 1]))
        adj_matrix[:, 1, 2] = -((JAC[:, 0, 0] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 0]))
        adj_matrix[:, 2, 2] =  ((JAC[:, 0, 0] * JAC[:, 1, 1]) - (JAC[:, 0, 1] * JAC[:, 1, 0]))

    else:

        det_jac = (
              JAC[0, 0] * JAC[1, 1] * JAC[2, 2]
            + JAC[0, 1] * JAC[1, 2] * JAC[2, 0]
            + JAC[0, 2] * JAC[1, 0] * JAC[2, 1]
        ) - (
              JAC[2, 0] * JAC[1, 1] * JAC[0, 2]
            + JAC[2, 1] * JAC[1, 2] * JAC[0, 0]
            + JAC[2, 2] * JAC[1, 0] * JAC[0, 1]
        )

        adj_matrix = np.zeros((3, 3), dtype=float)
        adj_matrix[0, 0] =  ((JAC[1, 1] * JAC[2, 2]) - (JAC[2, 1] * JAC[1, 2]))
        adj_matrix[1, 0] = -((JAC[1, 0] * JAC[2, 2]) - (JAC[1, 2] * JAC[2, 0]))
        adj_matrix[2, 0] =  ((JAC[1, 0] * JAC[2, 1]) - (JAC[1, 1] * JAC[2, 0]))
        adj_matrix[0, 1] = -((JAC[0, 1] * JAC[2, 2]) - (JAC[0, 2] * JAC[2, 1]))
        adj_matrix[1, 1] =  ((JAC[0, 0] * JAC[2, 2]) - (JAC[0, 2] * JAC[2, 0]))
        adj_matrix[2, 1] = -((JAC[0, 0] * JAC[2, 1]) - (JAC[0, 1] * JAC[2, 0]))
        adj_matrix[0, 2] =  ((JAC[0, 1] * JAC[1, 2]) - (JAC[0, 2] * JAC[1, 1]))
        adj_matrix[1, 2] = -((JAC[0, 0] * JAC[1, 2]) - (JAC[0, 2] * JAC[1, 0]))
        adj_matrix[2, 2] =  ((JAC[0, 0] * JAC[1, 1]) - (JAC[0, 1] * JAC[1, 0]))

    return det_jac, (1 / det_jac) * adj_matrix

def get_stacked_detJAC_and_invJAC(JAC: np.ndarray, all_int_points: bool=False):

    """
    This method computes the determinant and inverse of Jacobian
    matrix for all elements for one integration points or all 
    integration points.

    Parameters
    ----------
    JAC: np.array
        The Jacobian matrices.

    all_int_points: bool, optional
        Controls when the processing are executed in all 
        integration points (default is False).

    Returns
    -------
    det_jac: np.ndarray
        The determinant of Jacobian matrix.

    inv_jac: np.ndarray
        The inverse of Jacobian matrix.
    """

    if all_int_points:

        N_int = JAC.shape[0]
        
        detJAC = (
              JAC[:, :, 0, 0] * JAC[:, :, 1, 1] * JAC[:, :, 2, 2]
            + JAC[:, :, 0, 1] * JAC[:, :, 1, 2] * JAC[:, :, 2, 0]
            + JAC[:, :, 0, 2] * JAC[:, :, 1, 0] * JAC[:, :, 2, 1]
        ) - (
              JAC[:, :, 2, 0] * JAC[:, :, 1, 1] * JAC[:, :, 0, 2]
            + JAC[:, :, 2, 1] * JAC[:, :, 1, 2] * JAC[:, :, 0, 0]
            + JAC[:, :, 2, 2] * JAC[:, :, 1, 0] * JAC[:, :, 0, 1]
        )
        det_jac = detJAC.reshape(-1, N_int, 1, 1)

        adj_matrix = np.zeros((detJAC.shape[0], N_int, 3, 3), dtype=float)
        adj_matrix[:, :, 0, 0] =  ((JAC[:, :, 1, 1] * JAC[:, :, 2, 2]) - (JAC[:, :, 2, 1] * JAC[:, :, 1, 2]))
        adj_matrix[:, :, 1, 0] = -((JAC[:, :, 1, 0] * JAC[:, :, 2, 2]) - (JAC[:, :, 1, 2] * JAC[:, :, 2, 0]))
        adj_matrix[:, :, 2, 0] =  ((JAC[:, :, 1, 0] * JAC[:, :, 2, 1]) - (JAC[:, :, 1, 1] * JAC[:, :, 2, 0]))
        adj_matrix[:, :, 0, 1] = -((JAC[:, :, 0, 1] * JAC[:, :, 2, 2]) - (JAC[:, :, 0, 2] * JAC[:, :, 2, 1]))
        adj_matrix[:, :, 1, 1] =  ((JAC[:, :, 0, 0] * JAC[:, :, 2, 2]) - (JAC[:, :, 0, 2] * JAC[:, :, 2, 0]))
        adj_matrix[:, :, 2, 1] = -((JAC[:, :, 0, 0] * JAC[:, :, 2, 1]) - (JAC[:, :, 0, 1] * JAC[:, :, 2, 0]))
        adj_matrix[:, :, 0, 2] =  ((JAC[:, :, 0, 1] * JAC[:, :, 1, 2]) - (JAC[:, :, 0, 2] * JAC[:, :, 1, 1]))
        adj_matrix[:, :, 1, 2] = -((JAC[:, :, 0, 0] * JAC[:, :, 1, 2]) - (JAC[:, :, 0, 2] * JAC[:, :, 1, 0]))
        adj_matrix[:, :, 2, 2] =  ((JAC[:, :, 0, 0] * JAC[:, :, 1, 1]) - (JAC[:, :, 0, 1] * JAC[:, :, 1, 0]))

    else:

        detJAC = (
              JAC[:, 0, 0] * JAC[:, 1, 1] * JAC[:, 2, 2]
            + JAC[:, 0, 1] * JAC[:, 1, 2] * JAC[:, 2, 0]
            + JAC[:, 0, 2] * JAC[:, 1, 0] * JAC[:, 2, 1]
        ) - (
              JAC[:, 2, 0] * JAC[:, 1, 1] * JAC[:, 0, 2]
            + JAC[:, 2, 1] * JAC[:, 1, 2] * JAC[:, 0, 0]
            + JAC[:, 2, 2] * JAC[:, 1, 0] * JAC[:, 0, 1]
        )
        det_jac = detJAC.reshape(-1, 1, 1)

        adj_matrix = np.zeros((detJAC.shape[0], 3, 3), dtype=float)
        adj_matrix[:, 0, 0] =  ((JAC[:, 1, 1] * JAC[:, 2, 2]) - (JAC[:, 2, 1] * JAC[:, 1, 2]))
        adj_matrix[:, 1, 0] = -((JAC[:, 1, 0] * JAC[:, 2, 2]) - (JAC[:, 1, 2] * JAC[:, 2, 0]))
        adj_matrix[:, 2, 0] =  ((JAC[:, 1, 0] * JAC[:, 2, 1]) - (JAC[:, 1, 1] * JAC[:, 2, 0]))
        adj_matrix[:, 0, 1] = -((JAC[:, 0, 1] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 1]))
        adj_matrix[:, 1, 1] =  ((JAC[:, 0, 0] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 0]))
        adj_matrix[:, 2, 1] = -((JAC[:, 0, 0] * JAC[:, 2, 1]) - (JAC[:, 0, 1] * JAC[:, 2, 0]))
        adj_matrix[:, 0, 2] =  ((JAC[:, 0, 1] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 1]))
        adj_matrix[:, 1, 2] = -((JAC[:, 0, 0] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 0]))
        adj_matrix[:, 2, 2] =  ((JAC[:, 0, 0] * JAC[:, 1, 1]) - (JAC[:, 0, 1] * JAC[:, 1, 0]))

    return det_jac, (1 / det_jac) * adj_matrix


class ACT_TETRAHEDRON_10C(Element3D):

    NODES_PER_ELEMENT = 10
    DOFS_PER_NODE = 1
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOFS_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivity = None
        self.element_label = "acoustic_tetrahedron_10"

        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.solids_connectivity = self.model.mesh.solids_connectivity

        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.solids_connectivity)

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def update_nodal_coordinates(self, nodal_coordinates: np.ndarray):
        self.nodal_coordinates = nodal_coordinates


    def update_solids_connectivity(self, connectivity: np.ndarray):
        self.connectivity = connectivity


    def define_integration_points(self):
        """ 
        This method defines the integration points and their
        weights for numerical integration.
        """

        self.nint = 15

        ax = 1 / 4
        bx = (7 + np.sqrt(15)) / 34
        cx = (7 - np.sqrt(15)) / 34
        dx = (13 - 3 * np.sqrt(15)) / 34
        ex = (13 + 3 * np.sqrt(15)) / 34
        fx = (5 - np.sqrt(15)) / 20
        gx = (5 + np.sqrt(15)) / 20

        p1 = 48 / 405
        p2 = 6 * (2665 - 14 * np.sqrt(15)) / 226800
        p3 = 6 * (2665 + 14 * np.sqrt(15)) / 226800
        p4 = 30 / 567

        self.pint = np.array([[ax, ax, ax],
                              [bx, bx, bx],
                              [bx, bx, dx],
                              [bx, dx, bx],
                              [dx, bx, bx],
                              [cx, cx, cx],
                              [cx, cx, ex],
                              [cx, ex, cx],
                              [ex, cx, cx],
                              [fx, fx, gx],
                              [fx, gx, fx],
                              [gx, fx, fx],
                              [fx, gx, gx],
                              [gx, fx, gx],
                              [gx, gx, fx]], dtype=float)

        self.wps = np.array([p1, p2, p2, p2, p2, 
                             p3, p3, p3, p3, p4, 
                             p4, p4, p4, p4, p4], dtype=float).reshape(-1, 1, 1)


    def process_shape_functions_and_derivatives(self):
        """
        This method returns the shape functions and its derivatives
        for all integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        l1 = self.pint[:, 0]
        l2 = self.pint[:, 1]
        l3 = self.pint[:, 2]

        self.phi, self.dphi = self.get_shape_functions_and_derivatives(l1, l2, l3)


    def get_shape_functions_and_derivatives(self, l1: np.ndarray|float, l2: np.ndarray|float, l3: np.ndarray|float):

        """
        This method returns the shape functions and its derivatives.
        
        Parameters
        ----------
        l1: np.ndarray
            The x coordinates of the integration points.
        
        l2: np.ndarray
            The y coordinates of the integration points.

        l3: np.ndarray
            The z coordinates of the integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        if isinstance(l1, np.ndarray):
            Nz = l1.size
        else:
            Nz = 1

        # shape functions
        phi = np.zeros((Nz, 1, self.NODES_PER_ELEMENT), dtype=float)

        l4 = 1 - l1 - l2 - l3
        phi[:, 0, 0] = (2 * l1 - 1) * l1       # ->      (1.0, 0.0, 0.0, 0.0)   I
        phi[:, 0, 1] = (2 * l2 - 1) * l2       # ->      (0.0, 1.0, 0.0, 0.0)   J
        phi[:, 0, 2] = (2 * l3 - 1) * l3       # ->      (0.0, 0.0, 1.0, 0.0)   K
        phi[:, 0, 3] = (2 * l4 - 1) * l4       # ->      (0.0, 0.0, 0.0, 1.0)   L
        phi[:, 0, 4] = 4 * l1 * l2             # ->      (0.5, 0.5, 0.0, 0.0)   M
        phi[:, 0, 5] = 4 * l2 * l3             # ->      (0.0, 0.5, 0.5, 0.0)   N
        phi[:, 0, 6] = 4 * l1 * l3             # ->      (0.5, 0.0, 0.5, 0.0)   O
        phi[:, 0, 7] = 4 * l1 * l4             # ->      (0.5, 0.0, 0.0, 0.5)   P
        phi[:, 0, 8] = 4 * l2 * l4             # ->      (0.0, 0.5, 0.0, 0.5)   Q
        phi[:, 0, 9] = 4 * l3 * l4             # ->      (0.0, 0.0, 0.5, 0.5)   R

        # derivatives of shape functions
        dphi = np.zeros((Nz, 3, self.NODES_PER_ELEMENT), dtype=float)

        dphi[:, 0, 0] =  4 * l1 - 1
        dphi[:, 0, 1] =  0
        dphi[:, 0, 2] =  0
        dphi[:, 0, 3] = -4 * l4 + 1
        dphi[:, 0, 4] =  4 * l2
        dphi[:, 0, 5] =  0
        dphi[:, 0, 6] =  4 * l3
        dphi[:, 0, 7] =  4 * (l4 - l1)
        dphi[:, 0, 8] = -4 * l2
        dphi[:, 0, 9] = -4 * l3

        dphi[:, 1, 0] =  0
        dphi[:, 1, 1] =  4 * l2 - 1
        dphi[:, 1, 2] =  0
        dphi[:, 1, 3] = -4 * l4 + 1
        dphi[:, 1, 4] =  4 * l1
        dphi[:, 1, 5] =  4 * l3
        dphi[:, 1, 6] =  0
        dphi[:, 1, 7] = -4 * l1
        dphi[:, 1, 8] =  4 * (l4 - l2)
        dphi[:, 1, 9] = -4 * l3

        dphi[:, 2, 0] =  0
        dphi[:, 2, 1] =  0
        dphi[:, 2, 2] =  4 * l3 - 1
        dphi[:, 2, 3] = -4 * l4 + 1
        dphi[:, 2, 4] =  0
        dphi[:, 2, 5] =  4 * l2
        dphi[:, 2, 6] =  4 * l1
        dphi[:, 2, 7] = -4 * l1
        dphi[:, 2, 8] = -4 * l2
        dphi[:, 2, 9] =  4 * (l4 - l3)

        if Nz == 1:
            return phi[0, :, :], dphi[0, :, :]
        else:
            return phi, dphi


    def get_stacked_nodal_coords(self, all_int_points: bool=False) -> np.ndarray:
        """
        This method returns the nodal coordinates of all elements in form 
        of a 3D matrix. Each plane of this matrix contains the nodal 
        coordiantes from all nodes relative to the i-th element.

        Parameter
        ---------
        all_int_points: bool, optional
            Controls when the processing are executed in all 
            integration points (default is False).

        Returns
        -------
        stacked_coords: np.ndarray
            A tridimensional matrix containing the nodal 
            coordinates of all elements.

        """
        nel = self.connectivity.shape[0]
        if all_int_points:
            stacked_coords = np.zeros((nel, 1, self.DOFS_PER_ELEMENT, 3), dtype=float)
            for j in range(self.DOFS_PER_ELEMENT):
                stacked_coords[:, 0, j, :] = self.nodal_coordinates[self.connectivity[:, j+1], 1:4]

        else:
            stacked_coords = np.zeros((nel, self.DOFS_PER_ELEMENT, 3), dtype=float)
            for j in range(self.DOFS_PER_ELEMENT):
                stacked_coords[:, j, :] = self.nodal_coordinates[self.connectivity[:, j+1], 1:4]

        return stacked_coords


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
        elem_nodes = self.connectivity[el_index, 1:]

        # element nodal coords
        coords = self.nodal_coordinates[elem_nodes, 1:4]

        # initializing variables
        Ke, Me = 0., 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrix
            JAC = self.dphi[i, :, :] @ coords

            # Jacobian determinant and inverse
            detJAC, invJAC = get_detJAC_and_invJAC(JAC)

            # shape functions
            N = self.phi[i, :].reshape(1, -1)

            # derivative of shape functions
            B = invJAC @ self.dphi[i, :, :]

            Ke += (1 / 6) * B.T @ B * (detJAC * self.wps[i])
            Me += (1 / 6) * N.T @ N * (detJAC * self.wps[i])

        # if el_index == 0:
        #     np.savetxt("Me_base.dat", Me, fmt="%.16e", delimiter=",")
        #     np.savetxt("Ke_base.dat", Ke, fmt="%.16e", delimiter=",")

        return Ke, Me


    def stacked_elementary_matrices_NtN_BtB_noloop(self):
        """
        This method computes all mass and stiffness matrices in
        stacked form without performing a loop between the
        integration points.

        Returns
        -------
        Ke: np.ndarray
            The elementary stiffness stacked matrices.

        Me: np.ndarray
            The elementary mass stacked matrices.
        """

        # stacked nodal coordinates
        stacked_coords = self.get_stacked_nodal_coords(all_int_points=True)

        # Jacobian matrices of all elements
        dphi_resh = self.dphi.reshape(1, self.nint, 3, self.NODES_PER_ELEMENT)
        JAC_stacked = dphi_resh @ stacked_coords

        # Jacobian determinants and inverses of all elements
        det_jacs, inv_jacs = get_stacked_detJAC_and_invJAC(JAC_stacked, all_int_points=True)

        # shape functions
        N = self.phi
        N_t = np.transpose(N, axes=(0, 2, 1))

        # derivative of shape functions
        B = inv_jacs @ dphi_resh
        B_t = np.transpose(B, axes=(0, 1, 3, 2))

        Ke = np.sum((1 / 6) * B_t @ B * (det_jacs * self.wps), axis=1)
        Me = np.sum((1 / 6) * N_t @ N * (det_jacs * self.wps), axis=1)

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

        # stacked nodal coordinates
        stacked_coords = self.get_stacked_nodal_coords()

        # initialize variables
        int2d_BtB = 0.
        int2d_NtN = 0.

        # integration loop
        for i in range(self.nint):

            # Jacobian matrices of all elements
            JAC_stacked = self.dphi[i, :, :] @ stacked_coords

            # Jacobian determinants and inverses of all elements
            det_jacs, inv_jacs = get_stacked_detJAC_and_invJAC(JAC_stacked)

            # shape functions
            N = self.phi[i, :]
            N_t = N.T

            # derivative of shape functions
            B = inv_jacs @ self.dphi[i, :, :]
            B_t = np.transpose(B, axes=(0, 2, 1))

            int2d_BtB += (1 / 6) * B_t @ B * (det_jacs * self.wps[i])
            int2d_NtN += (1 / 6) * N_t @ N * (det_jacs * self.wps[i])

        return int2d_BtB, int2d_NtN


    def process_particle_velocity(
            self,
            element_id : int,
            node_id : int,
            rho : float | np.ndarray,
            frequencies : np.ndarray,
            **kwargs
        ):
        """
        This method computes the particle velocity components in
        the x, y, and z directions.

        Parameters
        ----------
        element_id: int
            The element index.

        node_id: int
            The node index.

        rho: float
            The fluid density in kg/m³.

        frequencies: np.ndarray
            The frequencies vector.

        nodal_pressures: np.ndarray
            The nodal pressures solution.

        Return
        ------
        particle_velocity: np.array
            An array containing the particle velocity components in the
            x, y, and z directions.
        """

        solution = kwargs.get("solution")
        nodal_pressures = kwargs.get("nodal_pressures")
        node_ids = kwargs.get("node_ids")

        if node_ids is None:
            node_ids = self.connectivity[element_id, 1:]
    
        if isinstance(nodal_pressures, np.ndarray):
            Pe = nodal_pressures
        elif isinstance(solution, np.ndarray):
            Pe = solution[node_ids, :]    
        else:
            return None

        omega = 2 * np.pi * frequencies

        if self.connectivity is None:
            self.reorder_connect()

        p_calc = np.array([ [1.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0],
                            [0.0, 0.0, 0.0],
                            [0.5, 0.5, 0.0],
                            [0.0, 0.5, 0.5],
                            [0.5, 0.0, 0.5],
                            [0.5, 0.0, 0.0],
                            [0.0, 0.5, 0.0],
                            [0.0, 0.0, 0.5] ], dtype=float)

        index = np.where(node_ids==node_id)[0]
        if index.size != 1:
            return None

        # local coordinates
        (ssx, ttx, rrx) = p_calc[index[0], :]

        # derivative of the shape function at the selected point
        _, dphi = self.get_shape_functions_and_derivatives(ssx, ttx, rrx)

        # nodal coordinates from element
        coords = self.nodal_coordinates[node_ids, 1:4]

        # Jacobian matrix
        JAC = dphi @ coords

        # inverse of Jacobian matrix
        _, invJAC = get_detJAC_and_invJAC(JAC)
        
        # derivative of shape functions
        B = invJAC @ dphi

        # calculate the particle velocities components
        particle_velocity = -(1 / (1j * rho * omega)) * (B @ Pe)

        return particle_velocity


    def reorder_connect(self):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """
        if self.solids_connectivity.shape[1] == self.NODES_PER_ELEMENT + 4:
            self.connectivity = self.solids_connectivity[:, [0, 6, 4, 5, 7, 10, 8, 9, 12, 11, 13]]


    def generate_ind_rows_cols(self, reorder: bool = True):
        """ 
        This method processess the dofs indices (rows and columns) 
        for assembly
        """

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.solids_connectivity[:, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]]

        dofs, edofs = self.DOFS_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs * self.connectivity[:, 1:]

        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

        return self.ind_rows, self.ind_cols


def shape10TC(l1, l2, l3):
    """This function returns the shape functions and its derivatives."""

    # shape functions
    phi = np.zeros(10)

    l4 = 1 - l1 - l2 - l3
    phi[0] = (2 * l1 - 1) * l1       # ->      (1.0, 0.0, 0.0, 0.0)   I
    phi[1] = (2 * l2 - 1) * l2       # ->      (0.0, 1.0, 0.0, 0.0)   J
    phi[2] = (2 * l3 - 1) * l3       # ->      (0.0, 0.0, 1.0, 0.0)   K
    phi[3] = (2 * l4 - 1) * l4       # ->      (0.0, 0.0, 0.0, 1.0)   L
    phi[4] = 4 * l1 * l2             # ->      (0.5, 0.5, 0.0, 0.0)   M
    phi[5] = 4 * l2 * l3             # ->      (0.0, 0.5, 0.5, 0.0)   N
    phi[6] = 4 * l1 * l3             # ->      (0.5, 0.0, 0.5, 0.0)   O
    phi[7] = 4 * l1 * l4             # ->      (0.5, 0.0, 0.0, 0.5)   P
    phi[8] = 4 * l2 * l4             # ->      (0.0, 0.5, 0.0, 0.5)   Q
    phi[9] = 4 * l3 * l4             # ->      (0.0, 0.0, 0.5, 0.5)   R

    # derivatives of shape functions
    dphi = np.zeros((3, 10))

    dphi[0, 0] =  4 * l1 - 1
    dphi[0, 1] =  0
    dphi[0, 2] =  0
    dphi[0, 3] = -4 * l4 + 1
    dphi[0, 4] =  4 * l2
    dphi[0, 5] =  0
    dphi[0, 6] =  4 * l3
    dphi[0, 7] =  4 * (l4 - l1)
    dphi[0, 8] = -4 * l2
    dphi[0, 9] = -4 * l3

    dphi[1, 0] =  0
    dphi[1, 1] =  4 * l2 - 1
    dphi[1, 2] =  0
    dphi[1, 3] = -4 * l4 + 1
    dphi[1, 4] =  4 * l1
    dphi[1, 5] =  4 * l3
    dphi[1, 6] =  0
    dphi[1, 7] = -4 * l1
    dphi[1, 8] =  4 * (l4 - l2)
    dphi[1, 9] = -4 * l3

    dphi[2, 0] =  0
    dphi[2, 1] =  0
    dphi[2, 2] =  4 * l3 - 1
    dphi[2, 3] = -4 * l4 + 1
    dphi[2, 4] =  0
    dphi[2, 5] =  4 * l2
    dphi[2, 6] =  4 * l1
    dphi[2, 7] = -4 * l1
    dphi[2, 8] = -4 * l2
    dphi[2, 9] =  4 * (l4 - l3)

    return phi, dphi

# fmt: on

def velpartT4C(ee, coord, connect, rho, omega: np.ndarray, Pe, index=None):
    """ Recovering the particle velocity.
    """  
    # -------
    ncalc = 10
    # Seguir elem. coords. de acordo com connectiv.
    p_calc = np.array([ [1.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0],
                        [0.0, 0.0, 0.0],
                        [0.5, 0.5, 0.0],
                        [0.0, 0.5, 0.5],
                        [0.5, 0.0, 0.5],
                        [0.5, 0.0, 0.0],
                        [0.0, 0.5, 0.0],
                        [0.0, 0.0, 0.5] ], dtype=float)

    B = np.zeros((3,10))

    # integration
    for i in range(ncalc):

        if i != index:
            continue

        l1, l2, l3 = p_calc[i, 0], p_calc[i, 1], p_calc[i, 2]
        phi, dphi = shape10TC(l1,l2,l3)

        ie = connect[ee, 1:]
        dxdydz = dphi @ coord[ie, 1:10] 
        # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
        JAC = np.array([[dxdydz[0,0], dxdydz[0,1], dxdydz[0,2]],
                        [dxdydz[1,0], dxdydz[1,1], dxdydz[1,2]],
                        [dxdydz[2,0], dxdydz[2,1], dxdydz[2,2]]], dtype=float) 

        #Inverse Jacobian
        iJAC = np.linalg.inv(JAC)

        dphi_t = iJAC @ dphi

        for iii in range(10):
            B[0,iii] = dphi_t[0,iii]
            B[1,iii] = dphi_t[1,iii]
            B[2,iii] = dphi_t[2,iii]

        Vk = -(1/(1j*rho*omega)) * (B@Pe)

    return Vk