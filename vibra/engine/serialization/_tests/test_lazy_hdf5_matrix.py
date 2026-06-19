from pathlib import Path

import numpy as np
import pytest

from vibra.engine.serialization.lazy_hdf5_matrix import (
    COL_ERROR_MESSAGE_FORMAT,
    COLS_EMPTY_ERROR_MESSAGE,
    NUM_ROWS_ZERO_ERROR_MESSAGE,
    LazyHDF5MatrixLoader,
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


def test_write_and_read_full(hdf5_file_path: Path):
    num_rows = 10
    freqs = [1, 2, 3]

    writer = LazyHDF5MatrixWriter(hdf5_file_path, num_rows, freqs, float)

    for i, f in enumerate(freqs):
        writer.save(np.full((num_rows,), i, dtype=float), i)
    writer.close()

    reader = LazyHDF5MatrixLoader(hdf5_file_path)
    for i in range(len(freqs)):
        np.testing.assert_array_equal(reader[:, i], np.full(num_rows, i, dtype=float))


def test_partial_and_resume_write(hdf5_file_path: Path):
    num_rows = 10
    freqs = [1, 2, 3]
    writer = LazyHDF5MatrixWriter(hdf5_file_path, num_rows, freqs, float)
    writer.save(np.ones(num_rows, dtype=float), 0)
    writer.close()

    writer = LazyHDF5MatrixWriter(hdf5_file_path, num_rows, freqs, float, is_resume=True)
    writer.save(np.ones(num_rows, dtype=float) * 2, 2)
    writer.close()

    reader = LazyHDF5MatrixLoader(hdf5_file_path)
    np.testing.assert_array_equal(reader[:, 0], np.ones(num_rows))
    np.testing.assert_array_equal(reader[:, 2], np.ones(num_rows) * 2)
    with pytest.raises(ValueError, match=COL_ERROR_MESSAGE_FORMAT.format(1)):
        _ = reader[:, 1]


def test_read_column_not_filled(hdf5_file_path: Path):
    num_rows = 10
    freqs = [1, 2, 3]
    writer = LazyHDF5MatrixWriter(hdf5_file_path, num_rows, freqs, float)
    writer.save(np.ones(num_rows, dtype=float), 0)
    writer.close()

    reader = LazyHDF5MatrixLoader(hdf5_file_path)
    with pytest.raises(ValueError, match=COL_ERROR_MESSAGE_FORMAT.format(1)):
        _ = reader[:, 1]
