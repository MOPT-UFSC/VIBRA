from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import IntEnum, auto
from functools import cached_property
from itertools import chain

import numpy as np
from molde.colors.color import Color
from scipy.spatial.transform import Rotation
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkCommand, vtkDoubleArray, vtkIntArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkCamera, vtkGlyph3DMapper, vtkPropAssembly

from vibra.utils.time_utils import function_timer


@dataclass
class Entity:
    """
    A symbol that looks like a regular mesh.
    """

    shape_function: Callable[[], vtkPolyData]
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

    shape_function: Callable[[], vtkPolyData]
    position: Sequence[float]
    orientation: Sequence[float]
    color: Color
    tags: set[str]


@dataclass
class Billboard:
    """
    A 2D symbol that always faces the camera.
    """

    shape_function: Callable[[], vtkPolyData]
    position: Sequence[float]
    color: Color
    tags: set[str]


Symbol = Entity | Marker | Billboard


class SymbolType(IntEnum):
    """
    Numeric identifier for each symbol variant, stored in the VTK ``type`` array.
    """

    ENTITY = auto()
    MARKER = auto()
    BILLBOARD = auto()

    @classmethod
    def from_symbol(cls, symbol: Symbol) -> "SymbolType":
        return cls.ENTITY._class_to_type[type(symbol)]

    @property
    def symbol_class(self) -> type[Symbol]:
        return self._type_to_class[self]

    @cached_property
    def _class_to_type(self) -> dict[type[Symbol], "SymbolType"]:
        return {
            Entity: SymbolType.ENTITY,
            Marker: SymbolType.MARKER,
            Billboard: SymbolType.BILLBOARD,
        }

    @cached_property
    def _type_to_class(self) -> dict["SymbolType", type[Symbol]]:
        return {symbol_type: symbol_class for symbol_class, symbol_type in self._class_to_type.items()}


