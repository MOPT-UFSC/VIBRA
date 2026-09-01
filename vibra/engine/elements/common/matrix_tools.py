
import numpy as np


def get_3x3_matrix_determinant(A: np.ndarray):
    """
    This function computes the determinant of a 3x3 matrix.

    Parameters
    ----------
    A: np.array
        The 3x3 matrix.

    Returns
    -------
    det_A: np.ndarray
        The determinant of A matrix.

    """
    if len(A.shape) == 3:
        det_A = (
            A[:, 0, 0] * A[:, 1, 1] * A[:, 2, 2]
            + A[:, 0, 1] * A[:, 1, 2] * A[:, 2, 0]
            + A[:, 0, 2] * A[:, 1, 0] * A[:, 2, 1]
        ) - (
            A[:, 2, 0] * A[:, 1, 1] * A[:, 0, 2]
            + A[:, 2, 1] * A[:, 1, 2] * A[:, 0, 0]
            + A[:, 2, 2] * A[:, 1, 0] * A[:, 0, 1]
        )

        det_A = det_A.reshape(-1, 1, 1)

    else:
        det_A = (
            A[0, 0] * A[1, 1] * A[2, 2]
            + A[0, 1] * A[1, 2] * A[2, 0]
            + A[0, 2] * A[1, 0] * A[2, 1]
        ) - (
            A[2, 0] * A[1, 1] * A[0, 2]
            + A[2, 1] * A[1, 2] * A[0, 0]
            + A[2, 2] * A[1, 0] * A[0, 1]
        )

    return det_A


def get_2x2_matrix_determinant(A: np.ndarray):
    """
    This function computes the determinant of a 2x2 matrix.

    Parameters
    ----------
    A: np.array
        The 2x2 matrix.

    Returns
    -------
    det_A: np.ndarray
        The determinant of A matrix.

    """
    if len(A.shape) == 3:
        det_A = A[:, 0, 0] * A[:, 1, 1]  - A[:, 0, 1] * A[:, 1, 0]
        det_A = det_A.reshape(-1, 1, 1)

    else:
        det_A = A[0, 0] * A[1, 1]  - A[0, 1] * A[1, 0]

    return det_A


def get_2x2_matrix_inverse(A: np.ndarray, return_det: bool = False) -> np.ndarray:
    """
    This function computes the determinants and inverses
    of Jacobian matrices in stacked form.

    Parameters
    ----------
    A: np.array
        The matrix 2x2 to be inverted.

    return_det: bool, optional
        Control when the determinant will be returned.

    Returns
    -------
    inv_mat: np.ndarray
        The inverse of 2x2 matrices.

    """

    # determinant of the 2x2 matrix
    det_A = get_2x2_matrix_determinant(A)

    # compute the adjoint matrix
    if len(A.shape) == 3:
        adj_matrix = np.zeros((det_A.shape[0], 2, 2), dtype=float)
        adj_matrix[:, 0, 0] =  A[:, 1, 1]
        adj_matrix[:, 0, 1] = -A[:, 0, 1]
        adj_matrix[:, 1, 0] = -A[:, 1, 0]
        adj_matrix[:, 1, 1] =  A[:, 0, 0]

    else:
        adj_matrix = np.zeros((2, 2), dtype=float)
        adj_matrix[0, 0] =  A[:, 1, 1]
        adj_matrix[0, 1] = -A[:, 0, 1]
        adj_matrix[1, 0] = -A[:, 1, 0]
        adj_matrix[1, 1] =  A[:, 0, 0]

    # inverse of the Jacobian matrix
    inv_A = (1 / det_A) * adj_matrix

    if return_det:
        return inv_A, det_A

    return inv_A


