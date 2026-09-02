from typing import Any, override

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


class CommonSolution:
    analysis_id: AnalysisID = AnalysisID.NO_ANALYSIS

    def __init__(self):
        # After calling the init this "cannot" be modified anymore
        self._writeable = False

    def _immutable_array[T: Array1D | Array2D](self, array_like: T) -> T:
        """
        This methods converts to array and makes it immutable.

        We do not want anyone accidentally messing with our solution
        values, and forcing them to be immutable guarantees cache estability.
        """
        array = np.array(array_like, copy=True)
        array.setflags(write=False)
        return array

    def _optional_immutable_array[T: Array1D | Array2D | None](self, array_like: T) -> T:
        if array_like is None:
            return None
        return self._immutable_array(array_like)

    @override
    def __setattr__(self, name: str, value: Any):
        # workaround to make this class immutable
        if hasattr(self, "writeable") and not self._writeable and name != "writeable":
            raise ValueError(f"Class {self.__class__.__name__} is immutable")

        else:
            return super().__setattr__(name, value)
