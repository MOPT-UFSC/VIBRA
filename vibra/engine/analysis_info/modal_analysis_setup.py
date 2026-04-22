from dataclasses import KW_ONLY, dataclass

from vibra.engine.analysis_info import AnalysisID
from vibra.utils.dataclass_utils import ignore_extra_kwargs


@ignore_extra_kwargs
@dataclass
class ModalAnalysisSetup:
    _: KW_ONLY
    modes_number: int = 50
    sigma_factor: float = 1e-2
    analysis_id: int = AnalysisID.NO_ANALYSIS

    def as_dict(self):
        return {
            "modes_number": self.modes_number,
            "sigma_factor": self.sigma_factor,
        }
