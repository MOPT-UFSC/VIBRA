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

from molde.colors import Color, color_names
from vtkmodules.vtkIOGeometry import vtkOBJReader, vtkSTLReader

from .common_symbols_actor_fixed_size import CommonSymbolsActorFixedSize
from .common_symbols_actor_variable_size import CommonSymbolsActorVariableSize


class NewSymbolsActor(CommonSymbolsActorVariableSize):
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
            "force",
            position,
            orientation,
            color=color_names.RED,
            scale=0.3,
        )

    def add_spring_symbol(self, position, orientation):
        self.add_symbol(
            "spring",
            position,
            orientation,
            color=color_names.ORANGE,
            scale=0.3,
        )

    def add_prescribed_dof_symbol(self, position, orientation):
        self.add_symbol(
            "dof_cone",
            position,
            orientation,
            color=color_names.GREEN,
            scale=0.3,
        )

    def add_volume_velocity_symbol(self, position, orientation):
        self.add_symbol(
            "volume_velocity",
            position,
            orientation,
            color=color_names.RED,
            scale=0.3,
        )

    def add_damper_symbol(self, position, orientation):
        self.add_symbol(
            "damper",
            position,
            orientation,
            color=color_names.PINK,
            scale=0.3,
        )

    def add_mass_symbol(self, position, orientation):
        self.add_symbol(
            "mass",
            position,
            orientation,
            color=color_names.BLUE,
            scale=0.3,
        )

    def add_acoustic_pressure_symbol(self, position, orientation):
        self.add_symbol(
            "acoustic_pressure",
            position,
            orientation,
            color=color_names.PURPLE,
            scale=0.3,
        )

    def add_impedance_symbol(self, position, orientation):
        self.add_symbol(
            "impedance",
            position,
            orientation,
            color=color_names.GREEN,
            scale=0.3,
        )

    def _register_shapes(self):
        self.register_shape("force", self._get_force_source())
        self.register_shape("dof_cone", self._get_cone_source())
        self.register_shape("spring", self._get_spring_source())
        self.register_shape("volume_velocity", self._get_volume_velocity_source())
        self.register_shape("damper", self._get_damper_source())
        self.register_shape("mass", self._get_mass_source())
        self.register_shape("acoustic_pressure", self._get_acoustic_pressure_source())
        self.register_shape("impedance", self._get_impedance_source())

    def _get_force_source(self):
        source = vtkArrowSource()
        source.SetTipLength(.25)
        source.Update()
        return source.GetOutput()

    def _get_cone_source(self):
        source = vtkConeSource()
        source.SetHeight(.5)
        source.SetRadius(.7)
        source.Update()
        return source.GetOutput()

    def _get_spring_source(self):
        reader = vtkSTLReader()
        reader.SetFileName(str(SYMBOLS_DIR / "stl_files/spring_symbol.STL"))
        reader.Update()
        return reader.GetOutput()

    def _get_volume_velocity_source(self):
        source = vtkArrowSource()
        source.SetTipLength(.85)
        source.Update()
        return source.GetOutput()

    def _get_damper_source(self):
        reader = vtkOBJReader()
        reader.SetFileName(str(SYMBOLS_DIR / "structural/lumped_damper.obj"))
        reader.Update()
        return reader.GetOutput()

    def _get_mass_source(self):
        reader = vtkOBJReader()
        reader.SetFileName(str(SYMBOLS_DIR / "structural/new_lumped_mass.obj"))
        reader.Update()
        transform = vtkTransform()
        transform.RotateWXYZ(90, 0, 1, 0)
        transformation = vtkTransformPolyDataFilter()
        transformation.SetTransform(transform)
        transformation.SetInputData(reader.GetOutput())
        transformation.Update()
        return transformation.GetOutput()

    def _get_acoustic_pressure_source(self):
        source = vtkArrowSource()
        source.SetTipLength(.45)
        source.Update()
        return source.GetOutput()

    def _get_impedance_source(self):
        source = vtkCubeSource()
        source.SetBounds(0, 1, 0, 1, 0, 1)
        source.Update()
        return source.GetOutput()

    def _get_shape_obj_file(self, path: str):
        reader = vtkOBJReader()
        reader.SetFileName(str(SYMBOLS_DIR / "structural/lumped_damper.obj"))
        reader.Update()
        return reader.GetOutput()

    def _get_shape_stl_file(self, path: str):
        reader = vtkSTLReader()
        reader.SetFileName(str(path))
        reader.Update()
        return reader.GetOutput()

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
