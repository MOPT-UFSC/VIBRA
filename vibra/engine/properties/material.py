from dataclasses import dataclass


@dataclass
class Material:
    name: str
    density: float
    young_modulus: float