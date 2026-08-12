from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from molde.colors.color import Color
from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkIntArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkGlyph3DMapper, vtkPropAssembly

from vibra.utils.time_utils import function_timer


@dataclass
class Entity:
    """
    A symbol that looks like a regular mesh.
    """

    shape_function: Callable
    position: Sequence[float]
    orientation: Sequence[float]
    color: Color
    scale: float
    tags: set[str]


@dataclass
class Marker:
    """
    A symbol that resizes with the camera.
    Always keeping a constant size to the viewer.
    """

    shape_function: Callable
    position: Sequence[float]
    orientation: Sequence[float]
    color: Color
    tags: set[str]


@dataclass
class Billboard:
    """
    A 2D symbol that always faces the camera.
    """

    image_path: Path
    position: Sequence[float]
    tags: set[str]


Symbol = Entity | Marker | Billboard


class SymbolsActor(vtkPropAssembly):
    def __init__(self, *args, **kwargs):
        self._symbols: list[Symbol] = list()
        self._create_variables()

    def _create_variables(self):
        self.entity_points = vtkPoints()
        self.entity_sources = vtkIntArray()
        self.entity_sources.SetName("sources")
        self.entity_sources = vtkIntArray()
        self.entity_sources.SetName("sources")
        self.entity_rotations = vtkDoubleArray()
        self.entity_rotations.SetNumberOfComponents(3)
        self.entity_rotations.SetName("rotations")
        self.entity_scales = vtkDoubleArray()
        self.entity_scales.SetName("scales")
        self.entity_colors = vtkUnsignedCharArray()
        self.entity_colors.SetNumberOfComponents(3)
        self.entity_colors.SetName("colors")
        self.entity_data = vtkPolyData()
        self.entity_mapper = vtkGlyph3DMapper()
        self.entity_actor = vtkActor()

        self.entity_data.SetPoints(self.entity_points)
        self.entity_data.GetPointData().AddArray(self.entity_sources)
        self.entity_data.GetPointData().AddArray(self.entity_rotations)
        self.entity_data.GetPointData().AddArray(self.entity_scales)
        self.entity_data.GetPointData().SetScalars(self.entity_colors)
        self.entity_actor.SetMapper(self.entity_mapper)
        self.entity_mapper.SetInputData(self.entity_data)

        self.entity_mapper.SetSourceIndexArray("sources")
        self.entity_mapper.SetOrientationArray("rotations")
        self.entity_mapper.SetScaleArray("scales")
        self.entity_mapper.SourceIndexingOn()
        self.entity_mapper.ScalarVisibilityOn()
        self.entity_mapper.SetScaleModeToScaleByMagnitude()
        self.entity_mapper.SetScalarModeToUsePointData()
        self.entity_mapper.SetOrientationModeToDirection()

        self.AddPart(self.entity_actor)

    @function_timer
    def build(self):
        self.build_entities()
        self.build_markers()
        self.build_billboards()

    def _entities(self) -> list[Entity]:
        return [symbol for symbol in self._symbols if isinstance(symbol, Entity)]

    def _markers(self) -> list[Marker]:
        return [symbol for symbol in self._symbols if isinstance(symbol, Marker)]

    def _billboards(self) -> list[Billboard]:
        return [symbol for symbol in self._symbols if isinstance(symbol, Billboard)]

    def build_entities(self):
        self.entity_points.Reset()
        self.entity_rotations.Reset()
        self.entity_colors.Reset()
        self.entity_scales.Reset()
        self.entity_sources.Reset()

        shape_function_to_index = dict()
        for symbol in self._entities():
            if symbol.shape_function not in shape_function_to_index:
                index = len(shape_function_to_index)
                shape_function_to_index[symbol.shape_function] = index
                self.entity_mapper.SetSourceData(index, symbol.shape_function())

            self.entity_points.InsertNextPoint(symbol.position)
            self.entity_rotations.InsertNextTuple(symbol.orientation)
            self.entity_colors.InsertNextTuple(symbol.color.to_rgb())
            self.entity_scales.InsertNextValue(symbol.scale)
            self.entity_sources.InsertNextValue(shape_function_to_index[symbol.shape_function])

        self.entity_mapper.Modified()

    def build_markers(self):
        pass

    def build_billboards(self):
        pass

    def add_entity(
        self,
        shape_function: Callable,
        position: Sequence[float],
        orientation: Sequence[float],
        color: Color,
        scale: float,
        group: set[str] | None = None,
    ):
        if group is None:
            group = set()

        entity = Entity(shape_function, position, orientation, color, scale, group)
        self._symbols.append(entity)

    def add_marker(
        self,
        shape_function: Callable,
        position: Sequence[float],
        orientation: Sequence[float],
        color: Color,
        group: set[str] | None = None,
    ):
        if group is None:
            group = set()

        marker = Marker(shape_function, position, orientation, color, group)
        self._symbols.append(marker)

    def add_billboard(
        self,
        image_path: Path,
        position: Sequence[float],
        group: set[str] | None = None,
    ):
        if group is None:
            group = set()

        billboard = Billboard(image_path, position, group)
        self._symbols.append(billboard)
