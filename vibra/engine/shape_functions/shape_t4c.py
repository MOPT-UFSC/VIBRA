import numpy as np


def shapeT4C(ssx, ttx, rrx):
    """This function returns the shape functions and its derivatives."""
    # shape functions
    phi = np.array([1 - ssx - ttx - rrx, ttx, rrx, ssx], dtype=float)
    # derivatives
    dphi = np.array([[-1, 0, 0, 1], [-1, 1, 0, 0], [-1, 0, 1, 0]], dtype=float)

    return phi, dphi
