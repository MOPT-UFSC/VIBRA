from functools import cached_property
from typing import Any, Generator, Optional, Self

import numpy as np

from vibra.engine.analysis_info import AnalysisID

# Até dá pra deixar o tipo do array configurável
# mas só depois do python 3.12, acho que é muito
# recente pra forçar uma versão mais nova
Array1D = np.ndarray[
    tuple[int],
    float | complex,
]

Array2D = np.ndarray[
    tuple[int, int],
    float | complex,
]


class Common:
    analysis_id: AnalysisID = AnalysisID.NO_ANALYSIS

    def __init__(self):
        # After calling the init this "cannot" be modified anymore
        self._writeable = False

    def is_harmonic(self):
        return self.analysis_id.is_harmonic()

    def is_modal(self):
        return self.analysis_id.is_modal()

    def is_static(self):
        return self.analysis_id.is_static()

    def is_structural(self):
        return self.analysis_id.is_structural()

    def is_acoustic(self):
        return self.analysis_id.is_acoustic()

    def is_coupled(self):
        return self.analysis_id.is_coupled()

    def _immutable_array(self, array_like: np.typing.ArrayLike) -> Array1D | Array2D:
        """
        This methods converts to array and makes it immutable.

        We do not want anyone accidentally messing with our solution
        values, and forcing them to be immutable guarantees cache estability.
        """
        array = np.array(array_like, copy=True)
        array.setflags(write=False)
        return array

    def __setattr__(self, name: str, value: Any):
        # workaround to make this class immutable
        if hasattr(self, "writeable") and not self._writeable and name != "writeable":
            raise ValueError(f"Class {self.__class__.__name__} is immutable")

        else:
            return super().__setattr__(name, value)


class CommonModalSolution(Common):
    natural_frequencies: Array1D
    modal_shape: Array2D
    complex_natural_frequencies: Optional[Array1D] = None

    def __init__(
        self,
        natural_frequencies: Array1D,
        modal_shape: Array2D,
        complex_natural_frequencies: Optional[Array1D],
    ):
        self.natural_frequencies = self._immutable_array(natural_frequencies)
        self.modal_shape = self._immutable_array(modal_shape)
        if complex_natural_frequencies is not None:
            self.complex_natural_frequencies = self._immutable_array(complex_natural_frequencies)
        super().__init__()

    @cached_property
    def iscomplex(self):
        return np.iscomplex(self.natural_frequencies) or np.iscomplex(self.modal_shape)

    @cached_property
    def number_of_modes(self):
        return len(self.natural_frequencies)

    def get_row(self, row_index: int) -> Array1D:
        return self.modal_shape[row_index, :]

    def get_column(self, column_index: int) -> Array1D:
        return self.modal_shape[:, column_index]

    def __iter__(self) -> Generator[tuple[float | complex, Array1D], None, None]:
        yield from zip(self.natural_frequencies, self.modal_shape)

    def __eq__(self, other: Self) -> bool:
        return all(
            [
                np.allclose(self.natural_frequencies, other.natural_frequencies),
                np.allclose(self.modal_shape, other.modal_shape),
                np.allclose(self.complex_natural_frequencies, other.complex_natural_frequencies),
            ]
        )


class CommonHarmonicSolution(Common):
    frequencies: Array1D
    results: Array2D
    status: np.ndarray[tuple[int], bool]

    def __init__(
        self,
        frequencies: Array1D,
        results: Array2D,
        status: Optional[np.ndarray[tuple[int], bool]] = None,
    ):
        self.frequencies = self._immutable_array(frequencies)
        self.results = self._immutable_array(results)
        self.status = self._create_status(status)
        super().__init__()

    @cached_property
    def iscomplex(self):
        return np.iscomplex(self.frequencies) or np.iscomplex(self.results)

    @cached_property
    def number_of_frequencies(self):
        return len(self.number_of_frequencies)

    @cached_property
    def has_partial_solutions(self):
        return not all(self.status)

    def get_row(self, row_index: int) -> Array1D:
        return self.results[row_index, :]

    def get_column(self, column_index: int) -> Array1D:
        return self.results[:, column_index]

    def _create_status(self, status: Optional[np.ndarray[tuple[int], bool]]):
        if status is None:
            return np.ones_like(self.frequencies, dtype=bool)
        return self._immutable_array(status)

    def __iter__(self) -> Generator[tuple[float | complex, Array1D], None, None]:
        yield from zip(self.frequencies, self.results)

    def __eq__(self, other: Self) -> bool:
        return all(
            [
                np.allclose(self.frequencies, other.frequencies),
                np.allclose(self.results, other.results),
                np.allclose(self.status, other.status),
            ]
        )
