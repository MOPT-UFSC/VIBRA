import numpy as np

from vibra.engine.elements.elements_3d.solid_elements import Element3D
from vibra.engine.properties.material import Material

def shapeT10C(l1, l2, l3):
    """Shape Functions and Derivatives."""
    # shape functions
    phi = np.zeros(10)

    l4 = 1 - l1 - l2 - l3
    phi[0] = (2 * l2 - 1) * l2
    phi[1] = (2 * l1 - 1) * l1
    phi[2] = (2 * l3 - 1) * l3
    phi[3] = (2 * l4 - 1) * l4
    phi[4] = 4 * l1 * l2
    phi[5] = 4 * l1 * l3
    phi[6] = 4 * l2 * l3
    phi[7] = 4 * l2 * l4
    phi[8] = 4 * l1 * l4
    phi[9] = 4 * l3 * l4
    #

    # derivatives
    dphi = np.zeros((3, 10))
    #
    #########################################################
    dphi[0, 0] = 0
    dphi[0, 1] = 4 * l1 - 1
    dphi[0, 2] = 0
    dphi[0, 3] = (-2) * l4 + (2 * l4 - 1) * (-1)
    dphi[0, 4] = 4 * l2
    dphi[0, 5] = 4 * l3
    dphi[0, 6] = 0
    dphi[0, 7] = -4 * l2
    dphi[0, 8] = 4 * ((+1) * l4 + l1 * (-1))
    dphi[0, 9] = -4 * l3
    #
    dphi[1, 0] = (+2) * l2 + (2 * l2 - 1) * (+1)
    dphi[1, 1] = 0
    dphi[1, 2] = 0
    dphi[1, 3] = (-2) * l4 + (2 * l4 - 1) * (-1)
    dphi[1, 4] = 4 * l1
    dphi[1, 5] = 0
    dphi[1, 6] = 4 * l3
    dphi[1, 8] = -4 * l1
    dphi[1, 7] = 4 * ((+1) * l4 + l2 * (-1))
    dphi[1, 9] = -4 * l3
    #
    dphi[2, 0] = 0
    dphi[2, 1] = 0
    dphi[2, 2] = (+2) * l3 + (2 * l3 - 1) * (+1)
    dphi[2, 3] = (-2) * l4 + (2 * l4 - 1) * (-1)
    dphi[2, 4] = 0
    dphi[2, 5] = 4 * l1
    dphi[2, 6] = 4 * l2
    dphi[2, 7] = -4 * l2
    dphi[2, 8] = -4 * l1
    dphi[2, 9] = 4 * ((+1) * l4 + l3 * (-1))

    return phi, dphi


