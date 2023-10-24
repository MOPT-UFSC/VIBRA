import numpy as np

from vibra.engine.elements.surface_elements import Element2D


def shapeFZ4(ssx, ttx):
    """This function returns the shape functions and its derivatives."""
    # shape functions
    denominator = 4
    phi = np.array([(1.+ssx)*(1.+ttx), 
                    (1.-ssx)*(1.+ttx), 
                    (1.-ssx)*(1.-ttx), 
                    (1.+ssx)*(1.-ttx)], dtype=float).T / denominator

    # derivatives
    dphi = np.zeros((2,4), dtype=float)
    dphi[0,:] =  np.array([(1.+ttx), -(1.+ttx), -(1.-ttx), (1.-ttx)])
    dphi[1,:] =  np.array([(1.+ssx), (1.-ssx), -(1.-ssx), -(1.+ssx)])
    dphi = dphi/denominator
    
    return phi, dphi

def get_detJAC(JAC):
    # Inverse Jacobian
    detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  
    return detJAC

def get_detJAC_3D(JAC):
    # Inverse Jacobian
    detJAC = JAC[:,0,0] * JAC[:,1,1]  - JAC[:,0,1] * JAC[:,1,0]  
    return detJAC.reshape(-1, 1, 1)

def get_local_coordinates(coords):
    
    XX1, XX2, XX3, XX4 = coords[:, 1]
    YY1, YY2, YY3, YY4 = coords[:, 2]
    ZZ1, ZZ2, ZZ3, ZZ4 = coords[:, 3]

    vec13 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T
    vec14 = np.array([XX4-XX1, YY4-YY1, ZZ4-ZZ1]).T
    vec12 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T

    # Cosseno de direção
    XX = vec12/np.linalg.norm(vec12)
    vecZZ = np.cross(XX,vec14)
    ZZ = vecZZ/np.linalg.norm(vecZZ)
    vecYY = np.cross(ZZ,XX)
    YY = vecYY/np.linalg.norm(vecYY)
    COSDIR = np.array([XX,YY,ZZ]) 

    loc_x_axis = vec12.copy()
    loc_z_axis = np.cross(loc_x_axis, vec14)
    loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

    unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
    unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

    x1 = np.dot(vec13,unit_x_axis)
    x2 = np.dot(vec14,unit_x_axis)
    x3 = 0
    x4 = np.dot(vec12,unit_x_axis)
    y1 = np.dot(vec13,unit_y_axis)
    y2 = np.dot(vec14,unit_y_axis)
    y3 = 0
    y4 = np.dot(vec12,unit_y_axis)

    coord_loc = np.array([[x1, y1],
                          [x2, y2],
                          [x3, y3],
                          [x4, y4]], dtype=float)

    return coord_loc

