from dataclasses import dataclass

from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material


class ModelProperties:
    def __init__(self):
        self._reset_variables()
        self._material = Material(name="Steel", identifier=1, color=(200,200,200), density=7860, young_modulus=210e9, poisson_ratio=0.3)
        self._fluid = Fluid(name="Air", identifier=1, color=(200,200,200), fluid_density=1.215, speed_of_sound=343.2021)

    def _reset_variables(self):

        self.dissipation_model = None

        self.lines_with_loads = dict()
        self.lines_with_prescribed_dofs = dict()
        self.surfaces_with_prescribed_dofs = dict()
        self.volumes_with_prescribed_dofs = dict()

        self.surfaces_with_acoustic_pressure = dict()
        self.surfaces_with_volume_velocity = dict()
        self.surfaces_with_mass_flow_rate = dict()
        self.surfaces_with_particle_velocity = dict()

    def get_material(self, element=None) -> Material:
        return self._material

    def get_fluid(self, element=None) -> Fluid:
        return self._fluid

    def get_dissipation_model(self, element=None):
        return self.dissipation_model

    def set_material(self, material: Material, element=None):
        self._material = material

    def set_fluid(self, fluid: Fluid, element=None):
        self._fluid = fluid
    
    def set_dissipation_model(self, data, volume=None):
        self.dissipation_model = data

    def get_speed_of_sound(self, element=None):
        #
        fluid = self.get_fluid(element=element)
        c_0 = fluid.speed_of_sound
        #
        dissipation_model = self.get_dissipation_model(element=element)
        if dissipation_model is None:
            return c_0
        elif dissipation_model["model"] == "proportional damping":
            factor = dissipation_model["speed of sound factor"]
            return (1 + factor*1j)*c_0

    def set_structural_boundary_condition(self, data):
        #
        if "line" in data["entity_type"]:
            for _id in data["entity_ids"]:
                self.lines_with_prescribed_dofs[_id] = data["values"]
        #
        if "surface" in data["entity_type"]:
            for _id in data["entity_ids"]:
                self.surfaces_with_prescribed_dofs[_id] = data["values"]

    def set_structural_load(self, data):
        #    
        if "line" in data["entity_type"]:
            for _id in data["entity_ids"]:
                self.lines_with_loads[_id] = data["values"]
        #
        if "surface" in data["entity_type"]:
            for _id in data["entity_ids"]:
                self.surfaces_with_loads[_id] = data["values"]

    def set_acoustic_pressure(self, data):
        #
        _data = data.copy()    
        if "surface" in data["entity_type"]:
            for _id in data["entity_ids"]:
                _data.pop("entity_ids")
                self.surfaces_with_acoustic_pressure[_id] = _data

    def set_mass_flow_rate(self, data):
        #
        _data = data.copy()
        if "surface" in _data["entity_type"]:
            for _id in _data["entity_ids"]:
                _data.pop("entity_ids")
                self.surfaces_with_mass_flow_rate[_id] = _data

    def set_volume_velocity(self, data):
        #
        _data = data.copy()
        if "surface" in _data["entity_type"]:
            for _id in _data["entity_ids"]:
                _data.pop("entity_ids")
                self.surfaces_with_volume_velocity[_id] = _data

    def set_particle_velocity(self, data):
        #
        _data = data.copy()           
        if "surface" in data["entity_type"]:
            for _id in data["entity_ids"]:
                _data.pop("entity_ids")
                self.surfaces_with_particle_velocity[_id] = _data

    def remove_volume_velocity(self, entity_id):
        if entity_id in self.surfaces_with_volume_velocity.keys():
            self.surfaces_with_volume_velocity.pop(entity_id)

    def reset_surfaces_with_prescribed_dofs(self):
        self.lines_with_prescribed_dofs = dict()
        self.surfaces_with_prescribed_dofs = dict()

    def reset_surfaces_with_loads(self):
        self.lines_with_loads = dict()
        self.surfaces_with_loads = dict()

    def reset_acoustic_pressure(self):
        self.surfaces_with_acoustic_pressure = dict()

    def reset_mass_flow_rate(self):
        self.surfaces_with_mass_flow_rate = dict()
        
    def reset_volume_velocity(self):
        self.surfaces_with_volume_velocity = dict()
                
    def reset_particle_velocity(self):
        self.surfaces_with_particle_velocity = dict()