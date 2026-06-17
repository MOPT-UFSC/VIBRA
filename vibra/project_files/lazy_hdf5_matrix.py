from pathlib import Path

import h5py
import numpy as np

HDF5_SOLUTION_FREQ_KEY = "solution"
HDF5_SOLUTION_STATUS_KEY = "solution_status"
HDF5_FREQ_KEY = "frequencies"

COL_ERROR_MESSAGE_FORMAT = "Column '{0}' not filled."
COLS_EMPTY_ERROR_MESSAGE = "Input 'cols' cannot be empty."
NUM_ROWS_ZERO_ERROR_MESSAGE = "Input 'num_rows' cannot be zero."


class LazyHDF5MatrixWriter:
    def __init__(self, filepath: Path, num_rows: int, cols: list, dtype, is_resume: bool = False):
        if len(cols) == 0:
            raise ValueError(COLS_EMPTY_ERROR_MESSAGE)

        if num_rows == 0:
            raise ValueError(NUM_ROWS_ZERO_ERROR_MESSAGE)

        num_cols = len(cols)
        self.filepath = filepath
        file_mode = "a" if is_resume else "w"
        self.file = h5py.File(self.filepath, file_mode)
        self.shape = (num_rows, num_cols)

        chunk_rows = min(num_rows, 2**20)
        chunk_cols = 1

        self.solution = self.create_dataset_if_not_exists(
            HDF5_SOLUTION_FREQ_KEY,
            shape=(num_rows, num_cols),
            chunks=(chunk_rows, chunk_cols),  # This is important for efficient read/load large matrices.
            dtype=dtype,
        )
        self.frequencies = self.create_dataset_if_not_exists(
            HDF5_FREQ_KEY,
            shape=(num_cols,),
            dtype=type(cols[0]),
            data=cols,
        )
        self.status = self.create_dataset_if_not_exists(
            HDF5_SOLUTION_STATUS_KEY,
            shape=(num_cols,),
            dtype=bool,
        )

    def has_column(self, index):
        return self.status[index]

    def create_dataset_if_not_exists(self, name, shape=None, dtype=None, data=None, **kwargs):
        if name in self.file:
            return self.file[name]

        return self.file.create_dataset(name, shape, dtype, data, **kwargs)

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            row_idx, col_idx = key
            if row_idx != slice(None):
                raise NotImplementedError("Partial assignment per row is not supported.")
        else:
            col_idx = key

        if isinstance(col_idx, (int, np.integer)):
            self.save(value, col_idx)
        else:
            raise NotImplementedError("Multiple column assignment is not supported.")

    def save(self, column, index: int, overwrite=False):
        if not overwrite and self.status[index]:
            return
        self.solution[:, index] = column
        self.status[index] = True
        self.file.flush()

    def save_extra_data(self, key: str, data, dtype=None):
        self.create_dataset_if_not_exists(key, data=data, dtype=dtype)
        self.file.flush()

    def close(self):
        if hasattr(self, "file") and self.file is not None:
            self.file.close()

    def __del__(self):
        self.close()


class LazyHDF5MatrixLoader:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self._solution_cache = {}

    @property
    def size(self) -> int:
        with h5py.File(self.filepath, "r") as f:
            return f[HDF5_SOLUTION_FREQ_KEY].size

    def __getitem__(self, key):
        with h5py.File(self.filepath, "r") as f:
            solution = f[HDF5_SOLUTION_FREQ_KEY]
            status = f[HDF5_SOLUTION_STATUS_KEY]
            shape = solution.shape

            def _get_column_data(col_idx):
                if col_idx in self._solution_cache:
                    return self._solution_cache[col_idx]
                if not status[col_idx]:
                    raise ValueError(COL_ERROR_MESSAGE_FORMAT.format(col_idx))
                self._solution_cache[col_idx] = solution[:, col_idx]
                return self._solution_cache[col_idx]

            if isinstance(key, tuple):
                row_idx, col_idx = key
            else:
                row_idx, col_idx = key, slice(None)

            if isinstance(col_idx, (int, np.integer)):
                return _get_column_data(col_idx)[row_idx]

            if isinstance(col_idx, slice):
                cols = range(*col_idx.indices(shape[1]))
            else:
                cols = col_idx

            cols = list(cols)

            for c in cols:
                if not status[c]:
                    raise ValueError(COL_ERROR_MESSAGE_FORMAT.format(col_idx))

            return np.stack([_get_column_data(i)[row_idx] for i in cols], axis=-1)

    def has_partial_solutions(self):
        if not self.filepath.exists():
            return False

        with h5py.File(self.filepath, "r") as f:
            status = f[HDF5_SOLUTION_STATUS_KEY][()]

        return not all(status)

    def get_extra_data(self, key: str):
        with h5py.File(self.filepath, "r") as f:
            if key not in f:
                raise KeyError(f"Dataset '{key}' not found in file.")
            return f[key][()]
