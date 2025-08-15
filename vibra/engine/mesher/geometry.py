from pathlib import Path
from typing import Iterator, Literal

import gmsh
import numpy as np

from vibra.utils.bidict import bidict

LengthUnits = Literal["milimeter", "inch"]


class Geometry:
    def __init__(
        self,
        path: str | Path | None = None,
        length_unit: LengthUnits = "milimeter",
    ):
        # connectivity
        self._solids_to_surfaces = bidict()
        self._surfaces_to_curves = bidict()
        self._curves_to_points = bidict()

        # centers
        self._solids_centers = dict()
        self._surfaces_centers = dict()
        self._curves_centers = dict()
        self._points_centers = dict()

        # normals
        self._surfaces_normals = dict()
        self._curves_normals = dict()
        self._points_normals = dict()

        # areas
        self._surfaces_areas = dict()
        self._curves_lengths = dict()
        self._solids_volumes = dict()

        # curvatures
        self._straight_curves = set()
        self._straight_surfaces = set()

        # About geometry information
        self.points = list()
        self.lines = list()
        self.surfaces = list()
        self.volumes = list()

        self.set_length_unit(length_unit)
        if path is not None:
            self.read_file(path)

    def read_file(self, file_path: str):
        gmsh.initialize()
        gmsh.open(file_path)

        gmsh.model.occ.synchronize()

        self._process_geometry_information()
        gmsh.finalize()

    def clear(self):
        self._solids_to_surfaces.clear()
        self._surfaces_to_curves.clear()
        self._curves_to_points.clear()

        # centers
        self._solids_centers.clear()
        self._surfaces_centers.clear()
        self._curves_centers.clear()
        self._points_centers.clear()

        # normals
        self._surfaces_normals.clear()
        self._curves_normals.clear()
        self._points_normals.clear()

        # areas
        self._surfaces_areas.clear()
        self._curves_lengths.clear()

        self._solids_volumes.clear()

        self._straight_curves.clear()
        self._straight_surfaces.clear()

    def set_length_unit(self, length_unit: LengthUnits):
        self.length_unit = length_unit
        self.length_unit_factor = self._get_length_unit_factor(length_unit)

        # You should not modify the lenght unit after reading the geometry
        # because it is misleading unless you correct all values.
        # TODO: replace this clear by a function that converts all length units.
        self.clear()

    def points_to_curves(self, *point_ids: int) -> Iterator[int]:
        for point_id in point_ids:
            for curve_id in self._curves_to_points.inverse.get(point_id, []):
                yield curve_id

    def points_to_surfaces(self, *point_ids: int) -> Iterator[int]:
        for curve_in in self.points_to_curves(*point_ids):
            for surface_id in self._surfaces_to_curves.inverse.get(curve_in, []):
                yield surface_id

    def points_to_solids(self, *point_ids: int) -> Iterator[int]:
        pass

    def curves_to_points(self, *line_ids: int) -> Iterator[int]:
        pass

    def curves_to_surfaces(self, *line_ids: int) -> Iterator[int]:
        pass

    def curves_to_solids(self, *line_ids: int) -> Iterator[int]:
        pass

    def surfaces_to_points(self, *surface_ids: int) -> Iterator[int]:
        pass

    def surfaces_to_curves(self, *surface_ids: int) -> Iterator[int]:
        pass

    def surfaces_to_solids(self, *surface_ids: int) -> Iterator[int]:
        pass

    def solids_to_points(self, *volume_ids: int) -> Iterator[int]:
        pass

    def solids_to_curves(self, *volume_ids: int) -> Iterator[int]:
        pass

    def solids_to_surfaces(self, *volume_ids: int) -> Iterator[int]:
        pass

    def is_curve_straight(self, curve_id: int) -> bool:
        return curve_id in self._straight_curves

    def is_surface_straight(self, surface_id: int) -> bool:
        return surface_id in self._straight_surfaces

    def solid_center(self, solid_id: int) -> np.ndarray | None:
        return self._solids_centers.get(solid_id)

    def surface_center(self, surface_id: int) -> np.ndarray | None:
        return self._surfaces_centers.get(surface_id)

    def curve_center(self, curve_id: int) -> np.ndarray | None:
        return self._curves_centers.get(curve_id)

    def point_center(self, point_id: int) -> np.ndarray | None:
        return self._points_centers.get(point_id)

    def surface_normal(self, surface_id: int) -> np.ndarray | None:
        return self._surfaces_normals.get(surface_id)

    def curve_normal(self, curve_id: int) -> np.ndarray | None:
        return self._curves_normals.get(curve_id)

    def point_normal(self, point_id: int) -> np.ndarray | None:
        return self._points_normals.get(point_id)

    def _process_geometry_information(self):
        self.clear()

        for dim, tag in gmsh.model.getEntities():
            _, downwards = gmsh.model.getAdjacencies(dim, tag)
            downwards = [int(_id) for _id in downwards]

            if dim == 0:
                self.points.append(tag)
                continue

            mass = gmsh.model.occ.getMass(dim, tag)

            if dim == 3:
                self._solids_volumes[tag] = mass * (self.length_unit_factor**3)
                self._solids_to_surfaces[tag] = tuple(downwards)
                self.volumes.append(tag)

            elif dim == 2:
                self._surfaces_areas[tag] = mass * (self.length_unit_factor**2)
                self._surfaces_to_curves[tag] = tuple(downwards)
                self.surfaces.append(tag)

            elif dim == 1:
                self._curves_lengths[tag] = mass * (self.length_unit_factor**1)
                self._curves_to_points[tag] = tuple(downwards)
                self.lines.append(tag)

    def _get_length_unit_factor(self, length_unit: LengthUnits) -> float:
        if length_unit == "milimeter":
            return 1e-3
        elif length_unit == "inch":
            return 0.0254
        else:
            raise ValueError(f'Invalid length unit "{length_unit}"')