class STRUCT_TETRAHEDRON_10S(Element3D):
    #
    nodes_per_element = 10
    dof_per_node = 3
    dof_per_element = nodes_per_element * dof_per_node

    def __init__(self, model):
        self.model = model
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()

    def initialize_variables(self):
        """ """
        self.element_label = "structural_tetrahedron_10"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connectivity = self.model.mesh.solids_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity)

    def define_integration_points(self):
        """ """
        # integration points
        self.nint = 4
        con1 = (5 - np.sqrt(5)) / 20
        con2 = (5 + 3 * np.sqrt(5)) / 20
        self.pint = np.array(
            [[con1, con1, con1], [con1, con1, con2], [con1, con2, con1], [con2, con1, con1]]
        )
        self.wps = np.array([1 / 4, 1 / 4, 1 / 4, 1 / 4])

    def process_shape_functions_and_derivatives(self):
        """This method processes the shape functions and their
        derivatives for all integration points.
        """
        l1 = self.pint[:, 0]
        l2 = self.pint[:, 1]
        l3 = self.pint[:, 2]
        #
        # shape functions
        phi = np.zeros((self.nint, self.nodes_per_element), dtype=float)
        #
        l4 = 1 - l1 - l2 - l3
        phi[:, 0] = (2 * l2 - 1) * l2
        phi[:, 1] = (2 * l1 - 1) * l1
        phi[:, 2] = (2 * l3 - 1) * l3
        phi[:, 3] = (2 * l4 - 1) * l4
        phi[:, 4] = 4 * l1 * l2
        phi[:, 5] = 4 * l1 * l3
        phi[:, 6] = 4 * l2 * l3
        phi[:, 7] = 4 * l2 * l4
        phi[:, 8] = 4 * l1 * l4
        phi[:, 9] = 4 * l3 * l4
        #
        # derivatives
        dphi = np.zeros((self.nint, self.dof_per_node, self.nodes_per_element), dtype=float)
        #
        dphi[:, 0, 0] = 0
        dphi[:, 0, 1] = 4 * l1 - 1
        dphi[:, 0, 2] = 0
        dphi[:, 0, 3] = (-2) * l4 + (2 * l4 - 1) * (-1)
        dphi[:, 0, 4] = 4 * l2
        dphi[:, 0, 5] = 4 * l3
        dphi[:, 0, 6] = 0
        dphi[:, 0, 7] = -4 * l2
        dphi[:, 0, 8] = 4 * ((+1) * l4 + l1 * (-1))
        dphi[:, 0, 9] = -4 * l3
        #
        dphi[:, 1, 0] = (+2) * l2 + (2 * l2 - 1) * (+1)
        dphi[:, 1, 1] = 0
        dphi[:, 1, 2] = 0
        dphi[:, 1, 3] = (-2) * l4 + (2 * l4 - 1) * (-1)
        dphi[:, 1, 4] = 4 * l1
        dphi[:, 1, 5] = 0
        dphi[:, 1, 6] = 4 * l3
        dphi[:, 1, 8] = -4 * l1
        dphi[:, 1, 7] = 4 * ((+1) * l4 + l2 * (-1))
        dphi[:, 1, 9] = -4 * l3
        #
        dphi[:, 2, 0] = 0
        dphi[:, 2, 1] = 0
        dphi[:, 2, 2] = (+2) * l3 + (2 * l3 - 1) * (+1)
        dphi[:, 2, 3] = (-2) * l4 + (2 * l4 - 1) * (-1)
        dphi[:, 2, 4] = 0
        dphi[:, 2, 5] = 4 * l1
        dphi[:, 2, 6] = 4 * l2
        dphi[:, 2, 7] = -4 * l2
        dphi[:, 2, 8] = -4 * l1
        dphi[:, 2, 9] = 4 * ((+1) * l4 + l3 * (-1))
        #
        self.phi = phi
        self.dphi = dphi

    def elementary_matrices(self, el_index: int, material: Material):
        """T10S stiffness and mass matrices.
        Solid187 not mixed (pure displacement)
        """

        const_mat, rho = self.get_constitutive_model(material, model_type="linear-isotropic")

        ie = self.connectivity[el_index, 1:]
        JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = self.get_detJAC_and_invJAC(JAC)
        dphi_t = invJAC @ self.dphi

        B = np.zeros((self.nint, 6, self.dof_per_element), dtype=float)
        B[:, 0, 0::3] = dphi_t[:, 0, :]
        B[:, 1, 1::3] = dphi_t[:, 1, :]
        B[:, 2, 2::3] = dphi_t[:, 2, :]
        B[:, 3, 0::3] = dphi_t[:, 1, :]
        B[:, 3, 1::3] = dphi_t[:, 0, :]
        B[:, 4, 0::3] = dphi_t[:, 2, :]
        B[:, 4, 2::3] = dphi_t[:, 0, :]
        B[:, 5, 1::3] = dphi_t[:, 2, :]
        B[:, 5, 2::3] = dphi_t[:, 1, :]

        N = np.zeros((self.nint, 3, self.dof_per_element), dtype=float)
        N[:, 0, 0::3] = self.phi
        N[:, 1, 1::3] = self.phi
        N[:, 2, 2::3] = self.phi

        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            Ke += (1 / 6) * B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])
            Me += (1 / 6) * rho * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i])

        return Ke, Me

    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivity = self.connectivity[:, [0, 6, 4, 5, 7, 10, 8, 9, 12, 11, 13]]

    def generate_ind_rows_cols(self):
        """This method processess the dof indices (rows and columns) for assembly"""

        self.reorder_connect()
        dof, edof = self.dof_per_node, self.dof_per_element

        ind_dof = (
            np.array(
                [
                    dof * self.connectivity[:, 1] - 1,
                    dof * self.connectivity[:, 1],
                    dof * self.connectivity[:, 1] + 1,
                    dof * self.connectivity[:, 2] - 1,
                    dof * self.connectivity[:, 2],
                    dof * self.connectivity[:, 2] + 1,
                    dof * self.connectivity[:, 3] - 1,
                    dof * self.connectivity[:, 3],
                    dof * self.connectivity[:, 3] + 1,
                    dof * self.connectivity[:, 4] - 1,
                    dof * self.connectivity[:, 4],
                    dof * self.connectivity[:, 4] + 1,
                    dof * self.connectivity[:, 5] - 1,
                    dof * self.connectivity[:, 5],
                    dof * self.connectivity[:, 5] + 1,
                    dof * self.connectivity[:, 6] - 1,
                    dof * self.connectivity[:, 6],
                    dof * self.connectivity[:, 6] + 1,
                    dof * self.connectivity[:, 7] - 1,
                    dof * self.connectivity[:, 7],
                    dof * self.connectivity[:, 7] + 1,
                    dof * self.connectivity[:, 8] - 1,
                    dof * self.connectivity[:, 8],
                    dof * self.connectivity[:, 8] + 1,
                    dof * self.connectivity[:, 9] - 1,
                    dof * self.connectivity[:, 9],
                    dof * self.connectivity[:, 9] + 1,
                    dof * self.connectivity[:, 10] - 1,
                    dof * self.connectivity[:, 10],
                    dof * self.connectivity[:, 10] + 1,
                ],
                dtype=int,
            )
            + 1
        ).T

        vect_indices = ind_dof.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dof, edof)).flatten()

        return self.ind_rows, self.ind_cols
