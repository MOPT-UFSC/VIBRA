import h5py
from pathlib import Path
from typing import TYPE_CHECKING

import h5py
import numpy as np

if TYPE_CHECKING:
    LazyArrayTypeHints = np.ndarray
else:
    LazyArrayTypeHints = object


class LazyArray(LazyArrayTypeHints):
    """
    This class is meant to access the content of an HDF5 array
    without storing everyting in memory at once, while behaving
    just like a np.ndarray.

    Although the h5py.File already implements the lazy approach, it
    does not have all the methods and attributes to be used seamlessly
    as a numpy array.

    This approach converts the data to np.ndarray if necessary to allow
    full compatibility.
    """

    def __init__(self, file_path: Path, internal_name: str):
        self.file_path = file_path
        self.internal_name = internal_name
    
    def is_valid(self) -> bool:
        return h5py.is_hdf5(self.file_path)

    def __getattr__(self, attribute: str):
        with h5py.File(self.file_path, "r") as f:
            dataset = f[self.internal_name]

            if hasattr(dataset, attribute):
                return getattr(dataset, attribute)
            else:
                array = np.array(dataset)
                return getattr(array, attribute)

    def __getitem__(self, *args, **kwargs):
        with h5py.File(self.file_path, "r") as f:
            dataset = f[self.internal_name]
            return dataset.__getitem__(*args, **kwargs)

    def __len__(self):
        with h5py.File(self.file_path, "r") as f:
            return f[self.internal_name].len()

    def __array__(self):
        return self[:]

    def __add__(self, other):
        return self[:] + other

    def __radd__(self, other):
        return other + self[:]

    def __sub__(self, other):
        return self[:] - other

    def __rsub__(self, other):
        return other - self[:]

    def __mul__(self, other):
        return self[:] * other

    def __rmul__(self, other):
        return other * self[:]

    def __truediv__(self, other):
        return self[:] / other

    def __rtruediv__(self, other):
        return other / self[:]

    def __floordiv__(self, other):
        return self[:] // other

    def __rfloordiv__(self, other):
        return other // self[:]

    def __mod__(self, other):
        return self[:] % other

    def __rmod__(self, other):
        return other % self[:]

    def __pow__(self, other):
        return self[:] ** other

    def __rpow__(self, other):
        return other ** self[:]

    def __neg__(self):
        return -self[:]

    def __pos__(self):
        return +self[:]

    def __abs__(self):
        return abs(self[:])

    def __eq__(self, other):
        return (self[:] == other).all()

    def __ne__(self, other):
        return (self[:] != other).any()

    def __lt__(self, other):
        return self[:] < other

    def __le__(self, other):
        return self[:] <= other

    def __gt__(self, other):
        return self[:] > other

    def __ge__(self, other):
        return self[:] >= other

    def __contains__(self, item):
        return item in self[:]

    def __round__(self, ndigits=None):
        return np.round(self[:], ndigits)

    def __hash__(self):
        return hash(self[:])