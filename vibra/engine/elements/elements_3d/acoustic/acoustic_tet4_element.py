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

    det_jac = (
                  JAC[0, 0] * JAC[1, 1] * JAC[2, 2]
                + JAC[0, 1] * JAC[1, 2] * JAC[2, 0]
                + JAC[0, 2] * JAC[1, 0] * JAC[2, 1]
                ) - (
                  JAC[2, 0] * JAC[1, 1] * JAC[0, 2]
                + JAC[2, 1] * JAC[1, 2] * JAC[0, 0]
                + JAC[2, 2] * JAC[1, 0] * JAC[0, 1]
                )

    # the adjoint matrix
    AUJJ = np.zeros((3, 3), dtype=float)

    AUJJ[0, 0] =  ((JAC[1, 1] * JAC[2, 2]) - (JAC[2, 1] * JAC[1, 2]))
    AUJJ[1, 0] = -((JAC[1, 0] * JAC[2, 2]) - (JAC[1, 2] * JAC[2, 0]))
    AUJJ[2, 0] =  ((JAC[1, 0] * JAC[2, 1]) - (JAC[1, 1] * JAC[2, 0]))
    AUJJ[0, 1] = -((JAC[0, 1] * JAC[2, 2]) - (JAC[0, 2] * JAC[2, 1]))
    AUJJ[1, 1] =  ((JAC[0, 0] * JAC[2, 2]) - (JAC[0, 2] * JAC[2, 0]))
    AUJJ[2, 1] = -((JAC[0, 0] * JAC[2, 1]) - (JAC[0, 1] * JAC[2, 0]))
    AUJJ[0, 2] =  ((JAC[0, 1] * JAC[1, 2]) - (JAC[0, 2] * JAC[1, 1]))
    AUJJ[1, 2] = -((JAC[0, 0] * JAC[1, 2]) - (JAC[0, 2] * JAC[1, 0]))
    AUJJ[2, 2] =  ((JAC[0, 0] * JAC[1, 1]) - (JAC[0, 1] * JAC[1, 0]))

    inv_jac = (1 / det_jac) * AUJJ

    return det_jac, inv_jac


def get_stacked_detJAC_and_invJAC(JAC: np.ndarray) -> np.ndarray:
    """
    This function computes the determinants and inverses
    of Jacobian matrices in stacked form.

    Parameters
    ----------
    JAC: np.array
        The stacked Jacobian matrices.

    Returns
    -------
    det_jacs: np.ndarray
        The stacked determinants of Jacobian matrices.

    inv_jacs: np.ndarray
        The stacked inverse of Jacobian matrices.

    """

    det_jacs = (  
                  JAC[:, 0, 0] * JAC[:, 1, 1] * JAC[:, 2, 2]
                + JAC[:, 0, 1] * JAC[:, 1, 2] * JAC[:, 2, 0]
                + JAC[:, 0, 2] * JAC[:, 1, 0] * JAC[:, 2, 1]
                ) - (
                  JAC[:, 2, 0] * JAC[:, 1, 1] * JAC[:, 0, 2]
                + JAC[:, 2, 1] * JAC[:, 1, 2] * JAC[:, 0, 0]
                + JAC[:, 2, 2] * JAC[:, 1, 0] * JAC[:, 0, 1]
                )

    det_jacs = det_jacs.reshape(-1, 1, 1)

    # the adjoint matrix
    nel = JAC.shape[0]
    AUJJ = np.zeros((nel, 3, 3), dtype=float)

    AUJJ[:, 0, 0] =  ((JAC[:, 1, 1] * JAC[:, 2, 2]) - (JAC[:, 2, 1] * JAC[:, 1, 2]))
    AUJJ[:, 1, 0] = -((JAC[:, 1, 0] * JAC[:, 2, 2]) - (JAC[:, 1, 2] * JAC[:, 2, 0]))
    AUJJ[:, 2, 0] =  ((JAC[:, 1, 0] * JAC[:, 2, 1]) - (JAC[:, 1, 1] * JAC[:, 2, 0]))
    AUJJ[:, 0, 1] = -((JAC[:, 0, 1] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 1]))
    AUJJ[:, 1, 1] =  ((JAC[:, 0, 0] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 0]))
    AUJJ[:, 2, 1] = -((JAC[:, 0, 0] * JAC[:, 2, 1]) - (JAC[:, 0, 1] * JAC[:, 2, 0]))
    AUJJ[:, 0, 2] =  ((JAC[:, 0, 1] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 1]))
    AUJJ[:, 1, 2] = -((JAC[:, 0, 0] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 0]))
    AUJJ[:, 2, 2] =  ((JAC[:, 0, 0] * JAC[:, 1, 1]) - (JAC[:, 0, 1] * JAC[:, 1, 0]))

    inv_jacs = (1 / det_jacs) * AUJJ

    return det_jacs, inv_jacs


