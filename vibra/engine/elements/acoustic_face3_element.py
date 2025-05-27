import numpy as np

from vibra.engine.elements.surface_elements import Element2D


def get_shape_functions_and_derivatives(ssx: np.ndarray, ttx: np.ndarray):

    """
    This function returns the shape functions and its derivatives.
    
    Parameters
    ----------
    ssx: np.ndarray
        The x coordinates of the integration points.
    
    ttx: np.ndarray
        The y coordinates of the integration points.

    Returns
    -------
    phi: np.ndarray
        The shape functions evaluated in the integration points.

    dphi: np.ndarray
        The shape functions derivatives.
    """

    # shape functions
    phi = np.array([1 - ssx - ttx, ttx, ssx], dtype=float).T

    # shape functions derivatives
    dphi = np.array([[-1, 0, 1],
                     [-1, 1, 0]], dtype=float)

    return phi, dphi

def get_jacobian_determinant(JAC: np.ndarray) -> float:
    """
    This function computes the determinant of the Jacobian
    matrix.

    Parameter
    ---------
    JAC: np.ndarray
        The Jacobian matrix.
    
    Return
    ------
    det_jac: float
        The determinant of the Jacobian matrix.
    """
    det_jac = JAC[0,0] * JAC[1,1]  - JAC[0,1] * JAC[1,0]  

    return det_jac

def get_local_coordinates(coords: np.ndarray) -> np.ndarray:
    """
    This funtion computes the local coordinates from global coordinates.

    Parameter
    ---------
    coords: np.ndarray
        An array containing the global coordinates to be converted.

    Returns
    -------
    coord_loc: np.ndarray
        The array of coordinates in the local coordinate system.
    """
    
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
    DOFS_PER_NODE = 1
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOFS_PER_NODE

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
        """ 
        Defines the integration points and their respective weights
        for the numerical integration processing.
        """
        self.nint = 3
        con1 = 1/6
        con2 = 2/3
        self.wps = 1/3
        self.pint = np.array([[con1, con1],
                              [con2, con1],
                              [con1, con2]], dtype=float)

    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        #
        self.phi, self.dphi = get_shape_functions_and_derivatives(ssx, ttx)

    def matrices_Z(self, el_index: int, rho: float = 1.0, impedance: float = 1.0) -> np.ndarray:
        """ 
        This method computes the elementary impedance matrix.

        Parameters
        ----------
        el_index: int
            The element index.
        
        rho: float, optional
            The fluid density in kg/m³.

        impedance: float, optional
            The specific impedance in kg/m².s.

        Returns
        -------
        Ze: np.ndarray
            The elementary impedance matrix.
        """

        ie = self.connect_face[el_index, :]
        coords = self.nodal_coordinates[ie, :]
        coord_loc = get_local_coordinates(coords)

        JAC = self.dphi @ coord_loc
        detJAC = get_jacobian_determinant(JAC)

        # N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        # N[:, 0, :] = self.phi

        # Ze = 0.
        # for i in range(self.nint):
        #     Ze += -(1/2) * (rho/impedance) * N[i, :, :].T @ N[i, :, :] * (detJAC*self.wps)
        #     # print(f"matrices_Z: index - {el_index} k - {i} {N[i, :, :]}")

        N = self.phi
        Ze = -(1/2) * (rho / impedance) * N.T @ N * (detJAC * self.wps)

        return Ze

    def excitation_F(self, el_index: int, Vn: float = 1.0) -> np.ndarray:
        """ 
        This method computes the elementary load vector due to the flow mass.

        Parameters
        ----------
        el_index: int
            The element index.
        
        Vn: float, optional
            The surface velocity normal to the surface in m/s.

        Returns
        -------
        Fe: np.ndarray
            The elementary load vector.
        """

        ie = self.connect_face[el_index, :]
        coords = self.nodal_coordinates[ie, :]
        coord_loc = get_local_coordinates(coords)

        JAC = self.dphi @ coord_loc
        detJAC = get_jacobian_determinant(JAC)

        N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        N[:, 0, :] = self.phi

        Fe = 0.
        for i in range(self.nint):            
            Fe += -(1/2) * Vn * N[i, :, :].T * (detJAC * self.wps)

        return Fe

        # N = self.phi
        # Fe = -(1/2) * Vn * np.sum(N.T, axis=0) * (detJAC * self.wps)

        # return Fe.reshape(-1, 1)

    def reorder_connect(self, connect_face):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """

        self.connect_face = connect_face[:, [0, 1, 2]]

    def generate_ind_rows_cols(self, connect_face):
        """
        This method processess the dofs indices (rows and columns) 
        for assembly
        """

        self.reorder_connect(connect_face)
        dofs, edofs = self.DOFS_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs * self.connect_face[:, :]

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
        con1 = 1/6
        con2 = 2/3
        wps = 1/3
        pint = np.array([[con1, con1],
                         [con2, con1],
                         [con1, con2]])

        ######################## Inicio da integração na face
        Fe = np.zeros((3,1),dtype=complex)
        N = np.zeros((1,3))
        # integration
        for i in range(nint):
            ssx, ttx = pint[i, 0], pint[i, 1]
            phi, dphi = get_shape_functions_and_derivatives(ssx, ttx)
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
        con1 = 1/6
        con2 = 2/3
        wps = 1/3
        pint = np.array([[con1, con1],
                         [con2, con1],
                         [con1, con2]])

        ######################## Inicio da integração na face
        Ze = np.zeros((3,3),dtype=complex)
        N = np.zeros((1,3))
        # integration
        for i in range(nint):
            ssx, ttx = pint[i, 0], pint[i, 1]
            phi, dphi = get_shape_functions_and_derivatives(ssx,ttx)
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
    
    
    def get_element_face_normal(self, connect):
        
        # ie = self.faces_connectivity[element_id, 4:]
        coords = self.nodal_coordinates[connect, 1:]

        P1 = coords[0, :]
        P2 = coords[1, :]
        P3 = coords[2, :]

        P2P1 = np.array(P2 - P1)
        P3P1 = np.array(P3 - P1)

        cross = np.cross(P2P1, P3P1)
        normal = cross / np.linalg.norm(cross)

        return normal