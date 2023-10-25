import numpy as np

from vibra.engine.elements.surface_elements import Element2D


def shapeFZ3(ssx,ttx):
    """This function returns the shape functions and its derivatives."""
    # shape functions
    phi = np.array([1 - ssx - ttx, ttx, ssx], dtype=float).T
    # shape functions derivatives
    dphi = np.array([[-1, 0, 1],
                     [-1, 1, 0]], dtype=float)
    return phi, dphi

def get_detJAC(JAC):
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

    x1 = 0. 
    x2 = np.dot(vec21,unit_x_axis)
    x3 = np.dot(vec31,unit_x_axis)
    y1 = 0.
    y2 = np.dot(vec21,unit_y_axis)
    y3 = np.dot(vec31,unit_y_axis)
    #
    coord_loc = np.array([[x1, y1],
                          [x2, y2],
                          [x3, y3]], dtype=float)
    return coord_loc

class ACT_FACE_3(Element2D):
    #
    NODES_PER_ELEMENT = 3
    DOF_PER_NODE = 1
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model):
        #
        self.model = model
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()

    def initialize_variables(self):
        """ """
        self.element_label = "acoustic_triangular_3"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connectivity = self.model.mesh.solids_connectivity
        self.faces_connectivity = self.model.mesh.faces_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity)

    def define_integration_points(self):
        """ """
        self.nint = 3
        con1 = 2/3
        con2 = 15/90
        self.wps = 1/3
        self.pint = np.array([  [con1, con1],
                                [con1, con2],
                                [con2, con1]  ], dtype=float)

    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        #
        self.phi, self.dphi = shapeFZ3(ssx, ttx)

    def matrices_Z(self, el_index, rho=1, impedance=1):
        """ Z matrices
        """

        ie = self.connect_face[el_index, :]
        coords = self.nodal_coordinates[ie, :]
        coord_loc = get_local_coordinates(coords)
        #
        JAC = self.dphi @ coord_loc
        detJAC = get_detJAC(JAC)
        # print(f"matrices_Z: index - {el_index} \n {coord_loc} {detJAC}")
        #
        N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        N[:, 0, :] = self.phi
        #
        Ze = 0.
        for i in range(self.nint):
            Ze += -(1/2) * (rho/impedance) * N[i, :, :].T @ N[i, :, :] * (detJAC*self.wps)
            # print(f"matrices_Z: index - {el_index} k - {i} {N[i, :, :]}")
        return Ze

    def excitation_F(self, el_index, Vn=1):
        """ F matrices
        """

        ie = self.connect_face[el_index, :]
        coords = self.nodal_coordinates[ie, :]
        coord_loc = get_local_coordinates(coords)
        #
        JAC = self.dphi @ coord_loc
        detJAC = get_detJAC(JAC)
        #
        N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        N[:, 0, :] = self.phi
        #
        Fe = 0.
        for i in range(self.nint):            
            Fe += -(1/2) * Vn * N[i, :, :].T * (detJAC * self.wps)
            # print(f"excitation_F: index - {el_index} : k - {i} {N[i, :, :]}")
        return Fe

    def reorder_connect(self, connect_face):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connect_face = connect_face[:, [0, 1, 2]]

    def generate_ind_rows_cols(self, connect_face):
        """ This method processess the dofs indices (rows and columns) for assembly"""

        self.reorder_connect(connect_face)
        dofs, edofs = self.DOF_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs*self.connect_face[:, :]

        vect_indices = ind_dofs.flatten()
        ind_rows_face = ((np.tile(vect_indices, (edofs,1))).T).flatten()
        ind_cols_face = (np.tile(ind_dofs, edofs)).flatten()

        return ind_rows_face, ind_cols_face

    def excitation_F_base(self, ee, Vn=1):
        """ F3 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        coord = self.nodal_coordinates
        connect_face = self.connect_face

        ############## Definir plano de trabalho e adaptar coordenadas para tal plano
        XX1, YY1, ZZ1 = coord[connect_face[ee,0],1], coord[connect_face[ee,0],2], coord[connect_face[ee,0],3]
        XX2, YY2, ZZ2 = coord[connect_face[ee,1],1], coord[connect_face[ee,1],2], coord[connect_face[ee,1],3]
        XX3, YY3, ZZ3 = coord[connect_face[ee,2],1], coord[connect_face[ee,2],2], coord[connect_face[ee,2],3]

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
            phi, dphi = shapeFZ3(ssx, ttx)
            #ie = connect_face[ee_face,1:]-1
            dxdy = dphi@coord_loc
            # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
            JAC = np.array([[dxdy[0,0], dxdy[0,1]],
                            [dxdy[1,0], dxdy[1,1]]], dtype=float)
            # print(f"forceF3: index - {ee} : k - {i} JAC {JAC}")
            #Inverse Jacobian
            detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  
            # N[0, :] = phi
            for iii in range(3):
                N[0,iii]=phi[iii]

            # print(f"forceF3: index - {ee} : k - {i} {N}")           
            Fe += -(1/2) * Vn * N.T * (detJAC * wps)

        return Fe

    def matrices_Z_base(self, ee, rho=1, impedance=1):
        """ Z3 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        coord = self.nodal_coordinates
        connect_face = self.connect_face

        ############## Definir plano de trabalho e adaptar coordenadas para tal plano
        XX1, YY1, ZZ1 = coord[connect_face[ee,0],1], coord[connect_face[ee,0],2], coord[connect_face[ee,0],3]
        XX2, YY2, ZZ2 = coord[connect_face[ee,1],1], coord[connect_face[ee,1],2], coord[connect_face[ee,1],3]
        XX3, YY3, ZZ3 = coord[connect_face[ee,2],1], coord[connect_face[ee,2],2], coord[connect_face[ee,2],3]

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
        # print(f"matricesZ3: index - {ee} \n {coord_loc}")

        ################ Definir pontos de integração 2D
        nint = 3
        con1 = 2/3
        con2 = 15/90
        wps = 1/3
        pint = np.array([[con1, con1],
                         [con1, con2],
                         [con2, con1]])

        ######################## Inicio da integração na face
        Ze = np.zeros((3,3),dtype=complex)
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
            # print(f"matricesZ3: index - {ee} \n {coord_loc} {detJAC} -> {i}")

            for iii in range(3):
                N[0, iii] = phi[iii]
            
            # print(f"matricesZ3: index - {ee} k - {i} {N}")
            
            Ze += -(1/2) * (rho/impedance) * N.T@N * (detJAC * wps)

        return Ze