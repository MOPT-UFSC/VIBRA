import builtins
import functools
import hashlib
import inspect
from collections.abc import Callable, Generator
from contextlib import contextmanager
from dataclasses import dataclass, fields
from enum import Enum, IntEnum, auto
from functools import partial, wraps
from typing import Any

import numpy as np
from molde.colors import Color, color_names
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget
from vtkmodules.vtkRenderingCore import vtkCoordinate

window_title = "Error"


class GeometryColorMode(IntEnum):
    EMPTY = auto()
    COLORED = auto()
    MATERIAL = auto()
    FLUID = auto()


@dataclass
class VisualizationFilter:
    points: bool = False
    lines: bool = False
    faces: bool = False
    solids: bool = False
    symbols: bool = False
    ghost: bool = True
    nodal_normal_symbols: bool = False
    element_normal_symbols: bool = False
    color_mode: GeometryColorMode = GeometryColorMode.COLORED

    @classmethod
    def all_false(cls):
        obj = cls()
        for field in fields(obj):
            if isinstance(getattr(obj, field.name), bool):
                setattr(obj, field.name, False)
        return obj

    @classmethod
    def all_true(cls):
        obj = cls()
        for field in fields(obj):
            if isinstance(getattr(obj, field.name), bool):
                setattr(obj, field.name, True)
        return obj


@dataclass
class GeometryRendererConfig:
    points_color: Color = color_names.WHITE
    lines_color: Color = color_names.WHITE
    surfaces_color: Color = color_names.WHITE
    selected_points_color: Color = color_names.RED
    selected_lines_color: Color = color_names.RED
    selected_surfaces_color: Color = color_names.BLUE
    points_size: int = 15
    lines_thickness: int = 3


@dataclass
class MeshRendererConfig:
    nodes_color: Color = color_names.YELLOW_5
    edges_color: Color = color_names.BLACK
    surfaces_color: Color = color_names.WHITE
    volumes_color: Color = color_names.GRAY_7
    selected_nodes_color: Color = color_names.RED
    selected_edges_color: Color = color_names.RED
    selected_surfaces_color: Color = color_names.BLUE_6
    selected_volumes_color: Color = color_names.BLUE
    nodes_size: int = 10
    edges_thickness: int = 1


@dataclass(frozen=True)
class SectionPlane:
    class SectionPlaneMode(Enum):
        DISABLED = auto()
        PREVIEWING = auto()
        CUTTING = auto()

    origin: tuple[float, float, float]
    normal: tuple[float, float, float]
    invert_value: bool = False
    mode: SectionPlaneMode = SectionPlaneMode.CUTTING

    def get_normal(self) -> tuple[float, float, float]:
        if self.invert_value:
            return tuple(-i for i in self.normal)  # pyright: ignore[reportReturnType]
        return self.normal


@contextmanager
def block_signals[T: QWidget](widget: T) -> Generator[T, None, None]:
    widget.blockSignals(True)
    try:
        yield widget
    finally:
        widget.blockSignals(False)


@contextmanager
def disable_updates(widget: QWidget):
    widget.setUpdatesEnabled(False)
    try:
        yield widget
    finally:
        widget.setUpdatesEnabled(True)


def qt_run_delayed(function):
    """
    Apparently sometimes qt needs a delay to correctly update its internal state.
    This decorator delays a function so they can propperly function.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        QTimer.singleShot(0, partial(function, *args, **kwargs))

    return wrapper


def world_to_screen_coords(xyz, renderer):
    coordinate = vtkCoordinate()
    coordinate.SetCoordinateSystemToWorld()
    coordinate.SetValue(xyz)
    view_coords = coordinate.GetComputedViewportValue(renderer)
    return np.array(view_coords)


def screen_to_world_coords(xyz, renderer):
    coordinate = vtkCoordinate()
    coordinate.SetCoordinateSystemToViewport()
    coordinate.SetValue(xyz)
    world_coords = coordinate.GetComputedWorldValue(renderer)
    return np.array(world_coords)


def qt_extensions(extensions: list[str]) -> str:
    return " ".join(f"*.{ext.upper()} *.{ext.lower()}" for ext in extensions)


def preview_cache[T: Callable[..., Any]](func: T) -> T:
    source_code = inspect.getsource(func)
    func_hash = hashlib.md5(source_code.encode("utf-8")).hexdigest()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_store = getattr(builtins, "__HOT_RELOAD_CACHE__", {})

        key = (func.__name__, func_hash, args, frozenset(kwargs.items()))

        if key not in cache_store:
            cache_store[key] = func(*args, **kwargs)

        return cache_store[key]

    return wrapper  # pyright: ignore[reportReturnType]