class ACT_FACE_4(Element2D):
    #
    NODES_PER_ELEMENT = 4
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
        self.nint = 4
        con = 1/np.sqrt(3)
        self.wps = 1        
        self.pint = np.array([  [ con,  con],
                                [-con,  con],
                                [-con, -con],
                                [ con, -con]  ], dtype=float)

    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]

        # shape functions
        denominator = 4
        phi = np.zeros((self.nint, self.NODES_PER_ELEMENT), dtype=float)
        phi[:, 0] = (1.+ssx)*(1.+ttx)
        phi[:, 1] = (1.-ssx)*(1.+ttx)
        phi[:, 2] = (1.-ssx)*(1.-ttx)
        phi[:, 3] = (1.+ssx)*(1.-ttx)
        self.phi = phi / denominator

        # derivatives
        dphi = np.zeros((self.nint, self.pint.shape[1], self.NODES_PER_ELEMENT), dtype=float)
        dphi[:, 0, 0] =  (1.+ttx) 
        dphi[:, 0, 1] = -(1.+ttx)
        dphi[:, 0, 2] = -(1.-ttx)
        dphi[:, 0, 3] =  (1.-ttx)
        dphi[:, 1, 0] =  (1.+ssx)
        dphi[:, 1, 1] =  (1.-ssx) 
        dphi[:, 1, 2] = -(1.-ssx)
        dphi[:, 1, 3] = -(1.+ssx)
        self.dphi = dphi/denominator

    def reorder_connect(self, connect_face):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connect_face = connect_face[:, [0, 1, 2, 3]]

    def generate_ind_rows_cols(self, connect_face):
        """ This method processess the dofs indices (rows and columns) for assembly"""

        self.reorder_connect(connect_face)
        dofs, edofs = self.DOF_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs*self.connect_face[:, :]

        vect_indices = ind_dofs.flatten()
        ind_rows_face = ((np.tile(vect_indices, (edofs,1))).T).flatten()
        ind_cols_face = (np.tile(ind_dofs, edofs)).flatten()

        return ind_rows_face, ind_cols_face
        
    def matrices_Z(self, el_index, rho=1, impedance=1):
        """ Z matrices
        """

        ie = self.connect_face[el_index, :]
        coords = self.nodal_coordinates[ie, :]
        coord_loc = get_local_coordinates(coords)
        #
        JAC = self.dphi @ coord_loc
        detJAC = get_detJAC_3D(JAC)
        # print(f"matrices_Z: index - {el_index} \n {coord_loc} {detJAC}")
        #
        N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        N[:, 0, :] = self.phi
        #
        Ze = 0.
        for i in range(self.nint):
            Ze += (rho/impedance) * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :]*self.wps)
            # print(f"matrices_Z: index - {el_index} k - {i} {N[i, :, :]}")
        return Ze

    def excitation_F(self, el_index, Vn=1):
        """ F matrices
        """

        ie = self.connect_face[el_index, :]
        coords = self.nodal_coordinates[ie, :]
        coord_loc = get_local_coordinates(coords)

        # print(f" new: {coord_loc}")
        #
        JAC = self.dphi @ coord_loc
        detJAC = get_detJAC_3D(JAC)
        #
        N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        N[:, 0, :] = self.phi
        #
        Fe = 0.
        for i in range(self.nint):
            # print(f" new detJAC: {detJAC[i, :, :]}")     
            Fe += (1/4) * Vn * N[i, :, :].T * (detJAC[i, :, :] * self.wps)
            # print(f"excitation_F: index - {el_index} : k - {i} {N[i, :, :]}")
        return Fe

    def excitation_F_base(self, ee, Vn=1):
        """ F4 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        coord = self.nodal_coordinates
        connect_face = self.connect_face

        ############## Definir plano de trabalho e adaptar coordenadas para tal plano
        XX1, YY1, ZZ1 = coord[connect_face[ee,0],1], coord[connect_face[ee,0],2], coord[connect_face[ee,0],3]
        XX2, YY2, ZZ2 = coord[connect_face[ee,1],1], coord[connect_face[ee,1],2], coord[connect_face[ee,1],3]
        XX3, YY3, ZZ3 = coord[connect_face[ee,2],1], coord[connect_face[ee,2],2], coord[connect_face[ee,2],3]
        XX4, YY4, ZZ4 = coord[connect_face[ee,3],1], coord[connect_face[ee,3],2], coord[connect_face[ee,3],3]

        vec13 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T
        vec14 = np.array([XX4-XX1, YY4-YY1, ZZ4-ZZ1]).T
        vec12 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T

        #Cosseno de direção
        XX = vec12/np.linalg.norm(vec12)
        vecZZ = np.cross(XX,vec14)
        ZZ = vecZZ/np.linalg.norm(vecZZ)
        vecYY = np.cross(ZZ,XX)
        YY = vecYY/np.linalg.norm(vecYY)
        COSDIR = np.array([XX,YY,ZZ]) 

        loc_x_axis = vec12.copy()
        loc_z_axis = np.cross(loc_x_axis, vec14)
        loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

        unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
        unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

        x1 = np.dot(vec13,unit_x_axis)
        x2 = np.dot(vec14,unit_x_axis)
        x3 = 0
        x4 = np.dot(vec12,unit_x_axis)
        y1 = np.dot(vec13,unit_y_axis)
        y2 = np.dot(vec14,unit_y_axis)
        y3 = 0
        y4 = np.dot(vec12,unit_y_axis)

        coord_loc = np.array([[x1, y1],
                              [x2, y2],
                              [x3, y3],
                              [x4, y4]])
        
        # print(f"base: {coord_loc}")

        ################ Definir pontos de integração 2D
        nint, con, wps = 4, 1/np.sqrt(3), 1
        pint = np.array([[ con,  con],
                         [-con,  con],
                         [-con, -con],
                         [ con, -con]])

        ######################## Inicio da integração na face
        # Fe = np.zeros((4,1),dtype=complex)
        Fe = 0.
        N = np.zeros((1,4))
        # integration
        for i in range(nint):
            ssx, ttx = pint[i, 0], pint[i, 1]
            phi, dphi = shapeFZ4(ssx,ttx)
            #ie = connect_face[ee_face,1:]-1
            dxdy = dphi@coord_loc
            # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
            JAC = np.array([[dxdy[0,0], dxdy[0,1]],
                            [dxdy[1,0], dxdy[1,1]]], dtype=float) 
            #Inverse Jacobian
            detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  

            for iii in range(4):
                N[0,iii]=phi[iii]
            
            Fe += (1/4) * Vn * N.T * (detJAC * wps)
            # print(f"base detJAC: {detJAC}")     

        return Fe

    def matrices_Z_base(self, ee, rho=1, impedance=1):
        """ Z4 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        coord = self.nodal_coordinates
        connect_face = self.connect_face

        ############## Definir plano de trabalho e adaptar coordenadas para tal plano
        XX1, YY1, ZZ1 = coord[connect_face[ee,0],1], coord[connect_face[ee,0],2], coord[connect_face[ee,0],3]
        XX2, YY2, ZZ2 = coord[connect_face[ee,1],1], coord[connect_face[ee,1],2], coord[connect_face[ee,1],3]
        XX3, YY3, ZZ3 = coord[connect_face[ee,2],1], coord[connect_face[ee,2],2], coord[connect_face[ee,2],3]
        XX4, YY4, ZZ4 = coord[connect_face[ee,3],1], coord[connect_face[ee,3],2], coord[connect_face[ee,3],3]

        vec13 = np.array([XX3-XX1, YY3-YY1, ZZ3-ZZ1]).T
        vec14 = np.array([XX4-XX1, YY4-YY1, ZZ4-ZZ1]).T
        vec12 = np.array([XX2-XX1, YY2-YY1, ZZ2-ZZ1]).T

        #Cosseno de direção
        XX = vec12/np.linalg.norm(vec12)
        vecZZ = np.cross(XX,vec14)
        ZZ = vecZZ/np.linalg.norm(vecZZ)
        vecYY = np.cross(ZZ,XX)
        YY = vecYY/np.linalg.norm(vecYY)
        COSDIR = np.array([XX,YY,ZZ]) 

        loc_x_axis = vec12.copy()
        loc_z_axis = np.cross(loc_x_axis, vec14)
        loc_y_axis = np.cross(loc_z_axis, loc_x_axis)

        unit_x_axis = loc_x_axis/np.linalg.norm(loc_x_axis)
        unit_y_axis = loc_y_axis/np.linalg.norm(loc_y_axis)

        x1 = np.dot(vec13,unit_x_axis)
        x2 = np.dot(vec14,unit_x_axis)
        x3 = 0
        x4 = np.dot(vec12,unit_x_axis)
        y1 = np.dot(vec13,unit_y_axis)
        y2 = np.dot(vec14,unit_y_axis)
        y3 = 0
        y4 = np.dot(vec12,unit_y_axis)

        coord_loc = np.array([[x1, y1],
                              [x2, y2],
                              [x3, y3],
                              [x4, y4]])

        ################ Definir pontos de integração 2D
        nint, con, wps = 4, 1/np.sqrt(3), 1
        pint = np.array([[ con,  con],
                         [-con,  con],
                         [-con, -con],
                         [ con, -con]])

        ######################## Inicio da integração na face
        Area = 0
        Ze = 0.
        # Ze = np.zeros((4,4),dtype=complex)
        N = np.zeros((1,4))
        # integration
        for i in range(nint):
            ssx, ttx = pint[i, 0], pint[i, 1]
            phi, dphi = shapeFZ4(ssx,ttx)
            #ie = connect_face[ee_face,1:]-1
            dxdy = dphi@coord_loc
            # note: dxdr, dydr, dzdr, dxds, dyds, dzds, dxdt, dydt, dzdt 
            JAC = np.array([[dxdy[0,0], dxdy[0,1]],
                            [dxdy[1,0], dxdy[1,1]]], dtype=float) 
            #Inverse Jacobian
            detJAC = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  

            for iii in range(4):
                N[0,iii]=phi[iii]
            
            Ze += (rho/impedance) * N.T@N * (detJAC * wps)

        return Ze