def get_3x3_matrix_inverse(A: np.ndarray, return_det: bool = False) -> np.ndarray:
    """
    This function computes the determinants and inverses
    of Jacobian matrices in stacked form.

    Parameters
    ----------
    A: np.array
        The matrix 3x3 to be inverted.

    return_det: bool, optional
        Control when the determinant will be returned.

    Returns
    -------
    inv_mat: np.ndarray
        The inverse of 3x3 matrices.

    """

    # determinant of the 3x3 matrix
    det_A = get_3x3_matrix_determinant(A)

    # compute the adjoint matrix
    if len(det_A.shape) == 3:
        adj_matrix = np.zeros((det_A.shape[0], 3, 3), dtype=float)
        adj_matrix[:, 0, 0] =  ((A[:, 1, 1] * A[:, 2, 2]) - (A[:, 2, 1] * A[:, 1, 2]))
        adj_matrix[:, 1, 0] = -((A[:, 1, 0] * A[:, 2, 2]) - (A[:, 1, 2] * A[:, 2, 0]))
        adj_matrix[:, 2, 0] =  ((A[:, 1, 0] * A[:, 2, 1]) - (A[:, 1, 1] * A[:, 2, 0]))
        adj_matrix[:, 0, 1] = -((A[:, 0, 1] * A[:, 2, 2]) - (A[:, 0, 2] * A[:, 2, 1]))
        adj_matrix[:, 1, 1] =  ((A[:, 0, 0] * A[:, 2, 2]) - (A[:, 0, 2] * A[:, 2, 0]))
        adj_matrix[:, 2, 1] = -((A[:, 0, 0] * A[:, 2, 1]) - (A[:, 0, 1] * A[:, 2, 0]))
        adj_matrix[:, 0, 2] =  ((A[:, 0, 1] * A[:, 1, 2]) - (A[:, 0, 2] * A[:, 1, 1]))
        adj_matrix[:, 1, 2] = -((A[:, 0, 0] * A[:, 1, 2]) - (A[:, 0, 2] * A[:, 1, 0]))
        adj_matrix[:, 2, 2] =  ((A[:, 0, 0] * A[:, 1, 1]) - (A[:, 0, 1] * A[:, 1, 0]))

    else:
        adj_matrix = np.zeros((3, 3), dtype=float)
        adj_matrix[0, 0] =  ((A[1, 1] * A[2, 2]) - (A[2, 1] * A[1, 2]))
        adj_matrix[1, 0] = -((A[1, 0] * A[2, 2]) - (A[1, 2] * A[2, 0]))
        adj_matrix[2, 0] =  ((A[1, 0] * A[2, 1]) - (A[1, 1] * A[2, 0]))
        adj_matrix[0, 1] = -((A[0, 1] * A[2, 2]) - (A[0, 2] * A[2, 1]))
        adj_matrix[1, 1] =  ((A[0, 0] * A[2, 2]) - (A[0, 2] * A[2, 0]))
        adj_matrix[2, 1] = -((A[0, 0] * A[2, 1]) - (A[0, 1] * A[2, 0]))
        adj_matrix[0, 2] =  ((A[0, 1] * A[1, 2]) - (A[0, 2] * A[1, 1]))
        adj_matrix[1, 2] = -((A[0, 0] * A[1, 2]) - (A[0, 2] * A[1, 0]))
        adj_matrix[2, 2] =  ((A[0, 0] * A[1, 1]) - (A[0, 1] * A[1, 0]))

    # inverse of the Jacobian matrix
    inv_A = (1 / det_A) * adj_matrix

    if return_det:
        return inv_A, det_A

    return inv_A


    # def get_detJAC(self, JAC: np.ndarray):
    #     """
    #     This function computes the determinant of Jacobian matrix.

    #     Parameters
    #     ----------
    #     JAC: np.array
    #         The Jacobian matrices.

    #     Returns
    #     -------
    #     det_jac: np.ndarray
    #         The determinant of Jacobian matrix.

    #     """
    #     if len(JAC.shape) == 3:

    #         det_jac = (
    #             JAC[:, 0, 0] * JAC[:, 1, 1] * JAC[:, 2, 2]
    #             + JAC[:, 0, 1] * JAC[:, 1, 2] * JAC[:, 2, 0]
    #             + JAC[:, 0, 2] * JAC[:, 1, 0] * JAC[:, 2, 1]
    #         ) - (
    #             JAC[:, 2, 0] * JAC[:, 1, 1] * JAC[:, 0, 2]
    #             + JAC[:, 2, 1] * JAC[:, 1, 2] * JAC[:, 0, 0]
    #             + JAC[:, 2, 2] * JAC[:, 1, 0] * JAC[:, 0, 1]
    #         )

    #         det_jac = det_jac.reshape(-1, 1, 1)

    #     else:

    #         det_jac = (
    #             JAC[0, 0] * JAC[1, 1] * JAC[2, 2]
    #             + JAC[0, 1] * JAC[1, 2] * JAC[2, 0]
    #             + JAC[0, 2] * JAC[1, 0] * JAC[2, 1]
    #         ) - (
    #             JAC[2, 0] * JAC[1, 1] * JAC[0, 2]
    #             + JAC[2, 1] * JAC[1, 2] * JAC[0, 0]
    #             + JAC[2, 2] * JAC[1, 0] * JAC[0, 1]
    #         )

    #     return det_jac


    # def get_detJAC_and_invJAC(self, JAC: np.ndarray):
    #     """
    #     This function computes the determinant and inverse
    #     of Jacobian matrix.

    #     Parameters
    #     ----------
    #     JAC: np.array
    #         The Jacobian matrices.

    #     Returns
    #     -------
    #     det_jac: np.ndarray
    #         The determinant of Jacobian matrix.

    #     inv_jac: np.ndarray
    #         The inverse of Jacobian matrix.
    #     """

    #     det_jac = self.get_detJAC(JAC)

    #     if len(JAC.shape) == 3:
    #         adj_matrix = np.zeros((det_jac.shape[0], 3, 3), dtype=float)
    #         adj_matrix[:, 0, 0] =  ((JAC[:, 1, 1] * JAC[:, 2, 2]) - (JAC[:, 2, 1] * JAC[:, 1, 2]))
    #         adj_matrix[:, 1, 0] = -((JAC[:, 1, 0] * JAC[:, 2, 2]) - (JAC[:, 1, 2] * JAC[:, 2, 0]))
    #         adj_matrix[:, 2, 0] =  ((JAC[:, 1, 0] * JAC[:, 2, 1]) - (JAC[:, 1, 1] * JAC[:, 2, 0]))
    #         adj_matrix[:, 0, 1] = -((JAC[:, 0, 1] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 1]))
    #         adj_matrix[:, 1, 1] =  ((JAC[:, 0, 0] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 0]))
    #         adj_matrix[:, 2, 1] = -((JAC[:, 0, 0] * JAC[:, 2, 1]) - (JAC[:, 0, 1] * JAC[:, 2, 0]))
    #         adj_matrix[:, 0, 2] =  ((JAC[:, 0, 1] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 1]))
    #         adj_matrix[:, 1, 2] = -((JAC[:, 0, 0] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 0]))
    #         adj_matrix[:, 2, 2] =  ((JAC[:, 0, 0] * JAC[:, 1, 1]) - (JAC[:, 0, 1] * JAC[:, 1, 0]))

    #     else:
    #         adj_matrix = np.zeros((3, 3), dtype=float)
    #         adj_matrix[0, 0] =  ((JAC[1, 1] * JAC[2, 2]) - (JAC[2, 1] * JAC[1, 2]))
    #         adj_matrix[1, 0] = -((JAC[1, 0] * JAC[2, 2]) - (JAC[1, 2] * JAC[2, 0]))
    #         adj_matrix[2, 0] =  ((JAC[1, 0] * JAC[2, 1]) - (JAC[1, 1] * JAC[2, 0]))
    #         adj_matrix[0, 1] = -((JAC[0, 1] * JAC[2, 2]) - (JAC[0, 2] * JAC[2, 1]))
    #         adj_matrix[1, 1] =  ((JAC[0, 0] * JAC[2, 2]) - (JAC[0, 2] * JAC[2, 0]))
    #         adj_matrix[2, 1] = -((JAC[0, 0] * JAC[2, 1]) - (JAC[0, 1] * JAC[2, 0]))
    #         adj_matrix[0, 2] =  ((JAC[0, 1] * JAC[1, 2]) - (JAC[0, 2] * JAC[1, 1]))
    #         adj_matrix[1, 2] = -((JAC[0, 0] * JAC[1, 2]) - (JAC[0, 2] * JAC[1, 0]))
    #         adj_matrix[2, 2] =  ((JAC[0, 0] * JAC[1, 1]) - (JAC[0, 1] * JAC[1, 0]))

    #     return det_jac, (1 / det_jac) * adj_matrix