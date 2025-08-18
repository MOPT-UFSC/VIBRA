from enum import Enum
import numpy as np
from molde.colors import color_names, Color
from molde.actors import CommonSymbolsActorVariableSize

from typing import Callable

from vibra import app
from vibra.interface.viewer_3d import sources

Triple = tuple[float, float, float]


class SymbolsActor(CommonSymbolsActorVariableSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_dict_property_name_to_build_function()
        self.configure_appearance()
        self.build()
        self.set_zbuffer_offsets(1, -6600)

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def _build_dict_property_name_to_build_function(self):
        self.prop_name_to_build_func = {
            "surface_velocity": self._build_surface_velocity,
            "prescribed_dofs": self._build_prescribed_dofs,
            "nodal_loads": self._build_nodal_loads,
            "distributed_loads": self._build_distributed_loads,
            "normal_pressure_load": self._build_normal_pressure_load,
            "specific_impedance": self._build_specific_impedance,
            "transfer_impedance": self._build_transfer_impedance,
            "mass_flow_rate": self._build_mass_flow_rate,
            "degrees_of_freedom_decoupling": self._build_dofs_decoupling,
            "absorption_surface": self._build_absorption_surface,
            "acoustic_pressure": self._build_acoustic_pressure,
            "reciprocating_compressor_excitation": self._build_reciprocating_compressor,
            "dissipation_model": self._build_dissipation_model,
            "acoustic_transfer_element_data": self._build_acoustic_transfer_element_data,
            "incident_plane_wave": self._build_incident_plane_wave,
            "mass_source": self._build_mass_source,
        }

    def _call_build_functions(self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1):
        # build a dict to map prop name to fun
        if property_name in self.prop_name_to_build_func.keys():
            self.prop_name_to_build_func[property_name](
                property_name=property_name, surface_id=surface_id, line_id=line_id, point_id=point_id
            )

    def build(self):
        self.clear_symbols()
        self._build_nodal_normals()

        point_properties = app().project.model.properties.point_properties
        for property_name, point_id in point_properties.keys():
            self._call_build_functions(property_name, point_id=point_id)

        line_properties = app().project.model.properties.line_properties
        for property_name, line_id in line_properties.keys():
            self._call_build_functions(property_name, line_id=line_id)

        surface_properties = app().project.model.properties.surface_properties
        for property_name, surface_id in surface_properties.keys():
            self._call_build_functions(property_name, surface_id=surface_id)

        super().build()

    def _get_center_coords_and_normals(self, surface_id: int) -> tuple[np.ndarray, np.ndarray]:
        mesh = app().project.model.mesh
        surface_nodes = mesh.nodes_from_surfaces.get(surface_id)
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
            return surface_coordinates[index, :], surface_normals[index, :]

        return center_coords, avg_normal

    def _get_center_coords_and_normals_line(self, line_id: int) -> tuple[np.ndarray, np.ndarray]:
        mesh = app().project.model.mesh
        line_nodes = mesh.nodes_from_lines.get(line_id)
        line_coordinates = mesh.nodal_coordinates[line_nodes, 1:]
        center_coords = np.average(line_coordinates, axis=0)
        dist = np.linalg.norm(line_coordinates - center_coords, axis=1)
        index = np.argmin(dist)

        # Returns the 3 points around the center (including it)
        return (line_coordinates[index - 1, :], line_coordinates[index, :], line_coordinates[index + 1, :])

    def _get_center_coords_and_normals_point(self, point_id: int) -> tuple[np.ndarray, np.ndarray]:
        mesh = app().project.model.mesh
        point_nodes = mesh.nodes_from_points.get(point_id)
        points_coordinates = mesh.nodal_coordinates[point_nodes, 1:]

        return points_coordinates

    def _build_surface_velocity(self, surface_id: int = -1, *args, **kwargs):
        # how to display this symbol without normal???
        if surface_id is None:
            return

        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_surface_velocity_source, coords, normal, color=color_names.RED_6)

    def _build_nodal_normals(self):
        mesh = app().project.model.mesh
        for node_id, normal_vector in mesh.nodal_normals_data.items():
            coords = mesh.nodal_coordinates[node_id, 1:]
            self.add_symbol(sources.create_outwards_arrow_source, coords, normal_vector, color=color_names.GRAY)

    def _build_prescribed_dofs(self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1):
        coords = None
        property = None

        if surface_id != -1:
            coords, _ = self._get_center_coords_and_normals(surface_id)
            surface_properties = app().project.model.properties.surface_properties
            property = surface_properties[property_name, surface_id]

        if line_id != -1:
            coords = self._get_center_coords_and_normals_line(line_id)[1]
            line_properties = app().project.model.properties.line_properties
            property = line_properties[property_name, line_id]

        if point_id != -1:
            coords = self._get_center_coords_and_normals_point(point_id)
            point_properties = app().project.model.properties.point_properties
            property = point_properties[property_name, point_id]

        if coords is not None and property is not None:
            x, y, z, *_ = property["values"]

            # handle table attributed values
            x = x[0] if isinstance(x, np.ndarray) else x
            y = y[0] if isinstance(y, np.ndarray) else y
            z = z[0] if isinstance(z, np.ndarray) else z

            # alternate add_symbol function to a generic one
            if x is not None:
                self.add_symbol(sources.create_cone_source, coords, (1, 0, 0), color=color_names.GREEN)

            if y is not None:
                self.add_symbol(sources.create_cone_source, coords, (0, 1, 0), color=color_names.GREEN)

            if z is not None:
                self.add_symbol(sources.create_cone_source, coords, (0, 0, 1), color=color_names.GREEN)

    def _build_nodal_loads(self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1):
        if surface_id != -1:
            surface_properties = app().project.model.properties.surface_properties
            property = surface_properties[property_name, surface_id]
            coords, normal = self._get_center_coords_and_normals(surface_id)

            Fx, Fy, Fz, Mx, My, Mz = [(i if i is not None else 0) for i in property["values"]]
            force_orientation = np.real((Fx, Fy, Fz))
            m_orientation = np.real((Mx, My, Mz))

            if np.any(force_orientation):
                is_pointing = np.dot(normal, force_orientation) < 0
                shape = sources.create_arrow_source if is_pointing else sources.create_outwards_arrow_source
                self.add_symbol(shape, coords, force_orientation, color=color_names.RED_2)
            if np.any(m_orientation):
                is_pointing = np.dot(normal, m_orientation) < 0
                shape = sources.create_double_arrow_source if is_pointing else sources.create_outwards_arrow_source
                self.add_symbol(shape, coords, m_orientation, color=color_names.BLUE_3)

        property = None
        coord = None

        if line_id != -1:
            coord = self._get_center_coords_and_normals_line(line_id)[1]
            line_properties = app().project.model.properties.line_properties
            property = line_properties[property_name, line_id]

        if point_id != -1:
            coord = self._get_center_coords_and_normals_point(point_id)
            point_properties = app().project.model.properties.point_properties
            property = point_properties[property_name, point_id]

        if property is not None and coord is not None:
            Fx, Fy, Fz, Mx, My, Mz = [(i if i is not None else 0) for i in property["values"]]
            force_orientation = np.real((Fx, Fy, Fz))
            m_orientation = np.real((Mx, My, Mz))

            if np.any(force_orientation):
                self.add_symbol(sources.create_arrow_source, coord, force_orientation, color=color_names.RED_2)
            if np.any(m_orientation):
                self.add_symbol(sources.create_double_arrow_source, coord, m_orientation, color=color_names.BLUE_3)

    def _build_distributed_loads(self, property_name: str, surface_id: int = -1, line_id: int = -1, *args, **kwargs):
        if surface_id != -1:
            surface_properties = app().project.model.properties.surface_properties
            property = surface_properties[property_name, surface_id]

            coords, normal = self._get_center_coords_and_normals(surface_id)
            x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]

            # handle table attributed values
            x = x[0] if isinstance(x, np.ndarray) else x
            y = y[0] if isinstance(y, np.ndarray) else y
            z = z[0] if isinstance(z, np.ndarray) else z

            orientation = np.real((x, y, z))
            is_pointing = np.dot(normal, orientation) < 0
            shape = (
                sources.create_quadruple_arrow_source if is_pointing else sources.create_outwards_triple_arrow_source
            )
            self.add_symbol(shape, coords, orientation, color=color_names.RED_2)

        if line_id != -1:
            line_properties = app().project.model.properties.line_properties
            property = line_properties[property_name, line_id]

            coords = self._get_center_coords_and_normals_line(line_id)
            x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]

            # handle table attributed values
            x = x[0] if isinstance(x, np.ndarray) else x
            y = y[0] if isinstance(y, np.ndarray) else y
            z = z[0] if isinstance(z, np.ndarray) else z

            orientation = np.real((x, y, z))
            self.add_symbol(sources.create_arrow_source, coords[0], orientation, color=color_names.RED_2)
            self.add_symbol(sources.create_arrow_source, coords[1], orientation, color=color_names.RED_2)
            self.add_symbol(sources.create_arrow_source, coords[2], orientation, color=color_names.RED_2)

    def _build_normal_pressure_load(self, property_name: str, surface_id: int = -1, *args, **kwargs):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]

        coords, normal = self._get_center_coords_and_normals(surface_id)
        x = property["values"][0]

        # handle table attributed values
        x = x[0] if isinstance(x, np.ndarray) else x

        shape = sources.create_outwards_normal_pressure_load if np.real(x) > 0 else sources.create_normal_pressure_load
        self.add_symbol(shape, coords, normal, color=color_names.RED_2)

    def _build_specific_impedance(self, property_name: str, surface_id: int = -1, *args, **kwargs):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]

        coords, normal = self._get_center_coords_and_normals(surface_id)
        shape = (
            sources.create_anechoic_termination_source
            if "anechoic_termination" in property.keys()
            else sources.create_impedance_source
        )
        self.add_symbol(shape, coords, normal, color=color_names.PURPLE_2)

    def _build_transfer_impedance(self, surface_id: int = -1, *args, **kwargs):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_transfer_impedance_source, coords, normal, color=color_names.PURPLE_2)

    def _build_perforated_plate_model(self, surface_id: int = -1, *args, **kwargs):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_perforated_plate_source, coords, normal, color=color_names.RED)

    def _build_mass_flow_rate(self, surface_id: int = -1, *args, **kwargs):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_mass_flow_rate_source, coords, normal, color=color_names.PINK)

    def _build_dofs_decoupling(self, surface_id: int = -1, *args, **kwargs):
        surface_properties = app().project.model.properties.surface_properties
        if ("perforated_plate_model", surface_id) in surface_properties.keys():
            return
        if ("transfer_impedance", surface_id) in surface_properties.keys():
            return

        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_degrees_of_freedom_decoupling_source, coords, normal, color=color_names.GREEN)

    def _build_absorption_surface(self, surface_id: int = -1, *args, **kwargs):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_absorption_surface_source, coords, normal, color=color_names.GREEN)

    def _build_acoustic_pressure(self, surface_id: int = -1, *args, **kwargs):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_acoustic_pressure_source, coords, normal, color=color_names.RED_2)

    def _build_reciprocating_compressor(self, property_name: str, surface_id: int = -1, *args, **kwargs):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]

        color = None
        if property["connection_type"] == "discharge":
            shape = sources.create_compressor_discharge_source
            # vermelho, seta entra é azul
            color = color_names.RED_3
        elif property["connection_type"] == "suction":
            shape = sources.create_compressor_suction_source
            color = color_names.BLUE_3

        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(shape, coords, normal, color=color)

    def _build_dissipation_model(self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_dissipation_model_source, coords, normal, color=color_names.BLUE)

    def _build_viscous_thermal_loss_model(
        self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1
    ):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_dissipation_model_source, coords, normal, color=color_names.ORANGE)

    def _build_acoustic_transfer_element_data(
        self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1
    ):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(
            sources.create_acoustic_transfer_element_data_source, coords, normal, color=color_names.TURQUOISE
        )

    def _build_incident_plane_wave(
        self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1
    ):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]

        wave_vector = property.get("wave_vector")
        coords, _ = self._get_center_coords_and_normals(surface_id)

        self.add_symbol(sources.create_incident_plane_wave_source, coords, wave_vector, color=color_names.BLUE)

    def _build_mass_source(self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1):
        orientation = (0, 0, 0)

        if surface_id != -1:
            coords, _ = self._get_center_coords_and_normals(surface_id)
        if line_id != -1:
            coords = self._get_center_coords_and_normals_line(line_id)[1]
        if point_id != -1:
            coords = self._get_center_coords_and_normals_point(point_id)

        color_fir_sphere = color_names.RED.copy()
        self.add_symbol(sources.create_mass_load_first_layer_source, coords, orientation, color=color_fir_sphere)

        color_sec_sphere = color_names.YELLOW.with_rgba(a=150)
        self.add_symbol(sources.create_mass_load_second_layer_source, coords, orientation, color=color_sec_sphere)

        color_third_sphere = color_names.GREEN.with_rgba(a=100)
        self.add_symbol(sources.create_mass_load_third_layer_source, coords, orientation, color=color_third_sphere)

        color_fourth_sphere = color_names.BLUE.with_rgba(a=50)
        self.add_symbol(sources.create_mass_load_fourth_layer_source, coords, orientation, color=color_fourth_sphere)
