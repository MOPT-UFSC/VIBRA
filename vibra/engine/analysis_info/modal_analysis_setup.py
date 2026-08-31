from dataclasses import dataclass

from vibra.engine.analysis_info import AnalysisID
from vibra.utils.dataclass_utils import ignore_extra_kwargs


@ignore_extra_kwargs
@dataclass(kw_only=True)
class ModalAnalysisSetup:
    analysis_id: AnalysisID = AnalysisID.NO_ANALYSIS
    modes_number: int = 50
    sigma_factor: float = 1e-2
    outdated_solution: bool = False

    def as_dict(self):
        return {
            "modes_number": self.modes_number,
            "sigma_factor": self.sigma_factor,
            "outdated_solution" : self.outdated_solution,
        }
