from dataclasses import dataclass, asdict
import json
from pathlib import Path

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


def load_material_list(path):
    path = Path(path)
    with open(path, "r") as file:
        data = json.load(file)
        material_list = [Material(**kwargs) for kwargs in data]
    return material_list


def save_material_list(path, material_list):
    dict_list = [asdict(material) for material in material_list]
    path = Path(path)
    with open(path, "w") as file:
        json.dump(dict_list, file, indent=2)
