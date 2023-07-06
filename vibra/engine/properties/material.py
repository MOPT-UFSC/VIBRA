from dataclasses import dataclass


@dataclass
class Material:
    name: str
    identifier: int
    color: list
    density: float
    young_modulus: float
    poisson_ratio: float
    thermal_expansion_coefficient: float
