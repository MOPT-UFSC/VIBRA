from pathlib import Path
import numpy as np
import h5py

HDF5_SOLUTION_FREQ_KEY = 'solution'
HDF5_SOLUTION_STATUS_KEY = 'solution_status'
HDF5_FREQ_KEY = 'frequencies'

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
        file_mode = 'a' if is_resume else 'w'
        self.file = h5py.File(self.filepath, file_mode)
        self.shape = (num_rows, num_cols)

        if HDF5_SOLUTION_FREQ_KEY in self.file:
            self.solution = self.file[HDF5_SOLUTION_FREQ_KEY]
            self.status = self.file[HDF5_SOLUTION_STATUS_KEY]
            self.frequencies = self.file[HDF5_FREQ_KEY]
        else:
            self.solution = self.file.create_dataset(
                HDF5_SOLUTION_FREQ_KEY,
                shape=(num_rows, num_cols),
                chunks=(num_rows, 1), # This is important for efficient read/load large matrices.
                dtype=dtype
            )
            self.frequencies = self.file.create_dataset(
                HDF5_FREQ_KEY,
                shape=(num_cols,),
                dtype=type(cols[0]),
                data=cols
            )
            self.status = self.file.create_dataset(
                HDF5_SOLUTION_STATUS_KEY,
                shape=(num_cols,),
                dtype=bool
            )
            self.status[:] = False

    def has_column(self, index):
        return self.status[index]

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

    def close(self):
        if hasattr(self, 'file'):
            self.file.close()
            self.file = None

    def __del__(self):
        self.close()


class LazyHDF5MatrixLoader:
    def __init__(self, filepath: Path):
        self.filepath = filepath

    def __getitem__(self, key):
        with h5py.File(self.filepath, 'r') as f:
            solution = f[HDF5_SOLUTION_FREQ_KEY]
            status = f[HDF5_SOLUTION_STATUS_KEY]
            shape = solution.shape

            def _get_column_data(col_idx):
                if not status[col_idx]:
                    raise ValueError(COL_ERROR_MESSAGE_FORMAT.format(col_idx))
                return solution[:, col_idx]

            if isinstance(key, tuple):
                row_idx, col_idx = key
            else:
                row_idx, col_idx = key, slice(None)

            if isinstance(col_idx, (int, np.integer)):
                if not status[col_idx]:
                    raise ValueError(COL_ERROR_MESSAGE_FORMAT.format(col_idx))
                return solution[row_idx, col_idx]

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
        with h5py.File(self.filepath, 'r') as f:
            status = f[HDF5_SOLUTION_STATUS_KEY][()]
        
        return not all(status)
