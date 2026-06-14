from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

from molde import Color
from vibra import app
import numpy as np
import numpy.typing as npt


@dataclass
class SymbolProperty:
    shape: Callable
    coords: np.ndarray
    normal: np.ndarray
    color: Color


class SymbolsPositioner:
    def __init__(self) -> None:
        self._property_symbols_dict: dict[int, list[SymbolProperty]] = defaultdict(list)

    def reset_properties_count(self):
        self._property_symbols_dict.clear()

    def add_property(self, surface_id: int, shape: Callable, coords: np.ndarray, normal: np.ndarray, color: Color):
        if coords.shape != (3,) or normal.shape != (3,):
            raise ValueError(f"Expected a 1D array with exactly 3 elements, got shape {coords.shape=} and {normal.shape=}")

        self._property_symbols_dict[surface_id].append(SymbolProperty(shape, coords, normal, color))

    def positioned_symbols(self):
        for surface_id, symbols in self._property_symbols_dict.items():
            if len(symbols) == 1:
                yield symbols[0]
                continue

            normal = symbols[0].normal
            center = symbols[0].coords
            spacing_radius, axis_1, axis_2 = self._get_surface_symbol_layout_frame(surface_id, normal)
            coords = self._calculate_ring_position(axis_1, axis_2, spacing_radius, len(symbols))

            for i, symbol in enumerate(symbols):
                yield SymbolProperty(symbol.shape, coords[i] + center, symbol.normal, symbol.color)

    def _get_surface_symbol_layout_frame(self, surface_id: int, normal: npt.NDArray[np.float64]) -> tuple[float, npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        if surface_id < 0:
            raise ValueError("surface_id must be >= than 0")
        if normal.shape != (3,):
            raise ValueError(f"Expected a 1D array with exactly 3 elements, got shape {normal.shape=}")

        normal_ = np.asarray(normal, dtype=float)
        normal_norm = np.linalg.norm(normal_)
        normal_ /= normal_norm

        refer = np.array([1.0, 0.0, 0.0])
        if abs(np.dot(normal_, refer)) > 0.9:
            refer = np.array([0.0, 1.0, 0.0])

        axis_1 = np.cross(normal_, refer)
        axis_1_norm = np.linalg.norm(axis_1)
        axis_1 /= axis_1_norm

        axis_2 = np.cross(axis_1, normal_)
        axis_2_norm = np.linalg.norm(axis_2)
        axis_2 /= axis_2_norm

        if (mesh := app().project.model.mesh) is None:
            return 0, axis_1, axis_2
        if (surface_nodes := mesh.get_nodes_from_surface(surface_id)) is None:
            return 0, axis_1, axis_2
        if mesh.nodal_coordinates is None:
            return 0, axis_1, axis_2
        if (surface_coordinates := mesh.nodal_coordinates[surface_nodes, 1:]) is None:
            return 0, axis_1, axis_2

        width = np.ptp(surface_coordinates @ axis_1)
        height = np.ptp(surface_coordinates @ axis_2)
        min_size = min(width, height)

        return min_size / 4, axis_1, axis_2

    def _calculate_ring_position(
        self, ort1: npt.NDArray[np.float64], ort2: npt.NDArray[np.float64], radius: float, n_vertices: int
    ) -> npt.NDArray[np.float64]:
        if n_vertices < 2:
            return np.array([0, 0, 0])

        angle = 2 * np.pi / float(n_vertices)

        points = np.asarray([np.sin(i * angle) * ort1 + np.cos(i * angle) * ort2 for i in range(n_vertices)])
        points *= radius

        return points
