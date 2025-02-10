from molde import Color

from dataclasses import dataclass
from vtkmodules.vtkRenderingCore import vtkActor
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import vtkGlyph3DMapper
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkDoubleArray,
    vtkUnsignedCharArray,
)


Triple = tuple[float, float, float]


@dataclass
class Symbol:
    shape_name: str
    position: Triple
    orientation: Triple
    color: Color
    scale: float


class SymbolActorFixedSize(vtkActor):
    def __init__(self):
        self._shapes: dict[str, vtkPolyData] = dict()
        self._symbols: list[Symbol] = list()

    def build(self):
        data = vtkPolyData()
        points = vtkPoints()
        mapper = vtkGlyph3DMapper()

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
        # colors.SetNumberOfTuples(len(self._symbols))

        shape_name_to_index = dict()
        for index, (name, shape) in enumerate(self._shapes.items()):
            shape_name_to_index[name] = index
            mapper.SetSourceData(index, shape)

        for symbol in self._symbols:
            points.InsertNextPoint(symbol.position)
            rotations.InsertNextTuple(symbol.orientation)
            colors.InsertNextTuple(symbol.color.to_rgb())
            scales.InsertNextValue(symbol.scale)
            sources.InsertNextValue(shape_name_to_index[symbol.shape_name])

        data.SetPoints(points)
        data.GetPointData().AddArray(sources)
        data.GetPointData().AddArray(rotations)
        data.GetPointData().AddArray(scales)
        data.GetPointData().SetScalars(colors)

        mapper.SetInputData(data)
        mapper.SetSourceIndexArray("sources")
        mapper.SetOrientationArray("rotations")
        mapper.SetScaleArray("scales")
        mapper.SourceIndexingOn()
        mapper.ScalarVisibilityOn()
        mapper.SetScaleModeToScaleByMagnitude()
        mapper.SetScalarModeToUsePointData()
        mapper.SetOrientationModeToDirection()
        mapper.Update()

        self.SetMapper(mapper)

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
