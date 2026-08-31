
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_1d.line_elements import Element1D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


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
        The array of the stacked coordinates in the local coordinate system.
    """

    X1, X2, X3 = coords[:, 1]
    Y1, Y2, Y3 = coords[:, 2]
    Z1, Z2, Z3 = coords[:, 3]

    vec_13 = np.array([X3-X1, Y3-Y1, Z3-Z1]).T
    vec_32 = np.array([X2-X3, Y2-Y3, Z2-Z3]).T

    coord_loc = np.zeros((3, 1), dtype=float)
    coord_loc[0, 0] = -np.linalg.norm(vec_13)
    coord_loc[1, 0] = np.linalg.norm(vec_32)

    return coord_loc


class LINE_3(Element1D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):

        self.model = model
        self.dof_per_node = dof_per_node
        self.nodes_per_element = nodes_per_element

        self.connectivities = None
        self.element_label = ""
        self.nodal_coordinates = self.model.mesh.nodal_coordinates

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    @property
    def dof_per_element(self):
        return self.nodes_per_element * self.dof_per_node


    def define_integration_points(self):
        """ 
        Defines the integration points and their respective weights
        for the numerical integration processing.
        """
        self.nint_K = 2
        self.nint_M = 2


    def get_shape_functions_and_derivatives(self, xi: np.ndarray):

        """
        This function returns the shape functions and its derivatives.
        
        Parameters
        ----------
        xi: np.ndarray
            The x coordinates of the integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        # shape functions
        phi = np.zeros((xi.size, 1, self.nodes_per_element), dtype=float)

        phi[:, 0, 0] = 0.5*(-xi + xi**2)
        phi[:, 0, 1] = 0.5*( xi + xi**2)
        phi[:, 0, 2] = (1 - xi**2)

        # shape functions derivatives
        dphi = np.zeros((xi.size, 1, self.nodes_per_element), dtype=float)

        dphi[:, 0, 0] = -0.5 + xi
        dphi[:, 0, 1] =  0.5 + xi
        dphi[:, 0, 2] = -2*xi

        return phi, dphi


    def get_integration_points_data(self, integration_points: int=3):
        """ 
        Defines the integration points and their respective weights
        for the numerical integration processing.
        """

        if integration_points == 2:

            a = 1 / np.sqrt(3)
            p_int = np.array([-a, a], dtype=float)
            wps = np.array([1, 1], dtype=float)

        elif integration_points == 3:

            a = np.sqrt(15) / 5
            w1 = 5/9
            w2 = 8/9
            p_int = np.array([-a, a, 0.0], dtype=float)
            wps = np.array([w1, w1, w2], dtype=float)

        else:
            NotImplementedError(f"Non-implement integration points for {integration_points}.")
            return (None, None)

        return (p_int, wps.reshape(-1, 1, 1))


    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """

        # calculate the shape functions and derivatives for stiffness matrix
        pint_K, self.wps_K = self.get_integration_points_data(integration_points=self.nint_K)
        self.phi_K, self.dphi_K = self.get_shape_functions_and_derivatives(pint_K)

        # calculate the shape functions and derivatives for mass matrix
        pint_M, self.wps_M = self.get_integration_points_data(integration_points=self.nint_M)
        self.phi_M, self.dphi_M = self.get_shape_functions_and_derivatives(pint_M)


    def get_stacked_local_coordinates(self) -> np.ndarray:
        """
        This funtion computes the local coordinates from global coordinates.

        Parameter
        ---------
        coords: np.ndarray
            An array containing the global coordinates to be converted.

        Returns
        -------
        coord_loc: np.ndarray
            The array of the stacked coordinates in the local coordinate system.
        """

        # #Jacobian ###############
        # delta_x = x2 - x1
        # delta_y = y2 - y1
        # delta_z = z2 - z1
        # le  = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2) 
        # #
        # delta_x_31 = x3 - x1
        # delta_y_31 = y3 - y1
        # delta_z_31 = z3 - z1
        # l31 = np.sqrt(delta_x_31**2 + delta_y_31**2 + delta_z_31**2) 
        # #
        # delta_x_23 = x2 - x3
        # delta_y_23 = y2 - y3
        # delta_z_23 = z2 - z3
        # l23 = np.sqrt(delta_x_23**2 + delta_y_23**2 + delta_z_23**2) 
        # #
        # pksi = pint_k[i]
        # detJac = pksi*(-l31+l23) + (le)/2
        # invJac = 1/detJac
        # #

        X1 = self.nodal_coordinates[self.connectivities[:, 0], 1]
        Y1 = self.nodal_coordinates[self.connectivities[:, 0], 2]
        Z1 = self.nodal_coordinates[self.connectivities[:, 0], 3]

        X2 = self.nodal_coordinates[self.connectivities[:, 1], 1]
        Y2 = self.nodal_coordinates[self.connectivities[:, 1], 2]
        Z2 = self.nodal_coordinates[self.connectivities[:, 1], 3]

        X3 = self.nodal_coordinates[self.connectivities[:, 2], 1]
        Y3 = self.nodal_coordinates[self.connectivities[:, 2], 2]
        Z3 = self.nodal_coordinates[self.connectivities[:, 2], 3]

        nel = self.connectivities.shape[0]
        vec_13 = np.array([X3-X1, Y3-Y1, Z3-Z1]).T
        vec_32 = np.array([X2-X3, Y2-Y3, Z2-Z3]).T
        # vec_21 = np.array([X2-X1, Y2-Y1, Z2-Z1]).T

        coord_loc = np.zeros((nel, self.nodes_per_element, 1), dtype=float)
        coord_loc[:, 0, 0] = -np.linalg.norm(vec_13, axis=1)
        coord_loc[:, 1, 0] = np.linalg.norm(vec_32, axis=1)

        return coord_loc#, Le


    def reorder_connect(self, connectivities: np.ndarray):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model.

        Parameter
        ---------
        connectivities: np.ndarray
            An array containing the lines connectivities.
        """
        self.connectivities = connectivities[:, [0, 1, 2]]


