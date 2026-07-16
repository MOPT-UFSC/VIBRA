from contextlib import contextmanager
from dataclasses import dataclass
from enum import IntEnum, auto
from functools import partial, wraps
from typing import Generator, TypeVar

import numpy as np
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
    normal_symbols: bool = False
    color_mode: GeometryColorMode = GeometryColorMode.COLORED

    @classmethod
    def all_false(cls):
        # It is dumb, but it works
        args = [False] * 7
        return cls(*args)

    @classmethod
    def all_true(cls):
        # It is dumb, but it works
        args = [True] * 7
        return cls(*args)


T = TypeVar("T", bound=QWidget)


@contextmanager
def block_signals(widget: T) -> Generator[T, None, None]:
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
