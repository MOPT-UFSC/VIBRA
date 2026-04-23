from pathlib import Path

import h5py
import numpy as np
import pytest

from vibra.utils.lazy_array import LazyArray


@pytest.fixture
def hdf5_path(datadir: Path):
    return datadir / "test.hdf5"


def write_hdf5(hdf5_path: Path):
    with h5py.File(hdf5_path, "w") as f:
        f["lost"] = np.array([4, 8, 15, 16, 23, 42])
        f["fibonacci"] = np.array([0, 1, 1, 2, 3, 5, 8, 11])
        f["pascal"] = np.array(
            [
                [1, 1, 1, 1],
                [1, 2, 3, 4],
                [1, 3, 6, 10],
                [1, 4, 10, 20],
                [1, 5, 15, 35],
            ]
        )


def test_basic_funcionality(hdf5_path: Path):
    write_hdf5(hdf5_path)

    fibonacci = LazyArray(hdf5_path, "fibonacci")
    lost = LazyArray(hdf5_path, "lost")
    pascal = LazyArray(hdf5_path, "pascal")

    assert fibonacci.shape == (8,)
    assert lost.shape == (6,)
    assert pascal.shape == (5, 4)
    assert pascal.size == 20

    assert lost[2] == 15
    assert lost[-1] == 42
    assert (fibonacci[3:6] == (2, 3, 5)).all()

    ref = ((4, 10, 20), (5, 15, 35))
    assert (pascal[3:, 1:4] == ref).all()

    assert np.min(pascal) == 1
    assert np.max(pascal) == 35

    for i in lost:
        assert i == 4
        break  # one iteration is enough

    for i in reversed(lost):
        assert i == 42
        break  # one iteration is enough

    fibonacci_ref = [0, 1, 1, 2, 3, 5, 8, 11]
    assert (fibonacci == fibonacci_ref).all()

    assert 42 in lost
    assert 95 not in lost


def test_dunders(hdf5_path: Path):
    write_hdf5(hdf5_path)

    fibonacci = LazyArray(hdf5_path, "fibonacci")
    fibonacci_ref = [0, 1, 1, 2, 3, 5, 8, 11]

    assert fibonacci == fibonacci_ref
    assert not (fibonacci == [0, 1, 2, 3, 4, 5, 6, 7])
    assert fibonacci != [0, 1, 2, 3, 4, 5, 6, 7]
    assert not (fibonacci != fibonacci_ref)
    assert (fibonacci > -1).any()
    assert not (fibonacci > 100).any()
    assert (fibonacci <= 100).any()
    assert not (fibonacci <= -1).any()
    assert 0 in fibonacci
    assert 99 not in fibonacci

    assert (fibonacci + 1 == [1, 2, 2, 3, 4, 6, 9, 12]).all()
    assert (1 + fibonacci == [1, 2, 2, 3, 4, 6, 9, 12]).all()
    assert (fibonacci - 1 == [-1, 0, 0, 1, 2, 4, 7, 10]).all()
    assert (1 - fibonacci == [1, 0, 0, -1, -2, -4, -7, -10]).all()
    assert (fibonacci * 2 == [0, 2, 2, 4, 6, 10, 16, 22]).all()
    assert (2 * fibonacci == [0, 2, 2, 4, 6, 10, 16, 22]).all()
    assert (fibonacci / 2 == [0.0, 0.5, 0.5, 1.0, 1.5, 2.5, 4.0, 5.5]).all()
    assert (fibonacci // 2 == [0, 0, 0, 1, 1, 2, 4, 5]).all()
    assert (fibonacci % 3 == [0, 1, 1, 2, 0, 2, 2, 2]).all()
    assert (fibonacci**2 == [0, 1, 1, 4, 9, 25, 64, 121]).all()

    assert (-fibonacci == [0, -1, -1, -2, -3, -5, -8, -11]).all()
    assert (+fibonacci == fibonacci_ref).all()
    assert ((abs(-fibonacci) == fibonacci_ref).all()).all()
