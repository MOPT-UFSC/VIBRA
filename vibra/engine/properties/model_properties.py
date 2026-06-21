import json
from typing import Callable, Optional

import numpy as np

from vibra.engine.properties import FluidLibrary, MaterialLibrary
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material

DEFAULT_MATERIAL = Material(
    name="Steel",
    identifier=1,
    color=(200, 200, 200),
    material_density=7860,
    elasticity_modulus=210e9,
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

    def __init__(self, disable_resume_callback: Optional[Callable] = None):
        self.disable_resume_callback = disable_resume_callback
        self._reset_variables()
    
    def _reset_variables(self):
        self.material_library = MaterialLibrary.default()
        self.fluid_library = FluidLibrary.default()

        self.acoustic_imported_tables = dict()
        self.structural_imported_tables = dict()

        self.global_properties = dict()
        self.group_properties = dict()
        self.volume_properties = dict()
        self.surface_properties = dict()
        self.line_properties = dict()
        self.point_properties = dict()
        self.element_properties = dict()
        self.nodal_properties = dict()

        # self.global_properties["material", "global"] = DEFAULT_MATERIAL
        # self.global_properties["fluid", "global"] = DEFAULT_FLUID

    def get_fluid_density(self, fluid: Fluid, proportional_damping: dict | None) -> float | complex:
        rho_0 = fluid.fluid_density
        if proportional_damping is None:
            return rho_0

        factor = proportional_damping.get("fluid_density_factor", 0)
        return (1 + factor * 1j) * rho_0

    def get_speed_of_sound(self, fluid: Fluid, proportional_damping: dict | None) -> float | complex:
        c_0 = fluid.speed_of_sound
        if proportional_damping is None:
            return c_0

        factor = proportional_damping.get("speed_of_sound_factor", 0)
        return (1 + factor * 1j) * c_0

    def _set_property(
        self,
        property: str,
        data: dict | Fluid | Material,
        node: int | None = None,
        element: int | None = None,
        point: int | None = None,
        line: int | None = None,
        surface: int | tuple[int] | None = None,
        volume: int | None = None,
        group: int | None = None,
    ):
        """
        This method sets a data to a property by node, element, line, surface or volume
        if any of these exists. Otherwise sets the property as global.

        """
        if isinstance(data, dict):

            values_list = list()
            group_label = self.get_data_group_label(property)

            if "real_values" in data.keys() and "imag_values" in data.keys():
                for i, a in enumerate(data["real_values"]):

                    if a is None:
                        values_list.append(None)

                    else:
                        b = data["imag_values"][i]  
                        if b is None:
                            values_list.append(a)
                        else:
                            values_list.append(a + 1j*b)

            elif "table_names" in data.keys():
                if group_label == "acoustic":
                    imported_tables = self.acoustic_imported_tables
                else:
                    imported_tables = self.structural_imported_tables

                frequencies_list = list()
                for i, table_name in enumerate(data["table_names"]):
                    if table_name is None:
                        values_list.append(None)
                        continue

                    if table_name in imported_tables.keys():
                        data_array = imported_tables[table_name]

                        table_frequencies = [float(freq) for freq in data_array[:, 0]]
                        frequencies_list.append(table_frequencies)

                        if data_array.shape[1] >= 3:
                            values = data_array[:, 1] + 1j * data_array[:, 2]
                        else:
                            values = data_array[:, 1]

                        values_list.append(values)

                data["tables_frequencies"] = frequencies_list

            elif "values" in data.keys():
                values_list = data["values"]

            data["values"] =  values_list

        elif isinstance(data, Material) and (data not in self.material_library):
            self.material_library.add(data)

        elif isinstance(data, Fluid) and (data not in self.fluid_library):
            self.fluid_library.add(data)

        if node is not None:
            self.nodal_properties[property, node] = data

        elif volume is not None:
            self.volume_properties[property, volume] = data

        elif surface is not None:
            self.surface_properties[property, surface] = data

        elif line is not None:
            self.line_properties[property, line] = data

        elif point is not None:
            self.point_properties[property, point] = data

        elif element is not None:
            self.element_properties[property, element] = data

        elif group is not None:
            self.group_properties[property, group] = data

        else:
            self.global_properties[property, "global"] = data

        if self.disable_resume_callback is not None:
            self.disable_resume_callback()

    def _get_property(self, property: str, node=None, element=None, point=None, line=None, surface=None, volume=None):
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

        if (property, point) in self.point_properties:
            return self.point_properties[property, point]

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
            self.point_properties,
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
                      self.volume_properties,
                      self.surface_properties,
                      self.line_properties,
                      self.point_properties,
                      self.group_properties,
                      self.global_properties,
                      self.nodal_properties,
                      self.element_properties,
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

        if self.disable_resume_callback is not None:
            self.disable_resume_callback()

    def remove_material(self, material: Material):
        self.material_library.pop(material)
        to_remove = list()
        for entity_name, property_name, tags, prop_data in self.iterate_properties():
            if prop_data == material:
                to_remove.append((entity_name, tags))

        for entity_name, tags in to_remove:
            match entity_name:
                case "volume":
                    self._remove_volume_property("material", tags)
                case "surface":
                    self._remove_surface_property("material", tags)

    def remove_fluid(self, fluid: Fluid):
        self.fluid_library.pop(fluid)
        to_remove = list()
        for entity_name, property_name, tags, prop_data in self.iterate_properties():
            if prop_data == fluid:
                to_remove.append((entity_name, tags))

        for entity_name, tags in to_remove:
            match entity_name:
                case "volume":
                    self._remove_volume_property("fluid", tags)
                case "surface":
                    self._remove_surface_property("fluid", tags)

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

    def _remove_point_property(self, property: str, point_id: int):
        """Remove a point property at specific point_id."""
        key = (property, point_id)
        if key in self.point_properties.keys():
            self.point_properties.pop(key)

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

    def remove_table_files_from_point(self, point_id: int, property_name: str):
        table_names = self.get_property_related_table_names(property_name, point_id, "points")
        self._remove_table_files(table_names)

    def remove_table_files_from_line(self, line_id: int, property_name: str):
        table_names = self.get_property_related_table_names(property_name, line_id, "lines")
        self._remove_table_files(table_names)

    def remove_table_files_from_surface(self, surface_id: int, property_name: str):
        table_names = self.get_property_related_table_names(property_name, surface_id, "surfaces")
        self._remove_table_files(table_names)

    def remove_table_files_from_volume(self, volume_id: int, property_name: str):
        table_names = self.get_property_related_table_names(property_name, volume_id, "volumes")
        self._remove_table_files(table_names)

    def _remove_table_files(self, table_names: list):
        for table_name in table_names:
            self.remove_imported_tables("", table_name)

    # TODO: group_label argument is used on calls across the program. Need to remove later
    def remove_imported_tables(self, group_label: str, table_name: str):
        #TODO: is it possible both have the same table_names? I am counting with this, need to check for problems
        if table_name in self.acoustic_imported_tables.keys():
            self.acoustic_imported_tables.pop(table_name)

        if table_name in self.structural_imported_tables.keys():
            self.structural_imported_tables.pop(table_name)

    def get_data_group_label(self, property : str) -> str:

        acoustic_labels = [ 
                           "acoustic_pressure",
                           "surface_velocity",
                           "incident_plane_wave",
                           "specific_impedance",
                           "transfer_impedance",
                           "absorption_surface",
                           "perforated_plate_model",
                           "compressor_excitation_spectrum",
                           "compressor_excitation_waveform",
                           "reciprocating_compressor_excitation",
                           "acoustic_transfer_element",
                            "porous_material_model",
                           "mass_source",
                           ]

        structural_labels = [
                            "surface_thickness",
                            "prescribed_dof",
                            "nodal_loads", 
                            "distributed_loads", 
                            "normal_pressure_load",
                            ]

        if property in acoustic_labels:
            return "acoustic"
        elif property in structural_labels:
            return "structural"
        else:
            return "general"

    def get_property_related_table_names(self, property : str, selected_ids : int | list | tuple, selection: str) -> list:
        """
        """
        table_names = list()
        if isinstance(selected_ids, int):
            test_key = (property, selected_ids)
        elif isinstance(selected_ids, list) and len(selected_ids) == 1:
            test_key = (property, selected_ids[0])
        elif isinstance(selected_ids, list) and len(selected_ids) == 2:
            test_key = (property, selected_ids[0], selected_ids[1])
        elif isinstance(selected_ids, tuple) and len(selected_ids) == 2:
            test_key = (property, selected_ids)
        else:
            return table_names

        if selection == "surfaces":
            _properties = self.surface_properties
        elif selection == "lines":
            _properties = self.line_properties
        elif selection == "points":
            _properties = self.point_properties
        elif selection == "nodes":
            _properties = self.nodal_properties
        else:
            return table_names

        data = _properties.get(test_key)
        if isinstance(data, dict):
            if "table_names" in data.keys():
                for table_name in data["table_names"]:
                    if table_name is not None:
                        table_names.append(table_name)

        return table_names
    
    def process_all_tables_frequencies_vectors(self) -> list:
        """
        This method process the frequencies vectors from all imported tables.
        """

        frequencies_from_tables = list()

        for _, _, _, prop_data in self.iterate_properties():

            if not isinstance(prop_data, dict):
                continue

            tables_frequencies = prop_data.get("tables_frequencies")
            if tables_frequencies is None:
                continue

            if not isinstance(tables_frequencies, list):
                continue

            for frequencies in tables_frequencies:
                if frequencies in frequencies_from_tables:
                    continue

                frequencies_from_tables.append(frequencies)

        return frequencies_from_tables

    def is_the_volume_property_present_in_the_model(self, property_to_check: str):

        for (property, _) in self.volume_properties.keys():
            if property == property_to_check:
                return True

        return False

    def is_the_surface_property_present_in_the_model(self, property_to_check: str):

        for (property, _) in self.surface_properties.keys():
            if property == property_to_check:
                return True

        return False
    
    def is_there_a_prescribed_velocity_or_acceleration_in_the_model(self) -> bool:
        for _, property_name, _, data in self.iterate_properties():
            if property_name != "prescribed_dof":
                continue

            if isinstance(data, dict):
                if data.get("integrate"):
                    return True
        
        return False
    
    def get_entities_without_property(self, property: str, **kwargs):

        entities_without_property = list()
        volume_ids = kwargs.get("volumes", list())
        surface_ids = kwargs.get("surfaces", list())

        if volume_ids:
            for volume_id in volume_ids:
                data = self._get_property(property, volume=volume_id)
                if data is None:
                    entities_without_property.append(volume_id)

        elif surface_ids:
            for surface_id in kwargs.get("surfaces", list()):
                data = self._get_property(property, surface=surface_id)
                if data is None:
                    entities_without_property.append(surface_id)
    
        return entities_without_property
    
    def iterate_properties(self):
        property_dicts = {
            "global": self.global_properties,
            "group": self.group_properties,
            "volume": self.volume_properties,
            "surface": self.surface_properties,
            "line": self.line_properties,
            "point": self.point_properties,
            "element": self.element_properties,
            "node": self.nodal_properties,
        }

        for entity_name, property_dict in property_dicts.items():
            for key, value in property_dict.items():
                property_name, tags = key
                yield entity_name, property_name, tags, value

    def get_properties_from_points(self, point_ids: set[int]) -> list[tuple[str, int]]:
        return self._get_properties_from_entities(point_ids, self.point_properties)
    
    def get_properties_from_lines(self, line_ids: set[int]) -> list[tuple[str, int]]:
        return self._get_properties_from_entities(line_ids, self.line_properties)

    def get_properties_from_surfaces(self, surface_ids: set[int]) -> list[tuple[str, int]]:
        return self._get_properties_from_entities(surface_ids, self.surface_properties)

    def get_properties_from_volumes(self, volume_ids: set[int]) -> list[tuple[str, int]]:
        return self._get_properties_from_entities(volume_ids, self.volume_properties)

    def _get_properties_from_entities(self, entity_ids: set[int], entity_properties: dict) -> list[tuple[str, int]]:
        properties_found: list[tuple[str, int]] = list()

        for property_name, entity_id in entity_properties.keys():
            if entity_id in entity_ids:
                properties_found.append((property_name, entity_id))
        
        return properties_found

if __name__ == "__main__":
    p = ModelProperties()
    with open("teste.json", "w") as file:
        file.write(p.as_json())

    q = ModelProperties()
    with open("teste.json", "r") as file:
        data = json.load(file)
        q.load_json(data)
