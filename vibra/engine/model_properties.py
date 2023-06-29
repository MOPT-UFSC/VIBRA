from vibra.engine.fluid import Fluid
from vibra.engine.material import Material
from dataclasses import dataclass


class ModelProperty:
    def __init__(self):
        self._material = None
        self._fluid = None
    
    def get_material(self) -> Material:
        return self._material
    
    def get_fluid(self) -> Fluid:
        return self._fluid

    def set_material(self, material: Material):
        self._material = material

    def set_fluid(self, fluid: Fluid):
        self._fluid = fluid
