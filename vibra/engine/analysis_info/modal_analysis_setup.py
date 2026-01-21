from dataclasses import dataclass


@dataclass
class ModalAnalysisSetup:
    modes_number: int
    sigma_factor: float

    def as_dict(self):
        return {
            "modes_number": self.modes_number,
            "sigma_factor": self.sigma_factor,
        }
