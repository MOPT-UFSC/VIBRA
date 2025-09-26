
from vibra.engine.elements.surface_elements import Element2D

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


def shapeFZ4(ssx, ttx):
    """This function returns the shape functions and its derivatives."""

    # shape functions
    denominator = 4
    phi = np.array([(1.+ssx)*(1.+ttx), 
                    (1.-ssx)*(1.+ttx), 
                    (1.-ssx)*(1.-ttx), 
                    (1.+ssx)*(1.-ttx)], dtype=float).T / denominator

    # derivatives of shape functions
    dphi = np.zeros((2, 4), dtype=float)
    dphi[0,:] =  np.array([(1.+ttx), -(1.+ttx), -(1.-ttx), (1.-ttx)])
    dphi[1,:] =  np.array([(1.+ssx), (1.-ssx), -(1.-ssx), -(1.+ssx)])
    dphi = dphi / denominator

    return phi, dphi


def get_detJAC(JAC: np.ndarray):
    # Inverse Jacobian
    detJAC = JAC[0, 0] * JAC[1, 1]  - JAC[0, 1] * JAC[1, 0]  
    return detJAC


def get_detJAC_3D(JAC: np.ndarray):
    # Inverse Jacobian
    detJAC = JAC[:, 0, 0] * JAC[:, 1, 1]  - JAC[:, 0, 1] * JAC[:, 1, 0]  
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


class ACT_QUADRANGLE_4(Element2D):
    #
    NODES_PER_ELEMENT = 4
    DOF_PER_NODE = 1
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model: "Model"):
        #
        self.model = model
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def initialize_variables(self):
        """
        """
        self.connectivities = None
        self.element_label = "acoustic_triangular_3"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates


    def define_integration_points(self):
        """ """
        self.nint = 4
        con = 1 / np.sqrt(3)
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
        phi[:, 0] = (1 + ssx)*(1 + ttx)
        phi[:, 1] = (1 - ssx)*(1 + ttx)
        phi[:, 2] = (1 - ssx)*(1 - ttx)
        phi[:, 3] = (1 + ssx)*(1 - ttx)
        self.phi = phi / denominator

        # derivatives
        dphi = np.zeros((self.nint, self.pint.shape[1], self.NODES_PER_ELEMENT), dtype=float)
        dphi[:, 0, 0] =  (1 + ttx) 
        dphi[:, 0, 1] = -(1 + ttx)
        dphi[:, 0, 2] = -(1 - ttx)
        dphi[:, 0, 3] =  (1 - ttx)
        dphi[:, 1, 0] =  (1 + ssx)
        dphi[:, 1, 1] =  (1 - ssx) 
        dphi[:, 1, 2] = -(1 - ssx)
        dphi[:, 1, 3] = -(1 + ssx)
        self.dphi = dphi/denominator


    def reorder_connect(self, connect_face: np.ndarray):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivities = connect_face[:, [0, 1, 2, 3]]


    def generate_ind_rows_cols(self, connect_face):
        """ This method processess the dof indices (rows and columns) for assembly"""

        self.reorder_connect(connect_face)
        dof, edof = self.DOF_PER_NODE, self.DOF_PER_ELEMENT
        ind_dof = dof * self.connectivities[:, :]

        vect_indices = ind_dof.flatten()
        ind_rows_face = ((np.tile(vect_indices, (edof,1))).T).flatten()
        ind_cols_face = (np.tile(ind_dof, edof)).flatten()

        return ind_rows_face, ind_cols_face


    def matrices_Z(self, el_index, rho=1, impedance=1):
        """ Z matrices
        """

        # element nodal coordiantes
        nodal_coords = self.nodal_coordinates[self.connectivities[el_index, :], :]

        # nodal coordiantes in the local CS
        coord_loc = get_local_coordinates(nodal_coords)

        # Jacobian matrix
        JAC = self.dphi @ coord_loc
        
        # determinant of the Jacobian matrix
        detJAC = get_detJAC_3D(JAC)
        
        # initialize the variable Ze
        Ze = 0.

        # integration loop
        for i in range(self.nint):
            N = self.phi[i, 0, :]
            Ze += -(rho / impedance) * N.T @ N * (detJAC[i, :, :]*self.wps)

        return Ze


    def excitation_F(self, el_index, Vn=1):
        """ F matrices
        """


        # element nodal coordiantes
        nodal_coords = self.nodal_coordinates[self.connectivities[el_index, :], :]

        # nodal coordiantes in the local CS
        coord_loc = get_local_coordinates(nodal_coords)

        # Jacobian matrix
        JAC = self.dphi @ coord_loc
        
        # determinant of the Jacobian matrix
        detJAC = get_detJAC_3D(JAC)

        # initialize the variable Fe
        Fe = 0.

        # integration loop
        for i in range(self.nint):
            N = self.phi[i, 0, :]  
            Fe += -(1/4) * Vn * N.T * (detJAC[i, :, :] * self.wps)

        return Fe


    def excitation_F_base(self, ee, Vn=1):
        """ F4 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        coord = self.nodal_coordinates
        connect_face = self.connectivities

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
            
            Fe += -(1/4) * Vn * N.T * (detJAC * wps)
            # print(f"base detJAC: {detJAC}")     

        return Fe

    def matrices_Z_base(self, ee, rho=1, impedance=1):
        """ Z4 matrices
        """
        #Check Connectivity -- Ansys = Gmsh

        coord = self.nodal_coordinates
        connect_face = self.connectivities

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
            
            Ze += -(rho/impedance) * N.T@N * (detJAC * wps)

        return Ze