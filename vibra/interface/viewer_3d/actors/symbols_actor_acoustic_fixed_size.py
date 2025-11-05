import numpy as np
from molde.colors import color_names
from molde.actors import CommonSymbolsActorFixedSize

from vibra import app
from vibra.interface.viewer_3d import sources


class SymbolsActorAcousticFixedSize(CommonSymbolsActorFixedSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_dict_property_name_to_build_function()
        self.configure_appearance()
        self.build()
        # self.set_zbuffer_offsets(1, -6600)

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def _build_dict_property_name_to_build_function(self):
        self.prop_name_to_build_func = {
            "reciprocating_compressor_excitation": self._build_reciprocating_compressor_excitation_symbol,
            "compressor_excitation_waveform": self._build_compressor_excitation_waveform_symbol,
        }

    def _call_build_functions(self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1, node_id: int = -1):
        if property_name in self.prop_name_to_build_func.keys():
            self.prop_name_to_build_func[property_name](
                property_name=property_name,
                surface_id=surface_id,
                line_id=line_id,
                point_id=point_id,
                node_id=node_id                                                                                 
            )

    def build(self):
        self.clear_symbols()
        
        surface_properties = app().project.model.properties.surface_properties
        for property_name, surface_id in surface_properties.keys():
            self._call_build_functions(property_name, surface_id=surface_id)

        super().build()

    def _get_center_coords_and_normals(self, surface_id: int) -> tuple[np.ndarray, np.ndarray]:
        mesh = app().project.model.mesh
        surface_nodes = mesh.get_nodes_from_surface(surface_id)
        surface_coordinates = mesh.nodal_coordinates[surface_nodes, 1:]

        surface_normals = mesh.normals_surface.get(surface_id)
        if surface_normals is None:
            eface_normals = mesh.get_stacked_normals_for_surface_elements(surface_id)
            avg_normal = np.average(eface_normals, axis=0).flatten()

        else:
            avg_normal = np.average(surface_normals, axis=0).round(6)

        curvatures_surface = mesh.curvatures_surface.get(surface_id)
        contains_curvature = (curvatures_surface is not None) and np.any(curvatures_surface)
        center_coords = np.average(surface_coordinates, axis=0)

        if contains_curvature:
            # Finds the node that is closest to the center coords
            dist = np.linalg.norm(surface_coordinates - center_coords, axis=1)
            index = np.argmin(dist)
            index_max = np.argmax(dist)
            return surface_coordinates[index, :], surface_normals[index, :], dist[index_max]

        dist = np.linalg.norm(surface_coordinates - center_coords, axis=1)
        index = np.argmax(dist)

        return center_coords, avg_normal, dist[index]

    def _build_reciprocating_compressor_excitation_symbol(self, property_name: str, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]

        shape = None
        color = None
        letter_color = None
        if property["connection_type"] == "discharge":
            shape = sources.create_compressor_discharge_source
            # vermelho, seta entra é azul
            color = color_names.RED_3
            letter_color = color_names.RED_1

        elif property["connection_type"] == "suction":
            shape = sources.create_compressor_suction_source
            color = color_names.BLUE_3
            letter_color = color_names.BLUE_1

        coords, normal, max_dist = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(shape, coords, normal, color=color, scale=1.985 * max_dist)
        self.add_symbol(sources.create_compressor_r_reciprocating_source, coords, normal, color=letter_color, scale=1.985 * max_dist)
    
    def _build_compressor_excitation_waveform_symbol(self, property_name: str, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]

        shape = None
        color = None
        compressor_type_shape = None
        letter_color = None
        if property["connection_type"] == "discharge":
            shape = sources.create_compressor_discharge_source
            color = color_names.RED_3
            letter_color = color_names.RED_1

        else: # elif property["connection_type"] == "suction":
            shape = sources.create_compressor_suction_source
            color = color_names.BLUE_3
            letter_color = color_names.BLUE_1
            
        # draw a letter on the compressor
        if property["compressor_type"] == "screw":
            compressor_type_shape = sources.create_compressor_s_screw_source
        else:
            compressor_type_shape = sources.create_compressor_r_reciprocating_source
            
        coords, normal, max_dist = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(shape, coords, normal, color=color, scale=1.985 * max_dist)
        self.add_symbol(sources.create_compressor_f_frequency_source, coords, normal, color=letter_color, scale=1.985 * max_dist)
        self.add_symbol(compressor_type_shape, coords, normal, color=letter_color, scale=1.985 * max_dist)
    
    def _build_compressor_excitation_spectrum_symbol(self, property_name: str, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]

        shape = None
        color = None
        compressor_type_shape = None
        letter_color = None
        if property["connection_type"] == "discharge":
            shape = sources.create_compressor_discharge_source
            color = color_names.RED_3
            letter_color = color_names.RED_1

        else: # elif property["connection_type"] == "suction":
            shape = sources.create_compressor_suction_source
            color = color_names.BLUE_3
            letter_color = color_names.BLUE_1
        
        # draw a letter on the compressor
        if property["compressor_type"] == "screw":
            compressor_type_shape = sources.create_compressor_s_screw_source
        else:
            compressor_type_shape = sources.create_compressor_r_reciprocating_source

        coords, normal, max_dist = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(shape, coords, normal, color=color, scale=1.985 * max_dist)
        self.add_symbol(sources.create_compressor_t_time_source, coords, normal, color=letter_color, scale=1.985 * max_dist)
        self.add_symbol(compressor_type_shape, coords, normal, color=letter_color, scale=1.985 * max_dist)