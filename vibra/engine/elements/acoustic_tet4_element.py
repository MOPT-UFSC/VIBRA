import numpy as np

from vibra.engine.elements.solid_elements import Element3D

# fmt: off

def shapeT4C(ssx, ttx, rrx):
    """This function returns the shape functions and its derivatives."""
    # shape functions
    phi = np.array([1 - ssx - ttx - rrx, ttx, rrx, ssx], dtype=float).T
    # derivatives
    dphi = np.array([[-1, 0, 0, 1], 
                     [-1, 1, 0, 0], 
                     [-1, 0, 1, 0]], dtype=float)
    return phi, dphi

def get_detJAC_and_invJAC(JAC):
    """ """

    detJAC = (
        JAC[0, 0] * JAC[1, 1] * JAC[2, 2]
        + JAC[0, 1] * JAC[1, 2] * JAC[2, 0]
        + JAC[0, 2] * JAC[1, 0] * JAC[2, 1]
    ) - (
        JAC[2, 0] * JAC[1, 1] * JAC[0, 2]
        + JAC[2, 1] * JAC[1, 2] * JAC[0, 0]
        + JAC[2, 2] * JAC[1, 0] * JAC[0, 1]
    )

    # adj(JAC)
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

    return detJAC, (1 / detJAC) * AUJJ