# def shape_3n(ksi):
#     """
# Created on Wed Nov 20 10:24:26 2019
# @author: Olavo M. Silva
# Linear shape functions and derivatives for 3-node topology

#     """
#     phi  = np.array( [0.5*(-ksi+ksi**2), 0.5*(+ksi+ksi**2), 1.0*(1+ksi**2)] )
#     dphi = np.array( [     (-0.5 + ksi),       (0.5 + ksi),        (2*ksi)] )
#     #       
#     return phi, dphi
# ######################################################  

# def matrices(x1,y1,z1,x2,y2,z2,x3,y3,z3):
#     """
#     """
#     npel = 3
#     ngln = 1
#     #
#     ###################################################################################################
#     #Preparing for numeric integration
#     nint_k = 2 #Stiff: reduced integration
#     pint_k = np.array([-0.577350269189626,0.577350269189626])
#     wfact_k = np.array([1.0,1.0])
#     nint_m = 3 #Mass: Full integration #Distributed external load: Full integration
#     pint_m = np.array([-0.774596669241483,0.7745966692414836, 0.0])
#     wfact_m = np.array([0.555555555555555,0.5555555555555555, 0.888888888888888])  # noqa: F841
#     #
#     Ke = np.zeros((npel*ngln,npel*ngln))
#     Me = np.zeros((npel*ngln,npel*ngln))
#     #
#     #Jacobian ###############
#     delta_x = x2 - x1
#     delta_y = y2 - y1
#     delta_z = z2 - z1
#     le  = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2) 
#     #
#     delta_x_31 = x3 - x1
#     delta_y_31 = y3 - y1
#     delta_z_31 = z3 - z1
#     l31 = np.sqrt(delta_x_31**2 + delta_y_31**2 + delta_z_31**2) 
#     #
#     delta_x_23 = x2 - x3
#     delta_y_23 = y2 - y3
#     delta_z_23 = z2 - z3
#     l23 = np.sqrt(delta_x_23**2 + delta_y_23**2 + delta_z_23**2) 
#     #
#     pksi = pint_k[i]
#     detJac = pksi*(-l31+l23) + (le)/2
#     invJac = 1/detJac
#     #
#     B = np.zeros((1,3))
#     N = np.zeros((1,3))
#     ############################## STIFFNESS MATRIX ###################################
#     for i in range(nint_k):

#         phi, dphi = shape_3n(pksi)
#         dphi = invJac*dphi
#         #
#         for iii in range(3):
#             B[0,iii]=dphi[0,iii]             
#         #       
#         Ke += B.T@B*(detJac*wfact_k[i])
#     #
#     ############################## MASS MATRIX ########################################
#     for i in range(nint_m):
#         pksi = pint_m[i]
#         phi, dphi = shape_3n(pksi)
#         #
#         for iii in range(3):
#             N[0,iii]=phi[iii]
#         #    
#         Me += N.T@N*(detJac*wfact_k[i])

#     return Ke, Me