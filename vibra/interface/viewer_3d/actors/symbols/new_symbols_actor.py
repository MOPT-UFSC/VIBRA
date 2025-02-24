from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkCylinderSource,
    vtkSphereSource,
    vtkConeSource,
    vtkCubeSource,
)

from vibra import SYMBOLS_DIR
from pathlib import Path
from molde.colors import Color, color_names
from vtkmodules.vtkIOGeometry import vtkOBJReader, vtkSTLReader

from .common_symbols_actor_fixed_size import CommonSymbolsActorFixedSize
from .common_symbols_actor_variable_size import CommonSymbolsActorVariableSize
from vtkmodules.vtkCommonDataModel import vtkPolyData


class NewSymbolsActor(CommonSymbolsActorFixedSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_appearance()
        self._register_shapes()
        self.build()

    def build(self):
        # add your custom code here
        for i in range(10):
            self.add_force_symbol(position=(i, 0, 0), orientation=(i, 0, 0))
            self.add_prescribed_dof_symbol(position=(i, 1, 0), orientation=(i, 1, 0))
            self.add_spring_symbol(position=(i, 2, 0), orientation=(i, 2, 0))
            self.add_volume_velocity_symbol(position=(i, 3, 0), orientation=(i, 3, 0))
            self.add_damper_symbol(position=(i, 4, 0), orientation=(i, 4, 0))
            self.add_mass_symbol(position=(i, 5, 0), orientation=(i, 5, 0))
            self.add_acoustic_pressure_symbol(position=(i, 6, 0), orientation=(i, 6, 0))
            self.add_impedance_symbol(position=(i, 7, 0), orientation=(i, 7, 0))

        super().build()

    def add_force_symbol(self, position, orientation):
        self.add_symbol(
            "arrow_1",
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
            scale=1,
        )

    def add_prescribed_dof_symbol(self, position, orientation):
        self.add_symbol(
            "cone",
            position,
            orientation,
            color=color_names.GREEN,
            scale=1,
        )

    def add_volume_velocity_symbol(self, position, orientation):
        self.add_symbol(
            "arrow_2",
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
            scale=1,
        )

    def add_mass_symbol(self, position, orientation):
        self.add_symbol(
            "mass",
            position,
            orientation,
            color=color_names.BLUE,
            scale=1,
        )

    def add_acoustic_pressure_symbol(self, position, orientation):
        self.add_symbol(
            "arrow_3",
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

    def _register_shapes(self):
        self.register_shape("arrow_1", self._get_arrow_1_source())
        self.register_shape("arrow_2", self._get_arrow_2_source())
        self.register_shape("arrow_3", self._get_arrow_3_source())
        self.register_shape("cone", self._get_cone_source())
        self.register_shape("cube", self._get_cube_source())
        self.register_shape("spring", self._get_spring_source())
        self.register_shape("damper", self._get_damper_source())
        self.register_shape("mass", self._get_mass_source())

    def _get_arrow_1_source(self):
        source = vtkArrowSource()
        source.SetTipLength(0.25)
        source.Update()
        return source.GetOutput()

    def _get_arrow_2_source(self):
        source = vtkArrowSource()
        source.SetTipLength(0.85)
        source.Update()
        return source.GetOutput()

    def _get_arrow_3_source(self):
        source = vtkArrowSource()
        source.SetTipLength(0.45)
        source.Update()
        return source.GetOutput()

    def _get_cone_source(self):
        source = vtkConeSource()
        source.SetHeight(0.4)
        source.SetRadius(0.2)
        source.SetResolution(12)
        source.Update()
        return source.GetOutput()

    def _get_cube_source(self):
        source = vtkCubeSource()
        source.SetBounds(0, 1, 0, 1, 0, 1)
        source.Update()
        return source.GetOutput()

    def _get_spring_source(self):
        return self._read_stl_file(SYMBOLS_DIR / "stl_files/spring_symbol.STL")

    def _get_damper_source(self):
        return self._read_obj_file(SYMBOLS_DIR / "structural/lumped_damper.obj")

    def _get_mass_source(self):
        return self._transform_source(
            self._read_obj_file(SYMBOLS_DIR / "structural/new_lumped_mass.obj"),
            rotation=(0, 90, 0),
        )

    def _read_obj_file(self, path: str | Path):
        reader = vtkOBJReader()
        reader.SetFileName(str(path))
        # reader.SetFileName(str(SYMBOLS_DIR / "structural/lumped_damper.obj"))
        reader.Update()
        return reader.GetOutput()

    def _read_stl_file(self, path: str | Path):
        reader = vtkSTLReader()
        reader.SetFileName(str(path))
        reader.Update()
        return reader.GetOutput()

    def _transform_source(
        self,
        source: vtkPolyData,
        position=(0, 0, 0),
        rotation=(0, 0, 0),
        scale=(0, 0, 0),
    ) -> vtkPolyData:
        transform = vtkTransform()
        transform.Translate(position)
        transform.Scale(scale)
        transform.RotateX(rotation[0])
        transform.RotateY(rotation[1])
        transform.RotateZ(rotation[2])
        transformation = vtkTransformPolyDataFilter()
        transformation.SetTransform(transform)
        transformation.SetInputData(source)
        transformation.Update()
        return transformation.GetOutput()

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()
