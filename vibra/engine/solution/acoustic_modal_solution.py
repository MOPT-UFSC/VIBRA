from typing import Self

from vibra.engine.analysis_info import AnalysisID

from .common_solution import CommonModalSolution


# a lot more stuff will be implemented soon
class AcousticModalSolution(CommonModalSolution):
    analysis_id = AnalysisID.ACOUSTIC_MODAL

    def __eq__(self, other: Self) -> bool:
        return all(
            [
                isinstance(other, AcousticModalSolution),
                super().__eq__(other),
            ]
        )
