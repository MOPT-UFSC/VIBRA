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
)

class NewSymbolsActor(CommonSymbolsActorVariableSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_appearance()
        self._register_shapes()
        self.build()

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def build(self):
        self._build_nodal_normals()
        self._build_surface_velocity()
        super().build()
        return
        # pos = (3, 0, 0)
        # self.add_force_symbol(pos, (1, 0, 0))
        # self.add_damper_symbol(pos, (1, 1, 0))
        # self.add_spring_symbol(pos, (1, 1, 0))
        # self.add_mass_symbol(pos, (-1, -1, 0))
        # self.add_normal_symbol(pos, (1, 1, 1))
        # super().build()

    def _build_surface_velocity(self):
        mesh = app().project.model.mesh
        surface_properties = app().project.model.properties.surface_properties
        orientation = np.array([1, 0, 0], dtype=float)

        for (property_name, surface_id), data in surface_properties.items():
            if property_name != "surface_velocity":
                continue

            surface_nodes = mesh.nodes_from_surfaces[surface_id]
            nodal_coords = mesh.nodal_coordinates[surface_nodes, 1:]

            for coords in nodal_coords:
                # I am not sure if this name is adequate.
                # We may either rename the function or
                # use different symbols for each velocity condition
                self.add_volume_velocity_symbol(coords, orientation)

    def _build_nodal_normals(self):
        mesh = app().project.model.mesh
        for node_id, normal_vector in mesh.nodal_normals_data.items():
            coords = mesh.nodal_coordinates[node_id, 1:]
            self.add_normal_symbol(coords, normal_vector)

    # Specifications on how each symbol should look like
    def add_force_symbol(self, position, orientation):
        self.add_symbol(
            "arrow",
            position,
            orientation,
            color=color_names.RED,
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

    def add_volume_velocity_symbol(self, position, orientation):
        self.add_symbol(
            "long_arrow",
            position,
            orientation,
            color=color_names.RED,
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
            "cube",
            position,
            orientation,
            color=color_names.GREEN,
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
