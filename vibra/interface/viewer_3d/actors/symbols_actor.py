import numpy as np
from molde.colors import color_names
from molde.actors import CommonSymbolsActorVariableSize

from vibra import app
from vibra.interface.viewer_3d.sources import (
    create_arrow_source,
    create_cone_source,
    create_cube_source,
    create_damper_source,
    create_double_arrow_source,
    create_long_arrow_source,
    create_mass_source,
    create_outwards_arrow_source,
    create_spring_source,
    create_perforated_plate_source,
    create_impedance_source,
    create_mass_flow_rate_source,
    create_triple_arrow_source,
    create_outwards_triple_arrow_source,
    create_normal_pressure_load,
    create_dofs_decpupling_source,
    create_absorption_surface_source,
)

class SymbolsActor(CommonSymbolsActorVariableSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_appearance()
        self._register_shapes()
        self.build()
        self.set_zbuffer_offsets(1, -6600)

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def build(self):
        self.clear_symbols()
        self._build_nodal_normals()
        self._build_surface_velocity()
        self._build_specific_impedance()
        self._build_prescribed_dofs()
        self._build_nodal_loads()
        self._build_distributed_loads()
        self._build_normal_pressure_load()
        self._build_perforated_plate()
        self._build_mass_flow_rate()
        self._build_dofs_decoupling()
        self._build_absorption_surface()
        super().build()

    def _get_center_coords_and_normals(self, surface_id: int) -> float:
        mesh = app().project.model.mesh

        surface_nodes = mesh.nodes_from_surfaces[surface_id]
        surface_normals = mesh.normals_surface.get(surface_id)
        surface_coordinates = mesh.nodal_coordinates[surface_nodes, 1:]

        curvatures_surface = mesh.curvatures_surface.get(surface_id)
        contains_curvature = (curvatures_surface is not None) and np.any(curvatures_surface)
        center_coords = np.average(surface_coordinates, axis=0)

        if contains_curvature:
            # Finds the node that is closest to the center coords
            dist = np.linalg.norm(surface_coordinates - center_coords, axis=1)
            index = np.argmin(dist)
            return surface_coordinates[index, :], surface_normals[index, :]

        else:
            return center_coords, np.average(surface_normals, axis=0)


    def _build_surface_velocity(self):
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id) in surface_properties.keys():
            if property_name != "surface_velocity":
                continue

            coords, normal = self._get_center_coords_and_normals(surface_id)
            self.add_normal_surface_velocity_symbol(coords, normal)

    def _build_nodal_normals(self):
        mesh = app().project.model.mesh
        for node_id, normal_vector in mesh.nodal_normals_data.items():
            coords = mesh.nodal_coordinates[node_id, 1:]
            self.add_normal_symbol(coords, normal_vector)

    def _build_prescribed_dofs(self):
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id), property in surface_properties.items():
            if property_name != "prescribed_dofs":
                continue

            coords, _ = self._get_center_coords_and_normals(surface_id)
            x, y, z, *_ = property["values"]

            if x is not None:
                self.add_prescribed_dof_symbol(coords, (1, 0, 0))

            if y is not None:
                self.add_prescribed_dof_symbol(coords, (0, 1, 0))

            if z is not None:
                self.add_prescribed_dof_symbol(coords, (0, 0, 1))

    def _build_nodal_loads(self):
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id), property in surface_properties.items():
            if property_name != "nodal_loads":
                continue

            coords, normal = self._get_center_coords_and_normals(surface_id)
            x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]
            orientation = np.real((x, y, z))
            is_pointing = np.dot(normal, orientation) < 0
            self.add_force_symbol(coords, orientation, is_pointing)
            
    def _build_distributed_loads(self):
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id), property in surface_properties.items():
            if property_name != "distributed_loads":
                continue

            coords, normal = self._get_center_coords_and_normals(surface_id)
            x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]
            orientation = np.real((x, y, z))
            is_pointing = np.dot(normal, orientation) < 0
            self.add_distributed_loads_symbol(coords, orientation, is_pointing)
    
    def _build_normal_pressure_load(self):
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id), property in surface_properties.items():
            if property_name != "normal_pressure_load":
                continue

            coords, normal = self._get_center_coords_and_normals(surface_id)
            self.add_normal_pressure_load_symbol(coords, normal)
    
    def _build_specific_impedance(self):
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id), property in surface_properties.items():
            if property_name != "specific_impedance":
                continue
            
            coords, normal = self._get_center_coords_and_normals(surface_id)
            self.add_impedance_symbol(coords, normal)

    def _build_perforated_plate(self):
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id), property in surface_properties.items():
            if property_name != "perforated_plate_model":
                continue

            coords, normal = self._get_center_coords_and_normals(surface_id)
            self.add_perforated_plate_symbol(coords, normal)

    def _build_mass_flow_rate(self):
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id), property in surface_properties.items():
            if property_name != "mass_flow_rate":
                continue

            coords, normal = self._get_center_coords_and_normals(surface_id)
            self.add_mass_flow_rate_symbol(coords, normal)
    
    def _build_dofs_decoupling(self):
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id), _ in surface_properties.items():
            print(property_name)
            if property_name != "degrees_of_freedom_decoupling":
                continue

            coords, normal = self._get_center_coords_and_normals(surface_id)
            self.add_dofs_decoupling_symbol(coords, normal)
    
    def _build_absorption_surface(self):
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id), _ in surface_properties.items():
            if property_name != "absorption_surface" and 0:
                continue

            coords, normal = self._get_center_coords_and_normals(surface_id)
            self.add_absorption_surface_symbol(coords, normal)
        

    # Specifications on how each symbol should look like
    def add_force_symbol(self, position, orientation, pointing=True):
        shape_name = "arrow" if pointing else "outwards_arrow"
        self.add_symbol(
            shape_name,
            position,
            orientation,
            color=color_names.RED_2,
            scale=1,
        )
    
    def add_distributed_loads_symbol(self, position, orientation, pointing=False):
        shape_name = "distributed_loads_outwards" if pointing else "distributed_loads"
        self.add_symbol(
            shape_name,
            position,
            orientation,
            color=color_names.RED_2,
            scale=1,
        )
    
    def add_normal_pressure_load_symbol(self, position, orientation):
        self.add_symbol(
            "normal_pressure_load",
            position,
            orientation,
            color=color_names.RED_2,
            scale=1,
        )

    def add_spring_symbol(self, position, orientation):
        self.add_symbol(
            "spring",
            position,
            orientation,
            color=color_names.ORANGE,
            scale=0.8,
        )

    def add_prescribed_dof_symbol(self, position, orientation):
        self.add_symbol(
            "cone",
            position,
            orientation,
            color=color_names.GREEN,
            scale=0.4,
        )

    def add_normal_surface_velocity_symbol(self, position, orientation):
        self.add_symbol(
            "outwards_arrow",
            position,
            orientation,
            color=color_names.RED_6,
            scale=1,
        )

    def add_damper_symbol(self, position, orientation):
        self.add_symbol(
            "damper",
            position,
            orientation,
            color=color_names.PINK,
            scale=0.8,
        )

    def add_mass_symbol(self, position, orientation):
        self.add_symbol(
            "mass",
            position,
            orientation,
            color=color_names.BLUE,
            scale=2,
        )

    def add_acoustic_pressure_symbol(self, position, orientation):
        self.add_symbol(
            "double_arrow",
            position,
            orientation,
            color=color_names.PURPLE,
            scale=1,
        )

    def add_impedance_symbol(self, position, orientation):
        self.add_symbol(
            "impedance",
            position,
            orientation,
            color=color_names.PURPLE_2,
            scale=1,
        )

    def add_normal_symbol(self, position, orientation):
        self.add_symbol(
            "outwards_arrow",
            position,
            orientation,
            color=color_names.GRAY,
            scale=1,
        )
    
    def add_perforated_plate_symbol(self, position, orientation):
        self.add_symbol(
            "perforated_plate",
            position,
            orientation,
            color=color_names.RED,
            scale=1,
        )
    
    def add_mass_flow_rate_symbol(self, position, orientation):
        self.add_symbol(
            "mass_flow_rate",
            position,
            orientation,
            color=color_names.PINK_4,
            scale=1,
        )
    
    def add_dofs_decoupling_symbol(self, position, orientation):
        self.add_symbol(
            "dofs_decoupling",
            position,
            orientation,
            color=color_names.GREEN,
            scale=1,
        )
    
    def add_absorption_surface_symbol(self, position, orientation):
        self.add_symbol(
            "absorption_surface",
            position,
            orientation,
            color=color_names.GREEN,
            scale=1,
        )

    # Preload the symbol shapes (they are likelly used in many symbols)
    def _register_shapes(self):
        self.register_shape("arrow", create_arrow_source())
        self.register_shape("long_arrow", create_long_arrow_source())
        self.register_shape("double_arrow", create_double_arrow_source())
        self.register_shape("outwards_arrow", create_outwards_arrow_source())
        self.register_shape("cone", create_cone_source())
        self.register_shape("cube", create_cube_source())
        self.register_shape("spring", create_spring_source())
        self.register_shape("damper", create_damper_source())
        self.register_shape("mass", create_mass_source())
        self.register_shape("perforated_plate", create_perforated_plate_source())
        self.register_shape("impedance", create_impedance_source())
        self.register_shape("mass_flow_rate", create_mass_flow_rate_source())
        self.register_shape("distributed_loads", create_triple_arrow_source())
        self.register_shape("distributed_loads_outwards", create_outwards_triple_arrow_source())
        self.register_shape("normal_pressure_load", create_normal_pressure_load())
        self.register_shape("dofs_decoupling", create_dofs_decpupling_source())
        self.register_shape("absorption_surface", create_absorption_surface_source())
