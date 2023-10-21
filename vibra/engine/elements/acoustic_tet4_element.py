import numpy as np

from vibra.engine.elements.element import Element


def shape4TC(ssx, ttx, rrx):
    """This function returns the shape functions and its derivatives."""
    # shape functions
    phi = np.array([1 - ssx - ttx - rrx, ttx, rrx, ssx], dtype=float)
    # derivatives
    dphi = np.array([[-1, 0, 0, 1], 
                     [-1, 1, 0, 0], 
                     [-1, 0, 1, 0]], dtype=float)
    return phi, dphi

def shapeFZ3(ssx,ttx):
    """This function returns the shape functions and its derivatives."""
    # shape functions
    phi = np.array([1-ssx-ttx, ttx, ssx], dtype=float)
    # derivatives
    dphi = np.array([[-1, 0, 1],
                     [-1, 1, 0]], dtype=float)
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

def get_detJAC_2D(JAC):
    # Inverse Jacobian
    detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  
    return detJAC

def get_local_coordinates(coords):
    
    XX1, XX2, XX3 = coords[:, 1]
    YY1, YY2, YY3 = coords[:, 2]
    ZZ1, ZZ2, ZZ3 = coords[:, 3]

    vec21 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
    vec31 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T

    loc_x_axis = vec21.copy()
    loc_z_axis = np.cross(loc_x_axis, vec31)
    loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

    unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
    unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

    x1 = 0 
    x2 = np.dot(vec21,unit_x_axis)
    x3 = np.dot(vec31,unit_x_axis)
    y1 = 0
    y2 = np.dot(vec21,unit_y_axis)
    y3 = np.dot(vec31,unit_y_axis)
    #
    coord_loc = np.array([[x1, y1],
                            [x2, y2],
                            [x3, y3]])
    return coord_loc

