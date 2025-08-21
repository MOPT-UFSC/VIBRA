from enum import Enum
import numpy as np
from molde.colors import color_names, Color
from molde.actors import CommonSymbolsActorVariableSize

from typing import Callable

from vibra import app
from vibra.interface.viewer_3d import sources

Triple = tuple[float, float, float]


class SymbolsActorStructural(CommonSymbolsActorVariableSize):
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
            "prescribed_dofs": self._build_prescribed_dofs,
            "nodal_loads": self._build_nodal_loads,
            "distributed_loads": self._build_distributed_loads,
            "normal_pressure_load": self._build_normal_pressure_load,
        }

    def _call_build_functions(self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1):
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
            U_R = [(i if i is not None else 0) for i in property["values"]]

            # handle table attributed values
            for index, i in enumerate(U_R):
                U_R[index] = i[0] if isinstance(i, np.ndarray) else i

            # alternate add_symbol function to a generic one
            for index, v in enumerate(U_R):
                if index < 3 and v != 0:
                    self.add_symbol(sources.create_cone_source, coords, (index==0, index==1, index==2), color=color_names.GREEN)
                elif index >= 3 and v != 0:
                    self.add_symbol(sources.create_double_cone_source, coords, (index==3, index==4, index==5), color=color_names.RED_5)    

    def _build_nodal_loads(self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1):
        if surface_id != -1:
            surface_properties = app().project.model.properties.surface_properties
            property = surface_properties[property_name, surface_id]
            coords, _ = self._get_center_coords_and_normals(surface_id)
            
            F_M = [(i if i is not None else 0) for i in property["values"]]
            if len(F_M) == 3:
                Fx, Fy, Fz = F_M
                Mx, My, Mz = 0, 0, 0
            else:
                Fx, Fy, Fz, Mx, My, Mz = F_M

            force_orientation = np.real((Fx, Fy, Fz))
            m_orientation = np.real((Mx, My, Mz))

            if np.any(force_orientation):
                self.add_symbol(sources.create_arrow_source, coords, force_orientation, color=color_names.RED_2)
            if np.any(m_orientation):
                self.add_symbol(sources.create_double_arrow_source, coords, m_orientation, color=color_names.BLUE_5)

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
            F_M = [(i if i is not None else 0) for i in property["values"]]
            if len(F_M) == 3:
                Fx, Fy, Fz = F_M
                Mx, My, Mz = 0, 0, 0
            else:
                Fx, Fy, Fz, Mx, My, Mz = F_M
                
            force_orientation = np.real((Fx, Fy, Fz))
            m_orientation = np.real((Mx, My, Mz))

            if np.any(force_orientation):
                self.add_symbol(sources.create_arrow_source, coord, force_orientation, color=color_names.RED_2)
            if np.any(m_orientation):
                self.add_symbol(sources.create_double_arrow_source, coord, m_orientation, color=color_names.BLUE_5)

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
        if surface_id == -1:
            return
        
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]

        coords, normal = self._get_center_coords_and_normals(surface_id)
        x = property["values"][0]

        # handle table attributed values
        x = x[0] if isinstance(x, np.ndarray) else x

        shape = sources.create_outwards_normal_pressure_load if np.real(x) > 0 else sources.create_normal_pressure_load
        self.add_symbol(shape, coords, normal, color=color_names.RED_2)