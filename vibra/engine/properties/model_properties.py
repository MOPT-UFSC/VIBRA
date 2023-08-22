from dataclasses import dataclass

from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material

DEFAULT_MATERIAL = Material(
    name="Steel",
    identifier=1,
    color=(200, 200, 200),
    density=7860,
    young_modulus=210e9,
    poisson_ratio=0.3,
)
DEFAULT_FLUID = Fluid(
    name="Air", identifier=1, color=(200, 200, 200), fluid_density=1.215, speed_of_sound=343.2021
)


class ModelProperties:
    """
    Class that stores all properties of a model.

    All properties can be setted per node, element, entity,
    volume or globally.

    The only functions that deals with data are _set_property,
    _get_property and _reset_property. All the others are just
    wrappers that call these ones.

    I know it may seem a little weird to structure the data this
    way because it would probably be faster to just use one dict
    for each property in each level of the structure.
    But the current approach is (I hope) a lot less error prone.
    It uses few dicts and we do not need to care if the data
    is handled correctly for each case, because few functions
    handles it, reducing the points of failure.

    Also, the speed is only a requirement on the retrieval of
    data (because it is done multiple times by every element),
    and it is pretty fast. The other operations are proportional
    to things that a human can put here manually (and by the real
    world requirements of the model), so of course a computer can
    handle it in fractions of a second.

    """

    def __init__(self, model=None):
        self._reset_variables()

    def _reset_variables(self):
        self.global_properties = dict()
        self.volume_properties = dict()
        self.entity_properties = dict()
        self.element_properties = dict()
        self.nodal_properties = dict()

        self.global_properties["material"] = DEFAULT_MATERIAL
        self.global_properties["fluid"] = DEFAULT_FLUID

        # Remove this when no more needed
        self.lines_with_loads = dict()
        self.lines_with_prescribed_dofs = dict()
        self.surfaces_with_prescribed_dofs = dict()
        self.volumes_with_prescribed_dofs = dict()

        self.surfaces_with_acoustic_pressure = dict()
        self.surfaces_with_volume_velocity = dict()
        self.surfaces_with_mass_flow_rate = dict()
        self.surfaces_with_particle_velocity = dict()

    def get_material(self, element=None) -> Material:
        return self._get_property("material")

    def get_fluid(self, element=None) -> Fluid:
        return self._get_property("fluid")

    def get_dissipation_model(self, element=None):
        return self._get_property("dissipation_model")

    def set_material(self, material: Material, element=None):
        self._set_property("material", material)

    def set_fluid(self, fluid: Fluid, element=None):
        self._set_property("fluid", fluid)

    def set_dissipation_model(self, data, volume=None):
        self._set_property("dissipation_model", data)

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
            return (1 + factor * 1j) * c_0

    # Update the following functions to use the structure
    # with less dicts
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

    #
    def _set_property(
        self, property: str, value, node=None, element=None, entity=None, volume=None
    ):
        """
        Sets a value to a property by node, element, entity or volume
        if any of these exists. Otherwise sets the property as global.

        """
        if node is not None:
            self.nodal_properties[property, node] = node
        elif volume is not None:
            self.volume_properties[property, volume] = value
        elif entity is not None:
            self.entity_properties[property, entity] = value
        elif element is not None:
            self.element_properties[property, element] = value
        else:
            self.global_properties[property] = value

    def _get_property(self, property: str, node=None, element=None, entity=None, volume=None):
        """
        Finds the value that corresponds to the property needed.
        Checks node, element, entity, volume and global data by
        this respective order of priority.
        If the any of this is defined returns None.
        """
        if (property, node) in self.nodal_properties:
            return self.nodal_properties[property, node]

        if (property, element) in self.element_properties:
            return self.element_properties[property, element]

        if (property, entity) in self.entity_properties:
            return self.entity_properties[property, entity]

        if (property, volume) in self.volume_properties:
            return self.volume_properties[property, volume]

        if property in self.global_properties:
            return self.global_properties[property]

        return None

    def _reset_property(self, property: str):
        """
        Clears all instances of a specific property from the structure.
        """
        data_dicts = [
            self.nodal_properties,
            self.element_properties,
            self.entity_properties,
            self.volume_properties,
            self.global_properties,
        ]

        for data in data_dicts:
            keys_to_remove = []

            for key, val in data.items():
                existing_property, _ = key
                if property == existing_property:
                    keys_to_remove.append(property)

            for key in keys_to_remove:
                data.pop(key)
