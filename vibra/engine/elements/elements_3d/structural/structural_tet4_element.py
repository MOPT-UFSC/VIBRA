import numpy as np

from vibra.engine.elements.solid_elements import Element3D
from vibra.engine.properties.material import Material

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

# fmt: off


class STRUCT_TETRAHEDRON_4S(Element3D):

    NODES_PER_ELEMENT = 4
    DOF_PER_NODE = 3
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model: "Model"):

        self.model = model

        self.connectivity = None
        self.element_label = "structural_tetrahedron_4"
        
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.solids_connectivity = self.model.mesh.solids_connectivity

        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.solids_connectivity)

        self.define_integration_points()
        self.process_shape_functions_and_derivatives()


    def define_integration_points(self, integration_points: int=4):
        """ 
        This method defines the integration points and their
        weights for numerical integration.
        """
        # NOTE: Atalla, Noureddine.; Sgard Franck. Finite Element and Boundary Methods in Structural Acoustics and Vibration. 1st Ed. 2015
        # The numerical integration points and their respective weights for the 4- and 5-point integration rules are found on page 177.

        # 4-point integration rule for unit tetrahedron element
        if integration_points == 4:

            self.nint = 4

            a = (5 - np.sqrt(5)) / 20
            b = (5 + 3 * np.sqrt(5)) / 20

            w1 = 1/24

            self.num_int_data = np.array([
                [a, a, a, w1], 
                [a, a, b, w1], 
                [a, b, a, w1], 
                [b, a, a, w1],
                ], dtype=float)

        # 5-point integration rule for unit tetrahedron element
        else:

            self.nint = 5

            a = 1/4
            b = 1/6
            c = 1/2

            w1 = -2/15
            w2 = 3/40

            self.num_int_data = np.array([
                [a, a, a, w1],
                [b, b, b, w2],
                [b, b, c, w2],
                [b, c, b, w2],
                [c, b, b, w2],
                ], dtype=float)

        self.wps = self.num_int_data[:, -1].reshape(-1, 1, 1)


    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """

        ## coordinates from integration points
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
        phi = np.zeros((Nz, self.NODES_PER_ELEMENT), dtype=float)

        # define isoparametric coordiante xi_4
        xi_4 = 1 - xi_1 - xi_2 - xi_3

        phi[:, 0] = xi_4      # ->      (0.0, 0.0, 0.0)   Node 1
        phi[:, 1] = xi_2      # ->      (0.0, 1.0, 0.0)   Node 2
        phi[:, 2] = xi_3      # ->      (0.0, 0.0, 1.0)   Node 3
        phi[:, 3] = xi_1      # ->      (1.0, 0.0, 0.0)   Node 4

        ## derivatives of shape functions (obtained from the Atalla and Sgard proposed shape functions)
        dphi = np.zeros((3, self.NODES_PER_ELEMENT), dtype=float)
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


    def elementary_matrices(self, el_index: int, material: Material):
        """Stiffness and mass matrices.
        This is not a p-u mixed fomulation. Do not compare with SOLID285.
        """

        rho = material.material_density
        const_mat, rho = self.get_constitutive_model(material, model_type="linear-isotropic")

        # nodes from element
        elem_nodes = self.connectivity[el_index, 1:]

        # element nodal coords
        coords = self.nodal_coordinates[elem_nodes, 1:4]

        # Jacobian matrix
        JAC = self.dphi @ coords

        # Jacobian determinant and inverse
        detJAC, invJAC = self.get_detJAC_and_invJAC(JAC)

        # derivatives
        dphi_t = invJAC @ self.dphi

        B = np.zeros((6, self.DOF_PER_ELEMENT), dtype=float)
        B[0, 0::3] = dphi_t[0, :]
        B[1, 1::3] = dphi_t[1, :]
        B[2, 2::3] = dphi_t[2, :]
        B[3, 0::3] = dphi_t[1, :]
        B[3, 1::3] = dphi_t[0, :]
        B[4, 0::3] = dphi_t[2, :]
        B[4, 2::3] = dphi_t[0, :]
        B[5, 1::3] = dphi_t[2, :]
        B[5, 2::3] = dphi_t[1, :]

        N = np.zeros((self.nint, 3, self.DOF_PER_ELEMENT), dtype=float)
        N[:, 0, 0::3] = self.phi
        N[:, 1, 1::3] = self.phi
        N[:, 2, 2::3] = self.phi

        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            Ke += B.T @ const_mat @ B * (detJAC * self.wps[i])
            Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC * self.wps[i])

        return Ke, Me


    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        if self.solids_connectivity.shape[1] == self.NODES_PER_ELEMENT + 4:
            self.connectivity = self.solids_connectivity[:, [0, 6, 4, 5, 7]]


    def generate_ind_rows_cols(self, reorder: bool = True):
        """This method processess the dof indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.solids_connectivity[:, [0, 4, 5, 6, 7]]

        dof = self.DOF_PER_NODE
        edof = self.DOF_PER_ELEMENT
        n_el = self.solids_connectivity.shape[0]

        local_dof = np.arange(dof, dtype=int)
        ind_dof = np.zeros((n_el, edof), dtype=int)

        for j in range(self.NODES_PER_ELEMENT):
            ind_dof[:, j*dof : (1 + j)*dof] = dof * self.connectivity[:, j+1].reshape(-1, 1) + local_dof

        self.ind_rows = ((np.tile(ind_dof.flatten(), (edof, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dof, edof)).flatten()

        return self.ind_rows, self.ind_cols

# fmt: on