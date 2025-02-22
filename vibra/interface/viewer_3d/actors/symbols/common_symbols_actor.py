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


class CommonSymbolsActor(vtkActor):
    def __init__(self, *args, **kwargs):
        self._shapes: dict[str, vtkPolyData] = dict()
        self._symbols: list[Symbol] = list()
    
    def register_shape(self, name: str, shape: vtkPolyData):
        self._shapes[name] = shape
    
    def add_force_symbol(self, position: Triple, orientation: Triple):
        self.add_symbol("arrow", position, orientation, Color(1, 0, 0))

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

    def common_build(self) -> vtkPolyData:
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
