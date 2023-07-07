from dataclasses import dataclass


@dataclass
class Material:
    name: str
    identifier: int
    color: str
    density: float
    young_modulus: float
    poisson_ratio: float
    thermal_expansion_coefficient: float = 0.0

    @property
    def shear_modulus(self):
        return self.young_modulus / (2 * (1 + self.poisson_ratio))
