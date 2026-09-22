
from typing import TYPE_CHECKING

from vibra.engine.elements.elements_3d.solid_elements import Element3D

if TYPE_CHECKING:
    from vibra.engine.model import Model

import numpy as np


class Pyramid13(Element3D):

    def __init__(self, model: "Model", dof_per_node: int, nodes_per_element: int):

        self.model = model
        self.dof_per_node = dof_per_node
        self.nodes_per_element = nodes_per_element

        self.connectivities = None
        self.element_label = ""

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    @property
    def corner_nodes_indices(self):
        return np.arange(5, dtype=int)


    def define_integration_points(self, integration_points: int=11):
        """ 
        This method defines the integration points and their
        weights for numerical integration.
        """
        self.nint = integration_points
        self.num_int_data = self.integration_points_data_for_tetrahedrons(integration_points)
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
        self.phi_inv = self.inverse_of_trilinear_shape_functions()


    def inverse_of_trilinear_shape_functions(self):
        """
        This method returns the inverse of shape functions matrix N applied
        at integration points (Gauss-Legendre quadrature points).
        """
        N = self.phi
        n_intp, n_nodes = N.shape

        if n_intp == n_nodes:
            # print("N_int = N_nodes")
            return np.linalg.inv(N)

        elif n_intp > n_nodes:
            # print("N_int > N_nodes")
            return np.linalg.inv(N.T @ N) @ N.T

        else:
            print("Not implemented stress extrapolation for N_int < N_nodes")
            return None

    def get_shape_functions_and_derivatives(self, xi: np.ndarray | float, eta: np.ndarray | float, zeta: np.ndarray | float):

        """
        This method returns the shape functions and its derivatives.
        
        Parameters
        ----------
        xi: np.ndarray
            The x coordinates of the integration points.
        
        eta: np.ndarray
            The y coordinates of the integration points.

        zeta: np.ndarray
            The z coordinates of the integration points.

        Returns
        -------
        phi: np.ndarray
            The shape functions evaluated in the integration points.

        dphi: np.ndarray
            The shape functions derivatives.
        """

        if isinstance(xi, np.ndarray):
            Nz = xi.size
        else:
            Nz = 1

        ##NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015

        # define the shape functions (Atalla and Sgard, 2015, pg. 170)
        phi = np.zeros((Nz, self.nodes_per_element), dtype=float)

        # Intermediate base nodes (Node 6 to 9) -> Indices 5 a 8
        phi[:, 5] = 0.5 * (1.0 - xi**2) * (1.0 - eta) * ((1 - zeta) / 2.0)  # Node 6 -> (-1.0, -1.0, -1.0)   
        phi[:, 6] = 0.5 * (1.0 + xi) * (1.0 - eta**2) * ((1 - zeta) / 2.0)  # Node 7 -> (-1.0, -1.0, -1.0) 
        phi[:, 7] = 0.5 * (1.0 - xi**2) * (1.0 + eta) * ((1 - zeta) / 2.0)  # Node 8 -> (-1.0, -1.0, -1.0) 
        phi[:, 8] = 0.5 * (1.0 - xi) * (1.0 - eta**2) * ((1 - zeta) / 2.0)  # Node 9 -> (-1.0, -1.0, -1.0) 

        # Intermediate edges nodes (Node 10 a 13) -> Indices 9 a 12
        phi[:, 9]  = 0.25 * (1.0 - xi) * (1.0 - eta) * (1.0 + zeta)  # Node 10 -> (-1.0, -1.0, -1.0) 
        phi[:, 10] = 0.25 * (1.0 + xi) * (1.0 - eta) * (1.0 + zeta)  # Node 11 -> (-1.0, -1.0, -1.0) 
        phi[:, 11] = 0.25 * (1.0 + xi) * (1.0 + eta) * (1.0 + zeta)  # Node 12 -> (-1.0, -1.0, -1.0) 
        phi[:, 12] = 0.25 * (1.0 - xi) * (1.0 + eta) * (1.0 + zeta)  # Node 13 -> (-1.0, -1.0, -1.0) 

        # 3. Base vertices nodes (Node 1 to 4) -> Indices 0 a 3 (Rational formulation)
        rat_term = (xi * eta) / (1 - zeta)
        
        phi[:, 0] = 0.25 * ((1.0 - xi) * (1.0 - eta) * (1 - zeta) + rat_term * (1.0 - xi) * (1.0 - eta)) - 0.5 * (phi[:, 5] + phi[:, 8]) - phi[:, 9]
        phi[:, 1] = 0.25 * ((1.0 + xi) * (1.0 - eta) * (1 - zeta) - rat_term * (1.0 + xi) * (1.0 - eta)) - 0.5 * (phi[:, 5] + phi[:, 6]) - phi[:, 10]
        phi[:, 2] = 0.25 * ((1.0 + xi) * (1.0 + eta) * (1 - zeta) + rat_term * (1.0 + xi) * (1.0 + eta)) - 0.5 * (phi[:, 6] + phi[:, 7]) - phi[:, 11]
        phi[:, 3] = 0.25 * ((1.0 - xi) * (1.0 + eta) * (1 - zeta) - rat_term * (1.0 - xi) * (1.0 + eta)) - 0.5 * (phi[:, 7] + phi[:, 8]) - phi[:, 12]

        # 4. Apex vertex (Node 5) -> Index 4
        phi[:, 4] = 0.5 * (1.0 + zeta) - (phi[:, 9] + phi[:, 10] + phi[:, 11] + phi[:, 12])

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((Nz, 3, self.nodes_per_element), dtype=float)

        # dN / dxi
        dphi[:, 0, 0] = (1 / 4) * (-(1 - eta) + eta * (1 + zeta) / (2 * (1 - zeta))) 
        dphi[:, 0, 1] = (1 / 4) * (+(1 - eta) - eta * (1 + zeta) / (2 * (1 - zeta)))
        dphi[:, 0, 2] = (1 / 4) * (+(1 - eta) + eta * (1 + zeta) / (2 * (1 - zeta)))
        dphi[:, 0, 3] = (1 / 4) * (-(1 - eta) - eta * (1 + zeta) / (2 * (1 - zeta)))
        dphi[:, 0, 4] = 0

        # dN / deta
        dphi[:, 1, 0] = (1 / 4) * (-(1 - xi) + (xi * (1 + zeta) / (2 * (1 - zeta))))
        dphi[:, 1, 1] = (1 / 4) * (-(1 - xi) - (xi * (1 + zeta) / (2 * (1 - zeta))))
        dphi[:, 1, 2] = (1 / 4) * (+(1 - xi) + (xi * (1 + zeta) / (2 * (1 - zeta))))
        dphi[:, 1, 3] = (1 / 4) * (+(1 - xi) - (xi * (1 + zeta) / (2 * (1 - zeta))))
        dphi[:, 1, 4] =  0

        # dN / dzeta
        dphi[:, 2, 0] = (1 / 4) * (-(1 / 2) + (xi * eta) / ((1 - zeta)**2))
        dphi[:, 2, 1] = (1 / 4) * (-(1 / 2) - (xi * eta) / ((1 - zeta)**2))
        dphi[:, 2, 2] = (1 / 4) * (-(1 / 2) + (xi * eta) / ((1 - zeta)**2))
        dphi[:, 2, 3] = (1 / 4) * (-(1 / 2) - (xi * eta) / ((1 - zeta)**2))
        dphi[:, 2, 4] = (1 / 2) * zeta

        if Nz == 1:
            return phi[0, :], dphi[0, :, :]

        return phi, dphi


    def reorder_connect(self):
        """
        Reordering connectivity matrix to adequate 
        the GMSH connectivity to the FE model
        """
        # GMSH nodes ordering -> [0, 1, 2, 3, 4, 5, 8, 10, 6, 7, 9, 11, 12]
        self.connectivities = self.model.mesh.solids_connectivity[:, [4, 5, 6, 7, 8, 9, 12, 14, 10, 11, 13, 15, 16]]


