import numpy as np

from vibra.engine.elements.solid_elements import Element3D
from vibra.engine.properties.material import Material


def get_detJAC_and_invJAC(JAC):
    """ """

    detJAC = (
        JAC[:, 0, 0] * JAC[:, 1, 1] * JAC[:, 2, 2]
        + JAC[:, 0, 1] * JAC[:, 1, 2] * JAC[:, 2, 0]
        + JAC[:, 0, 2] * JAC[:, 1, 0] * JAC[:, 2, 1]
    ) - (
        JAC[:, 2, 0] * JAC[:, 1, 1] * JAC[:, 0, 2]
        + JAC[:, 2, 1] * JAC[:, 1, 2] * JAC[:, 0, 0]
        + JAC[:, 2, 2] * JAC[:, 1, 0] * JAC[:, 0, 1]
    )
    detJAC = detJAC.reshape(-1, 1, 1)
    # adj(JAC)
    AUJJ = np.zeros((detJAC.shape[0], 3, 3), dtype=float)
    AUJJ[:, 0, 0] = 1 * ((JAC[:, 1, 1] * JAC[:, 2, 2]) - (JAC[:, 2, 1] * JAC[:, 1, 2]))
    AUJJ[:, 1, 0] = -1 * ((JAC[:, 1, 0] * JAC[:, 2, 2]) - (JAC[:, 1, 2] * JAC[:, 2, 0]))
    AUJJ[:, 2, 0] = 1 * ((JAC[:, 1, 0] * JAC[:, 2, 1]) - (JAC[:, 1, 1] * JAC[:, 2, 0]))
    AUJJ[:, 0, 1] = -1 * ((JAC[:, 0, 1] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 1]))
    AUJJ[:, 1, 1] = 1 * ((JAC[:, 0, 0] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 0]))
    AUJJ[:, 2, 1] = -1 * ((JAC[:, 0, 0] * JAC[:, 2, 1]) - (JAC[:, 0, 1] * JAC[:, 2, 0]))
    AUJJ[:, 0, 2] = 1 * ((JAC[:, 0, 1] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 1]))
    AUJJ[:, 1, 2] = -1 * ((JAC[:, 0, 0] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 0]))
    AUJJ[:, 2, 2] = 1 * ((JAC[:, 0, 0] * JAC[:, 1, 1]) - (JAC[:, 0, 1] * JAC[:, 1, 0]))

    return detJAC, (1 / detJAC) * AUJJ


class STRUCT_HEXAHEDRON_8(Element3D):
    #
    NODES_PER_ELEMENT = 8
    DOFS_PER_NODE = 3
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOFS_PER_NODE

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
        phi = np.zeros((self.nint, self.NODES_PER_ELEMENT), dtype=float)
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
        dphi = np.zeros((self.nint, self.DOFS_PER_NODE, self.NODES_PER_ELEMENT), dtype=float)
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

    def get_constitutive_model(self, material: Material, model_type="linear-isotropic"):
        """This methdo returns the material constitutive model."""

        self.material = material
        vv = self.material.poisson_ratio
        E = self.material.elasticity_modulus

        if model_type == "linear-isotropic":
            # Constititive model - Linear isotropic material
            #
            tempc = E / ((1 + vv) * (1 - 2 * vv))
            tempn = (1 - 2 * vv) / 2
            tempt = 1 - vv
            #
            const_law = np.array(
                [
                    [tempt, vv, vv, 0, 0, 0],
                    [vv, tempt, vv, 0, 0, 0],
                    [vv, vv, tempt, 0, 0, 0],
                    [0, 0, 0, tempn, 0, 0],
                    [0, 0, 0, 0, tempn, 0],
                    [0, 0, 0, 0, 0, tempn],
                ]
            )

            return tempc * const_law

    def elementary_matrices(self, el_index: int, material: Material):
        """This method returns elementary stiffness and mass matrices for HEXAHEDRON-8 nodes.
        ANSYS SOLID45 w/o extra diplacements (very simple)
        """

        const_mat = self.get_constitutive_model(material, model_type="linear-isotropic")
        rho = self.material.material_density

        ie = self.connectivity[el_index, 1:]
        JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = get_detJAC_and_invJAC(JAC)
        dphi_t = invJAC @ self.dphi

        B = np.zeros((self.nint, 6, self.DOFS_PER_ELEMENT), dtype=float)
        B[:, 0, 0::3] = dphi_t[:, 0, :]
        B[:, 1, 1::3] = dphi_t[:, 1, :]
        B[:, 2, 2::3] = dphi_t[:, 2, :]
        B[:, 3, 0::3] = dphi_t[:, 1, :]
        B[:, 3, 1::3] = dphi_t[:, 0, :]
        B[:, 4, 0::3] = dphi_t[:, 2, :]
        B[:, 4, 2::3] = dphi_t[:, 0, :]
        B[:, 5, 1::3] = dphi_t[:, 2, :]
        B[:, 5, 2::3] = dphi_t[:, 1, :]

        N = np.zeros((self.nint, 3, self.DOFS_PER_ELEMENT), dtype=float)
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
        """This method processess the dofs indices (rows and columns) for assembly"""

        self.reorder_connect()
        dofs, edofs = self.DOFS_PER_NODE, self.DOFS_PER_ELEMENT

        ind_dofs = (
            np.array(
                [
                    dofs * self.connectivity[:, 1] - 1,
                    dofs * self.connectivity[:, 1],
                    dofs * self.connectivity[:, 1] + 1,
                    dofs * self.connectivity[:, 2] - 1,
                    dofs * self.connectivity[:, 2],
                    dofs * self.connectivity[:, 2] + 1,
                    dofs * self.connectivity[:, 3] - 1,
                    dofs * self.connectivity[:, 3],
                    dofs * self.connectivity[:, 3] + 1,
                    dofs * self.connectivity[:, 4] - 1,
                    dofs * self.connectivity[:, 4],
                    dofs * self.connectivity[:, 4] + 1,
                    dofs * self.connectivity[:, 5] - 1,
                    dofs * self.connectivity[:, 5],
                    dofs * self.connectivity[:, 5] + 1,
                    dofs * self.connectivity[:, 6] - 1,
                    dofs * self.connectivity[:, 6],
                    dofs * self.connectivity[:, 6] + 1,
                    dofs * self.connectivity[:, 7] - 1,
                    dofs * self.connectivity[:, 7],
                    dofs * self.connectivity[:, 7] + 1,
                    dofs * self.connectivity[:, 8] - 1,
                    dofs * self.connectivity[:, 8],
                    dofs * self.connectivity[:, 8] + 1,
                ],
                dtype=int,
            )
            + 1
        ).T

        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

        return self.ind_rows, self.ind_cols
