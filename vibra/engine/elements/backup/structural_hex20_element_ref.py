import numpy as np

from vibra.engine.elements.elements_3d.solid_elements import Element3D
from vibra.engine.properties.material import Material


class StructHexahedron20(Element3D):
    #
    nodes_per_element = 20
    dof_per_node = 3
    dof_per_element = nodes_per_element * dof_per_node

    def __init__(self, model):
        self.model = model
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()

    def initialize_variables(self):
        """ """
        self.element_label = "structural_hexahedron_20"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connectivity = self.model.mesh.solids_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity)

    def define_integration_points(self):
        """ """
        # integration points
        self.nint = 14
        self.wps = np.zeros((self.nint))
        con1 = np.sqrt(19 / 33)
        con2 = np.sqrt(19 / 30)
        # self.pint = np.zeros((self.nint,3))
        self.pint = np.array(
            [
                [-con1, -con1, -con1],
                [con1, -con1, -con1],
                [con1, con1, -con1],
                [-con1, con1, -con1],
                [-con1, -con1, con1],
                [con1, -con1, con1],
                [con1, con1, con1],
                [-con1, con1, con1],
                [-con2, 0, 0],
                [0, 0, -con2],
                [0, con2, 0],
                [0, 0, con2],
                [0, -con2, 0],
                [con2, 0, 0],
            ]
        )
        #
        for ixc in [0, 1, 2, 3, 4, 5, 6, 7]:
            self.wps[ixc] = 121 / 361
        #
        for ixc in [8, 9, 10, 11, 12, 13]:
            self.wps[ixc] = 320 / 361

    def process_shape_functions_and_derivatives(self):
        """This method processes the shape functions and their
        derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        rrx = self.pint[:, 2]
        #
        div8 = 1 / 8
        div4 = 1 / 4
        # shape functions
        phit = np.zeros((self.nint, self.nodes_per_element), dtype=float)
        #
        phit[:, 0] = div8 * (1 - ssx) * (1 - ttx) * (1 - rrx) * (-ssx - ttx - rrx - 2)
        phit[:, 1] = div8 * (1 + ssx) * (1 - ttx) * (1 - rrx) * (ssx - ttx - rrx - 2)
        phit[:, 2] = div8 * (1 + ssx) * (1 + ttx) * (1 - rrx) * (ssx + ttx - rrx - 2)
        phit[:, 3] = div8 * (1 - ssx) * (1 + ttx) * (1 - rrx) * (-ssx + ttx - rrx - 2)
        phit[:, 4] = div8 * (1 - ssx) * (1 - ttx) * (1 + rrx) * (-ssx - ttx + rrx - 2)
        phit[:, 5] = div8 * (1 + ssx) * (1 - ttx) * (1 + rrx) * (ssx - ttx + rrx - 2)
        phit[:, 6] = div8 * (1 + ssx) * (1 + ttx) * (1 + rrx) * (ssx + ttx + rrx - 2)
        phit[:, 7] = div8 * (1 - ssx) * (1 + ttx) * (1 + rrx) * (-ssx + ttx + rrx - 2)
        #
        phit[:, 8] = div4 * (1 - ssx**2) * (1 - ttx) * (1 - rrx)
        phit[:, 9] = div4 * (1 + ssx) * (1 - ttx**2) * (1 - rrx)
        phit[:, 10] = div4 * (1 - ssx**2) * (1 + ttx) * (1 - rrx)
        phit[:, 11] = div4 * (1 - ssx) * (1 - ttx**2) * (1 - rrx)
        phit[:, 12] = div4 * (1 - ssx**2) * (1 - ttx) * (1 + rrx)
        phit[:, 13] = div4 * (1 + ssx) * (1 - ttx**2) * (1 + rrx)
        phit[:, 14] = div4 * (1 - ssx**2) * (1 + ttx) * (1 + rrx)
        phit[:, 15] = div4 * (1 - ssx) * (1 - ttx**2) * (1 + rrx)
        phit[:, 16] = div4 * (1 - ssx) * (1 - ttx) * (1 - rrx**2)
        phit[:, 17] = div4 * (1 + ssx) * (1 - ttx) * (1 - rrx**2)
        phit[:, 18] = div4 * (1 + ssx) * (1 + ttx) * (1 - rrx**2)
        phit[:, 19] = div4 * (1 - ssx) * (1 + ttx) * (1 - rrx**2)
        #
        # derivatives
        dphit = np.zeros((self.nint, self.dof_per_node, self.nodes_per_element), dtype=float)
        #
        dphit[:, 0, 0] = div8 * (1 - ttx) * (1 - rrx) * (-(-ssx - ttx - rrx - 2) + (1 - ssx) * (-1))
        dphit[:, 0, 1] = div8 * (1 - ttx) * (1 - rrx) * (+(ssx - ttx - rrx - 2) + (1 + ssx) * (1))
        dphit[:, 0, 2] = div8 * (1 + ttx) * (1 - rrx) * (+(ssx + ttx - rrx - 2) + (1 + ssx) * (1))
        dphit[:, 0, 3] = div8 * (1 + ttx) * (1 - rrx) * (-(-ssx + ttx - rrx - 2) + (1 - ssx) * (-1))
        dphit[:, 0, 4] = div8 * (1 - ttx) * (1 + rrx) * (-(-ssx - ttx + rrx - 2) + (1 - ssx) * (-1))
        dphit[:, 0, 5] = div8 * (1 - ttx) * (1 + rrx) * (+(ssx - ttx + rrx - 2) + (1 + ssx) * (1))
        dphit[:, 0, 6] = div8 * (1 + ttx) * (1 + rrx) * (+(ssx + ttx + rrx - 2) + (1 + ssx) * (1))
        dphit[:, 0, 7] = div8 * (1 + ttx) * (1 + rrx) * (-(-ssx + ttx + rrx - 2) + (1 - ssx) * (-1))
        dphit[:, 0, 8] = div4 * (-2 * ssx) * (1 - ttx) * (1 - rrx)
        dphit[:, 0, 9] = div4 * (1) * (1 - ttx**2) * (1 - rrx)
        dphit[:, 0, 10] = div4 * (-2 * ssx) * (1 + ttx) * (1 - rrx)
        dphit[:, 0, 11] = div4 * (-1) * (1 - ttx**2) * (1 - rrx)
        dphit[:, 0, 12] = div4 * (-2 * ssx) * (1 - ttx) * (1 + rrx)
        dphit[:, 0, 13] = div4 * (1) * (1 - ttx**2) * (1 + rrx)
        dphit[:, 0, 14] = div4 * (-2 * ssx) * (1 + ttx) * (1 + rrx)
        dphit[:, 0, 15] = div4 * (-1) * (1 - ttx**2) * (1 + rrx)
        dphit[:, 0, 16] = div4 * (-1) * (1 - ttx) * (1 - rrx**2)
        dphit[:, 0, 17] = div4 * (1) * (1 - ttx) * (1 - rrx**2)
        dphit[:, 0, 18] = div4 * (1) * (1 + ttx) * (1 - rrx**2)
        dphit[:, 0, 19] = div4 * (-1) * (1 + ttx) * (1 - rrx**2)
        #
        dphit[:, 1, 0] = div8 * (1 - ssx) * (1 - rrx) * (-(-ssx - ttx - rrx - 2) + (1 - ttx) * (-1))
        dphit[:, 1, 1] = div8 * (1 + ssx) * (1 - rrx) * (-(ssx - ttx - rrx - 2) + (1 - ttx) * (-1))
        dphit[:, 1, 2] = div8 * (1 + ssx) * (1 - rrx) * (+(ssx + ttx - rrx - 2) + (1 + ttx) * (1))
        dphit[:, 1, 3] = div8 * (1 - ssx) * (1 - rrx) * (+(-ssx + ttx - rrx - 2) + (1 + ttx) * (1))
        dphit[:, 1, 4] = div8 * (1 - ssx) * (1 + rrx) * (-(-ssx - ttx + rrx - 2) + (1 - ttx) * (-1))
        dphit[:, 1, 5] = div8 * (1 + ssx) * (1 + rrx) * (-(ssx - ttx + rrx - 2) + (1 - ttx) * (-1))
        dphit[:, 1, 6] = div8 * (1 + ssx) * (1 + rrx) * (+(ssx + ttx + rrx - 2) + (1 + ttx) * (1))
        dphit[:, 1, 7] = div8 * (1 - ssx) * (1 + rrx) * (+(-ssx + ttx + rrx - 2) + (1 + ttx) * (1))
        dphit[:, 1, 8] = div4 * (1 - ssx**2) * (-1) * (1 - rrx)
        dphit[:, 1, 9] = div4 * (1 + ssx) * (-2 * ttx) * (1 - rrx)
        dphit[:, 1, 10] = div4 * (1 - ssx**2) * (1) * (1 - rrx)
        dphit[:, 1, 11] = div4 * (1 - ssx) * (-2 * ttx) * (1 - rrx)
        dphit[:, 1, 12] = div4 * (1 - ssx**2) * (-1) * (1 + rrx)
        dphit[:, 1, 13] = div4 * (1 + ssx) * (-2 * ttx) * (1 + rrx)
        dphit[:, 1, 14] = div4 * (1 - ssx**2) * (1) * (1 + rrx)
        dphit[:, 1, 15] = div4 * (1 - ssx) * (-2 * ttx) * (1 + rrx)
        dphit[:, 1, 16] = div4 * (1 - ssx) * (-1) * (1 - rrx**2)
        dphit[:, 1, 17] = div4 * (1 + ssx) * (-1) * (1 - rrx**2)
        dphit[:, 1, 18] = div4 * (1 + ssx) * (1) * (1 - rrx**2)
        dphit[:, 1, 19] = div4 * (1 - ssx) * (1) * (1 - rrx**2)
        #
        dphit[:, 2, 0] = div8 * (1 - ssx) * (1 - ttx) * (-(-ssx - ttx - rrx - 2) + (1 - rrx) * (-1))
        dphit[:, 2, 1] = div8 * (1 + ssx) * (1 - ttx) * (-(ssx - ttx - rrx - 2) + (1 - rrx) * (-1))
        dphit[:, 2, 2] = div8 * (1 + ssx) * (1 + ttx) * (-(ssx + ttx - rrx - 2) + (1 - rrx) * (-1))
        dphit[:, 2, 3] = div8 * (1 - ssx) * (1 + ttx) * (-(-ssx + ttx - rrx - 2) + (1 - rrx) * (-1))
        dphit[:, 2, 4] = div8 * (1 - ssx) * (1 - ttx) * (+(-ssx - ttx + rrx - 2) + (1 + rrx) * (1))
        dphit[:, 2, 5] = div8 * (1 + ssx) * (1 - ttx) * (+(ssx - ttx + rrx - 2) + (1 + rrx) * (1))
        dphit[:, 2, 6] = div8 * (1 + ssx) * (1 + ttx) * (+(ssx + ttx + rrx - 2) + (1 + rrx) * (1))
        dphit[:, 2, 7] = div8 * (1 - ssx) * (1 + ttx) * (+(-ssx + ttx + rrx - 2) + (1 + rrx) * (1))
        dphit[:, 2, 8] = div4 * (1 - ssx**2) * (1 - ttx) * (-1)
        dphit[:, 2, 9] = div4 * (1 + ssx) * (1 - ttx**2) * (-1)
        dphit[:, 2, 10] = div4 * (1 - ssx**2) * (1 + ttx) * (-1)
        dphit[:, 2, 11] = div4 * (1 - ssx) * (1 - ttx**2) * (-1)
        dphit[:, 2, 12] = div4 * (1 - ssx**2) * (1 - ttx) * (1)
        dphit[:, 2, 13] = div4 * (1 + ssx) * (1 - ttx**2) * (1)
        dphit[:, 2, 14] = div4 * (1 - ssx**2) * (1 + ttx) * (1)
        dphit[:, 2, 15] = div4 * (1 - ssx) * (1 - ttx**2) * (1)
        dphit[:, 2, 16] = div4 * (1 - ssx) * (1 - ttx) * (-2 * rrx)
        dphit[:, 2, 17] = div4 * (1 + ssx) * (1 - ttx) * (-2 * rrx)
        dphit[:, 2, 18] = div4 * (1 + ssx) * (1 + ttx) * (-2 * rrx)
        dphit[:, 2, 19] = div4 * (1 - ssx) * (1 + ttx) * (-2 * rrx)

        self.phi = phit
        self.dphi = dphit
        # return phit, dphit

    def elementary_matrices(self, el_index: int, material: Material):
        """This method returns elementary stiffness and mass matrices for HEXAHEDRON-20 nodes.
        ANSYS SOLID95 - Do not compare with new Ansys solid elements
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
            Ke += B[i, :, :].T @ const_mat @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])
            Me += rho * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i])

        return Ke, Me

    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivity = self.connectivity[
            :, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19]
        ]

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
                    dof * self.connectivity[:, 11] - 1,
                    dof * self.connectivity[:, 11],
                    dof * self.connectivity[:, 11] + 1,
                    dof * self.connectivity[:, 12] - 1,
                    dof * self.connectivity[:, 12],
                    dof * self.connectivity[:, 12] + 1,
                    dof * self.connectivity[:, 13] - 1,
                    dof * self.connectivity[:, 13],
                    dof * self.connectivity[:, 13] + 1,
                    dof * self.connectivity[:, 14] - 1,
                    dof * self.connectivity[:, 14],
                    dof * self.connectivity[:, 14] + 1,
                    dof * self.connectivity[:, 15] - 1,
                    dof * self.connectivity[:, 15],
                    dof * self.connectivity[:, 15] + 1,
                    dof * self.connectivity[:, 16] - 1,
                    dof * self.connectivity[:, 16],
                    dof * self.connectivity[:, 16] + 1,
                    dof * self.connectivity[:, 17] - 1,
                    dof * self.connectivity[:, 17],
                    dof * self.connectivity[:, 17] + 1,
                    dof * self.connectivity[:, 18] - 1,
                    dof * self.connectivity[:, 18],
                    dof * self.connectivity[:, 18] + 1,
                    dof * self.connectivity[:, 19] - 1,
                    dof * self.connectivity[:, 19],
                    dof * self.connectivity[:, 19] + 1,
                    dof * self.connectivity[:, 20] - 1,
                    dof * self.connectivity[:, 20],
                    dof * self.connectivity[:, 20] + 1,
                ],
                dtype=int,
            )
            + 1
        ).T

        vect_indices = ind_dof.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edof, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dof, edof)).flatten()

        return self.ind_rows, self.ind_cols
