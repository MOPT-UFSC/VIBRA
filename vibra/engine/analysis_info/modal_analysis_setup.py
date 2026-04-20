from dataclasses import dataclass, fields
from functools import wraps
from vibra.engine.analysis_info import AnalysisID

def ignore_extra_kwargs(cls):
    original_init = cls.__init__

    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        
        # expected fields of original dataclass
        expected_fields = {f.name for f in fields(cls)}

        # filter the unnecessary kwargs
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in expected_fields}

        original_init(self, *args, **filtered_kwargs)

    cls.__init__ = new_init
    return cls


@ignore_extra_kwargs
@dataclass
class ModalAnalysisSetup:
    modes_number: int
    sigma_factor: float
    analysis_id: int = AnalysisID.NO_ANALYSIS

    def as_dict(self):
        return {
            "modes_number": self.modes_number,
            "sigma_factor": self.sigma_factor,
        }
