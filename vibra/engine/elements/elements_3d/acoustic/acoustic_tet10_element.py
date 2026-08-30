
from typing import TYPE_CHECKING

from vibra.engine.elements.solid_elements import Element3D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import logging

import numpy as np


def get_all_detJAC_and_invJAC(JAC: np.ndarray):

    """
    This method computes the determinant and inverse of Jacobian
    matrix for all elements for one integration points or all 
    integration points.

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

    return det_jac, (1 / det_jac) * adj_matrix


class ACT_TETRAHEDRON_10C(Element3D):

    NODES_PER_ELEMENT = 10
    DOF_PER_NODE = 1
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivities = None
        self.element_label = "acoustic_tetrahedron_10"

        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.solids_connectivity = self.model.mesh.solids_connectivity

        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.solids_connectivity)

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def update_nodal_coordinates(self, nodal_coordinates: np.ndarray):
        self.nodal_coordinates = nodal_coordinates


    def define_integration_points(self, integration_points: int=11):
        """ 
        This method defines the integration points and their
        weights for numerical integration.
        """
        self.nint = integration_points
        self.num_int_data = self.integration_points_data_for_tetrahedrons(integration_points)
        self.wps = self.num_int_data[:, -1].reshape(-1, 1, 1)


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

        xi_1 = self.num_int_data[:, 0]
        xi_2 = self.num_int_data[:, 1]
        xi_3 = self.num_int_data[:, 2]

        self.phi, self.dphi = self.get_shape_functions_and_derivatives(xi_1, xi_2, xi_3)


    def get_shape_functions_and_derivatives(self, xi_1: np.ndarray | float, xi_2: np.ndarray | float, xi_3: np.ndarray | float):

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

        # define the shape functions (Atalla and Sgard, 2015, pg. 170)
        phi = np.zeros((Nz, 1, self.NODES_PER_ELEMENT), dtype=float)

        # define the isoparametric coordiante l4
        xi_4 = 1 - xi_1 - xi_2 - xi_3

        phi[:, 0, 0] = (2 * xi_4 - 1) * xi_4       # ->      (0.0, 0.0, 0.0)   Node 1
        phi[:, 0, 1] = (2 * xi_2 - 1) * xi_2       # ->      (0.0, 1.0, 0.0)   Node 2
        phi[:, 0, 2] = (2 * xi_3 - 1) * xi_3       # ->      (0.0, 0.0, 1.0)   Node 3
        phi[:, 0, 3] = (2 * xi_1 - 1) * xi_1       # ->      (1.0, 0.0, 0.0)   Node 4
        phi[:, 0, 4] = 4 * xi_4 * xi_2             # ->      (0.0, 0.5, 0.0)   Node 5
        phi[:, 0, 5] = 4 * xi_2 * xi_3             # ->      (0.0, 0.5, 0.5)   Node 6
        phi[:, 0, 6] = 4 * xi_3 * xi_4             # ->      (0.0, 0.0, 0.5)   Node 7
        phi[:, 0, 7] = 4 * xi_1 * xi_4             # ->      (0.5, 0.0, 0.0)   Node 8
        phi[:, 0, 8] = 4 * xi_1 * xi_2             # ->      (0.5, 0.5, 0.0)   Node 9
        phi[:, 0, 9] = 4 * xi_1 * xi_3             # ->      (0.5, 0.0, 0.5)   Node 10

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((Nz, 3, self.NODES_PER_ELEMENT), dtype=float)

        dphi[:, 0, 0] = -4 * xi_4 + 1
        dphi[:, 0, 1] =  0
        dphi[:, 0, 2] =  0
        dphi[:, 0, 3] =  4 * xi_1 - 1
        dphi[:, 0, 4] = -4 * xi_2
        dphi[:, 0, 5] =  0
        dphi[:, 0, 6] = -4 * xi_3
        dphi[:, 0, 7] =  4 * (xi_4 - xi_1)
        dphi[:, 0, 8] =  4 * xi_2
        dphi[:, 0, 9] =  4 * xi_3

        dphi[:, 1, 0] = -4 * xi_4 + 1
        dphi[:, 1, 1] =  4 * xi_2 - 1
        dphi[:, 1, 2] =  0
        dphi[:, 1, 3] =  0
        dphi[:, 1, 4] =  4 * (xi_4 - xi_2)
        dphi[:, 1, 5] =  4 * xi_3
        dphi[:, 1, 6] = -4 * xi_3
        dphi[:, 1, 7] = -4 * xi_1
        dphi[:, 1, 8] =  4 * xi_1
        dphi[:, 1, 9] =  0

        dphi[:, 2, 0] = -4 * xi_4 + 1
        dphi[:, 2, 1] =  0
        dphi[:, 2, 2] =  4 * xi_3 - 1
        dphi[:, 2, 3] =  0
        dphi[:, 2, 4] = -4 * xi_2
        dphi[:, 2, 5] =  4 * xi_2
        dphi[:, 2, 6] =  4 * (xi_4 - xi_3)
        dphi[:, 2, 7] = -4 * xi_1
        dphi[:, 2, 8] =  0
        dphi[:, 2, 9] =  4 * xi_1

        if Nz == 1:
            return phi[0, :, :], dphi[0, :, :]

        return phi, dphi


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
        coords = self.nodal_coordinates[elem_nodes, 1:4]

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
        element_data_proc = self.element_data_processor(
            self.model, 
            "acoustic", 
            self.DOF_PER_NODE, 
            self.NODES_PER_ELEMENT,
            )

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
            node_ids = self.connectivities[element_id, :]
    
        if isinstance(nodal_pressures, np.ndarray):
            Pe = nodal_pressures
        elif isinstance(solution, np.ndarray):
            Pe = solution[self.model.fluid_node_mapping[node_ids], :]
        else:
            return

        omega = 2 * np.pi * frequencies

        if self.connectivities is None:
            self.reorder_connect()

        ## calculation points (Atalla and Sgard, 2015, pg. 170)
        p_calc = np.array([ [0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0],
                            [1.0, 0.0, 0.0],
                            [0.0, 0.5, 0.0],
                            [0.0, 0.5, 0.5],
                            [0.0, 0.0, 0.5],
                            [0.5, 0.0, 0.0],
                            [0.5, 0.5, 0.0],
                            [0.5, 0.0, 0.5] ], dtype=float)

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
        _, invJAC = self.get_detJAC_and_invJAC(JAC)

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
            self.connectivities = self.solids_connectivity[:, [6, 4, 5, 7, 10, 8, 9, 12, 11, 13]]


    def generate_ind_rows_cols(self, reorder: bool = True):
        """This method processess the dof indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivities = self.solids_connectivity[:, [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]]

        dof_indexes = self.dof_indexes_processor(
            self.model,
            "acoustic",
            self.DOF_PER_NODE,
            self.NODES_PER_ELEMENT,
            )

        return dof_indexes.get_rows_and_cols_indices_3D(self.connectivities)


