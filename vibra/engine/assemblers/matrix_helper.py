import numpy as np


def get_reordering_indices(rows: np.ndarray, cols: np.ndarray) -> np.ndarray:
    """
    This method returns the indices to reorder the sparse matrices in such
    a way that the rows and columns are lexically sorted and all data that
    are on the same position are grouped together into a single index.

    Parameters
    ----------
    rows: np.ndarray
        Array with the rows of the sparse matrix.
        It is assumed to be a 1D array.

    cols: np.ndarray
        Array with the columns of the sparse matrix.
        It is assumed to be a 1D array.

    returns
    -------
    np.ndarray
        Array with the indices to reorder the sparse matrices.
    """

    # Sorts rows and columns according to lexicographic order
    order: np.ndarray = np.lexsort((cols, rows))
    rows: np.ndarray = rows[order]
    cols: np.ndarray = cols[order]

    # Creates the indices to "unsort" the data sorted with the previous indices
    inverse_ordering = np.empty_like(order)
    inverse_ordering[order] = np.arange(len(order))

    # Identifies repeated rows and columns
    repeated = np.ones_like(rows, dtype=bool)
    repeated[0] = False
    repeated[1:] &= rows[1:] == rows[:-1]
    repeated[1:] &= cols[1:] == cols[:-1]

    # Assigns a unique index to each repeated row and column
    unified_indices = np.cumsum(~repeated) - 1
    reordering = unified_indices[inverse_ordering]
    return reordering


def reorder_data(data: np.ndarray, reordering: np.ndarray, target: np.ndarray | None = None) -> np.ndarray:
    """
    This method reorders the data according to the provided indices,
    summing values that occur in the same position.
    If no target is provided, it creates a zeroed array and use it.

    Parameters
    ---------
    data: np.ndarray
        The data to be reordered.
        It is assumed to be a 1D array.

    reordering: np.ndarray
        The indices to reorder the data.
        It is assumed to be a 1D array.

    target: np.ndarray, optional
        The target array to store the reordered data.
        It is assumed to be a 1D array.

    Returns
    -------
    target: np.ndarray
        The target array with the reordered data.
    """

    if target is None:
        n_different_values = np.max(reordering) + 1
        target = np.zeros(n_different_values, data.dtype)
    else:
        target *= 0

    np.add.at(target, reordering, data.flatten())
    return target
