import numpy as np

from vibra.engine.elements.solid_elements import Element3D

# fmt: off

def shape10TC(l1, l2, l3):
    """This function returns the shape functions and its derivatives."""
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


def get_detJAC_and_invJAC(JAC):
    """ """

    detJAC = (
        JAC[0, 0] * JAC[1, 1] * JAC[2, 2]
        + JAC[0, 1] * JAC[1, 2] * JAC[2, 0]
        + JAC[0, 2] * JAC[1, 0] * JAC[2, 1]
    ) - (
        JAC[2, 0] * JAC[1, 1] * JAC[0, 2]
        + JAC[2, 1] * JAC[1, 2] * JAC[0, 0]
        + JAC[2, 2] * JAC[1, 0] * JAC[0, 1]
    )

    # adj(JAC)
    AUJJ = np.zeros((3, 3), dtype=float)
    AUJJ[0, 0] = 1 * ((JAC[1, 1] * JAC[2, 2]) - (JAC[2, 1] * JAC[1, 2]))
    AUJJ[1, 0] = -1 * ((JAC[1, 0] * JAC[2, 2]) - (JAC[1, 2] * JAC[2, 0]))
    AUJJ[2, 0] = 1 * ((JAC[1, 0] * JAC[2, 1]) - (JAC[1, 1] * JAC[2, 0]))
    AUJJ[0, 1] = -1 * ((JAC[0, 1] * JAC[2, 2]) - (JAC[0, 2] * JAC[2, 1]))
    AUJJ[1, 1] = 1 * ((JAC[0, 0] * JAC[2, 2]) - (JAC[0, 2] * JAC[2, 0]))
    AUJJ[2, 1] = -1 * ((JAC[0, 0] * JAC[2, 1]) - (JAC[0, 1] * JAC[2, 0]))
    AUJJ[0, 2] = 1 * ((JAC[0, 1] * JAC[1, 2]) - (JAC[0, 2] * JAC[1, 1]))
    AUJJ[1, 2] = -1 * ((JAC[0, 0] * JAC[1, 2]) - (JAC[0, 2] * JAC[1, 0]))
    AUJJ[2, 2] = 1 * ((JAC[0, 0] * JAC[1, 1]) - (JAC[0, 1] * JAC[1, 0]))

    return detJAC, (1 / detJAC) * AUJJ


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


