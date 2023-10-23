import json
import os
from dataclasses import dataclass

from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.project_file import ProjectFile

DEFAULT_MATERIAL = Material(
    name="Steel",
    identifier=1,
    color=(200, 200, 200),
    density=7860,
    young_modulus=210e9,
    poisson_ratio=0.3,
)

DEFAULT_FLUID = Fluid(
    name="Air",
    identifier=1,
    color=(200, 200, 200),
    fluid_density=1.215,
    speed_of_sound=343.2021,
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
        self.file = ProjectFile()
        self._reset_variables()

    def _reset_variables(self):
        self.global_properties = dict()
        self.volume_properties = dict()
        self.surface_properties = dict()
        self.line_properties = dict()
        self.element_properties = dict()
        self.nodal_properties = dict()

        self.global_properties["material", "global"] = DEFAULT_MATERIAL
        self.global_properties["fluid", "global"] = DEFAULT_FLUID

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

    def get_structural_boundary_condition(self, surface):
        return self._get_property("prescribed_dofs", surface=surface)

    def get_structural_load(self, surface):
        return self._get_property("structural_load", surface=surface)

    def set_structural_boundary_condition(self, data, line_id, surface_id):
        if line_id is not None:
            self._set_property("prescribed_dofs", data, line_id)
        if surface_id is not None:
            self._set_property("prescribed_dofs", data, surface_id)

    def set_structural_load(self, data, line_id, surface_id):
        if line_id is not None:
            self._set_property("structural_load", data, line_id)
        if surface_id is not None:
            self._set_property("structural_load", data, surface_id)

    def get_acoustic_pressure(self, surface):
        return self._get_property("acoustic_pressure", surface=surface)

    def get_mass_flow_rate(self, surface):
        return self._get_property("mass_flow_rate", surface=surface)

    def get_volume_velocity(self, surface):
        return self._get_property("volume_velocity", surface=surface)

    def get_surface_velocity(self, surface):
        return self._get_property("surface_velocity", surface=surface)

    def get_specific_impedance(self, surface):
        return self._get_property("specific_impedance", surface=surface)

    def set_acoustic_pressure(self, data, surface):
        self._set_property("acoustic_pressure", data, surface=surface)

    def set_mass_flow_rate(self, data, surface):
        self._set_property("mass_flow_rate", data, surface=surface)

    def set_volume_velocity(self, data, surface):
        self._set_property("volume_velocity", data, surface=surface)

    def set_surface_velocity(self, data, surface):
        self._set_property("surface_velocity", data, surface=surface)

    def set_specific_impedance(self, data, surface):
        self._set_property("specific_impedance", data, surface=surface)

    def _set_property(
        self, property: str, value, node=None, element=None, line=None, surface=None, volume=None
    ):
        """
        Sets a value to a property by node, element, line, surface or volume
        if any of these exists. Otherwise sets the property as global.

        """
        if node is not None:
            self.nodal_properties[property, node] = node
        elif volume is not None:
            self.volume_properties[property, volume] = value
        elif surface is not None:
            self.surface_properties[property, surface] = value
        elif line is not None:
            self.line_properties[property, line] = value
        elif element is not None:
            self.element_properties[property, element] = value
        else:
            self.global_properties[property, "global"] = value

    def _get_property(
        self, property: str, node=None, element=None, line=None, surface=None, volume=None
    ):
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

        if (property, line) in self.line_properties:
            return self.line_properties[property, line]

        if (property, surface) in self.surface_properties:
            return self.surface_properties[property, surface]

        if (property, volume) in self.volume_properties:
            return self.volume_properties[property, volume]

        if (property, "global") in self.global_properties:
            return self.global_properties[property, "global"]

        return None

    def check_if_there_are_tables_at_the_model(self):
        """This method checks if there are imported table of values in
        the model. It returns True if exists or False elsewhere.
        """
        data_dicts = [
            self.nodal_properties,
            self.element_properties,
            self.line_properties,
            self.surface_properties,
            self.volume_properties,
            self.global_properties,
        ]

        for data_dict in data_dicts:
            for data in data_dict.values():
                if isinstance(data, dict):
                    if "table_name" in data.keys():
                        return True
        else:
            return False

    def _reset_property(self, property: str):
        """
        Clears all instances of a specific property from the structure.
        """
        data_dicts = [
            self.nodal_properties,
            self.element_properties,
            self.line_properties,
            self.surface_properties,
            self.volume_properties,
            self.global_properties,
        ]

        for data in data_dicts:
            keys_to_remove = []

            for key in data.keys():
                if len(key) == 2:
                    existing_property, _ = key
                else:
                    existing_property = key

                if property == existing_property:
                    keys_to_remove.append(key)

            for _key in keys_to_remove:
                data.pop(_key)

    def _remove_nodal_property(self, property: str, nodal_id: int):
        """Remove a nodal property at specific nodal_id."""
        key = (property, nodal_id)
        if key in self.nodal_properties.keys():
            self.nodal_properties.pop(key)

    def _remove_element_property(self, property: str, element_id: int):
        """Remove a element property at specific element_id."""
        key = (property, element_id)
        if key in self.element_properties.keys():
            self.element_properties.pop(key)

    def _remove_line_property(self, property: str, line_id: int):
        """Remove a line property at specific line_id."""
        key = (property, line_id)
        if key in self.line_properties.keys():
            self.line_properties.pop(key)

    def _remove_surface_property(self, property: str, surface_id: int):
        """Remove a surface property at specific surface_id."""
        key = (property, surface_id)
        if key in self.surface_properties.keys():
            self.surface_properties.pop(key)

    def _remove_volume_property(self, property: str, volume_id: int):
        """Remove a volume property at specific volume_id."""
        key = (property, volume_id)
        if key in self.volume_properties.keys():
            self.volume_properties.pop(key)

    # TODO: remove this
    def as_json(self):
        def normalize(prop: dict):
            """
            Sadly json doesn't accepts tuple keys,
            so we need to convert it to a string like:
            "property id" = value
            """
            return {f"{p} {i}": v for (p, i), v in prop.items()}

        data = dict(
            # global_properties = normalize(self.global_properties),
            volume_properties=normalize(self.volume_properties),
            surface_properties=normalize(self.surface_properties),
            line_properties=normalize(self.line_properties),
            element_properties=normalize(self.element_properties),
            nodal_properties=normalize(self.nodal_properties),
        )
        return json.dumps(data, indent=2)

    # TODO: remove this
    def load_json(self, data: dict):
        def denormalize(prop: dict):
            new_prop = dict()
            for key, val in prop.items():
                p, i = key.split()
                p = p.strip()
                i = int(i)
                new_prop[p, i] = val
            return new_prop

        self.global_properties = denormalize(data["global_properties"])
        self.volume_properties = denormalize(data["volume_properties"])
        self.surface_properties = denormalize(data["surface_properties"])
        self.line_properties = denormalize(data["line_properties"])
        self.element_properties = denormalize(data["element_properties"])
        self.nodal_properties = denormalize(data["nodal_properties"])

    def export_model_properties(self):
        try:
            path = os.path.join(self.file.project_path, "model_properties.json")
            with open(path, "w") as file:
                file.write(self.as_json())
        except Exception as error:
            print(str(error))


if __name__ == "__main__":
    p = ModelProperties()
    with open("teste.json", "w") as file:
        file.write(p.as_json())

    q = ModelProperties()
    with open("teste.json", "r") as file:
        data = json.load(file)
        q.load_json(data)
