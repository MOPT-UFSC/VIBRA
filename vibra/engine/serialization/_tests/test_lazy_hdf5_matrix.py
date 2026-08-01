from pathlib import Path

import pytest

from vibra.engine.serialization.lazy_hdf5_matrix import (
    COLS_EMPTY_ERROR_MESSAGE,
    NUM_ROWS_ZERO_ERROR_MESSAGE,
    LazyHDF5MatrixWriter,
)


@pytest.fixture
def hdf5_file_path(datadir: Path):
    return datadir / "matrix.h5"


def test_writer_input_validation(hdf5_file_path: Path):
    with pytest.raises(ValueError, match=COLS_EMPTY_ERROR_MESSAGE):
        LazyHDF5MatrixWriter(hdf5_file_path, 10, [], float)

    with pytest.raises(ValueError, match=NUM_ROWS_ZERO_ERROR_MESSAGE):
        LazyHDF5MatrixWriter(hdf5_file_path, 0, [5], float)
