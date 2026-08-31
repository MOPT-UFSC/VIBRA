import numpy as np

from vibra.engine.elements.solid_elements import Element3D
from vibra.engine.properties.material import Material


class STRUCT_HEXAHEDRON_8(Element3D):
    #
    nodes_per_element = 8
    dof_per_node = 3
    dof_per_element = nodes_per_element * dof_per_node

    def __init__(self, model):
        self.model = model
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()

    def initialize_variables(self):
        """ """
        self.element_label = "structural_hexahedron_8"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connectivity = self.model.mesh.solids_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity)

    def define_integration_points(self):
        """ """
        # integration points
        self.nint = 8
        con = 1 / np.sqrt(3)
        self.wps = 1

        self.pint = np.array(
            [
                [-con, -con, -con],
                [con, -con, -con],
                [con, con, -con],
                [-con, con, -con],
                [-con, -con, con],
                [con, -con, con],
                [con, con, con],
                [-con, con, con],
            ]
        )

    def process_shape_functions_and_derivatives(self):
        """This method processes the shape functions and their
        derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        rrx = self.pint[:, 2]
        #
        denominator = 8
        # shape functions
        phi = np.zeros((self.nint, self.nodes_per_element), dtype=float)
        #
        phi[:, 0] = (1.0 - ssx) * (1.0 - ttx) * (1.0 - rrx)
        phi[:, 1] = (1.0 + ssx) * (1.0 - ttx) * (1.0 - rrx)
        phi[:, 2] = (1.0 + ssx) * (1.0 + ttx) * (1.0 - rrx)
        phi[:, 3] = (1.0 - ssx) * (1.0 + ttx) * (1.0 - rrx)
        phi[:, 4] = (1.0 - ssx) * (1.0 - ttx) * (1.0 + rrx)
        phi[:, 5] = (1.0 + ssx) * (1.0 - ttx) * (1.0 + rrx)
        phi[:, 6] = (1.0 + ssx) * (1.0 + ttx) * (1.0 + rrx)
        phi[:, 7] = (1.0 - ssx) * (1.0 + ttx) * (1.0 + rrx)
        phi = phi / denominator
        #
        # derivatives
        dphi = np.zeros((self.nint, self.dof_per_node, self.nodes_per_element), dtype=float)
        #
        dphi[:, 0, 0] = (-1.0) * (1.0 - ttx) * (1.0 - rrx)
        dphi[:, 0, 1] = (1.0) * (1.0 - ttx) * (1.0 - rrx)
        dphi[:, 0, 2] = (1.0) * (1.0 + ttx) * (1.0 - rrx)
        dphi[:, 0, 3] = (-1.0) * (1.0 + ttx) * (1.0 - rrx)
        dphi[:, 0, 4] = (-1.0) * (1.0 - ttx) * (1.0 + rrx)
        dphi[:, 0, 5] = (1.0) * (1.0 - ttx) * (1.0 + rrx)
        dphi[:, 0, 6] = (1.0) * (1.0 + ttx) * (1.0 + rrx)
        dphi[:, 0, 7] = (-1.0) * (1.0 + ttx) * (1.0 + rrx)

        dphi[:, 1, 0] = (1.0 - ssx) * (-1.0) * (1.0 - rrx)
        dphi[:, 1, 1] = (1.0 + ssx) * (-1.0) * (1.0 - rrx)
        dphi[:, 1, 2] = (1.0 + ssx) * (1.0) * (1.0 - rrx)
        dphi[:, 1, 3] = (1.0 - ssx) * (1.0) * (1.0 - rrx)
        dphi[:, 1, 4] = (1.0 - ssx) * (-1.0) * (1.0 + rrx)
        dphi[:, 1, 5] = (1.0 + ssx) * (-1.0) * (1.0 + rrx)
        dphi[:, 1, 6] = (1.0 + ssx) * (1.0) * (1.0 + rrx)
        dphi[:, 1, 7] = (1.0 - ssx) * (1.0) * (1.0 + rrx)

        dphi[:, 2, 0] = (1.0 - ssx) * (1.0 - ttx) * (-1.0)
        dphi[:, 2, 1] = (1.0 + ssx) * (1.0 - ttx) * (-1.0)
        dphi[:, 2, 2] = (1.0 + ssx) * (1.0 + ttx) * (-1.0)
        dphi[:, 2, 3] = (1.0 - ssx) * (1.0 + ttx) * (-1.0)
        dphi[:, 2, 4] = (1.0 - ssx) * (1.0 - ttx) * (1.0)
        dphi[:, 2, 5] = (1.0 + ssx) * (1.0 - ttx) * (1.0)
        dphi[:, 2, 6] = (1.0 + ssx) * (1.0 + ttx) * (1.0)
        dphi[:, 2, 7] = (1.0 - ssx) * (1.0 + ttx) * (1.0)

        dphi = dphi / denominator

        self.phi = phi
        self.dphi = dphi

    def elementary_matrices(self, el_index: int, material: Material):
        """This method returns elementary stiffness and mass matrices for HEXAHEDRON-8 nodes.
        ANSYS SOLID45 w/o extra diplacements (very simple)
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
            Ke += B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC[i, :, :] * self.wps)
            Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps)

        return Ke, Me

    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivity = self.connectivity[:, [0, 4, 5, 6, 7, 8, 9, 10, 11]]

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
                ],
                dtype=int,
            )
            + 1
        ).T

        vect_indices = ind_dof.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dof, edof)).flatten()

        return self.ind_rows, self.ind_cols
