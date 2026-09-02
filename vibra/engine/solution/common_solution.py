from typing import Any, override

import numpy as np

from vibra.engine.analysis_info import AnalysisID


class CommonSolution:
    analysis_id: AnalysisID = AnalysisID.NO_ANALYSIS

    def __init__(self):
        # After calling the init this "cannot" be modified anymore
        self._writeable = False

    def _immutable_array(self, array_like: np.ndarray) -> np.ndarray:
        """
        This methods converts to array and makes it immutable.

        We do not want anyone accidentally messing with our solution
        values, and forcing them to be immutable guarantees cache estability.
        """
        array = np.array(array_like, copy=True)
        array.setflags(write=False)
        return array

    def _optional_immutable_array(self, array_like: np.ndarray | None) -> np.ndarray | None:
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
