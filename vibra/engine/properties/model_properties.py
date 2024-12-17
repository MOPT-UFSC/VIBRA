import json
import numpy as np
import os
from dataclasses import dataclass

from vibra import app
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
# from vibra.project.project_file import *


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

        self._reset_variables()

    def _reset_variables(self):

        self.acoustic_imported_tables = dict()
        self.structural_imported_tables = dict()

        self.global_properties = dict()
        self.group_properties = dict()
        self.volume_properties = dict()
        self.surface_properties = dict()
        self.line_properties = dict()
        self.element_properties = dict()
        self.nodal_properties = dict()

        self.global_properties["material", "global"] = DEFAULT_MATERIAL
        self.global_properties["fluid", "global"] = DEFAULT_FLUID

    def get_material(self, element=None, **kwargs) -> Material:
        return self._get_property("material", **kwargs)

    def get_fluid(self, **kwargs) -> Fluid:
        return self._get_property("fluid", **kwargs)

    def get_dissipation_model(self, **kwargs):
        return self._get_property("dissipation_model", **kwargs)
    
    def get_lrf_model_inputs(self, element_id):
        return self._get_property("lrf_eq_model", element=element_id)

    def set_material(self, material: Material, surface=None, volume=None):
        self._set_property("material", material, surface=surface, volume=volume)

    def set_fluid(self, fluid: Fluid, surface=None, volume=None):
        self._set_property("fluid", fluid, surface=surface, volume=volume)

    def set_dissipation_model(self, data, **kwargs):
        self._set_property("dissipation_model", data, **kwargs)

    def set_porous_material_model_data(self, data, **kwargs):
        self._set_property("porous_material_model", data, **kwargs)

    def get_fluid_density(self, fluid, **kwargs):
        rho_0 = fluid.fluid_density
        dissipation_model = self.get_dissipation_model(**kwargs)
        if dissipation_model is None:
            return rho_0
        elif dissipation_model["model"] == "proportional damping":
            factor = dissipation_model["fluid density factor"]
            return (1 + factor * 1j) * rho_0

    def get_speed_of_sound(self, fluid, **kwargs):
        c_0 = fluid.speed_of_sound
        dissipation_model = self.get_dissipation_model(**kwargs)
        if dissipation_model is None:
            return c_0
        elif dissipation_model["model"] == "proportional damping":
            factor = dissipation_model["speed of sound factor"]
            return (1 + factor * 1j) * c_0
        
    def get_lrf_model_inputs(self):
        pass

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

    def get_porous_material_model_data(self, volume):
        return self._get_property("porous_material_model", volume=volume)

    def _set_property(self, property: str, data: dict | Fluid | Material, node=None, element=None, line=None, surface=None, volume=None, group=None):
        """
        Sets a data to a property by node, element, line, surface or volume
        if any of these exists. Otherwise sets the property as global.

        """

        if isinstance(data, dict):

            tables_values = list()
            group_label = self.get_data_group_label(property)

            if "real_values" in data.keys() and "imag_values" in data.keys():
                for i, a in enumerate(data["real_values"]):
                    if a is None:
                        tables_values.append(None)
                    else:
                        b = data["imag_values"][i]
                        tables_values.append(a + 1j*b)

            if "table_names" in data.keys():

                if group_label == "acoustic":
                    imported_tables = self.acoustic_imported_tables
                else:
                    imported_tables = self.structural_imported_tables

                for i, table_name in enumerate(data["table_names"]):

                    if table_name is None:
                        tables_values.append(None)
                        continue

                    if table_name in imported_tables.keys():
                        data_array = imported_tables[table_name]
                        values = data_array[:, 1] + 1j*data_array[:, 2]
                        tables_values.append(values)

            data["values"] = tables_values

        if node is not None:
            self.nodal_properties[property, node] = data

        elif volume is not None:
            self.volume_properties[property, volume] = data

        elif surface is not None:
            self.surface_properties[property, surface] = data

        elif line is not None:
            self.line_properties[property, line] = data

        elif element is not None:
            self.element_properties[property, element] = data

        elif group is not None:
            self.group_properties[property, group] = data

        else:
            self.global_properties[property, "global"] = data

    def _get_property(self, property: str, node=None, element=None, line=None, surface=None, volume=None):
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
                    if "table_names" in data.keys():
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
                      self.group_properties,
                      self.global_properties
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

    def _remove_group_property(self, property: str, group_id: int):
        """Remove a group property at specific group_id."""
        key = (property, group_id)
        if key in self.group_properties.keys():
            self.group_properties.pop(key)

    def add_imported_tables(self, group_label: str, table_name: str, data: np.ndarray | list | tuple):
        """
        """
        if group_label == "acoustic":
            self.acoustic_imported_tables[table_name] = data
        elif group_label == "structural":
            self.structural_imported_tables[table_name] = data

    def remove_imported_tables(self, group_label: str, table_name: str):
        """
        """
        if group_label == "acoustic":
            if table_name in self.acoustic_imported_tables.keys():
                self.acoustic_imported_tables.pop(table_name)

        elif group_label == "structural":
            if table_name in self.structural_imported_tables.keys():
                self.structural_imported_tables.pop(table_name)

    def get_data_group_label(self, property : str):

        acoustic_labels = [ 
                            "acoustic_pressure",
                            "surface_velocity",
                            "mass_flow_rate",
                            "specific_impedance",
                            "radiation_impedance",
                            "reciprocating_compressor_excitation",
                            "reciprocating_pump_excitation",
                            "acoustic_transfer_element"
                           ]

        if property in acoustic_labels:
            return "acoustic"
        else:
            return "structural"

    def get_surface_related_table_names(self, property : str, surface_ids : int | list) -> list:
        """
        """
        table_names = list()
        if isinstance(surface_ids, int):
            test_key = (property, surface_ids)

        elif isinstance(surface_ids, list) and len(surface_ids) == 1:
            test_key = (property, surface_ids[0])

        elif isinstance(surface_ids, list) and len(surface_ids) == 2:
            test_key = (property, surface_ids[0], surface_ids[1])

        else:
            return table_names

        if test_key in self.surface_properties.keys():
            data = self.surface_properties[test_key]

            if "table_names" in data.keys():
                for table_name in data["table_names"]:
                    if table_name is not None:
                        table_names.append(table_name)

        return table_names

if __name__ == "__main__":
    p = ModelProperties()
    with open("teste.json", "w") as file:
        file.write(p.as_json())

    q = ModelProperties()
    with open("teste.json", "r") as file:
        data = json.load(file)
        q.load_json(data)
