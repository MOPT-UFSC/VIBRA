import numpy as np

from vibra.engine.elements.solid_elements import (Element3D)


def shapeH20(ssx, ttx, rrx):
    """Shape Functions and Derivatives."""
    div8 = 1 / 8
    div4 = 1 / 4
    # shape functions
    phit = np.zeros(20, dtype=float)
    # #
    phit[0] = div8 * (1 - ssx) * (1 - ttx) * (1 - rrx) * (-ssx - ttx - rrx - 2)
    phit[1] = div8 * (1 + ssx) * (1 - ttx) * (1 - rrx) * (ssx - ttx - rrx - 2)
    phit[2] = div8 * (1 + ssx) * (1 + ttx) * (1 - rrx) * (ssx + ttx - rrx - 2)
    phit[3] = div8 * (1 - ssx) * (1 + ttx) * (1 - rrx) * (-ssx + ttx - rrx - 2)
    phit[4] = div8 * (1 - ssx) * (1 - ttx) * (1 + rrx) * (-ssx - ttx + rrx - 2)
    phit[5] = div8 * (1 + ssx) * (1 - ttx) * (1 + rrx) * (ssx - ttx + rrx - 2)
    phit[6] = div8 * (1 + ssx) * (1 + ttx) * (1 + rrx) * (ssx + ttx + rrx - 2)
    phit[7] = div8 * (1 - ssx) * (1 + ttx) * (1 + rrx) * (-ssx + ttx + rrx - 2)
    #
    phit[8] = div4 * (1 - ssx**2) * (1 - ttx) * (1 - rrx)
    phit[9] = div4 * (1 + ssx) * (1 - ttx**2) * (1 - rrx)
    phit[10] = div4 * (1 - ssx**2) * (1 + ttx) * (1 - rrx)
    phit[11] = div4 * (1 - ssx) * (1 - ttx**2) * (1 - rrx)
    phit[12] = div4 * (1 - ssx**2) * (1 - ttx) * (1 + rrx)
    phit[13] = div4 * (1 + ssx) * (1 - ttx**2) * (1 + rrx)
    phit[14] = div4 * (1 - ssx**2) * (1 + ttx) * (1 + rrx)
    phit[15] = div4 * (1 - ssx) * (1 - ttx**2) * (1 + rrx)
    phit[16] = div4 * (1 - ssx) * (1 - ttx) * (1 - rrx**2)
    phit[17] = div4 * (1 + ssx) * (1 - ttx) * (1 - rrx**2)
    phit[18] = div4 * (1 + ssx) * (1 + ttx) * (1 - rrx**2)
    phit[19] = div4 * (1 - ssx) * (1 + ttx) * (1 - rrx**2)

    # #derivatives
    dphit = np.zeros((3, 20), dtype=float)
    # #
    dphit[0, 0] = div8 * (1 - ttx) * (1 - rrx) * (-(-ssx - ttx - rrx - 2) + (1 - ssx) * (-1))
    dphit[0, 1] = div8 * (1 - ttx) * (1 - rrx) * (+(ssx - ttx - rrx - 2) + (1 + ssx) * (1))
    dphit[0, 2] = div8 * (1 + ttx) * (1 - rrx) * (+(ssx + ttx - rrx - 2) + (1 + ssx) * (1))
    dphit[0, 3] = div8 * (1 + ttx) * (1 - rrx) * (-(-ssx + ttx - rrx - 2) + (1 - ssx) * (-1))
    dphit[0, 4] = div8 * (1 - ttx) * (1 + rrx) * (-(-ssx - ttx + rrx - 2) + (1 - ssx) * (-1))
    dphit[0, 5] = div8 * (1 - ttx) * (1 + rrx) * (+(ssx - ttx + rrx - 2) + (1 + ssx) * (1))
    dphit[0, 6] = div8 * (1 + ttx) * (1 + rrx) * (+(ssx + ttx + rrx - 2) + (1 + ssx) * (1))
    dphit[0, 7] = div8 * (1 + ttx) * (1 + rrx) * (-(-ssx + ttx + rrx - 2) + (1 - ssx) * (-1))
    dphit[0, 8] = div4 * (-2 * ssx) * (1 - ttx) * (1 - rrx)
    dphit[0, 9] = div4 * (1) * (1 - ttx**2) * (1 - rrx)
    dphit[0, 10] = div4 * (-2 * ssx) * (1 + ttx) * (1 - rrx)
    dphit[0, 11] = div4 * (-1) * (1 - ttx**2) * (1 - rrx)
    dphit[0, 12] = div4 * (-2 * ssx) * (1 - ttx) * (1 + rrx)
    dphit[0, 13] = div4 * (1) * (1 - ttx**2) * (1 + rrx)
    dphit[0, 14] = div4 * (-2 * ssx) * (1 + ttx) * (1 + rrx)
    dphit[0, 15] = div4 * (-1) * (1 - ttx**2) * (1 + rrx)
    dphit[0, 16] = div4 * (-1) * (1 - ttx) * (1 - rrx**2)
    dphit[0, 17] = div4 * (1) * (1 - ttx) * (1 - rrx**2)
    dphit[0, 18] = div4 * (1) * (1 + ttx) * (1 - rrx**2)
    dphit[0, 19] = div4 * (-1) * (1 + ttx) * (1 - rrx**2)
    # #
    dphit[1, 0] = div8 * (1 - ssx) * (1 - rrx) * (-(-ssx - ttx - rrx - 2) + (1 - ttx) * (-1))
    dphit[1, 1] = div8 * (1 + ssx) * (1 - rrx) * (-(ssx - ttx - rrx - 2) + (1 - ttx) * (-1))
    dphit[1, 2] = div8 * (1 + ssx) * (1 - rrx) * (+(ssx + ttx - rrx - 2) + (1 + ttx) * (1))
    dphit[1, 3] = div8 * (1 - ssx) * (1 - rrx) * (+(-ssx + ttx - rrx - 2) + (1 + ttx) * (1))
    dphit[1, 4] = div8 * (1 - ssx) * (1 + rrx) * (-(-ssx - ttx + rrx - 2) + (1 - ttx) * (-1))
    dphit[1, 5] = div8 * (1 + ssx) * (1 + rrx) * (-(ssx - ttx + rrx - 2) + (1 - ttx) * (-1))
    dphit[1, 6] = div8 * (1 + ssx) * (1 + rrx) * (+(ssx + ttx + rrx - 2) + (1 + ttx) * (1))
    dphit[1, 7] = div8 * (1 - ssx) * (1 + rrx) * (+(-ssx + ttx + rrx - 2) + (1 + ttx) * (1))
    dphit[1, 8] = div4 * (1 - ssx**2) * (-1) * (1 - rrx)
    dphit[1, 9] = div4 * (1 + ssx) * (-2 * ttx) * (1 - rrx)
    dphit[1, 10] = div4 * (1 - ssx**2) * (1) * (1 - rrx)
    dphit[1, 11] = div4 * (1 - ssx) * (-2 * ttx) * (1 - rrx)
    dphit[1, 12] = div4 * (1 - ssx**2) * (-1) * (1 + rrx)
    dphit[1, 13] = div4 * (1 + ssx) * (-2 * ttx) * (1 + rrx)
    dphit[1, 14] = div4 * (1 - ssx**2) * (1) * (1 + rrx)
    dphit[1, 15] = div4 * (1 - ssx) * (-2 * ttx) * (1 + rrx)
    dphit[1, 16] = div4 * (1 - ssx) * (-1) * (1 - rrx**2)
    dphit[1, 17] = div4 * (1 + ssx) * (-1) * (1 - rrx**2)
    dphit[1, 18] = div4 * (1 + ssx) * (1) * (1 - rrx**2)
    dphit[1, 19] = div4 * (1 - ssx) * (1) * (1 - rrx**2)
    # #
    dphit[2, 0] = div8 * (1 - ssx) * (1 - ttx) * (-(-ssx - ttx - rrx - 2) + (1 - rrx) * (-1))
    dphit[2, 1] = div8 * (1 + ssx) * (1 - ttx) * (-(ssx - ttx - rrx - 2) + (1 - rrx) * (-1))
    dphit[2, 2] = div8 * (1 + ssx) * (1 + ttx) * (-(ssx + ttx - rrx - 2) + (1 - rrx) * (-1))
    dphit[2, 3] = div8 * (1 - ssx) * (1 + ttx) * (-(-ssx + ttx - rrx - 2) + (1 - rrx) * (-1))
    dphit[2, 4] = div8 * (1 - ssx) * (1 - ttx) * (+(-ssx - ttx + rrx - 2) + (1 + rrx) * (1))
    dphit[2, 5] = div8 * (1 + ssx) * (1 - ttx) * (+(ssx - ttx + rrx - 2) + (1 + rrx) * (1))
    dphit[2, 6] = div8 * (1 + ssx) * (1 + ttx) * (+(ssx + ttx + rrx - 2) + (1 + rrx) * (1))
    dphit[2, 7] = div8 * (1 - ssx) * (1 + ttx) * (+(-ssx + ttx + rrx - 2) + (1 + rrx) * (1))
    dphit[2, 8] = div4 * (1 - ssx**2) * (1 - ttx) * (-1)
    dphit[2, 9] = div4 * (1 + ssx) * (1 - ttx**2) * (-1)
    dphit[2, 10] = div4 * (1 - ssx**2) * (1 + ttx) * (-1)
    dphit[2, 11] = div4 * (1 - ssx) * (1 - ttx**2) * (-1)
    dphit[2, 12] = div4 * (1 - ssx**2) * (1 - ttx) * (1)
    dphit[2, 13] = div4 * (1 + ssx) * (1 - ttx**2) * (1)
    dphit[2, 14] = div4 * (1 - ssx**2) * (1 + ttx) * (1)
    dphit[2, 15] = div4 * (1 - ssx) * (1 - ttx**2) * (1)
    dphit[2, 16] = div4 * (1 - ssx) * (1 - ttx) * (-2 * rrx)
    dphit[2, 17] = div4 * (1 + ssx) * (1 - ttx) * (-2 * rrx)
    dphit[2, 18] = div4 * (1 + ssx) * (1 + ttx) * (-2 * rrx)
    dphit[2, 19] = div4 * (1 - ssx) * (1 + ttx) * (-2 * rrx)

    return phit, dphit