class ACT_TETRAHEDRON_4C(Element):
    #
    NODES_PER_ELEMENT = 4
    NODES_PER_ELEMENT_2D = 3
    DOF_PER_NODE = 1
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE
    DOFS_PER_ELEMENT_2D = NODES_PER_ELEMENT_2D * DOF_PER_NODE

    def __init__(self, model):
        #
        self.model = model
        self.initialize_variables()
        self.define_integration_points_3D()
        self.define_integration_points_2D()
        self.process_shape_functions_and_derivatives_3D()
        self.process_shape_functions_and_derivatives_2D()

    def initialize_variables(self):
        """ """
        self.element_label = "acoustic_tetrahedron_4"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connectivity = self.model.mesh.solids_connectivity
        self.faces_connectivity = self.model.mesh.faces_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity)

    def define_integration_points_3D(self):
        """ """
        # integration points
        self.nint = 4
        con1 = (5 - np.sqrt(5))/20
        con2 = (5 + 3 * np.sqrt(5))/20
        self.wps_3D = 1/4

        self.pint = np.array([[con1, con1, con1], 
                              [con1, con1, con2], 
                              [con1, con2, con1], 
                              [con2, con1, con1]])

    def define_integration_points_2D(self):
        """ """
        # integration points
        self.nint_2D = 3
        con1 = 2/3
        con2 = 15/90
        self.wps_2D = 1/3
        self.pint_2D = np.array([[con1, con1],
                                 [con1, con2],
                                 [con2, con1]])

    def process_shape_functions_and_derivatives_3D(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        rrx = self.pint[:, 2]
        #
        self.phi, self.dphi = shape4TC(ssx, ttx, rrx)

    def process_shape_functions_and_derivatives_2D(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        #
        self.phi_2D, self.dphi_2D = shapeFZ3(ssx, ttx)

    def elementary_matrices(self, el_index):
        """
        Stiffness and mass matrices.
        """

        # fluid = self.model.properties.get_fluid(element=el_index)
        # rho = fluid.fluid_density
        # c_0 = fluid.speed_of_sound

        c_0 = self.model.properties.get_speed_of_sound(element=el_index)
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
            Ke += (1 / 6) * B.T @ B * (detJAC * self.wps_3D)
            Me += (1 / 6) * (1 / c_0**2) * N[i, :, :].T @ N[i, :, :] * (detJAC * self.wps_3D)

        return Ke, Me

    def matricesZ3(self, el_index, rho, imped):
        """ Z3 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        # ############## Definir plano de trabalho e adaptar coordenadas para tal plano
        # XX1, YY1, ZZ1 = coord[connect_face[ee,1]-1,1], coord[connect_face[ee,1]-1,2], coord[connect_face[ee,1]-1,3]
        # XX2, YY2, ZZ2 = coord[connect_face[ee,2]-1,1], coord[connect_face[ee,2]-1,2], coord[connect_face[ee,2]-1,3]
        # XX3, YY3, ZZ3 = coord[connect_face[ee,3]-1,1], coord[connect_face[ee,3]-1,2], coord[connect_face[ee,3]-1,3]

        ie = self.connect_face[el_index, 1:]
        # coords = self.nodal_coordinates[ie, 1:]
        # coord_loc = get_local_coordinates(coords)

        XX1, XX2, XX3 = self.nodal_coordinates[ie, 1]
        YY1, YY2, YY3 = self.nodal_coordinates[ie, 2]
        ZZ1, ZZ2, ZZ3 = self.nodal_coordinates[ie, 3]

        vec21 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
        vec31 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T

        loc_x_axis = vec21.copy()
        loc_z_axis = np.cross(loc_x_axis, vec31)
        loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

        unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
        unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

        x1 = 0 
        x2 = np.dot(vec21,unit_x_axis)
        x3 = np.dot(vec31,unit_x_axis)
        y1 = 0 
        y2 = np.dot(vec21,unit_y_axis)
        y3 = np.dot(vec31,unit_y_axis)
        #
        coord_loc = np.array([[x1, y1],
                              [x2, y2],
                              [x3, y3]])
        #
        # JAC = self.dphi_2D @ coord_loc
        # detJAC = get_detJAC_2D(JAC)
        #
        # N = np.zeros((self.nint_2D, 1, self.DOFS_PER_ELEMENT_2D), dtype=float)
        # N[:, 0, :] = self.phi_2D
        #
        Ze = 0 + 0j
        N = np.zeros((1,3))
        for i in range(self.nint_2D):
            # Ze += (1/2) * (rho/imped) * N[i, :, :].T @ N[i, :, :] * (detJAC*self.wps_2D)

            ssx, ttx = self.pint_2D[i, 0], self.pint_2D[i, 1]
            phi, dphi = shapeFZ3(ssx, ttx)
            # ie = connect_face[ee_face,1:]-1
            dxdy = dphi@coord_loc
            # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
            JAC = np.array([[dxdy[0,0], dxdy[0,1]],
                            [dxdy[1,0], dxdy[1,1]]], dtype=float) 
            #Inverse Jacobian
            detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  

            for iii in range(3):
                N[0, iii] = phi[iii]
            
            Ze += (1/2)*rho*(1/imped)*N.T @ N*(detJAC*self.wps_2D)

        return Ze

    def excitationF3(self, el_index, Vn=1):
        """ F3 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        ############## Definir plano de trabalho e adaptar coordenadas para tal plano
        # XX1, YY1, ZZ1 = coord[connect_face[ee,1]-1,1], coord[connect_face[ee,1]-1,2], coord[connect_face[ee,1]-1,3]
        # XX2, YY2, ZZ2 = coord[connect_face[ee,2]-1,1], coord[connect_face[ee,2]-1,2], coord[connect_face[ee,2]-1,3]
        # XX3, YY3, ZZ3 = coord[connect_face[ee,3]-1,1], coord[connect_face[ee,3]-1,2], coord[connect_face[ee,3]-1,3]

        ie = self.connect_face[el_index, 1:]
        # coords = self.nodal_coordinates[ie, 1:]
        # coord_loc = get_local_coordinates(coords)

        XX1, XX2, XX3 = self.nodal_coordinates[ie, 1]
        YY1, YY2, YY3 = self.nodal_coordinates[ie, 2]
        ZZ1, ZZ2, ZZ3 = self.nodal_coordinates[ie, 3]

        vec21 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T
        vec31 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T

        loc_x_axis = vec21.copy()
        loc_z_axis = np.cross(loc_x_axis, vec31)
        loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

        unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
        unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

        x1 = 0 
        x2 = np.dot(vec21,unit_x_axis)
        x3 = np.dot(vec31,unit_x_axis)
        y1 = 0 
        y2 = np.dot(vec21,unit_y_axis)
        y3 = np.dot(vec31,unit_y_axis)

        coord_loc = np.array([[x1, y1],
                              [x2, y2],
                              [x3, y3]])

        ################ Definir pontos de integração 2D
        nint = 3
        con1 = 2/3
        con2 = 15/90
        wps = 1/3
        pint = np.array([[con1, con1],
                         [con1, con2],
                         [con2, con1]])

        ######################## Inicio da integração na face
        Fe = np.zeros((3,1),dtype=complex)
        N = np.zeros((1,3))
        # integration
        for i in range(nint):
            ssx, ttx = pint[i, 0], pint[i, 1]
            phi, dphi = shapeFZ3(ssx,ttx)
            #ie = connect_face[ee_face,1:]-1
            dxdy = dphi@coord_loc
            # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
            JAC = np.array([[dxdy[0,0], dxdy[0,1]],
                            [dxdy[1,0], dxdy[1,1]]], dtype=float) 
            #Inverse Jacobian
            detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  

            for iii in range(3):
                N[0, iii] = phi[iii]
            
            Fe += (1/2)*Vn*N.T*(detJAC*wps)

        return Fe

    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivity = self.connectivity[:, [0, 6, 4, 5, 7]]

    def reorder_face_connect(self, connect_face):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connect_face = connect_face[:, [0, 3, 1, 2]]

    def generate_ind_rows_cols(self):
        """ This method processess the dofs indices (rows and columns) for assembly"""

        self.reorder_connect()
        dofs, edofs = self.DOF_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs * self.connectivity[:, 1:]

        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

        return self.ind_rows, self.ind_cols

    def generate_ind_rows_cols_2D(self, connect_face):
        """ This method processess the dofs indices (rows and columns) for assembly"""

        self.reorder_face_connect(connect_face)
        dofs, edofs = self.DOF_PER_NODE, self.DOFS_PER_ELEMENT_2D
        ind_dofs = dofs*connect_face[:, 1:]

        vect_indices = ind_dofs.flatten()
        ind_rows_face = ((np.tile(vect_indices, (edofs,1))).T).flatten()
        ind_cols_face = (np.tile(ind_dofs, edofs)).flatten()

        return ind_rows_face, ind_cols_face