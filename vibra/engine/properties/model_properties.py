from dataclasses import dataclass

from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material


class ModelProperties:
    def __init__(self):
        self._reset_variables()
        self._material = Material(name="Steel", identifier=1, color=(200,200,200), density=7860, young_modulus=210e9, poisson_ratio=0.3)
        self._fluid = Fluid(name="Air", identifier=1, color=(200,200,200), fluid_density=1.215, speed_of_sound=343.2021)

    def _reset_variables(self):
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

    def set_material(self, material: Material, element=None):
        self._material = material

    def set_fluid(self, fluid: Fluid, element=None):
        self._fluid = fluid

    def set_structural_boundary_condition(self, data):
        try:
            
            if "line" in data["entity_type"]:
                for _id in data["entity_ids"]:
                    self.lines_with_prescribed_dofs[_id] = data["values"]

            if "surface" in data["entity_type"]:
                for _id in data["entity_ids"]:
                    self.surfaces_with_prescribed_dofs[_id] = data["values"]

        except Exception as error_log:
            print(str(error_log))


    def set_structural_load(self, data):
        try:
            
            if "line" in data["entity_type"]:
                for _id in data["entity_ids"]:
                    self.lines_with_loads[_id] = data["values"]

            if "surface" in data["entity_type"]:
                for _id in data["entity_ids"]:
                    self.surfaces_with_loads[_id] = data["values"]

        except Exception as error_log:
            print(str(error_log))


    def set_acoustic_pressure(self, data):
        try:
            
            if "surface" in data["entity_type"]:
                for _id in data["entity_ids"]:
                    self.surfaces_with_acoustic_pressure[_id] = data["values"]

        except Exception as error_log:
            print(str(error_log))


    def set_mass_flow_rate(self, data):
        try:
            
            if "surface" in data["entity_type"]:
                for _id in data["entity_ids"]:
                    self.surfaces_with_mass_flow_rate[_id] = data["values"]

        except Exception as error_log:
            print(str(error_log))


    def set_volume_velocity(self, data):
        try:
            
            if "surface" in data["entity_type"]:
                for _id in data["entity_ids"]:
                    self.surfaces_with_volume_velocity[_id] = [data["values"], data["averaged"]]

        except Exception as error_log:
            print(str(error_log))
    

    def set_particle_velocity(self, data):
        try:
            
            if "surface" in data["entity_type"]:
                for _id in data["entity_ids"]:
                    self.surfaces_with_particle_velocity[_id] = data["values"]

        except Exception as error_log:
            print(str(error_log))

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