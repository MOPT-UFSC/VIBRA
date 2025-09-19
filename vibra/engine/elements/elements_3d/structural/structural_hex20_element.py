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


class STRUCT_HEXAHEDRON_20(Element3D):
    #
    NODES_PER_ELEMENT = 20
    DOF_PER_NODE = 3
    DOF_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

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
        phit = np.zeros((self.nint, self.NODES_PER_ELEMENT), dtype=float)
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
        dphit = np.zeros((self.nint, self.DOF_PER_NODE, self.NODES_PER_ELEMENT), dtype=float)
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
        """This method returns elementary stiffness and mass matrices for HEXAHEDRON-20 nodes.
        ANSYS SOLID95 - Do not compare with new Ansys solid elements
        """

        const_mat = self.get_constitutive_model(material, model_type="linear-isotropic")
        rho = self.material.material_density

        ie = self.connectivity[el_index, 1:]
        JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = get_detJAC_and_invJAC(JAC)
        dphi_t = invJAC @ self.dphi

        B = np.zeros((self.nint, 6, self.DOF_PER_ELEMENT), dtype=float)
        B[:, 0, 0::3] = dphi_t[:, 0, :]
        B[:, 1, 1::3] = dphi_t[:, 1, :]
        B[:, 2, 2::3] = dphi_t[:, 2, :]
        B[:, 3, 0::3] = dphi_t[:, 1, :]
        B[:, 3, 1::3] = dphi_t[:, 0, :]
        B[:, 4, 0::3] = dphi_t[:, 2, :]
        B[:, 4, 2::3] = dphi_t[:, 0, :]
        B[:, 5, 1::3] = dphi_t[:, 2, :]
        B[:, 5, 2::3] = dphi_t[:, 1, :]

        N = np.zeros((self.nint, 3, self.DOF_PER_ELEMENT), dtype=float)
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
        """This method processess the dofs indices (rows and columns) for assembly"""

        self.reorder_connect()
        dofs, edofs = self.DOF_PER_NODE, self.DOF_PER_ELEMENT
        ind_dof = (
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
                    dofs * self.connectivity[:, 9] - 1,
                    dofs * self.connectivity[:, 9],
                    dofs * self.connectivity[:, 9] + 1,
                    dofs * self.connectivity[:, 10] - 1,
                    dofs * self.connectivity[:, 10],
                    dofs * self.connectivity[:, 10] + 1,
                    dofs * self.connectivity[:, 11] - 1,
                    dofs * self.connectivity[:, 11],
                    dofs * self.connectivity[:, 11] + 1,
                    dofs * self.connectivity[:, 12] - 1,
                    dofs * self.connectivity[:, 12],
                    dofs * self.connectivity[:, 12] + 1,
                    dofs * self.connectivity[:, 13] - 1,
                    dofs * self.connectivity[:, 13],
                    dofs * self.connectivity[:, 13] + 1,
                    dofs * self.connectivity[:, 14] - 1,
                    dofs * self.connectivity[:, 14],
                    dofs * self.connectivity[:, 14] + 1,
                    dofs * self.connectivity[:, 15] - 1,
                    dofs * self.connectivity[:, 15],
                    dofs * self.connectivity[:, 15] + 1,
                    dofs * self.connectivity[:, 16] - 1,
                    dofs * self.connectivity[:, 16],
                    dofs * self.connectivity[:, 16] + 1,
                    dofs * self.connectivity[:, 17] - 1,
                    dofs * self.connectivity[:, 17],
                    dofs * self.connectivity[:, 17] + 1,
                    dofs * self.connectivity[:, 18] - 1,
                    dofs * self.connectivity[:, 18],
                    dofs * self.connectivity[:, 18] + 1,
                    dofs * self.connectivity[:, 19] - 1,
                    dofs * self.connectivity[:, 19],
                    dofs * self.connectivity[:, 19] + 1,
                    dofs * self.connectivity[:, 20] - 1,
                    dofs * self.connectivity[:, 20],
                    dofs * self.connectivity[:, 20] + 1,
                ],
                dtype=int,
            )
            + 1
        ).T

        vect_indices = ind_dof.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dof, edofs)).flatten()

        return self.ind_rows, self.ind_cols
