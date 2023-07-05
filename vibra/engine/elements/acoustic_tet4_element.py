import numpy as np
from scipy.sparse import csr_matrix

# from scipy.sparse.linalg import eigs
# from time import time
from vibra.engine.elements.element import Element


def shape4TC(ssx, ttx, rrx):
    """This function returns the shape functions and its derivatives."""
    # shape functions
    phi = np.array([1 - ssx - ttx - rrx, ttx, rrx, ssx], dtype=float)
    # derivatives
    dphi = np.array([[-1, 0, 0, 1], [-1, 1, 0, 0], [-1, 0, 1, 0]], dtype=float)

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


class ACT_TETRAHEDRON_4C(Element):
    # Element Constants
    NODES_PER_ELEMENT = 4
    DOF_PER_NODE = 1
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model):
        self.model = model

        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()

    def initialize_variables(self):
        """ """
        self.element_label = "acoustic_tetrahedron_4"
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
        self.wps = 1 / 4

        self.pint = np.array(
            [[con1, con1, con1], [con1, con1, con2], [con1, con2, con1], [con2, con1, con1]]
        )

    def process_shape_functions_and_derivatives(self):
        """
        This method processes the shape functions and their
        derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        rrx = self.pint[:, 2]
        #
        self.phi, self.dphi = shape4TC(ssx, ttx, rrx)

    def elementary_matrices(self, el_index):
        """
        Stiffness and mass matrices.
        """

        fluid = self.model.properties.get_fluid(element=el_index)

        rho = fluid.density
        c_0 = fluid.speed_of_sound
        ie = self.connectivity[el_index, 1:] - 1
        #
        JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = get_detJAC_and_invJAC(JAC)
        dphi_t = invJAC @ self.dphi
        #
        B = np.zeros((3, self.DOFS_PER_ELEMENT), dtype=float)
        N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        #
        B[0, :] = dphi_t[0, :]
        B[1, :] = dphi_t[1, :]
        B[2, :] = dphi_t[2, :]
        #
        N[:, 0, :] = self.phi

        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            Ke += (1 / 6) * B.T @ B * (detJAC * self.wps)
            Me += (1 / 6) * (1 / c_0**2) * N[i, :, :].T @ N[i, :, :] * (detJAC * self.wps)

        return Ke, Me

    def reorder_connect(self):
        """ """
        self.connectivity = self.connectivity[:, [0, 6, 4, 5, 7]]

    def generate_ind_rows_cols(self):
        """ """
        # processing the dofs indices (rows and columns) for assembly
        self.reorder_connect()
        dofs, edofs = self.DOF_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs * self.connectivity[:, 1:]

        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

        return self.ind_rows, self.ind_cols
