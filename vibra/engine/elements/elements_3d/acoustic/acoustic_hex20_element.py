# fmt: off

from vibra.engine.elements.solid_elements import Element3D

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

import logging
import numpy as np

class ACT_HEXAHEDRON_20C(Element3D):

    NODES_PER_ELEMENT = 20
    DOF_PER_NODE = 1
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivity = None
        self.element_label = "acoustic_hexahedron_20"

        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.solids_connectivity = self.model.mesh.solids_connectivity

        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.solids_connectivity)

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def define_integration_points(self, integration_points: int = 27):
        """ 
        This method defines the integration points and their
        weights for numerical integration.
        """
        self.nint = integration_points
        self.num_int_data = self.integration_points_data_for_hexahedrons(integration_points)
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

        ## coordinates from integration points
        xi_1 = self.num_int_data[:, 0]
        xi_2 = self.num_int_data[:, 1]
        xi_3 = self.num_int_data[:, 2]

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

        phi[:, 0, 0] = (1 - xi_1) * (1 - xi_2) * (1 - xi_3) * (-xi_1 - xi_2 - xi_3 - 2) / 8      # ->      (-1.0, -1.0, -1.0)   Node 1
        phi[:, 0, 1] = (1 + xi_1) * (1 - xi_2) * (1 - xi_3) * ( xi_1 - xi_2 - xi_3 - 2) / 8      # ->      ( 1.0, -1.0, -1.0)   Node 2
        phi[:, 0, 2] = (1 + xi_1) * (1 + xi_2) * (1 - xi_3) * ( xi_1 + xi_2 - xi_3 - 2) / 8      # ->      ( 1.0,  1.0, -1.0)   Node 3
        phi[:, 0, 3] = (1 - xi_1) * (1 + xi_2) * (1 - xi_3) * (-xi_1 + xi_2 - xi_3 - 2) / 8      # ->      (-1.0,  1.0, -1.0)   Node 4
        phi[:, 0, 4] = (1 - xi_1) * (1 - xi_2) * (1 + xi_3) * (-xi_1 - xi_2 + xi_3 - 2) / 8      # ->      (-1.0, -1.0,  1.0)   Node 5
        phi[:, 0, 5] = (1 + xi_1) * (1 - xi_2) * (1 + xi_3) * ( xi_1 - xi_2 + xi_3 - 2) / 8      # ->      ( 1.0, -1.0,  1.0)   Node 6
        phi[:, 0, 6] = (1 + xi_1) * (1 + xi_2) * (1 + xi_3) * ( xi_1 + xi_2 + xi_3 - 2) / 8      # ->      ( 1.0,  1.0,  1.0)   Node 7
        phi[:, 0, 7] = (1 - xi_1) * (1 + xi_2) * (1 + xi_3) * (-xi_1 + xi_2 + xi_3 - 2) / 8      # ->      (-1.0,  1.0,  1.0)   Node 8

        phi[:, 0, 8 ] = (1 - xi_1**2) * (1 - xi_2) * (1 - xi_3) / 4                              # ->      ( 0.0, -1.0, -1.0)   Node 9
        phi[:, 0, 9 ] = (1 + xi_1) * (1 - xi_2**2) * (1 - xi_3) / 4                              # ->      ( 1.0,  0.0, -1.0)   Node 10
        phi[:, 0, 10] = (1 - xi_1**2) * (1 + xi_2) * (1 - xi_3) / 4                              # ->      ( 0.0,  1.0, -1.0)   Node 11
        phi[:, 0, 11] = (1 - xi_1) * (1 - xi_2**2) * (1 - xi_3) / 4                              # ->      (-1.0,  0.0, -1.0)   Node 12
        phi[:, 0, 12] = (1 - xi_1**2) * (1 - xi_2) * (1 + xi_3) / 4                              # ->      ( 0.0, -1.0,  1.0)   Node 17
        phi[:, 0, 13] = (1 + xi_1) * (1 - xi_2**2) * (1 + xi_3) / 4                              # ->      ( 1.0,  0.0,  1.0)   Node 18
        phi[:, 0, 14] = (1 - xi_1**2) * (1 + xi_2) * (1 + xi_3) / 4                              # ->      ( 0.0,  1.0,  1.0)   Node 19
        phi[:, 0, 15] = (1 - xi_1) * (1 - xi_2**2) * (1 + xi_3) / 4                              # ->      (-1.0,  0.0,  1.0)   Node 20
        phi[:, 0, 16] = (1 - xi_1) * (1 - xi_2) * (1 - xi_3**2) / 4                              # ->      (-1.0, -1.0,  0.0)   Node 13
        phi[:, 0, 17] = (1 + xi_1) * (1 - xi_2) * (1 - xi_3**2) / 4                              # ->      ( 1.0, -1.0,  0.0)   Node 14
        phi[:, 0, 18] = (1 + xi_1) * (1 + xi_2) * (1 - xi_3**2) / 4                              # ->      ( 1.0,  1.0,  0.0)   Node 15
        phi[:, 0, 19] = (1 - xi_1) * (1 + xi_2) * (1 - xi_3**2) / 4                              # ->      (-1.0,  1.0,  0.0)   Node 16

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((Nz, 3, self.NODES_PER_ELEMENT), dtype=float)

        dphi[:, 0, 0 ] =  (1 - xi_2) * (1 - xi_3) * (2*xi_1 + xi_2 + xi_3 + 1) / 8
        dphi[:, 0, 1 ] =  (1 - xi_2) * (1 - xi_3) * (2*xi_1 - xi_2 - xi_3 - 1) / 8
        dphi[:, 0, 2 ] =  (1 + xi_2) * (1 - xi_3) * (2*xi_1 + xi_2 - xi_3 - 1) / 8
        dphi[:, 0, 3 ] =  (1 + xi_2) * (1 - xi_3) * (2*xi_1 - xi_2 + xi_3 + 1) / 8
        dphi[:, 0, 4 ] =  (1 - xi_2) * (1 + xi_3) * (2*xi_1 + xi_2 - xi_3 + 1) / 8
        dphi[:, 0, 5 ] =  (1 - xi_2) * (1 + xi_3) * (2*xi_1 - xi_2 + xi_3 - 1) / 8
        dphi[:, 0, 6 ] =  (1 + xi_2) * (1 + xi_3) * (2*xi_1 + xi_2 + xi_3 - 1) / 8
        dphi[:, 0, 7 ] =  (1 + xi_2) * (1 + xi_3) * (2*xi_1 - xi_2 - xi_3 + 1) / 8
        dphi[:, 0, 8 ] = (-2*xi_1) * (1 - xi_2) * (1 - xi_3) / 4
        dphi[:, 0, 9 ] = (1) * (1 - xi_2**2) * (1 - xi_3) / 4
        dphi[:, 0, 10] = (-2*xi_1) * (1 + xi_2) * (1 - xi_3) / 4
        dphi[:, 0, 11] = (-1) * (1 - xi_2**2) * (1 - xi_3) / 4
        dphi[:, 0, 12] = (-2*xi_1) * (1 - xi_2) * (1 + xi_3) / 4
        dphi[:, 0, 13] = (1) * (1 - xi_2**2) * (1 + xi_3) / 4
        dphi[:, 0, 14] = (-2*xi_1) * (1 + xi_2) * (1 + xi_3) / 4
        dphi[:, 0, 15] = (-1) * (1 - xi_2**2) * (1 + xi_3) / 4
        dphi[:, 0, 16] = (-1) * (1 - xi_2) * (1 - xi_3**2) / 4
        dphi[:, 0, 17] = (1) * (1 - xi_2) * (1 - xi_3**2) / 4
        dphi[:, 0, 18] = (1) * (1 + xi_2) * (1 - xi_3**2) / 4
        dphi[:, 0, 19] = (-1) * (1 + xi_2) * (1 - xi_3**2) / 4

        dphi[:, 1, 0 ] = (1 - xi_1) * (1 - xi_3) * ( xi_1 + 2*xi_2 + xi_3 + 1) / 8
        dphi[:, 1, 1 ] = (1 + xi_1) * (1 - xi_3) * (-xi_1 + 2*xi_2 + xi_3 + 1) / 8
        dphi[:, 1, 2 ] = (1 + xi_1) * (1 - xi_3) * ( xi_1 + 2*xi_2 - xi_3 - 1) / 8
        dphi[:, 1, 3 ] = (1 - xi_1) * (1 - xi_3) * (-xi_1 + 2*xi_2 - xi_3 - 1) / 8 
        dphi[:, 1, 4 ] = (1 - xi_1) * (1 + xi_3) * ( xi_1 + 2*xi_2 - xi_3 + 1) / 8
        dphi[:, 1, 5 ] = (1 + xi_1) * (1 + xi_3) * (-xi_1 + 2*xi_2 - xi_3 + 1) / 8
        dphi[:, 1, 6 ] = (1 + xi_1) * (1 + xi_3) * ( xi_1 + 2*xi_2 + xi_3 - 1) / 8
        dphi[:, 1, 7 ] = (1 - xi_1) * (1 + xi_3) * (-xi_1 + 2*xi_2 + xi_3 - 1) / 8
        dphi[:, 1, 8 ] = (1 - xi_1**2) * (-1) * (1 - xi_3) / 4
        dphi[:, 1, 9 ] = (1 + xi_1) * (-2*xi_2) * (1 - xi_3) / 4
        dphi[:, 1, 10] = (1 - xi_1**2) * (1) * (1 - xi_3) / 4
        dphi[:, 1, 11] = (1 - xi_1) * (-2*xi_2) * (1 - xi_3) / 4
        dphi[:, 1, 12] = (1 - xi_1**2) * (-1) * (1 + xi_3) / 4
        dphi[:, 1, 13] = (1 + xi_1) * (-2*xi_2) * (1 + xi_3) / 4
        dphi[:, 1, 14] = (1 - xi_1**2) * (1) * (1 + xi_3) / 4
        dphi[:, 1, 15] = (1 - xi_1) * (-2*xi_2) * (1 + xi_3) / 4
        dphi[:, 1, 16] = (1 - xi_1) * (-1) * (1 - xi_3**2) / 4
        dphi[:, 1, 17] = (1 + xi_1) * (-1) * (1 - xi_3**2) / 4
        dphi[:, 1, 18] = (1 + xi_1) * (1) * (1 - xi_3**2) / 4
        dphi[:, 1, 19] = (1 - xi_1) * (1) * (1 - xi_3**2) / 4

        dphi[:, 2, 0 ] = (1 - xi_1) * (1 - xi_2) * ( xi_1 + xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 1 ] = (1 + xi_1) * (1 - xi_2) * (-xi_1 + xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 2 ] = (1 + xi_1) * (1 + xi_2) * (-xi_1 - xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 3 ] = (1 - xi_1) * (1 + xi_2) * ( xi_1 - xi_2 + 2*xi_3 + 1) / 8
        dphi[:, 2, 4 ] = (1 - xi_1) * (1 - xi_2) * (-xi_1 - xi_2 + 2*xi_3 - 1) / 8
        dphi[:, 2, 5 ] = (1 + xi_1) * (1 - xi_2) * ( xi_1 - xi_2 + 2*xi_3 - 1) / 8 
        dphi[:, 2, 6 ] = (1 + xi_1) * (1 + xi_2) * ( xi_1 + xi_2 + 2*xi_3 - 1) / 8
        dphi[:, 2, 7 ] = (1 - xi_1) * (1 + xi_2) * (-xi_1 + xi_2 + 2*xi_3 - 1) / 8
        dphi[:, 2, 8 ] = (1 - xi_1**2) * (1 - xi_2) * (-1) / 4
        dphi[:, 2, 9 ] = (1 + xi_1) * (1 - xi_2**2) * (-1) / 4
        dphi[:, 2, 10] = (1 - xi_1**2) * (1 + xi_2) * (-1) / 4
        dphi[:, 2, 11] = (1 - xi_1) * (1 - xi_2**2) * (-1) / 4
        dphi[:, 2, 12] = (1 - xi_1**2) * (1 - xi_2) * (1) / 4
        dphi[:, 2, 13] = (1 + xi_1) * (1 - xi_2**2) * (1) / 4
        dphi[:, 2, 14] = (1 - xi_1**2) * (1 + xi_2) * (1) / 4
        dphi[:, 2, 15] = (1 - xi_1) * (1 - xi_2**2) * (1) / 4
        dphi[:, 2, 16] = (1 - xi_1) * (1 - xi_2) * (-2*xi_3) / 4
        dphi[:, 2, 17] = (1 + xi_1) * (1 - xi_2) * (-2*xi_3) / 4
        dphi[:, 2, 18] = (1 + xi_1) * (1 + xi_2) * (-2*xi_3) / 4
        dphi[:, 2, 19] = (1 - xi_1) * (1 + xi_2) * (-2*xi_3) / 4

        if Nz == 1:
            return phi[0, :, :], dphi[0, :, :]

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

        # filter the acoustic elements connectivities
        element_ids = self.model.elements_per_domain.get("acoustic", np.array([]))
        acoustic_connect = self.connectivity[element_ids, :]

        nel = len(acoustic_connect)

        stacked_coords = np.zeros((nel, self.DOF_PER_ELEMENT, 3), dtype=float)
        for j in range(self.DOF_PER_ELEMENT):
            stacked_coords[:, j, :] = self.nodal_coordinates[acoustic_connect[:, j + 1], 1:4]

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
            detJAC, invJAC = self.get_detJAC_and_invJAC(JAC)

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

            progress = int(25 + 55*(i / self.nint))
            logging.info(f"Processing the elementary matrices data... [{progress}/100]")

            # Jacobian matrices of all elements
            JAC_stacked = self.dphi[i, :, :] @ stacked_coords

            # Jacobian determinants and inverses of all elements
            det_jacs, inv_jacs = self.get_detJAC_and_invJAC(JAC_stacked)

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

        ## calculation points (adapted from Atalla and Sgard, 2015, pg. 171)
        p_calc = np.array([ 
            [-1.0, -1.0, -1.0],      # ->      (-1.0, -1.0, -1.0)   Node 1
            [ 1.0, -1.0, -1.0],      # ->      ( 1.0, -1.0, -1.0)   Node 2
            [ 1.0,  1.0, -1.0],      # ->      ( 1.0,  1.0, -1.0)   Node 3
            [-1.0,  1.0, -1.0],      # ->      (-1.0,  1.0, -1.0)   Node 4
            [-1.0, -1.0,  1.0],      # ->      (-1.0, -1.0,  1.0)   Node 5
            [ 1.0, -1.0,  1.0],      # ->      ( 1.0, -1.0,  1.0)   Node 6
            [ 1.0,  1.0,  1.0],      # ->      ( 1.0,  1.0,  1.0)   Node 7
            [-1.0,  1.0,  1.0],      # ->      (-1.0,  1.0,  1.0)   Node 8
            [ 0.0, -1.0, -1.0],      # ->      ( 0.0, -1.0, -1.0)   Node 9
            [ 1.0,  0.0, -1.0],      # ->      ( 1.0,  0.0, -1.0)   Node 10
            [ 0.0,  1.0, -1.0],      # ->      ( 0.0,  1.0, -1.0)   Node 11
            [-1.0,  0.0, -1.0],      # ->      (-1.0,  0.0, -1.0)   Node 12
            [ 0.0, -1.0,  1.0],      # ->      ( 0.0, -1.0,  1.0)   Node 17
            [ 1.0,  0.0,  1.0],      # ->      ( 1.0,  0.0,  1.0)   Node 18
            [ 0.0,  1.0,  1.0],      # ->      ( 0.0,  1.0,  1.0)   Node 19
            [-1.0,  0.0,  1.0],      # ->      (-1.0,  0.0,  1.0)   Node 20
            [-1.0, -1.0,  0.0],      # ->      (-1.0, -1.0,  0.0)   Node 13
            [ 1.0, -1.0,  0.0],      # ->      ( 1.0, -1.0,  0.0)   Node 14
            [ 1.0,  1.0,  0.0],      # ->      ( 1.0,  1.0,  0.0)   Node 15
            [-1.0,  1.0,  0.0],      # ->      (-1.0,  1.0,  0.0)   Node 16
            ], dtype=float)

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


    def elementary_matrices_base(self, el_index):
        """H20 stiffness and mass matrices."""

        ie = self.connectivity[el_index, 1:]
        JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = self.get_detJAC_and_invJAC(JAC)
        dphi_t = invJAC @ self.dphi

        B = np.zeros((self.nint, 3, self.DOF_PER_ELEMENT_3D), dtype=float)
        B[:, 0, :] = dphi_t[:, 0, :]
        B[:, 1, :] = dphi_t[:, 1, :]
        B[:, 2, :] = dphi_t[:, 2, :]

        N = np.zeros((self.nint, 1, self.DOF_PER_ELEMENT_3D), dtype=float)
        N[:, 0, :] = self.phi

        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            Ke += B[i, :, :].T @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])
            Me += N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i])
            # Me += (1 / c_0**2) * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i])

        return Ke, Me


    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        if self.solids_connectivity.shape[1] == self.NODES_PER_ELEMENT + 4:
            self.connectivity = self.solids_connectivity[
                :, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19]
            ]


    def generate_ind_rows_cols(self, reorder: bool = True):
        """ 
        This method processess the dof indices (rows and columns) 
        for assembly
        """

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.solids_connectivity[
                :, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]

        # filter the acoustic elements connectivities
        element_ids = self.model.elements_per_domain.get("acoustic", np.array([]))
        acoustic_connect = self.connectivity[element_ids, :]

        dof, edof = self.DOF_PER_NODE, self.DOF_PER_ELEMENT
        n_el = element_ids.size

        local_dof = np.arange(dof, dtype=int)
        ind_dof = np.zeros((n_el, edof), dtype=int)

        for j in range(self.NODES_PER_ELEMENT):
            start = j * dof
            end = (j + 1) * dof
            elem_nodes = self.model.fluid_node_mapping[acoustic_connect[:, j + 1]]
            ind_dof[:, start : end] = dof * elem_nodes.reshape(-1, 1) + local_dof

        vect_indices = ind_dof.flatten()
        ordered_dofs = np.unique(vect_indices)

        ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        ind_cols = (np.tile(ind_dof, edof)).flatten()

        return ind_rows, ind_cols, ordered_dofs