def shape_functions_and_derivatives_13n(xi, eta, zeta):
    """
    Calcula as 13 funções de forma e suas respectivas derivadas parciais
    em relação a xi, eta e zeta para o elemento piramidal quadrático não-degenerado.
    
    Parâmetros:
    xi, eta, zeta : float
        Coordenadas isoparamétricas do ponto de avaliação.
        
    Retorna:
    N : numpy.ndarray
        Array de tamanho (13,) com as funções de forma.
    dN : numpy.ndarray
        Matriz de tamanho (3, 13) com as derivadas parciais.
        Linha 0: dN/dxi, Linha 1: dN/deta, Linha 2: dN/dzeta.
    """
    N = np.zeros(13)
    dN = np.zeros((3, 13))
    
    # Tolerância de segurança para evitar divisão por zero no ápice
    eps = 1e-14
    V = 1.0 - zeta
    if abs(V) < eps:
        V = eps
    
    # --- 1. Nós Intermediários da Base (N6 a N9 -> índices 5 a 8) ---
    N[5] = 0.25 * (1.0 - xi**2) * (1.0 - eta) * V
    dN[0, 5] = -0.5 * xi * (1.0 - eta) * V
    dN[1, 5] = -0.25 * (1.0 - xi**2) * V
    dN[2, 5] = -0.25 * (1.0 - xi**2) * (1.0 - eta)
    
    N[6] = 0.25 * (1.0 + xi) * (1.0 - eta**2) * V
    dN[0, 6] =  0.25 * (1.0 - eta**2) * V
    dN[1, 6] = -0.5 * eta * (1.0 + xi) * V
    dN[2, 6] = -0.25 * (1.0 + xi) * (1.0 - eta**2)
    
    N[7] = 0.25 * (1.0 - xi**2) * (1.0 + eta) * V
    dN[0, 7] = -0.5 * xi * (1.0 + eta) * V
    dN[1, 7] =  0.25 * (1.0 - xi**2) * V
    dN[2, 7] = -0.25 * (1.0 - xi**2) * (1.0 + eta)
    
    N[8] = 0.25 * (1.0 - xi) * (1.0 - eta**2) * V
    dN[0, 8] = -0.25 * (1.0 - eta**2) * V
    dN[1, 8] = -0.5 * eta * (1.0 - xi) * V
    dN[2, 8] = -0.25 * (1.0 - xi) * (1.0 - eta**2)

    # --- 2. Nós Intermediários das Arestas Inclinadas (N10 a N13 -> índices 9 a 12) ---
    Z = 1.0 + zeta
    N[9] = 0.25 * (1.0 - xi) * (1.0 - eta) * Z
    dN[0, 9] = -0.25 * (1.0 - eta) * Z
    dN[1, 9] = -0.25 * (1.0 - xi) * Z
    dN[2, 9] =  0.25 * (1.0 - xi) * (1.0 - eta)
    
    N[10] = 0.25 * (1.0 + xi) * (1.0 - eta) * Z
    dN[0, 10] =  0.25 * (1.0 - eta) * Z
    dN[1, 10] = -0.25 * (1.0 + xi) * Z
    dN[2, 10] =  0.25 * (1.0 + xi) * (1.0 - eta)
    
    N[11] = 0.25 * (1.0 + xi) * (1.0 + eta) * Z
    dN[0, 11] =  0.25 * (1.0 + eta) * Z
    dN[1, 11] =  0.25 * (1.0 + xi) * Z
    dN[2, 11] =  0.25 * (1.0 + xi) * (1.0 + eta)
    
    N[12] = 0.25 * (1.0 - xi) * (1.0 + eta) * Z
    dN[0, 12] = -0.25 * (1.0 + eta) * Z
    dN[1, 12] =  0.25 * (1.0 - xi) * Z
    dN[2, 12] =  0.25 * (1.0 - xi) * (1.0 + eta)

    # --- 3. Vértices da Base (N1 a N4 -> índices 0 a 3) ---
    term_rat = (xi * eta) / V
    dtr_dxi = eta / V
    dtr_deta = xi / V
    dtr_dzeta = (xi * eta) / (V**2)
    
    # Nó 1
    N[0] = 0.25 * ((1.0 - xi) * (1.0 - eta) * V + term_rat * (1.0 - xi) * (1.0 - eta)) - 0.5 * (N[5] + N[8]) - N[9]
    dN[0, 0] = 0.25 * (-(1.0 - eta) * V + dtr_dxi * (1.0 - xi) * (1.0 - eta) - term_rat * (1.0 - eta)) - 0.5 * (dN[0, 5] + dN[0, 8]) - dN[0, 9]
    dN[1, 0] = 0.25 * (-(1.0 - xi) * V + dtr_deta * (1.0 - xi) * (1.0 - eta) - term_rat * (1.0 - xi)) - 0.5 * (dN[1, 5] + dN[1, 8]) - dN[1, 9]
    dN[2, 0] = 0.25 * (-(1.0 - xi) * (1.0 - eta) + dtr_dzeta * (1.0 - xi) * (1.0 - eta)) - 0.5 * (dN[2, 5] + dN[2, 8]) - dN[2, 9]
    
    # Nó 2
    N[1] = 0.25 * ((1.0 + xi) * (1.0 - eta) * V - term_rat * (1.0 + xi) * (1.0 - eta)) - 0.5 * (N[5] + N[6]) - N[10]
    dN[0, 1] = 0.25 * ((1.0 - eta) * V - dtr_dxi * (1.0 + xi) * (1.0 - eta) - term_rat * (1.0 - eta)) - 0.5 * (dN[0, 5] + dN[0, 6]) - dN[0, 10]
    dN[1, 1] = 0.25 * (-(1.0 + xi) * V - dtr_deta * (1.0 + xi) * (1.0 - eta) + term_rat * (1.0 + xi)) - 0.5 * (dN[1, 5] + dN[1, 6]) - dN[1, 10]
    dN[2, 1] = 0.25 * (-(1.0 + xi) * (1.0 - eta) - dtr_dzeta * (1.0 + xi) * (1.0 - eta)) - 0.5 * (dN[2, 5] + dN[2, 6]) - dN[2, 10]
    
    # Nó 3
    N[2] = 0.25 * ((1.0 + xi) * (1.0 + eta) * V + term_rat * (1.0 + xi) * (1.0 + eta)) - 0.5 * (N[6] + N[7]) - N[11]
    dN[0, 2] = 0.25 * ((1.0 + eta) * V + dtr_dxi * (1.0 + xi) * (1.0 + eta) + term_rat * (1.0 + eta)) - 0.5 * (dN[0, 6] + dN[0, 7]) - dN[0, 11]
    dN[1, 2] = 0.25 * ((1.0 + xi) * V + dtr_deta * (1.0 + xi) * (1.0 + eta) + term_rat * (1.0 + xi)) - 0.5 * (dN[1, 6] + dN[1, 7]) - dN[1, 11]
    dN[2, 2] = 0.25 * (-(1.0 + xi) * (1.0 + eta) + dtr_dzeta * (1.0 + xi) * (1.0 + eta)) - 0.5 * (dN[2, 6] + dN[2, 7]) - dN[2, 11]
    
    # Nó 4
    N[3] = 0.25 * ((1.0 - xi) * (1.0 + eta) * V - term_rat * (1.0 - xi) * (1.0 + eta)) - 0.5 * (N[7] + N[8]) - N[12]
    dN[0, 3] = 0.25 * (-(1.0 + eta) * V - dtr_dxi * (1.0 - xi) * (1.0 + eta) + term_rat * (1.0 + eta)) - 0.5 * (dN[0, 7] + dN[0, 8]) - dN[0, 12]
    dN[1, 3] = 0.25 * ((1.0 - xi) * V - dtr_deta * (1.0 - xi) * (1.0 + eta) - term_rat * (1.0 - xi)) - 0.5 * (dN[1, 7] + dN[1, 8]) - dN[1, 12]
    dN[2, 3] = 0.25 * (-(1.0 - xi) * (1.0 + eta) - dtr_dzeta * (1.0 - xi) * (1.0 + eta)) - 0.5 * (dN[2, 7] + dN[2, 8]) - dN[2, 12]

    # --- 4. Ápice (N5 -> índice 4) ---
    N[4] = 0.5 * (1.0 + zeta) - (N[9] + N[10] + N[11] + N[12])
    dN[0, 4] = - (dN[0, 9] + dN[0, 10] + dN[0, 11] + dN[0, 12])
    dN[1, 4] = - (dN[1, 9] + dN[1, 10] + dN[1, 11] + dN[1, 12])
    dN[2, 4] = 0.5 - (dN[2, 9] + dN[2, 10] + dN[2, 11] + dN[2, 12])
    
    return N, dN
