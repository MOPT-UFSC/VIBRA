from dataclasses import dataclass

from vibra.engine.analysis_info import AnalysisID
from vibra.utils.dataclass_utils import ignore_extra_kwargs


@ignore_extra_kwargs
@dataclass(kw_only=True)
class StaticAnalysisSetup:
    self_weight: bool = False
    analysis_id: int = AnalysisID.NO_ANALYSIS
    outdated_solution: bool = False

    def as_dict(self):
        return {
            "self_weight": self.self_weight,
            "outdated_solution" : self.outdated_solution,
        }