def shape10TC(l1, l2, l3):
    """This function returns the shape functions and its derivatives."""

    # shape functions
    phi = np.zeros(10, dtype=float)

    l4 = 1 - l1 - l2 - l3

    # shape functions (Atalla and Sgard, 2015, pg. 170)
    phi[0, 0] = (2 * l4 - 1) * l4       # ->      (0.0, 0.0, 0.0)   Node 1
    phi[0, 1] = (2 * l2 - 1) * l2       # ->      (0.0, 1.0, 0.0)   Node 2
    phi[0, 2] = (2 * l3 - 1) * l3       # ->      (0.0, 0.0, 1.0)   Node 3
    phi[0, 3] = (2 * l1 - 1) * l1       # ->      (1.0, 0.0, 0.0)   Node 4
    phi[0, 4] = 4 * l4 * l2             # ->      (0.0, 0.5, 0.0)   Node 5
    phi[0, 5] = 4 * l2 * l3             # ->      (0.0, 0.5, 0.5)   Node 6
    phi[0, 6] = 4 * l3 * l4             # ->      (0.0, 0.0, 0.5)   Node 7
    phi[0, 7] = 4 * l1 * l4             # ->      (0.5, 0.0, 0.0)   Node 8
    phi[0, 8] = 4 * l1 * l2             # ->      (0.5, 0.5, 0.0)   Node 9
    phi[0, 9] = 4 * l1 * l3             # ->      (0.5, 0.0, 0.5)   Node 10

    # derivatives of shape functions
    dphi = np.zeros((3, 10), dtype=float)

    ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
    dphi[0, 0] = -4 * l4 + 1
    dphi[0, 1] =  0
    dphi[0, 2] =  0
    dphi[0, 3] =  4 * l1 - 1
    dphi[0, 4] = -4 * l2
    dphi[0, 5] =  0
    dphi[0, 6] = -4 * l3
    dphi[0, 7] =  4 * (l4 - l1)
    dphi[0, 8] =  4 * l2
    dphi[0, 9] =  4 * l3

    dphi[1, 0] = -4 * l4 + 1
    dphi[1, 1] =  4 * l2 - 1
    dphi[1, 2] =  0
    dphi[1, 3] =  0
    dphi[1, 4] =  4 * (l4 - l2)
    dphi[1, 5] =  4 * l3
    dphi[1, 6] = -4 * l3
    dphi[1, 7] = -4 * l1
    dphi[1, 8] =  4 * l1
    dphi[1, 9] =  0

    dphi[2, 0] = -4 * l4 + 1
    dphi[2, 1] =  0
    dphi[2, 2] =  4 * l3 - 1
    dphi[2, 3] =  0
    dphi[2, 4] = -4 * l2
    dphi[2, 5] =  4 * l2
    dphi[2, 6] =  4 * (l4 - l3)
    dphi[2, 7] = -4 * l1
    dphi[2, 8] =  0
    dphi[2, 9] =  4 * l1

    return phi, dphi


def velpartT4C(ee, coord, connect, rho, omega: np.ndarray, Pe, index=None):
    """ Recovering the particle velocity.
    """  
    # -------
    ncalc = 10
    # Seguir elem. coords. de acordo com connectiv.

    ## calculation points (Atalla and Sgard, 2015, pg. 170)
    p_calc = np.array([ [0.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0],
                        [1.0, 0.0, 0.0],
                        [0.0, 0.5, 0.0],
                        [0.0, 0.5, 0.5],
                        [0.0, 0.0, 0.5],
                        [0.5, 0.0, 0.0],
                        [0.5, 0.5, 0.0],
                        [0.5, 0.0, 0.5] ], dtype=float)

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