from abc import ABC
from typing import Any, Optional

import numpy as np

from vibra.engine.analysis_info import AnalysisID, AnalysisSetup

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


class CommonSolution(ABC):
    analysis_setup: AnalysisSetup

    def __init__(self):
        # After calling the init this "cannot" be modified anymore
        self._writeable = False

    @property
    def analysis_id(self) -> AnalysisID:
        return self.analysis_setup.analysis_id

    def _immutable_array(self, array_like: np.typing.ArrayLike) -> Array1D | Array2D:
        """
        This methods converts to array and makes it immutable.

        We do not want anyone accidentally messing with our solution
        values, and forcing them to be immutable guarantees cache estability.
        """
        array = np.array(array_like, copy=True)
        array.setflags(write=False)
        return array

    def _optional_immutable_array(self, array_like: np.typing.ArrayLike | None) -> Array1D | Array2D | None:
        if array_like is None:
            return None
        return self._immutable_array(array_like)

    def __setattr__(self, name: str, value: Any):
        # workaround to make this class immutable
        if hasattr(self, "writeable") and not self._writeable and name != "writeable":
            raise ValueError(f"Class {self.__class__.__name__} is immutable")

        else:
            return super().__setattr__(name, value)
