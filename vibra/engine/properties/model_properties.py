from dataclasses import dataclass

from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material


class ModelProperties:
    def __init__(self):
        self._material = Material(name="Steel", identifier=1, color=(200,200,200), density=7860, young_modulus=210e9, poisson_ratio=0.3)
        self._fluid = Fluid(name="Air", identifier=1, color=(200,200,200), fluid_density=1.215, speed_of_sound=343.2021)

    def get_material(self, element=None) -> Material:
        return self._material

    def get_fluid(self, element=None) -> Fluid:
        return self._fluid

    def set_material(self, material: Material, element=None):
        self._material = material

    def set_fluid(self, fluid: Fluid, element=None):
        self._fluid = fluid