class SymbolsActor(vtkPropAssembly):
    def __init__(self, camera: vtkCamera):
        super().__init__()

        self.camera = camera
        self._symbols: list[Symbol] = []
        self._create_variables()

    @function_timer
    def build(self):
        self.build_entities()
        # self.build_markers()
        # self.build_billboards()

    def add_entity(
        self,
        shape_function: Callable[[], vtkPolyData],
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
        shape_function: Callable[[], vtkPolyData],
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
        shape_function: Callable[[], vtkPolyData],
        position: Sequence[float],
        color: Color,
        group: set[str] | None = None,
    ):
        if group is None:
            group = set()

        billboard = Billboard(shape_function, position, color, group)
        self._symbols.append(billboard)

    def get_camera_facing_rotation(self):
        forward = -np.array(self.camera.GetDirectionOfProjection())
        forward /= np.linalg.norm(forward)
        up = np.array(self.camera.GetViewUp())
        right = np.cross(up, forward)
        right /= np.linalg.norm(right)
        up = np.cross(forward, right)

        matrix = np.column_stack((forward, -up, right))
        x, y, z, w = Rotation.from_matrix(matrix).as_quat("zxy")
        return w, x, y, z

    def camera_update(self, *args):
        points_view = vtk_to_numpy(self.symbol_points.GetData())
        scale_view = vtk_to_numpy(self.symbol_scales)
        rotation_view = vtk_to_numpy(self.symbol_rotation)
        type_view = vtk_to_numpy(self.symbol_type)

        markers = type_view == int(SymbolType.MARKER)
        billboards = type_view == int(SymbolType.BILLBOARD)

        camera_position = self.camera.GetPosition()
        diff = points_view[markers | billboards] - camera_position
        scale_view[markers | billboards] = 0.02 * np.linalg.norm(diff, axis=1)
        rotation = self.get_camera_facing_rotation()
        rotation_view[billboards] = rotation

        self.symbol_scales.Modified()
        self.symbol_data.Modified()
        self.symbol_mapper.Modified()

    def _create_variables(self):
        self.camera.AddObserver(vtkCommand.ModifiedEvent, self.camera_update)

        self.symbol_points = vtkPoints()
        self.symbol_sources = vtkIntArray()
        self.symbol_sources.SetName("sources")
        self.symbol_sources = vtkIntArray()
        self.symbol_sources.SetName("sources")
        self.symbol_rotation = vtkDoubleArray()
        self.symbol_rotation.SetNumberOfComponents(4)
        self.symbol_rotation.SetName("rotations")
        self.symbol_scales = vtkDoubleArray()
        self.symbol_scales.SetName("scales")
        self.symbol_colors = vtkUnsignedCharArray()
        self.symbol_colors.SetNumberOfComponents(3)
        self.symbol_colors.SetName("colors")
        self.symbol_type = vtkIntArray()
        self.symbol_type.SetName("type")

        self.symbol_data = vtkPolyData()
        self.symbol_data.SetPoints(self.symbol_points)
        self.symbol_data.GetPointData().AddArray(self.symbol_sources)
        self.symbol_data.GetPointData().AddArray(self.symbol_rotation)
        self.symbol_data.GetPointData().AddArray(self.symbol_scales)
        self.symbol_data.GetPointData().SetScalars(self.symbol_colors)

        self.symbol_mapper = vtkGlyph3DMapper()
        self.symbol_mapper.SetInputData(self.symbol_data)
        self.symbol_mapper.SetSourceIndexArray("sources")
        self.symbol_mapper.SetOrientationArray("rotations")
        self.symbol_mapper.SetScaleArray("scales")
        self.symbol_mapper.SourceIndexingOn()
        self.symbol_mapper.ScalarVisibilityOn()
        self.symbol_mapper.SetScaleModeToScaleByMagnitude()
        self.symbol_mapper.SetScalarModeToUsePointData()
        self.symbol_mapper.SetOrientationModeToQuaternion()

        self.entity_actor = vtkActor()
        self.entity_actor.SetMapper(self.symbol_mapper)
        self.AddPart(self.entity_actor)

    def _entities(self) -> list[Entity]:
        return [symbol for symbol in self._symbols if isinstance(symbol, Entity)]

    def _markers(self) -> list[Marker]:
        return [symbol for symbol in self._symbols if isinstance(symbol, Marker)]

    def _billboards(self) -> list[Billboard]:
        return [symbol for symbol in self._symbols if isinstance(symbol, Billboard)]

    def build_entities(self):
        self.symbol_points.Reset()
        self.symbol_rotation.Reset()
        self.symbol_colors.Reset()
        self.symbol_scales.Reset()
        self.symbol_sources.Reset()

        shape_function_to_index = {}
        for symbol in self._symbols:
            if symbol.shape_function not in shape_function_to_index:
                index = len(shape_function_to_index)
                shape_function_to_index[symbol.shape_function] = index
                self.symbol_mapper.SetSourceData(index, symbol.shape_function())

            if isinstance(symbol, Entity):
                self.symbol_scales.InsertNextValue(symbol.scale)
            else:
                self.symbol_scales.InsertNextValue(1)

            if isinstance(symbol, Entity | Marker):
                quaternion = Rotation.from_euler("XYZ", symbol.orientation, degrees=True).as_quat()
                self.symbol_rotation.InsertNextTuple((quaternion[3], quaternion[0], quaternion[1], quaternion[2]))
            else:
                self.symbol_rotation.InsertNextTuple((0, 0, 0, 0))

            self.symbol_type.InsertNextValue(SymbolType.from_symbol(symbol))

            self.symbol_points.InsertNextPoint(symbol.position)
            self.symbol_colors.InsertNextTuple(symbol.color.to_rgb())
            self.symbol_sources.InsertNextValue(shape_function_to_index[symbol.shape_function])

        self.symbol_mapper.Modified()