class ACT_TETRAHEDRON_10C(Element3D):
    NODES_PER_ELEMENT = 10
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
        self.element_label = "acoustic_tetrahedron_10"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connectivity = self.model.mesh.solids_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity)

    def define_integration_points(self):
        """ """
        self.nint = 15
        ax = 1 / 4
        bx = (7 + np.sqrt(15)) / 34
        cx = (7 - np.sqrt(15)) / 34
        dx = (13 - 3 * np.sqrt(15)) / 34
        ex = (13 + 3 * np.sqrt(15)) / 34

        p1 = 48 / 405
        p2 = 6 * (2665 - 14 * np.sqrt(15)) / 226800
        p3 = 6 * (2665 + 14 * np.sqrt(15)) / 226800
        p4 = 30 / 567

        fx = (5 - np.sqrt(15)) / 20
        gx = (5 + np.sqrt(15)) / 20
        self.pint = np.array(
            [
                [ax, ax, ax],
                [bx, bx, bx],
                [bx, bx, dx],
                [bx, dx, bx],
                [dx, bx, bx],
                [cx, cx, cx],
                [cx, cx, ex],
                [cx, ex, cx],
                [ex, cx, cx],
                [fx, fx, gx],
                [fx, gx, fx],
                [gx, fx, fx],
                [fx, gx, gx],
                [gx, fx, gx],
                [gx, gx, fx],
            ],
            dtype=float,
        )
        self.wps = np.array(
            [p1, p2, p2, p2, p2, p3, p3, p3, p3, p4, p4, p4, p4, p4, p4], dtype=float
        )

    def process_shape_functions_and_derivatives(self):
        """This method processes the shape functions and their
        derivatives for all integration points.
        """
        l1 = self.pint[:, 0]
        l2 = self.pint[:, 1]
        l3 = self.pint[:, 2]
        #
        # shape functions
        # phi = np.zeros(10)
        phi = np.zeros((self.nint, self.NODES_PER_ELEMENT), dtype=float)
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
        dphi = np.zeros((self.nint, 3, self.NODES_PER_ELEMENT), dtype=float)
        #
        #########################################################
        # dphi[:, 0, 0] = 0
        dphi[:, 0, 1] = 4 * l1 - 1
        # dphi[:, 0, 2] = 0
        dphi[:, 0, 3] = (-2) * l4 + (2 * l4 - 1) * (-1)
        dphi[:, 0, 4] = 4 * l2
        dphi[:, 0, 5] = 4 * l3
        # dphi[:, 0, 6] = 0
        dphi[:, 0, 7] = -4 * l2
        dphi[:, 0, 8] = 4 * ((+1) * l4 + l1 * (-1))
        dphi[:, 0, 9] = -4 * l3
        #
        dphi[:, 1, 0] = (+2) * l2 + (2 * l2 - 1) * (+1)
        # dphi[:, 1, 1] = 0
        # dphi[:, 1, 2] = 0
        dphi[:, 1, 3] = (-2) * l4 + (2 * l4 - 1) * (-1)
        dphi[:, 1, 4] = 4 * l1
        # dphi[:, 1, 5] = 0
        dphi[:, 1, 6] = 4 * l3
        dphi[:, 1, 8] = -4 * l1
        dphi[:, 1, 7] = 4 * ((+1) * l4 + l2 * (-1))
        dphi[:, 1, 9] = -4 * l3
        #
        # dphi[:, 2, 0] = 0
        # dphi[:, 2, 1] = 0
        dphi[:, 2, 2] = (+2) * l3 + (2 * l3 - 1) * (+1)
        dphi[:, 2, 3] = (-2) * l4 + (2 * l4 - 1) * (-1)
        # dphi[:, 2, 4] = 0
        dphi[:, 2, 5] = 4 * l1
        dphi[:, 2, 6] = 4 * l2
        dphi[:, 2, 7] = -4 * l2
        dphi[:, 2, 8] = -4 * l1
        dphi[:, 2, 9] = 4 * ((+1) * l4 + l3 * (-1))
        #
        self.phi = phi
        self.dphi = dphi

    def elementary_matrices(self, el_index):
        """T10S stiffness and mass matrices.
        Solid187 not mixed (pure displacement)
        """
        #
        # fluid = self.model.properties.get_fluid(element=el_index)
        # rho = fluid.fluid_density
        # c_0 = fluid.speed_of_sound
        # c_0 = self.model.properties.get_speed_of_sound(element=el_index)

        ie = self.connectivity[el_index, 1:]
        #
        JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = get_detJAC_and_invJAC(JAC)
        dphi_t = invJAC @ self.dphi
        #
        B = np.zeros((self.nint, 3, self.DOFS_PER_ELEMENT), dtype=float)
        N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        #
        B[:, 0, :] = dphi_t[:, 0, :]
        B[:, 1, :] = dphi_t[:, 1, :]
        B[:, 2, :] = dphi_t[:, 2, :]
        #
        N[:, 0, :] = self.phi
        #
        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):

            Ke += (1 / 6) * B[i, :, :].T @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])
            Me += ((1 / 6) * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i]))
            # Me += ((1 / 6) * (1 / c_0**2) * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i]))

        return Ke, Me

    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivity = self.connectivity[:, [0, 6, 4, 5, 7, 10, 8, 9, 12, 11, 13]]

    def generate_ind_rows_cols(self, reorder=True):
        """This method processess the dofs indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.connectivity[:, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]]

        dofs, edofs = self.DOFS_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs * self.connectivity[:, 1:]

        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

        return self.ind_rows, self.ind_cols
    
# fmt: on