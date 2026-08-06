from collections import defaultdict

import numpy as np
from molde.actors import CommonSymbolsActorVariableSize
from molde.colors import color_names

from vibra import app
from vibra.interface.viewer_3d import sources
from vibra.interface.viewer_3d.actors.symbols_positioner import SymbolsPositioner


class SymbolsActorAcoustic(CommonSymbolsActorVariableSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._surface_symbols_positioner: SymbolsPositioner | None = None

        self._build_dict_property_name_to_build_function()
        self.configure_appearance()
        self.build()
        self.set_zbuffer_offsets(1, -6600)
        # as the symbols do not change size when zooming, this is needed for reset_camera to work properly
        self.UseBoundsOff()

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def _build_dict_property_name_to_build_function(self):
        self.prop_name_to_build_func = {
            "surface_velocity": self._build_surface_velocity,
            "specific_impedance": self._build_specific_impedance,
            "transfer_impedance": self._build_transfer_impedance,
            "degrees_of_freedom_decoupling": self._build_dof_decoupling,
            "absorption_surface": self._build_absorption_surface,
            "acoustic_pressure": self._build_acoustic_pressure,
            "proportional_damping": self._build_proportional_damping,
            "acoustic_transfer_element_data": self._build_acoustic_transfer_element_data,
            "incident_plane_wave": self._build_incident_plane_wave,
            "mass_source": self._build_mass_source,
        }

    def _call_build_functions(self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1, node_id: int = -1):
        if property_name in self.prop_name_to_build_func.keys():
            self.prop_name_to_build_func[property_name](
                property_name=property_name, surface_id=surface_id, line_id=line_id, point_id=point_id, node_id=node_id
            )

    def build(self):
        self.clear_symbols()
        self._build_nodal_normals()
        self._build_element_normals()

        point_properties = app().project.model.properties.point_properties
        for property_name, point_id in point_properties.keys():
            if property_name in self.prop_name_to_build_func.keys():
                self._call_build_functions(property_name, point_id=point_id)

        line_properties = app().project.model.properties.line_properties
        for property_name, line_id in line_properties.keys():
            if property_name in self.prop_name_to_build_func.keys():
                self._call_build_functions(property_name, line_id=line_id)

        nodal_properties = app().project.model.properties.nodal_properties
        for property_name, node_id in nodal_properties.keys():
            if property_name in self.prop_name_to_build_func.keys():
                self._call_build_functions(property_name, node_id=node_id)

        surface_properties = app().project.model.properties.surface_properties
        dict_surface_id_total_symbols = self._count_symbols_foreach_surface(surface_properties)
        self._surface_symbols_positioner = SymbolsPositioner(app().project.model.mesh)
        self._surface_symbols_positioner.reset_count(dict_surface_id_total_symbols)

        for property_name, surface_id in surface_properties.keys():
            self._call_build_functions(property_name, surface_id=surface_id)

        super().build()

    def _count_symbols_foreach_surface(self, surface_properties: dict) -> dict[int, int]:
        surface_symbol_totals: dict[int, int] = defaultdict(int)
        for property_name, surface_id in surface_properties.keys():
            if property_name not in self.prop_name_to_build_func.keys():
                continue

            if property_name == "degrees_of_freedom_decoupling":
                if ("perforated_plate_model", surface_id) in surface_properties.keys():
                    continue
                if ("transfer_impedance", surface_id) in surface_properties.keys():
                    continue

            surface_symbol_totals[surface_id] += 1

        return surface_symbol_totals

    def _get_symbol_coords_and_normal(self, surface_id: int) -> tuple[np.ndarray, np.ndarray]:
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
        contains_curvature = (curvatures_surface is not None) and (np.average(curvatures_surface) > 1e-4)

        target_coords = mesh.get_geometric_surface_center(surface_id)

        if target_coords is None:
            target_coords = np.average(surface_coordinates, axis=0)

        if self._surface_symbols_positioner is not None:
            # avoids overlapping symbols
            target_coords = self._surface_symbols_positioner.next_surface_position(surface_id, target_coords, avg_normal, surface_coordinates)

        if contains_curvature and surface_normals is not None:
            # Finds the node that is closest to the center coords
            dist = np.linalg.norm(surface_coordinates - target_coords, axis=1)
            index = np.argmin(dist)
            target_coords, avg_normal = surface_coordinates[index, :], surface_normals[index, :]

        return target_coords, avg_normal

    def _get_center_coords_from_line(self, line_id: int) -> tuple[np.ndarray, np.ndarray]:
        mesh = app().project.model.mesh
        nodes = mesh.get_nodes_from_line(line_id)
        line_coordinates = mesh.nodal_coordinates[nodes, 1:]
        center_coords = np.average(line_coordinates, axis=0)
        dist = np.linalg.norm(line_coordinates - center_coords, axis=1)
        index = np.argmin(dist)

        # Returns the 3 points around the center (including it)
        return (line_coordinates[index - 1, :], line_coordinates[index, :], line_coordinates[index + 1, :])

    def _get_coords_from_point(self, point_id: int) -> tuple[np.ndarray, np.ndarray]:
        mesh = app().project.model.mesh
        point_nodes = mesh.nodes_from_points.get(point_id)
        points_coordinates = mesh.nodal_coordinates[point_nodes, 1:]

        return points_coordinates

    def _get_coords_from_node(self, node_id: int):
        mesh = app().project.model.mesh
        node = mesh.nodal_coordinates[node_id]
        return node

    def _build_nodal_normals(self):
        if not app().main_window.results_widget.visualization_filter.nodal_normal_symbols:
            return

        mesh = app().project.model.mesh
        for (_, node_id), normal_vector in mesh.nodal_normals_data.items():
            coords = mesh.nodal_coordinates[node_id, 1:]
            self.add_symbol(sources.create_outwards_arrow_source, coords, normal_vector, color=color_names.GRAY)

    def _build_element_normals(self):
        if not app().main_window.results_widget.visualization_filter.element_normal_symbols:
            return

        mesh = app().project.model.mesh
        for normal, centers in mesh.element_normals_data.values():
            center = np.average(centers, axis=0).flatten()
            self.add_symbol(
                sources.create_outwards_arrow_source,
                center,
                normal,
                color=color_names.GRAY,
            )

    def _build_surface_velocity(self, surface_id: int = -1, *args, **kwargs):
        # how to display this symbol without normal???
        if surface_id is None or surface_id == -1:
            return

        coords, normal = self._get_symbol_coords_and_normal(surface_id)
        self.add_symbol(sources.create_surface_velocity_source, coords, normal, color=color_names.RED_6)

    def _build_specific_impedance(self, property_name: str, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]

        coords, normal = self._get_symbol_coords_and_normal(surface_id)
        shape = sources.create_anechoic_termination_source if "anechoic_termination" in property.keys() else sources.create_impedance_source
        self.add_symbol(shape, coords, normal, color=color_names.PURPLE_2)

    def _build_transfer_impedance(self, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        coords, normal = self._get_symbol_coords_and_normal(surface_id)
        self.add_symbol(sources.create_transfer_impedance_source, coords, normal, color=color_names.PURPLE_2)

    def _build_perforated_plate_model(self, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        coords, normal = self._get_symbol_coords_and_normal(surface_id)
        self.add_symbol(sources.create_perforated_plate_source, coords, normal, color=color_names.RED)

    def _build_mass_flow_rate(self, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        coords, normal = self._get_symbol_coords_and_normal(surface_id)
        self.add_symbol(sources.create_mass_flow_rate_source, coords, normal, color=color_names.PINK)

    def _build_dof_decoupling(self, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        surface_properties = app().project.model.properties.surface_properties
        if ("perforated_plate_model", surface_id) in surface_properties.keys():
            return
        if ("transfer_impedance", surface_id) in surface_properties.keys():
            return

        coords, normal = self._get_symbol_coords_and_normal(surface_id)
        self.add_symbol(sources.create_degrees_of_freedom_decoupling_source, coords, normal, color=color_names.GREEN)

    def _build_absorption_surface(self, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        coords, normal = self._get_symbol_coords_and_normal(surface_id)
        self.add_symbol(sources.create_absorption_surface_source, coords, normal, color=color_names.GREEN)

    def _build_acoustic_pressure(self, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        coords, normal = self._get_symbol_coords_and_normal(surface_id)
        self.add_symbol(sources.create_acoustic_pressure_source, coords, normal, color=color_names.RED_2)

    def _build_proportional_damping(self, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        coords, normal = self._get_symbol_coords_and_normal(surface_id)
        self.add_symbol(sources.create_dissipation_model_source, coords, normal, color=color_names.BLUE)

    def _build_viscous_thermal_loss_model(self, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        coords, normal = self._get_symbol_coords_and_normal(surface_id)
        self.add_symbol(sources.create_dissipation_model_source, coords, normal, color=color_names.ORANGE)

    def _build_acoustic_transfer_element_data(self, surface_id: int = -1):
        if surface_id == -1:
            return

        coords, normal = self._get_symbol_coords_and_normal(surface_id)
        self.add_symbol(sources.create_acoustic_transfer_element_data_source, coords, normal, color=color_names.TURQUOISE)

    def _build_incident_plane_wave(self, property_name: str, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return

        prop_data = app().project.model.properties._get_property(property_name, surface=surface_id)
        if not isinstance(prop_data, dict):
            return

        ipw_vector = prop_data.get("ipw_vector")
        coords, _ = self._get_symbol_coords_and_normal(surface_id)

        self.add_symbol(sources.create_incident_plane_wave_source, coords, ipw_vector, color=color_names.BLUE)

    def _build_mass_source(self, surface_id: int = -1, line_id: int = -1, point_id: int = -1, node_id: int = -1, *args, **kwargs):
        orientation = (0, 0, 0)

        if surface_id != -1:
            coords, _ = self._get_symbol_coords_and_normal(surface_id)

        if line_id != -1:
            coords = self._get_center_coords_from_line(line_id)[1]

        if point_id != -1:
            coords = self._get_coords_from_point(point_id)

        if node_id != -1:
            coords = self._get_coords_from_node(node_id)[1:]

        color_fir_sphere = color_names.RED.copy()
        self.add_symbol(sources.create_mass_load_first_layer_source, coords, orientation, color=color_fir_sphere)

        color_sec_sphere = color_names.YELLOW.with_rgba(a=150)
        self.add_symbol(sources.create_mass_load_second_layer_source, coords, orientation, color=color_sec_sphere)

        color_third_sphere = color_names.GREEN.with_rgba(a=100)
        self.add_symbol(sources.create_mass_load_third_layer_source, coords, orientation, color=color_third_sphere)

        color_fourth_sphere = color_names.BLUE.with_rgba(a=50)
        self.add_symbol(sources.create_mass_load_fourth_layer_source, coords, orientation, color=color_fourth_sphere)
