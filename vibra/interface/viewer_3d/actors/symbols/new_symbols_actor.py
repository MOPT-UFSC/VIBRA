from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkCylinderSource,
    vtkSphereSource,
    vtkConeSource,
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

    def add_force_symbol(self):
        self.add_symbol(
            "force",
            position=(2, 0, 0),
            orientation=(1, 0, 0),
            color=color_names.RED,
            scale=0.3,
        )

    def add_spring_symbol(self):
        self.add_symbol(
            "spring",
            position=(4, 0, 0),
            orientation=(1, 0, 0),
            color=color_names.ORANGE,
            scale=0.3,
        )

    def add_DOF_cone_symbol(self):
        self.add_symbol(
            "DOF_cone",
            position=(6, 0, 0),
            orientation=(1, 0, 0),
            color=color_names.GREEN,
            scale=0.3,
        )

    def add_volume_velocity_symbol(self):
        self.add_symbol(
            "volume_velocity",
            position=(2, 2, 0),
            orientation=(1, 0, 0),
            color=color_names.RED,
            scale=0.3,
        )

    def add_damper_symbol(self):
        self.add_symbol(
            "damper",
            position=(4, 2, 0),
            orientation=(1, 0, 0),
            color=color_names.PINK,
            scale=0.3,
        )

    def add_mass_symbol(self):
        self.add_symbol(
            "mass",
            position=(6, 2, 0),
            orientation=(1, 0, 0),
            color=color_names.BLUE,
            scale=0.3,
        )

    def add_acoustic_pressure_symbol(self):
        self.add_symbol(
            "acoustic_pressure",
            position=(8, 2, 0),
            orientation=(1, 0, 0),
            color=color_names.PURPLE,
            scale=0.3,
        )

    def add_impedance_symbol(self):
        self.add_symbol(
            "impedance",
            position=(10, 2, 0),
            orientation=(1, 0, 0),
            color=color_names.GREEN,
            scale=0.3,
        )

    def build(self):
        self.add_force_symbol()
        self.add_DOF_cone_symbol()
        self.add_spring_symbol()
        self.add_volume_velocity_symbol()
        self.add_damper_symbol()
        self.add_mass_symbol()
        self.add_acoustic_pressure_symbol()
        self.add_impedance_symbol()

        super().build()

    def _register_shapes(self):
        self.register_shape("force", self._get_force_source())
        self.register_shape("DOF_cone", self._get_cone_source())
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
