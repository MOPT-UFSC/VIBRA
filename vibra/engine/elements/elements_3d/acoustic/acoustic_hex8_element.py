# fmt: off

from vibra.engine.elements.solid_elements import Element3D

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


def get_detJAC_and_invJAC(JAC: np.ndarray):
    """
    This function computes the determinant and inverse of Jacobian matrix. If multiple 
    Jacobian matrices are inputed in the form of a stacked 3D matrix, then, the deteterminant 
    and inverse of Jacobian matrix will be calculated for all elements.

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


class ACT_HEXAHEDRON_8C(Element3D):

    NODES_PER_ELEMENT = 8
    DOF_PER_NODE = 1
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivity = None
        self.element_label = "acoustic_hexahedron_8"

        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.solids_connectivity = self.model.mesh.solids_connectivity

        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.solids_connectivity)

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def define_integration_points(self, integration_points: int=8):
        """
        This method defines the integration points and their
        weights for numerical integration.
        """
        # 8-node hexahedron integration rule (Atalla and Sgard, 2015, pg. 182)
        if integration_points == 8:
       
            self.nint = 8
            a = 1 / np.sqrt(3)
            w1 = 1

            self.pint = np.array( [ [-a, -a, -a],
                                    [ a, -a, -a],
                                    [ a,  a, -a],
                                    [-a,  a, -a],
                                    [-a, -a,  a],
                                    [ a, -a,  a],
                                    [ a,  a,  a],
                                    [-a,  a,  a] ], dtype=float)

            self.wps = np.array([w1, w1, w1, w1, w1, w1, w1, w1], dtype=float)


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

        xi_1 = self.pint[:, 0]
        xi_2 = self.pint[:, 1]
        xi_3 = self.pint[:, 2]

        self.phi, self.dphi = self.get_shape_functions_and_derivatives(xi_1, xi_2, xi_3)


    def get_shape_functions_and_derivatives(self, xi_1: np.ndarray|float, xi_2: np.ndarray|float, xi_3: np.ndarray|float):

        """
        This method returns the shape functions and its derivatives.
        
        Parameters
        ----------
        xi_1: np.ndarray
            The x coordinates of the integration points.
        
        xi_2: np.ndarray
            The y coordinates of the integration points.

        xi_3: np.ndarray
            The z coordinates of the integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        if isinstance(xi_1, np.ndarray):
            Nz = xi_1.size
        else:
            Nz = 1

        ##NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015

        # define the shape functions (Atalla and Sgard, 2015, pg. 171)
        phi = np.zeros((Nz, 1, self.NODES_PER_ELEMENT), dtype=float)

        phi[:, 0, 0] = (1.0 - xi_1) * (1.0 - xi_2) * (1.0 - xi_3) / 8       # ->      (-1.0, -1.0, -1.0)   Node 1
        phi[:, 0, 1] = (1.0 + xi_1) * (1.0 - xi_2) * (1.0 - xi_3) / 8       # ->      ( 1.0, -1.0, -1.0)   Node 2
        phi[:, 0, 2] = (1.0 + xi_1) * (1.0 + xi_2) * (1.0 - xi_3) / 8       # ->      ( 1.0,  1.0, -1.0)   Node 3
        phi[:, 0, 3] = (1.0 - xi_1) * (1.0 + xi_2) * (1.0 - xi_3) / 8       # ->      (-1.0,  1.0, -1.0)   Node 4
        phi[:, 0, 4] = (1.0 - xi_1) * (1.0 - xi_2) * (1.0 + xi_3) / 8       # ->      (-1.0, -1.0,  1.0)   Node 5
        phi[:, 0, 5] = (1.0 + xi_1) * (1.0 - xi_2) * (1.0 + xi_3) / 8       # ->      ( 1.0, -1.0,  1.0)   Node 6
        phi[:, 0, 6] = (1.0 + xi_1) * (1.0 + xi_2) * (1.0 + xi_3) / 8       # ->      ( 1.0,  1.0,  1.0)   Node 7
        phi[:, 0, 7] = (1.0 - xi_1) * (1.0 + xi_2) * (1.0 + xi_3) / 8       # ->      (-1.0,  1.0,  1.0)   Node 8

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((self.nint, 3, self.NODES_PER_ELEMENT), dtype=float)

        dphi[:, 0, 0] = -(1.0 - xi_2) * (1.0 - xi_3) / 8
        dphi[:, 0, 1] =  (1.0 - xi_2) * (1.0 - xi_3) / 8
        dphi[:, 0, 2] =  (1.0 + xi_2) * (1.0 - xi_3) / 8
        dphi[:, 0, 3] = -(1.0 + xi_2) * (1.0 - xi_3) / 8
        dphi[:, 0, 4] = -(1.0 - xi_2) * (1.0 + xi_3) / 8
        dphi[:, 0, 5] =  (1.0 - xi_2) * (1.0 + xi_3) / 8
        dphi[:, 0, 6] =  (1.0 + xi_2) * (1.0 + xi_3) / 8
        dphi[:, 0, 7] = -(1.0 + xi_2) * (1.0 + xi_3) / 8

        dphi[:, 1, 0] = -(1.0 - xi_1) * (1.0 - xi_3) / 8
        dphi[:, 1, 1] = -(1.0 + xi_1) * (1.0 - xi_3) / 8
        dphi[:, 1, 2] =  (1.0 + xi_1) * (1.0 - xi_3) / 8
        dphi[:, 1, 3] =  (1.0 - xi_1) * (1.0 - xi_3) / 8
        dphi[:, 1, 4] = -(1.0 - xi_1) * (1.0 + xi_3) / 8
        dphi[:, 1, 5] = -(1.0 + xi_1) * (1.0 + xi_3) / 8
        dphi[:, 1, 6] =  (1.0 + xi_1) * (1.0 + xi_3) / 8
        dphi[:, 1, 7] =  (1.0 - xi_1) * (1.0 + xi_3) / 8

        dphi[:, 2, 0] = -(1.0 - xi_1) * (1.0 - xi_2) / 8
        dphi[:, 2, 1] = -(1.0 + xi_1) * (1.0 - xi_2) / 8
        dphi[:, 2, 2] = -(1.0 + xi_1) * (1.0 + xi_2) / 8
        dphi[:, 2, 3] = -(1.0 - xi_1) * (1.0 + xi_2) / 8
        dphi[:, 2, 4] =  (1.0 - xi_1) * (1.0 - xi_2) / 8
        dphi[:, 2, 5] =  (1.0 + xi_1) * (1.0 - xi_2) / 8
        dphi[:, 2, 6] =  (1.0 + xi_1) * (1.0 + xi_2) / 8
        dphi[:, 2, 7] =  (1.0 - xi_1) * (1.0 + xi_2) / 8

        return phi, dphi


    def get_stacked_nodal_coords(self) -> np.ndarray:
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

        stacked_coords = np.zeros((nel, self.DOF_PER_ELEMENT, 3), dtype=float)
        for j in range(self.DOF_PER_ELEMENT):
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
            N = self.phi[i, :, :]

            # derivative of shape functions
            B = invJAC @ self.dphi[i, :, :]

            Ke += B.T @ B * (detJAC * self.wps[i])
            Me += N.T @ N * (detJAC * self.wps[i])

        # if el_index == 0:

        #     Ke_base, Me_base = self.elementary_matrices_base(el_index=el_index)
        #     np.savetxt("Me_base.dat", Me_base, fmt="%.16e", delimiter=",")
        #     np.savetxt("Ke_base.dat", Ke_base, fmt="%.16e", delimiter=",")

        #     np.savetxt("Me_new.dat", Me, fmt="%.16e", delimiter=",")
        #     np.savetxt("Ke_new.dat", Ke, fmt="%.16e", delimiter=",")

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
            det_jacs, inv_jacs = get_detJAC_and_invJAC(JAC_stacked)

            # shape functions
            N = self.phi[i, :, :]
            N_t = N.T

            # derivative of shape functions
            B = inv_jacs @ self.dphi[i, :, :]
            B_t = np.transpose(B, axes=(0, 2, 1))

            int2d_BtB += B_t @ B * (det_jacs * self.wps[i])
            int2d_NtN += N_t @ N * (det_jacs * self.wps[i])

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

        ## calculation points (Atalla and Sgard, 2015, pg. 170)
        p_calc = np.array([
            [-1.0, -1.0, -1.0],      # ->      (-1.0, -1.0, -1.0)   Node 1
            [ 1.0, -1.0, -1.0],      # ->      ( 1.0, -1.0, -1.0)   Node 2
            [ 1.0,  1.0, -1.0],      # ->      ( 1.0,  1.0, -1.0)   Node 3
            [-1.0,  1.0, -1.0],      # ->      (-1.0,  1.0, -1.0)   Node 4
            [-1.0, -1.0,  1.0],      # ->      (-1.0, -1.0,  1.0)   Node 5
            [ 1.0, -1.0,  1.0],      # ->      ( 1.0, -1.0,  1.0)   Node 6
            [ 1.0,  1.0,  1.0],      # ->      ( 1.0,  1.0,  1.0)   Node 7
            [-1.0,  1.0,  1.0],      # ->      (-1.0,  1.0,  1.0)   Node 8
            ], dtype=float)

        index = np.where(node_ids==node_id)[0]
        if index.size != 1:
            return None

        # local coordinates
        # (ssx, ttx, rrx) = p_calc[index[0], :]
        ssx, ttx, rrx = p_calc[:, 0], p_calc[:, 1], p_calc[:, 2]

        # derivative of the shape function at the selected point
        _, dphi = self.get_shape_functions_and_derivatives(ssx, ttx, rrx)

        # nodal coordinates from element
        coords = self.nodal_coordinates[node_ids, 1:4]

        # Jacobian matrix
        # JAC = dphi @ coords
        JAC = dphi[index[0], :, :] @ coords

        # inverse of Jacobian matrix
        _, invJAC = get_detJAC_and_invJAC(JAC)

        # derivative of shape functions
        # B = invJAC @ dphi
        B = invJAC @ dphi[index[0], :, :]

        # calculate the particle velocities components
        particle_velocity = -(1 / (1j * rho * omega)) * (B @ Pe)

        return particle_velocity


    def elementary_matrices_base(self, el_index):
        """H8 stiffness and mass matrices."""

        ie = self.connectivity[el_index, 1:]
        JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = get_detJAC_and_invJAC(JAC)
        dphi_t = invJAC @ self.dphi

        B = np.zeros((self.nint, 3, self.DOF_PER_ELEMENT), dtype=float)
        B[:, 0, :] = dphi_t[:, 0, :]
        B[:, 1, :] = dphi_t[:, 1, :]
        B[:, 2, :] = dphi_t[:, 2, :]

        N = np.zeros((self.nint, 1, self.DOF_PER_ELEMENT), dtype=float)
        N[:, 0, :] = self.phi[:, 0, :]

        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            Ke += B[i, :, :].T @ B[i, :, :] * (detJAC[i, :, :] * self.wps)
            Me += N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps)

        return Ke, Me


    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        if self.solids_connectivity.shape[1] == self.NODES_PER_ELEMENT + 4:
            self.connectivity = self.solids_connectivity[:, [0, 4, 5, 6, 7, 8, 9, 10, 11]]


    def generate_ind_rows_cols(self, reorder: bool = True):
        """This method processess the dof indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.solids_connectivity[:, [0, 4, 5, 6, 7, 8, 9, 10, 11]]

        dof, edof = self.DOF_PER_NODE, self.DOF_PER_ELEMENT
        ind_dof = dof * self.connectivity[:, 1:]

        vect_indices = ind_dof.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dof, edof)).flatten()

        return self.ind_rows, self.ind_cols