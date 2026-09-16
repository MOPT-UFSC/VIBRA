from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import IntEnum, auto
from functools import cache
from typing import Any

import numpy as np
from molde.colors.color import Color
from scipy.spatial.transform import Rotation
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkCommand, vtkDoubleArray, vtkIntArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkCamera, vtkGlyph3DMapper

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
    A symbol that always keeps a constant size to the viewer.
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
    def from_symbol(cls, symbol: Symbol) -> "SymbolType|None":
        return cls._class_to_type().get(type(symbol))

    @property
    def symbol_class(self) -> type[Symbol]:
        return self._type_to_class()[self]

    @classmethod
    @cache
    def _class_to_type(cls) -> dict[type[Symbol], "SymbolType"]:
        return {
            Entity: SymbolType.ENTITY,
            Marker: SymbolType.MARKER,
            Billboard: SymbolType.BILLBOARD,
        }

    @classmethod
    @cache
    def _type_to_class(cls) -> dict["SymbolType", type[Symbol]]:
        return {symbol_type: symbol_class for symbol_class, symbol_type in cls._class_to_type().items()}


class SymbolsActor(vtkActor):
    def __init__(self, camera: vtkCamera):
        super().__init__()

        self.camera = camera
        self.symbols: list[Symbol] = []
        self._create_variables()
        self._configure_actor()

    @property
    def entities(self) -> list[Entity]:
        return [symbol for symbol in self.symbols if isinstance(symbol, Entity)]

    @property
    def markers(self) -> list[Marker]:
        return [symbol for symbol in self.symbols if isinstance(symbol, Marker)]

    @property
    def billboards(self) -> list[Billboard]:
        return [symbol for symbol in self.symbols if isinstance(symbol, Billboard)]

    def _create_variables(self):
        self.symbol_points = vtkPoints()
        self.symbol_sources = vtkIntArray()
        self.symbol_rotation = vtkDoubleArray()
        self.symbol_scales = vtkDoubleArray()
        self.symbol_colors = vtkUnsignedCharArray()
        self.symbol_type = vtkIntArray()
        self.symbol_data = vtkPolyData()
        self.symbol_mapper = vtkGlyph3DMapper()

    def _configure_actor(self):
        self.camera.AddObserver(vtkCommand.ModifiedEvent, self.update_camera_callback)

        self.symbol_sources.SetName("sources")
        self.symbol_rotation.SetNumberOfComponents(4)
        self.symbol_rotation.SetName("rotations")
        self.symbol_scales.SetName("scales")
        self.symbol_colors.SetNumberOfComponents(3)
        self.symbol_colors.SetName("colors")
        self.symbol_type.SetName("type")

        self.symbol_data.SetPoints(self.symbol_points)
        self.symbol_data.GetPointData().AddArray(self.symbol_sources)
        self.symbol_data.GetPointData().AddArray(self.symbol_rotation)
        self.symbol_data.GetPointData().AddArray(self.symbol_scales)
        self.symbol_data.GetPointData().SetScalars(self.symbol_colors)

        self.symbol_mapper.SetInputData(self.symbol_data)
        self.symbol_mapper.SetSourceIndexArray("sources")
        self.symbol_mapper.SetOrientationArray("rotations")
        self.symbol_mapper.SetScaleArray("scales")
        self.symbol_mapper.SourceIndexingOn()
        self.symbol_mapper.ScalarVisibilityOn()
        self.symbol_mapper.SetScaleModeToScaleByMagnitude()
        self.symbol_mapper.SetScalarModeToUsePointData()
        self.symbol_mapper.SetOrientationModeToQuaternion()

        self.SetMapper(self.symbol_mapper)

    @function_timer
    def build(self):
        self.symbol_points.Reset()
        self.symbol_rotation.Reset()
        self.symbol_colors.Reset()
        self.symbol_scales.Reset()
        self.symbol_sources.Reset()

        shape_function_to_index = {}
        for symbol in self.symbols:
            if symbol.shape_function not in shape_function_to_index:
                index = len(shape_function_to_index)
                shape_function_to_index[symbol.shape_function] = index
                self.symbol_mapper.SetSourceData(index, symbol.shape_function())

            if isinstance(symbol, Entity):
                self.symbol_scales.InsertNextValue(symbol.scale)
            else:
                self.symbol_scales.InsertNextValue(1)

            if isinstance(symbol, Entity | Marker):
                quaternion = self._get_vector_orienting_quaternion(symbol.orientation)
                self.symbol_rotation.InsertNextTuple(quaternion)
            else:
                self.symbol_rotation.InsertNextTuple((0, 0, 0, 0))

            tp = SymbolType.from_symbol(symbol)
            if tp is not None:
                self.symbol_type.InsertNextValue(tp)

            self.symbol_points.InsertNextPoint(symbol.position)
            self.symbol_colors.InsertNextTuple(symbol.color.to_rgb())
            self.symbol_sources.InsertNextValue(shape_function_to_index[symbol.shape_function])

        self.symbol_mapper.Modified()

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
        self.symbols.append(entity)

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
        self.symbols.append(marker)

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
        self.symbols.append(billboard)

    def update_camera_callback(self, *_args: Any, **_kwargs: Any):
        points_view = vtk_to_numpy(self.symbol_points.GetData())
        scale_view = vtk_to_numpy(self.symbol_scales)
        rotation_view = vtk_to_numpy(self.symbol_rotation)
        type_view = vtk_to_numpy(self.symbol_type)

        markers = type_view == int(SymbolType.MARKER)
        billboards = type_view == int(SymbolType.BILLBOARD)

        camera_position = self.camera.GetPosition()
        diff = points_view[markers | billboards] - camera_position
        scale_view[markers | billboards] = 0.015 * np.linalg.norm(diff, axis=1)
        rotation = self._get_camera_facing_rotation()
        rotation_view[billboards] = rotation

        self.symbol_scales.Modified()
        self.symbol_data.Modified()
        self.symbol_mapper.Modified()

    def _get_camera_facing_rotation(self) -> tuple[float, float, float, float]:
        """
        Return a quaternion (w, x, y, z) that rotates the billboard so that its
        local +X axis points toward the viewer, while keeping its local +Z axis
        aligned with the camera up direction.
        """

        forward = -np.array(self.camera.GetDirectionOfProjection())
        forward /= np.linalg.norm(forward)
        up = np.array(self.camera.GetViewUp())
        right = np.cross(up, forward)
        right /= np.linalg.norm(right)
        up = np.cross(forward, right)

        matrix = np.column_stack((forward, -up, right))
        x, y, z, w = Rotation.from_matrix(matrix).as_quat("zxy")
        return w, x, y, z

    def _get_vector_orienting_quaternion(self, orientation: Sequence[float]) -> tuple[float, float, float, float]:
        """
        Return a quaternion (w, x, y, z) that rotates the symbols from its
        canonical direction (pointing toward +X) to the given direction vector.
        """
        target = np.asarray(orientation, dtype=float)
        norm = np.linalg.norm(target)
        if norm == 0:
            return (1, 0, 0, 0)

        reference = np.array([1.0, 0.0, 0.0])
        target = target / norm

        quaternion = Rotation.align_vectors(target.reshape(1, 3), reference.reshape(1, 3))[0].as_quat()
        return (quaternion[3], quaternion[0], quaternion[1], quaternion[2])
