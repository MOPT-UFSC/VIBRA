from dataclasses import dataclass


@dataclass
class Material:
    name: str
    density: float
    young_modulus: float
    poisson_ratio: float
    identifier: int = 0
    thermal_expansion_coefficient: float = 0.0
    color: tuple = (0, 0, 0)

    @property
    def shear_modulus(self):
        return self.young_modulus / (2 * (1 + self.poisson_ratio))
