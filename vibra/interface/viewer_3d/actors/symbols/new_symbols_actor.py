from molde.colors import color_names
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkConeSource,
    vtkCubeSource,
)

import numpy as np
from vibra import SYMBOLS_DIR, app

from .common_symbols_actor_fixed_size import CommonSymbolsActorFixedSize  # noqa: F401
from .common_symbols_actor_variable_size import CommonSymbolsActorVariableSize  # noqa: F401


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
        pos = (3, 0, 0)
        self.add_force_symbol(pos, (1, 0, 0))
        self.add_damper_symbol(pos, (1, 1, 0))
        self.add_spring_symbol(pos, (1, 1, 0))
        self.add_mass_symbol(pos, (-1, -1, 0))
        self.add_normal_symbol(pos, (1, 1, 1))
        super().build()
    
    def _build_surface_velocity(self):
        mesh = app().project.model.mesh
        surface_properties = app().project.model.properties.surface_properties
        orientation = np.array([-1, 0, 0], dtype=float)

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

    # def build_only_normals(self):
    #     self.add_normal_symbol((3, 0, 0), (1, 1, 1))

    #     self.clear_all()
    #     surface_properties = app().project.model.properties.surface_properties
    #     mesh = app().project.model.mesh

    #     for (property_name, surface_id) in surface_properties.keys():
    #         if property_name != "normal_pressure_load":
    #             continue 

    #         for elem_id in mesh.elements_from_surface[surface_id]:
    #             connect = mesh.faces_connectivity[elem_id, 4:]
    #             coords = np.average(mesh.nodal_coordinates[connect, 1:], axis=0)
    #             normal_vector = mesh.get_element_face_normal(connect)
    #             self.add_normal_symbol(coords, normal_vector)
    #             print("hi")

    #     super().build()

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
        self.register_shape("arrow", self._get_arrow_source())
        self.register_shape("long_arrow", self._get_long_arrow_source())
        self.register_shape("double_arrow", self._get_double_arrow_source())
        self.register_shape("outwards_arrow", self._get_outwards_arrow_source())
        self.register_shape("cone", self._get_cone_source())
        self.register_shape("cube", self._get_cube_source())
        self.register_shape("spring", self._get_spring_source())
        self.register_shape("damper", self._get_damper_source())
        self.register_shape("mass", self._get_mass_source())

    def _get_arrow_source(self):
        source = vtkArrowSource()
        source.SetTipLength(0.25)
        source.Update()

        return self.transform_polydata(
            source.GetOutput(),
            position=(-1, 0, 0),
        )

    def _get_long_arrow_source(self):
        source = vtkArrowSource()
        source.SetTipResolution(4)
        source.SetShaftResolution(4)
        source.SetTipLength(0.85)
        source.Update()

        return self.transform_polydata(
            source.GetOutput(),
            position=(-1, 0, 0),
        )

    def _get_double_arrow_source(self):
        arrow1 = vtkArrowSource()
        arrow1.SetTipLength(0.45)
        arrow1.Update()

        arrow2 = vtkArrowSource()
        arrow2.SetTipLength(0.3)
        arrow2.Update()

        source = vtkAppendPolyData()
        source.AddInputData(arrow1.GetOutput())
        source.AddInputData(arrow2.GetOutput())
        source.Update()
    
        return self.transform_polydata(
            source.GetOutput(),
            position=(-1, 0, 0),
        )

    def _get_outwards_arrow_source(self):
        source = vtkArrowSource()
        source.SetTipLength(0.25)
        source.Update()
        return source.GetOutput()

    def _get_cone_source(self):
        source = vtkConeSource()
        source.SetHeight(1)
        source.SetRadius(0.5)
        source.SetResolution(12)
        source.Update()
        return self.transform_polydata(
            source.GetOutput(),
            position=(-0.5, 0, 0),
        )

    def _get_cube_source(self):
        source = vtkCubeSource()
        source.SetBounds(0, 1, 0, 1, 0, 1)
        source.Update()
        return source.GetOutput()

    def _get_spring_source(self):
        polydata = self.read_stl_file(SYMBOLS_DIR / "stl_files/spring_symbol.STL")
        return self.transform_polydata(
            polydata,
            position=(-1.25, -0.18, 0.18),
            rotation=(0, 90, 0),
        )

    def _get_damper_source(self):
        polydata = self.read_obj_file(SYMBOLS_DIR / "structural/lumped_damper.obj")
        return self.transform_polydata(
            polydata,
            position=(-0.145, 0, 0),
        )

    def _get_mass_source(self):
        return self.transform_polydata(
            self.read_obj_file(SYMBOLS_DIR / "structural/new_lumped_mass.obj"),
            rotation=(0, -90, 0),
        )
