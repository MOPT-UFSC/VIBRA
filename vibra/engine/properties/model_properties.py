from dataclasses import dataclass

from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material


class ModelProperties:
    def __init__(self):
        self._material = None
        self._fluid = None

    def get_material(self, element=None) -> Material:
        return self._material

    def get_fluid(self, element=None) -> Fluid:
        return self._fluid

    def set_material(self, material: Material, element=None):
        self._material = material

    def set_fluid(self, fluid: Fluid, element=None):
        self._fluid = fluid