class ACT_TETRAHEDRON_4C(Element3D):

    DOF_PER_NODE = 1
    NODES_PER_ELEMENT = 4
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model):
        self.model = model
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()

    def initialize_variables(self):
        """ """
        self.element_label = "acoustic_tetrahedron_4"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connectivity = self.model.mesh.solids_connectivity
        self.faces_connectivity = self.model.mesh.faces_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity)

    def define_integration_points(self):
        """ """
        self.nint = 4
        con1 = (5 - np.sqrt(5))/20
        con2 = (5 + 3 * np.sqrt(5))/20
        self.wps = 1/4

        self.pint = np.array([[con1, con1, con1], 
                              [con1, con1, con2], 
                              [con1, con2, con1], 
                              [con2, con1, con1]])

    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        rrx = self.pint[:, 2]
        #
        self.phi, self.dphi = shapeT4C(ssx, ttx, rrx)

    def elementary_matrices(self, el_index):
        """
        Stiffness and mass matrices.
        """

        # fluid = self.model.properties.get_fluid(element=el_index)
        # rho = fluid.fluid_density
        # c_0 = fluid.speed_of_sound
        # c_0 = self.model.properties.get_speed_of_sound(element=el_index)
        ie = self.connectivity[el_index, 1:]
        #
        JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = get_detJAC_and_invJAC(JAC)
        dphi_t = invJAC @ self.dphi
        #
        B = np.zeros((3, self.DOFS_PER_ELEMENT), dtype=float)
        N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        #
        B[0, :] = dphi_t[0, :]
        B[1, :] = dphi_t[1, :]
        B[2, :] = dphi_t[2, :]
        #
        N[:, 0, :] = self.phi

        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            Ke += (1 / 6) * B.T @ B * (detJAC * self.wps)
            Me += (1 / 6) * N[i, :, :].T @ N[i, :, :] * (detJAC * self.wps)
            # Me += (1 / 6) * (1 / c_0**2) * N[i, :, :].T @ N[i, :, :] * (detJAC * self.wps)

        return Ke, Me
    
    def process_particle_velocity(  self, 
                                    element_id : int, 
                                    node_id : int, 
                                    rho : float, 
                                    frequencies : np.ndarray, 
                                    nodal_pressures : np.ndarray  ):
        """
        Process the particle velocity.
        """

        ie = self.connectivity[element_id, 1:]
        Pe = nodal_pressures[ie, :]

        p_calc = np.array([ [0, 0, 0],
                            [1, 0, 0],
                            [0, 0, 1],
                            [0, 1, 0] ], dtype=float)

        # ssx = p_calc[:, 0]
        # ttx = p_calc[:, 1]
        # rrx = p_calc[:, 2]

        for i, (ssx, ttx, rrx) in enumerate(p_calc):

            if ie[i] == node_id:
                    
                phi, dphi = shapeT4C(ssx, ttx, rrx)

                JAC = dphi @ self.nodal_coordinates[ie, 1:4]
                detJAC, invJAC = get_detJAC_and_invJAC(JAC)
                dphi_t = invJAC @ dphi

                B = np.zeros((3, self.DOFS_PER_ELEMENT), dtype=float)

                B[0, :] = dphi_t[0, :]
                B[1, :] = dphi_t[1, :]
                B[2, :] = dphi_t[2, :]

                omega = 2 * np.pi * frequencies

                Ve = (-1j / (rho * omega)) * (1 / np.sqrt(6)) * (B @ Pe)

                output = np.zeros((len(frequencies), 1+6), dtype=float)
                if node_id in [8350, 9368]:
                    if element_id in [81523]:
                        print(f"Node id: {node_id}")
                        print(f"Element id: {element_id}")
                        output[:, 0] = frequencies
                        output[:, 1] = np.real(Ve[0,:])
                        output[:, 2] = np.imag(Ve[0,:])
                        output[:, 3] = np.real(Ve[1,:])
                        output[:, 4] = np.imag(Ve[1,:])
                        output[:, 5] = np.real(Ve[2,:])
                        output[:, 6] = np.imag(Ve[2,:])
                        fname = f"particle_velocities_Vibra_{node_id}_{element_id}.dat"
                        np.savetxt(fname, output, delimiter=",")

                return Ve

    def velpartT4C(self, element_id, node_id, rho, freq, pressures):
        """ Stiffness and mass matrices.
        """  
        #Connect -- Ansys ---> Gmsh
        # connect_t  = connect.copy()
        # connect_t[ee,1] = connect[ee,3]
        # connect_t[ee,2] = connect[ee,1]
        # connect_t[ee,3] = connect[ee,2]
        # connect_t[ee,4] = connect[ee,4]
        # connect = connect_t.copy()
        #sugestao: mudar ordenação das funções de forma e derivadas
        #
        ie = self.connectivity[element_id, 1:]
        Pe = pressures[ie, :]

        # #
        # print(f"element_index: {element_id}")
        # print(f"nodes: {ie}")
        #
        # Pe = np.zeros((4, len(freq)), dtype=complex)
        # Pe[0, :] = pressures[connect[element_id,1], :]
        # Pe[1, :] = pressures[connect[element_id,2], :]
        # Pe[2, :] = pressures[connect[element_id,3], :]
        # Pe[3, :] = pressures[connect[element_id,4], :]

        #
        # -------
        ncalc = 4
        # Seguir elem. coords. de acordo com connectiv.
        pcalc = np.array([  [ 0, 0, 0],
                            [ 1, 0, 0],
                            [ 0, 0, 1],
                            [ 0, 1, 0]  ])
        # 
        VK = np.zeros((3,4), dtype=complex)
        AUJJ = np.zeros((3,3))
        B = np.zeros((3,4))

        # integration
        for i in range(ncalc):
            l1, l2, l3 = pcalc[i, 0], pcalc[i, 1], pcalc[i, 2]
            phi, dphi = shapeT4C(l1, l2, l3)
            dxdydz = dphi @ self.nodal_coordinates[ie, 1:4]
            # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
            JAC = np.array([[dxdydz[0,0], dxdydz[0,1], dxdydz[0,2]],
                            [dxdydz[1,0], dxdydz[1,1], dxdydz[1,2]],
                            [dxdydz[2,0], dxdydz[2,1], dxdydz[2,2]]], dtype=float)

            #detJAC = np.linalg.det(JAC)
            detJAC = (JAC[0,0] * JAC[1,1] * JAC[2,2] + 
                    JAC[0,1] * JAC[1,2] * JAC[2,0] + 
                    JAC[0,2] * JAC[1,0] * JAC[2,1]) - \
                    ( JAC[2,0] * JAC[1,1] * JAC[0,2] + 
                    JAC[2,1] * JAC[1,2] * JAC[0,0] + 
                    JAC[2,2] * JAC[1,0] * JAC[0,1])
            ## adj(JAC)
            AUJJ[0,0]= 1 * ((JAC[1,1] * JAC[2,2]) - (JAC[2,1] * JAC[1,2]))
            AUJJ[1,0]= -1 * ((JAC[1,0] * JAC[2,2]) - (JAC[1,2] * JAC[2,0]))
            AUJJ[2,0]= 1 * ((JAC[1,0] * JAC[2,1]) - (JAC[1,1] * JAC[2,0]))
            AUJJ[0,1]= -1 * ((JAC[0,1] * JAC[2,2]) - (JAC[0,2] * JAC[2,1]))
            AUJJ[1,1]= 1 * ((JAC[0,0] * JAC[2,2]) - (JAC[0,2] * JAC[2,0]))
            AUJJ[2,1]= -1 * ((JAC[0,0] * JAC[2,1]) - (JAC[0,1] * JAC[2,0]))
            AUJJ[0,2]= 1 * ((JAC[0,1] * JAC[1,2]) - (JAC[0,2] * JAC[1,1]))
            AUJJ[1,2]= -1 * ((JAC[0,0] * JAC[1,2]) - (JAC[0,2] * JAC[1,0]))
            AUJJ[2,2]= 1 * ((JAC[0,0] * JAC[1,1]) - (JAC[0,1] * JAC[1,0]))
            #Inverse Jacobian
            iJAC = (1/detJAC) * AUJJ # np.linalg.inv(JAC) 
            
            dphi_t = iJAC @ dphi
            
            for iii in range(4):
                B[0,iii]=dphi_t[0,iii]
                B[1,iii]=dphi_t[1,iii]
                B[2,iii]=dphi_t[2,iii]

            #for iii in range(4):
            #    N[0,iii]=phi[iii]
            omega = 2 * np.pi * freq

            VK = -(1j/(rho*omega))*(1/np.sqrt(6)) * (B @ Pe)
            # VK[:,i] = -(1j/(rho*omega))*(1/np.sqrt(6))*B @ Pe

        output = np.zeros((len(freq), 1+6), dtype=float)
        if node_id in [8350, 9368]:
            if element_id in [81523]:
                print(f"Node id: {node_id}")
                print(f"Element id: {element_id}")
                output[:, 0] = freq
                output[:, 1] = np.real(VK[0,:])
                output[:, 2] = np.imag(VK[0,:])
                output[:, 3] = np.real(VK[1,:])
                output[:, 4] = np.imag(VK[1,:])
                output[:, 5] = np.real(VK[2,:])
                output[:, 6] = np.imag(VK[2,:])
                fname = f"particle_velocities_Olavo_{node_id}_{element_id}.dat"
                np.savetxt(fname, output, delimiter=",")

        return VK

    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        if self.connectivity.shape[1] == self.NODES_PER_ELEMENT + 4:
            self.connectivity = self.connectivity[:, [0, 6, 4, 5, 7]]

    def generate_ind_rows_cols(self, reorder=True):
        """ This method processess the dofs indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.connectivity[:, [0, 4, 5, 6, 7]]

        dofs, edofs = self.DOF_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs * self.connectivity[:, 1:]

        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

        return self.ind_rows, self.ind_cols
    
# fmt: on