class ACT_TETRAHEDRON_4C(Element3D):

    DOFS_PER_NODE = 1
    NODES_PER_ELEMENT = 4
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOFS_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivity = None
        self.element_label = "acoustic_tetrahedron_4"

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

        self.nint = 4

        con1 = (5 - np.sqrt(5)) / 20
        con2 = (5 + 3 * np.sqrt(5)) / 20

        self.pint = np.array([[con1, con1, con1], 
                              [con1, con1, con2], 
                              [con1, con2, con1], 
                              [con2, con1, con1]], dtype=float)

        self.wps = 1 / 4


    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """

        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        rrx = self.pint[:, 2]

        self.phi, self.dphi = self.get_shape_functions_and_derivatives(ssx, ttx, rrx)


    def get_shape_functions_and_derivatives(self, ssx: np.ndarray, ttx: np.ndarray, rrx: np.ndarray) -> np.ndarray:

        """
        This function returns the shape functions and its derivatives.
        
        Parameters
        ----------
        ssx: np.ndarray
            The x coordinates of the integration points.
        
        ttx: np.ndarray
            The y coordinates of the integration points.

        rrx: np.ndarray
            The z coordinates of the integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        # shape functions
        phi = np.array([1 - ssx - ttx - rrx, ttx, rrx, ssx], dtype=float).T

        # derivatives
        dphi = np.array([[-1, 0, 0, 1], 
                        [-1, 1, 0, 0], 
                        [-1, 0, 1, 0]], dtype=float)

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

        # Jacobian matrix
        JAC = self.dphi @ coords

        # Jacobian determinant and inverse
        detJAC, invJAC = get_detJAC_and_invJAC(JAC)

        # shape functions
        N = self.phi

        # derivative of shape functions
        B = invJAC @ self.dphi

        Ke = (1 / 6) * B.T @ B * (detJAC * self.wps) * self.nint
        Me = (1 / 6) * N.T @ N * (detJAC * self.wps)

        return Ke, Me


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

        # stacked nodal coordinates
        stacked_coords = self.get_stacked_nodal_coords()

        # Jacobian matrices of all elements
        JAC_stacked = self.dphi @ stacked_coords

        # Jacobian determinants and inverses of all elements
        det_jacs, inv_jacs = get_stacked_detJAC_and_invJAC(JAC_stacked)

        # shape functions
        N = self.phi
        N_t = N.T

        # derivative of shape functions
        B = inv_jacs @ self.dphi
        B_t = np.transpose(B, axes=(0, 2, 1))

        Ke = (1 / 6) * B_t @ B * (det_jacs * self.wps) * self.nint
        Me = (1 / 6) * N_t @ N * (det_jacs * self.wps)

        return Ke, Me

    
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
        node_ids = kwargs.get("node_ids")
        if node_ids is None:
            node_ids = self.connectivity[element_id, 1:]

        solution = kwargs.get("solution")
        nodal_pressures = kwargs.get("nodal_pressures", )

        if isinstance(nodal_pressures, np.ndarray):
            Pe = nodal_pressures
        elif isinstance(solution, np.ndarray):
            Pe = solution[node_ids, :]    
        else:
            return 0.

        omega = 2 * np.pi * frequencies

        if self.connectivity is None:
            self.reorder_connect()

        p_calc = np.array([ [ 0, 0, 0 ],
                            [ 1, 0, 0 ],
                            [ 0, 1, 0 ],
                            [ 0, 0, 1 ] ], dtype=float)

        for i, (ssx, ttx, rrx) in enumerate(p_calc):
            if node_ids[i] != node_id:
                continue

            _, dphi = self.get_shape_functions_and_derivatives(ssx, ttx, rrx)
            JAC = dphi @ self.nodal_coordinates[node_ids, 1:4]

            _, invJAC = get_detJAC_and_invJAC(JAC)
            B = invJAC @ dphi

            particle_velocity = -(1 / (1j * rho * omega)) * (B @ Pe)

            return particle_velocity


    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        if self.solids_connectivity.shape[1] == self.NODES_PER_ELEMENT + 4:
            self.connectivity = self.solids_connectivity[:, [0, 6, 4, 5, 7]]


    def generate_ind_rows_cols(self, reorder: bool = True):
        """ This method processess the dofs indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.solids_connectivity[:, [0, 4, 5, 6, 7]]

        dofs, edofs = self.DOFS_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs * self.connectivity[:, 1:]

        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

        return self.ind_rows, self.ind_cols


    # def elementary_matrices_reference(self, el_index: int):
    #     """
    #     Stiffness and mass matrices.
    #     """

    #     ie = self.connectivity[el_index, 1:]
    #     JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]

    #     detJAC, invJAC = get_detJAC_and_invJAC(JAC)
    #     dphi_t = invJAC @ self.dphi

    #     B = np.zeros((3, self.DOFS_PER_ELEMENT), dtype=float)
    #     B[0, :] = dphi_t[0, :]
    #     B[1, :] = dphi_t[1, :]
    #     B[2, :] = dphi_t[2, :]

    #     N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
    #     N[:, 0, :] = self.phi

    #     # integration loop
    #     Ke, Me = 0, 0
    #     for i in range(self.nint):
    #         Ke += (1 / 6) * B.T @ B * (detJAC * self.wps)
    #         Me += (1 / 6) * N[i, :, :].T @ N[i, :, :] * (detJAC * self.wps)

    #     return Ke, Me

    # def velpartT4C(self, element_id, node_id, rho, freq, pressures):
    #     """ Stiffness and mass matrices.
    #     """  
    #     #Connect -- Ansys ---> Gmsh
    #     # connect_t  = connect.copy()
    #     # connect_t[ee,1] = connect[ee,3]
    #     # connect_t[ee,2] = connect[ee,1]
    #     # connect_t[ee,3] = connect[ee,2]
    #     # connect_t[ee,4] = connect[ee,4]
    #     # connect = connect_t.copy()
    #     #sugestao: mudar ordenação das funções de forma e derivadas
    #     #
    #     ie = self.connectivity[element_id, 1:]
    #     Pe = pressures[ie, :]

    #     # #
    #     # print(f"element_index: {element_id}")
    #     # print(f"nodes: {ie}")
    #     #
    #     # Pe = np.zeros((4, len(freq)), dtype=complex)
    #     # Pe[0, :] = pressures[connect[element_id,1], :]
    #     # Pe[1, :] = pressures[connect[element_id,2], :]
    #     # Pe[2, :] = pressures[connect[element_id,3], :]
    #     # Pe[3, :] = pressures[connect[element_id,4], :]

    #     #
    #     # -------
    #     ncalc = 4
    #     # Seguir elem. coords. de acordo com connectiv.
    #     pcalc = np.array([  [ 0, 0, 0],
    #                         [ 1, 0, 0],
    #                         [ 0, 0, 1],
    #                         [ 0, 1, 0]  ])
    #     # 
    #     VK = np.zeros((3,4), dtype=complex)
    #     AUJJ = np.zeros((3,3))
    #     B = np.zeros((3,4))

    #     # integration
    #     for i in range(ncalc):
    #         l1, l2, l3 = pcalc[i, 0], pcalc[i, 1], pcalc[i, 2]
    #         phi, dphi = get_shape_functions_and_derivatives(l1, l2, l3)
    #         dxdydz = dphi @ self.nodal_coordinates[ie, 1:4]
    #         # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
    #         JAC = np.array([[dxdydz[0,0], dxdydz[0,1], dxdydz[0,2]],
    #                         [dxdydz[1,0], dxdydz[1,1], dxdydz[1,2]],
    #                         [dxdydz[2,0], dxdydz[2,1], dxdydz[2,2]]], dtype=float)

    #         #detJAC = np.linalg.det(JAC)
    #         detJAC = (JAC[0,0] * JAC[1,1] * JAC[2,2] + 
    #                 JAC[0,1] * JAC[1,2] * JAC[2,0] + 
    #                 JAC[0,2] * JAC[1,0] * JAC[2,1]) - \
    #                 ( JAC[2,0] * JAC[1,1] * JAC[0,2] + 
    #                 JAC[2,1] * JAC[1,2] * JAC[0,0] + 
    #                 JAC[2,2] * JAC[1,0] * JAC[0,1])
    #         ## adj(JAC)
    #         AUJJ[0,0]= 1 * ((JAC[1,1] * JAC[2,2]) - (JAC[2,1] * JAC[1,2]))
    #         AUJJ[1,0]= -1 * ((JAC[1,0] * JAC[2,2]) - (JAC[1,2] * JAC[2,0]))
    #         AUJJ[2,0]= 1 * ((JAC[1,0] * JAC[2,1]) - (JAC[1,1] * JAC[2,0]))
    #         AUJJ[0,1]= -1 * ((JAC[0,1] * JAC[2,2]) - (JAC[0,2] * JAC[2,1]))
    #         AUJJ[1,1]= 1 * ((JAC[0,0] * JAC[2,2]) - (JAC[0,2] * JAC[2,0]))
    #         AUJJ[2,1]= -1 * ((JAC[0,0] * JAC[2,1]) - (JAC[0,1] * JAC[2,0]))
    #         AUJJ[0,2]= 1 * ((JAC[0,1] * JAC[1,2]) - (JAC[0,2] * JAC[1,1]))
    #         AUJJ[1,2]= -1 * ((JAC[0,0] * JAC[1,2]) - (JAC[0,2] * JAC[1,0]))
    #         AUJJ[2,2]= 1 * ((JAC[0,0] * JAC[1,1]) - (JAC[0,1] * JAC[1,0]))
    #         #Inverse Jacobian
    #         iJAC = (1/detJAC) * AUJJ # np.linalg.inv(JAC) 
            
    #         dphi_t = iJAC @ dphi
            
    #         for iii in range(4):
    #             B[0,iii]=dphi_t[0,iii]
    #             B[1,iii]=dphi_t[1,iii]
    #             B[2,iii]=dphi_t[2,iii]

    #         #for iii in range(4):
    #         #    N[0,iii]=phi[iii]
    #         omega = 2 * np.pi * freq

    #         VK = -(1j/(rho*omega))*(1/np.sqrt(6)) * (B @ Pe)
    #         # VK[:,i] = -(1j/(rho*omega))*(1/np.sqrt(6))*B @ Pe

    #     output = np.zeros((len(freq), 1+6), dtype=float)
    #     if node_id in [8416, 9368]:
    #         if element_id in [81523, 81986]:
    #             print(f"Node id: {node_id}")
    #             print(f"Element id: {element_id}")
    #             output[:, 0] = freq
    #             output[:, 1] = np.real(VK[0,:])
    #             output[:, 2] = np.imag(VK[0,:])
    #             output[:, 3] = np.real(VK[1,:])
    #             output[:, 4] = np.imag(VK[1,:])
    #             output[:, 5] = np.real(VK[2,:])
    #             output[:, 6] = np.imag(VK[2,:])
    #             fname = f"particle_velocities_Olavo_{node_id}_{element_id}.dat"
    #             np.savetxt(fname, output, delimiter=",")

    #     return VK