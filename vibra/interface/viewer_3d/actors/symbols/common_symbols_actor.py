from dataclasses import dataclass

from molde import Color
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkDistanceToCamera, vtkGlyph3DMapper, vtkRenderer

Triple = tuple[float, float, float]


@dataclass
class Symbol:
    shape_name: str
    position: Triple
    orientation: Triple
    color: Color
    scale: float


class CommonSymbolsActor(vtkActor):
    def __init__(self, *args, **kwargs):
        self._shapes: dict[str, vtkPolyData] = dict()
        self._symbols: list[Symbol] = list()

    def register_shape(self, name: str, shape: vtkPolyData):
        self._shapes[name] = shape

    def add_symbol(
        self,
        shape_name: str,
        position: Triple,
        orientation: Triple,
        color: Triple,
        scale: float = 1,
    ):
        symbol = Symbol(
            shape_name,
            position,
            orientation,
            color,
            scale,
        )
        self._symbols.append(symbol)

    def clear_shapes(self):
        self._shapes.clear()

    def clear_symbols(self):
        self._symbols.clear()

    def clear_all(self):
        self.clear_shapes()
        self.clear_symbols()

    def common_build(self):
        self.data = vtkPolyData()
        points = vtkPoints()

        self.mapper: vtkGlyph3DMapper = vtkGlyph3DMapper()
        self.SetMapper(self.mapper)

        sources = vtkIntArray()
        sources.SetName("sources")

        rotations = vtkDoubleArray()
        rotations.SetNumberOfComponents(3)
        rotations.SetName("rotations")

        scales = vtkDoubleArray()
        scales.SetName("scales")

        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("colors")

        shape_name_to_index = dict()
        for index, (name, shape) in enumerate(self._shapes.items()):
            shape_name_to_index[name] = index
            self.mapper.SetSourceData(index, shape)

        for symbol in self._symbols:
            points.InsertNextPoint(symbol.position)
            rotations.InsertNextTuple(symbol.orientation)
            colors.InsertNextTuple(symbol.color.to_rgb())
            scales.InsertNextValue(symbol.scale)
            sources.InsertNextValue(shape_name_to_index[symbol.shape_name])

        self.data.SetPoints(points)
        self.data.GetPointData().AddArray(sources)
        self.data.GetPointData().AddArray(rotations)
        self.data.GetPointData().AddArray(scales)
        self.data.GetPointData().SetScalars(colors)


class CommonSymbolsActorFixedSize(CommonSymbolsActor):
    def build(self):
        self.common_build()

        self.mapper.SetInputData(self.data)
        self.mapper.SetSourceIndexArray("sources")
        self.mapper.SetOrientationArray("rotations")
        self.mapper.SetScaleArray("scales")
        self.mapper.SourceIndexingOn()
        self.mapper.ScalarVisibilityOn()
        self.mapper.SetScaleModeToScaleByMagnitude()
        self.mapper.SetScalarModeToUsePointData()
        self.mapper.SetOrientationModeToDirection()
        self.mapper.Update()


class CommonSymbolsActorVariableSize(CommonSymbolsActor):
    def __init__(self, renderer: vtkRenderer):
        super().__init__()
        self.renderer = renderer

    def build(self):
        self.common_build()

        distance_to_camera = vtkDistanceToCamera()
        distance_to_camera.SetInputData(self.data)
        distance_to_camera.SetScreenSize(40)
        distance_to_camera.SetRenderer(self.renderer)

        self.mapper.SetInputConnection(distance_to_camera.GetOutputPort())
        self.mapper.SetSourceIndexArray("sources")
        self.mapper.SetOrientationArray("rotations")
        self.mapper.SetScaleArray("DistanceToCamera")
        self.mapper.SourceIndexingOn()
        self.mapper.ScalarVisibilityOn()
        self.mapper.SetScaleModeToScaleByMagnitude()
        self.mapper.SetScalarModeToUsePointData()
        self.mapper.SetOrientationModeToDirection()

        # shows the actor in front of everything else
        # offset = -66000
        offset = 0
        factor = 1.3
        self.mapper.SetResolveCoincidentTopologyToPolygonOffset()
        self.mapper.SetRelativeCoincidentTopologyLineOffsetParameters(factor, offset)
        self.mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(factor, offset)
        self.mapper.SetRelativeCoincidentTopologyPointOffsetParameter(offset)

        self.mapper.Update()
