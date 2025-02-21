from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkCylinderSource,
    vtkSphereSource,
    vtkConeSource,
)
from vibra import SYMBOLS_DIR

from molde.colors import Color
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
        self.add_symbol(
            "arrow",
            position=(2, 0, 0),
            orientation=(1, 0, 0),
            color=Color(255, 255, 0),
            scale=0.3,
        )

        self.add_symbol(
            "cone",
            position=(4, 0, 0),
            orientation=(1, 0, 0),
            color=Color(255, 255, 0),
            scale=0.3,
        )

        self.add_symbol(
            "cylinder",
            position=(6, 0, 0),
            orientation=(1, 0, 0),
            color=Color(0, 255, 0),
            scale=0.3,
        )

        self.add_symbol(
            "sphere",
            position=(8, 2, 0),
            orientation=(1, 0, 0),
            color=Color(0, 0, 255),
            scale=0.3,
        )

        self.add_symbol(
            "OBJ",
            position=(-2, 0, 0),
            orientation=(1, 0, 0),
            color=Color(255, 0, 0),
            scale=0.3,
        )

        self.add_symbol(
            "STL",
            position=(-4, 0, 0),
            orientation=(1, 0, 0),
            color=Color(255, 0, 0),
            scale=1,
        )

        super().build()

    def _register_shapes(self):
        lumped_source = self._get_shape_obj_file(SYMBOLS_DIR / "structural/lumped_damper.obj")
        damper_symbol = self._get_shape_stl_file(SYMBOLS_DIR / "stl_files/damper_symbol.STL")

        self.register_shape("arrow", self._get_arrow_source())
        self.register_shape("cone", self._get_cone_source())
        self.register_shape("cylinder", self._get_cylinder_source())
        self.register_shape("sphere", self._get_sphere_source())
        self.register_shape("OBJ", lumped_source)
        self.register_shape("STL", damper_symbol)
        # TODO: add the following shapes
        # spring

    def _get_arrow_source(self):
        source = vtkArrowSource()
        source.SetTipLength(0.25)
        source.Update()
        return source.GetOutput()

    def _get_cone_source(self):
        source = vtkConeSource()
        source.SetHeight(0.5)
        source.Update()
        return source.GetOutput()

    def _get_cylinder_source(self):
        source = vtkCylinderSource()
        source.SetHeight(2)
        source.Update()
        transform = vtkTransform()
        transform.Translate(1, 0, 0)
        transform.RotateZ(-90.0)
        # transformation
        transformation = vtkTransformPolyDataFilter()
        transformation.SetTransform(transform)
        transformation.SetInputData(source.GetOutput())
        transformation.Update()
        return transformation.GetOutput()

    def _get_sphere_source(self):
        source = vtkSphereSource()
        source.SetRadius(0.5)
        source.Update()
        return source.GetOutput()

    def _get_shape_obj_file(self, path: str):
        reader = vtkOBJReader()
        reader.SetFileName(str(path))
        reader.Update()
        return reader.GetOutput()

    def _get_shape_stl_file(self, path: str):
        reader = vtkSTLReader()
        reader.SetFileName(str(path))
        reader.Update()
        return reader.GetOutput()

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
