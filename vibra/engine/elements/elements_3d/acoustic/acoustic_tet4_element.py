
from typing import TYPE_CHECKING

from vibra.engine.elements.solid_elements import Element3D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import logging

import numpy as np


class ACT_TETRAHEDRON_4C(Element3D):

    dof_per_node = 1
    nodes_per_element = 4
    dof_per_element = nodes_per_element * dof_per_node

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivities = None
        self.element_label = "acoustic_tetrahedron_4"

        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.solids_connectivity = self.model.mesh.solids_connectivity

        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.solids_connectivity)

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def update_nodal_coordinates(self, nodal_coordinates: np.ndarray):
        self.nodal_coordinates = nodal_coordinates


    def define_integration_points(self, integration_points: int=4):
        """ 
        This method defines the integration points and their
        weights for numerical integration.
        """
        self.nint = integration_points
        self.num_int_data = self.integration_points_data_for_tetrahedrons(integration_points)
        self.wps = self.num_int_data[:, -1].reshape(-1, 1, 1)


    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """

        xi_1 = self.num_int_data[:, 0]
        xi_2 = self.num_int_data[:, 1]
        xi_3 = self.num_int_data[:, 2]

        self.phi, self.dphi = self.get_shape_functions_and_derivatives(xi_1, xi_2, xi_3)


    def get_shape_functions_and_derivatives(self, xi_1: np.ndarray, xi_2: np.ndarray, xi_3: np.ndarray) -> np.ndarray:

        """
        This function returns the shape functions and its derivatives.
        
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
        phi = np.zeros((Nz, 1, self.nodes_per_element), dtype=float)

        # define isoparametric coordiante xi_4
        xi_4 = 1 - xi_1 - xi_2 - xi_3

        phi[:, 0, 0] = xi_4      # ->      (0.0, 0.0, 0.0)   Node 1
        phi[:, 0, 1] = xi_2      # ->      (0.0, 1.0, 0.0)   Node 2
        phi[:, 0, 2] = xi_3      # ->      (0.0, 0.0, 1.0)   Node 3
        phi[:, 0, 3] = xi_1      # ->      (1.0, 0.0, 0.0)   Node 4

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((3, self.nodes_per_element), dtype=float)
        dphi[0, 0] = -1
        dphi[0, 1] =  0
        dphi[0, 2] =  0
        dphi[0, 3] =  1

        dphi[1, 0] = -1
        dphi[1, 1] =  1
        dphi[1, 2] =  0
        dphi[1, 3] =  0

        dphi[2, 0] = -1
        dphi[2, 1] =  0
        dphi[2, 2] =  1
        dphi[2, 3] =  0

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

        # Jacobian matrix
        JAC = self.dphi @ coords

        # Jacobian determinant and inverse
        det_jac, invJAC = self.get_detJAC_and_invJAC(JAC)

        # derivative of shape functions
        B = invJAC @ self.dphi

        # initialize variables
        int2d_BtB = 0.
        int2d_NtN = 0.

        # integration loop
        for i in range(self.nint):

            # shape functions
            N = self.phi[i, :]

            int2d_BtB += B.T @ B * (det_jac * self.wps[i])
            int2d_NtN += N.T @ N * (det_jac * self.wps[i])

        # # shape functions
        # N = self.phi

        # int2d_BtB = B.T @ B * (det_jac * self.wps) * self.nint
        # int2d_NtN = N.T @ N * (det_jac * self.wps)

        return int2d_BtB, int2d_NtN


    def stacked_elementary_matrices_NtN_BtB(self):
        """
        This method computes all mass and stiffness matrices in
        stacked form.

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
            self.dof_per_node, 
            self.nodes_per_element,
            )

        stacked_coords = element_data_proc.get_stacked_nodal_coords(self.connectivities)

        # Jacobian matrices of all elements
        JAC_stacked = self.dphi @ stacked_coords

        # Jacobian determinants and inverses of all elements
        det_jacs, inv_jacs = self.get_detJAC_and_invJAC(JAC_stacked)

        # derivative of shape functions
        B = inv_jacs @ self.dphi
        B_t = np.transpose(B, axes=(0, 2, 1))

        # initialize variables
        int2d_BtB = 0.
        int2d_NtN = 0.

        # integration loop
        for i in range(self.nint):

            progress = int(25 + 55*(i / self.nint))
            logging.info(f"Processing the elementary matrices data... [{progress}/100]")

            # shape functions
            N = self.phi[i, :]
            N_t = N.T

            int2d_BtB += B_t @ B * (det_jacs * self.wps[i])
            int2d_NtN += N_t @ N * (det_jacs * self.wps[i])

        # # shape functions
        # N = self.phi
        # N_t = N.T

        # # derivative of shape functions
        # B = inv_jacs @ self.dphi
        # B_t = np.transpose(B, axes=(0, 2, 1))

        # int2d_BtB = B_t @ B * (det_jacs * self.wps) * self.nint
        # int2d_NtN = N_t @ N * (det_jacs * self.wps)

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
            return 0.

        omega = 2 * np.pi * frequencies

        if self.connectivities is None:
            self.reorder_connect()

        ## calculation points (Atalla and Sgard, 2015, pg. 170)
        p_calc = np.array([ [ 0, 0, 0 ],
                            [ 0, 1, 0 ],
                            [ 1, 0, 0 ],
                            [ 0, 0, 1 ] ], dtype=float)

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
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        if self.solids_connectivity.shape[1] == self.nodes_per_element + 4:
            self.connectivities = self.solids_connectivity[:, [6, 4, 5, 7]]


    def generate_ind_rows_cols(self, reorder: bool = True):
        """ This method processess the dof indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivities = self.solids_connectivity[:, [4, 5, 6, 7]]

        dof_indexes = self.dof_indexes_processor(
            self.model,
            "acoustic",
            self.dof_per_node,
            self.nodes_per_element,
            )

        return dof_indexes.get_rows_and_cols_indices_3D(self.connectivities)