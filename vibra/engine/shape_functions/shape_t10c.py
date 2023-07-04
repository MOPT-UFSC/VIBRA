import numpy as np


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
