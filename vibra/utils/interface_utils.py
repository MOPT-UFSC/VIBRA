from dataclasses import dataclass
from enum import IntEnum, auto

import numpy as np
from vtkmodules.vtkRenderingCore import vtkCoordinate

window_title = "Error"


class ColorMode(IntEnum):
    EMPTY = auto()
    MATERIAL = auto()
    FLUID = auto()


@dataclass
class VisualizationFilter:
    points: bool = False
    lines: bool = False
    faces: bool = False
    solids: bool = False
    acoustic_symbols: bool = False
    structural_symbols: bool = False
    ghost: bool = True
    color_mode: ColorMode = ColorMode.EMPTY

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