def get_detJAC_and_invJAC_3D(JAC):
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


class ACT_HEXAHEDRON_20C(Element3D):
    #
    NODES_PER_ELEMENT = 20
    DOF_PER_NODE = 1
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model):
        self.model = model
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()

    def initialize_variables(self):
        """ """
        self.element_label = "acoustic_hexahedron_20"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connectivity = self.model.mesh.solids_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity)

    def define_integration_points(self):
        """ """
        self.nint = 27
        self.pint = np.array(
            [
                [-1, -1, -1],
                [-1, -1, 0],
                [-1, -1, 1],
                [-1, 0, -1],
                [-1, 0, 0],
                [-1, 0, 1],
                [-1, 1, -1],
                [-1, 1, 0],
                [-1, 1, 1],
                [0, -1, -1],
                [0, -1, 0],
                [0, -1, 1],
                [0, 0, -1],
                [0, 0, 0],
                [0, 0, 1],
                [0, 1, -1],
                [0, 1, 0],
                [0, 1, 1],
                [1, -1, -1],
                [1, -1, 0],
                [1, -1, 1],
                [1, 0, -1],
                [1, 0, 0],
                [1, 0, 1],
                [1, 1, -1],
                [1, 1, 0],
                [1, 1, 1],
            ],
            dtype=float,
        ) * np.sqrt(3 / 5)

        self.wps = np.array(
            [
                125,
                200,
                125,
                200,
                320,
                200,
                125,
                200,
                125,
                200,
                320,
                200,
                320,
                512,
                320,
                200,
                320,
                200,
                125,
                200,
                125,
                200,
                320,
                200,
                125,
                200,
                125,
            ],
            dtype=float,
        ) / (9**3)

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
        # #
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

        # #derivatives
        dphit = np.zeros((self.nint, 3, self.NODES_PER_ELEMENT), dtype=float)
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
        # #
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
        # #
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

    def elementary_matrices(self, el_index):
        """H20 stiffness and mass matrices."""

        # fluid = self.model.properties.get_fluid(element=el_index)
        # rho = fluid.fluid_density
        # c_0 = fluid.speed_of_sound

        c_0 = self.model.properties.get_speed_of_sound(element=el_index)
        ie = self.connectivity[el_index, 1:]

        #
        JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = get_detJAC_and_invJAC_3D(JAC)
        dphi_t = invJAC @ self.dphi
        #
        B = np.zeros((self.nint, 3, self.DOFS_PER_ELEMENT_3D), dtype=float)
        N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT_3D), dtype=float)
        #
        B[:, 0, :] = dphi_t[:, 0, :]
        B[:, 1, :] = dphi_t[:, 1, :]
        B[:, 2, :] = dphi_t[:, 2, :]
        #
        N[:, 0, :] = self.phi
        #
        # integration loop
        Ke, Me = 0, 0
        # Ke = np.zeros((self.DOFS_PER_ELEMENT_3D, self.DOFS_PER_ELEMENT_3D), dtype=float)
        # Me = np.zeros((self.DOFS_PER_ELEMENT_3D, self.DOFS_PER_ELEMENT_3D), dtype=float)
        for i in range(self.nint):
            Ke += B[i, :, :].T @ B[i, :, :] * (detJAC[i, :, :] * self.wps[i])
            Me += (1 / c_0**2) * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps[i])

        return Ke, Me

    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivity = self.connectivity[
            :, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19]
        ]

    def generate_ind_rows_cols(self):
        """This method processess the dofs indices (rows and columns) for assembly"""

        self.reorder_connect()
        dofs, edofs = self.DOF_PER_NODE, self.DOFS_PER_ELEMENT_3D
        ind_dofs = dofs * self.connectivity[:, 1:]

        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

        return self.ind_rows, self.ind_cols
