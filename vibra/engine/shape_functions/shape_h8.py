import numpy as np


def shapeH8(ssx, ttx, rrx):
    """Shape Functions and Derivatives."""
    denominator = 8
    # shape functions
    phi = np.zeros(8)
    #
    phi[0] = (1.0 - ssx) * (1.0 - ttx) * (1.0 - rrx)
    phi[1] = (1.0 + ssx) * (1.0 - ttx) * (1.0 - rrx)
    phi[2] = (1.0 + ssx) * (1.0 + ttx) * (1.0 - rrx)
    phi[3] = (1.0 - ssx) * (1.0 + ttx) * (1.0 - rrx)
    phi[4] = (1.0 - ssx) * (1.0 - ttx) * (1.0 + rrx)
    phi[5] = (1.0 + ssx) * (1.0 - ttx) * (1.0 + rrx)
    phi[6] = (1.0 + ssx) * (1.0 + ttx) * (1.0 + rrx)
    phi[7] = (1.0 - ssx) * (1.0 + ttx) * (1.0 + rrx)
    phi = phi / denominator

    # derivatives
    dphi = np.zeros((3, 8))
    #
    dphi[0, 0] = (-1.0) * (1.0 - ttx) * (1.0 - rrx)
    dphi[0, 1] = (1.0) * (1.0 - ttx) * (1.0 - rrx)
    dphi[0, 2] = (1.0) * (1.0 + ttx) * (1.0 - rrx)
    dphi[0, 3] = (-1.0) * (1.0 + ttx) * (1.0 - rrx)
    dphi[0, 4] = (-1.0) * (1.0 - ttx) * (1.0 + rrx)
    dphi[0, 5] = (1.0) * (1.0 - ttx) * (1.0 + rrx)
    dphi[0, 6] = (1.0) * (1.0 + ttx) * (1.0 + rrx)
    dphi[0, 7] = (-1.0) * (1.0 + ttx) * (1.0 + rrx)

    dphi[1, 0] = (1.0 - ssx) * (-1.0) * (1.0 - rrx)
    dphi[1, 1] = (1.0 + ssx) * (-1.0) * (1.0 - rrx)
    dphi[1, 2] = (1.0 + ssx) * (1.0) * (1.0 - rrx)
    dphi[1, 3] = (1.0 - ssx) * (1.0) * (1.0 - rrx)
    dphi[1, 4] = (1.0 - ssx) * (-1.0) * (1.0 + rrx)
    dphi[1, 5] = (1.0 + ssx) * (-1.0) * (1.0 + rrx)
    dphi[1, 6] = (1.0 + ssx) * (1.0) * (1.0 + rrx)
    dphi[1, 7] = (1.0 - ssx) * (1.0) * (1.0 + rrx)

    dphi[2, 0] = (1.0 - ssx) * (1.0 - ttx) * (-1.0)
    dphi[2, 1] = (1.0 + ssx) * (1.0 - ttx) * (-1.0)
    dphi[2, 2] = (1.0 + ssx) * (1.0 + ttx) * (-1.0)
    dphi[2, 3] = (1.0 - ssx) * (1.0 + ttx) * (-1.0)
    dphi[2, 4] = (1.0 - ssx) * (1.0 - ttx) * (1.0)
    dphi[2, 5] = (1.0 + ssx) * (1.0 - ttx) * (1.0)
    dphi[2, 6] = (1.0 + ssx) * (1.0 + ttx) * (1.0)
    dphi[2, 7] = (1.0 - ssx) * (1.0 + ttx) * (1.0)

    dphi = dphi / denominator

    return phi, dphi
