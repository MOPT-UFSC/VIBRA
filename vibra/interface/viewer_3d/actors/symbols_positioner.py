from collections import defaultdict

import numpy as np
from scipy.linalg import svd

from vibra.engine.mesher.mesh import Mesh


class SymbolsPositioner:
    def __init__(self, mesh, margin_factor: float = 0.25):
        self.mesh: Mesh = mesh

        self.margin_factor = margin_factor # how close is from the border

        self._surface_symbol_counts: dict[int, int] = defaultdict(int)
        self._surface_symbol_totals: dict[int, int] = dict()
        self._surface_position_cache: dict[int, tuple[np.ndarray, np.ndarray]] = dict()

    def reset_count(self, surface_symbol_totals: dict[int, int]):
        self._surface_symbol_counts.clear()
        self._surface_symbol_totals = dict(surface_symbol_totals)
        self._surface_position_cache.clear()

    def next_surface_position(self, surface_id: int, center_coords: np.ndarray, normal: np.ndarray, surface_coordinates: np.ndarray) -> np.ndarray:
        symbol_index = self._surface_symbol_counts[surface_id]
        self._surface_symbol_counts[surface_id] += 1
        total_symbols = self._surface_symbol_totals.get(surface_id, 1)

        if total_symbols <= 1:
            return center_coords

        cached_data = self._surface_position_cache.get(surface_id)
        if cached_data is None:
            cached_data = self._get_surface_axis_and_positions(surface_id, center_coords, normal, surface_coordinates, total_symbols)
            if cached_data is None:
                return center_coords

            self._surface_position_cache[surface_id] = cached_data

        axis, positions = cached_data

        if symbol_index >= len(positions):
            return center_coords

        return center_coords + positions[symbol_index] * axis

    def get_surface_boundary_coordinates(self, surface_id: int) -> np.ndarray | None:
        line_ids = self.mesh.lines_from_surface.get(surface_id, [])
        boundary_nodes = set()

        for line_id in line_ids:
            if (nodes := self.mesh.get_nodes_from_line(line_id)) is not None:
                boundary_nodes.update(nodes)

        if boundary_nodes:
            boundary_nodes = np.fromiter(boundary_nodes, dtype=int)
            return self.mesh.nodal_coordinates[boundary_nodes, 1:]

        return None

    def _get_surface_axis_and_positions(
        self,
        surface_id: int,
        center_coords: np.ndarray,
        normal: np.ndarray,
        surface_coordinates: np.ndarray,
        total_symbols: int,
    ) -> tuple[np.ndarray, np.ndarray] | None:

        normal_norm = np.linalg.norm(normal)
        unit_normal = normal / normal_norm

        if (limit_coordinates := self.get_surface_boundary_coordinates(surface_id)) is None:
            limit_coordinates = surface_coordinates

        vectors_from_center = limit_coordinates - center_coords
        # remove projections on normal
        plane_vectors = vectors_from_center - np.outer(vectors_from_center @ unit_normal, unit_normal)

        _, _, vh = svd(plane_vectors, full_matrices=False, compute_uv=True)
        axis = vh[0]

        projections = plane_vectors @ axis
        min_projection = np.min(projections)
        max_projection = np.max(projections)
        span = max_projection - min_projection

        margin = self.margin_factor * span
        positions = np.linspace(min_projection + margin, max_projection - margin, total_symbols)

        return axis, positions
