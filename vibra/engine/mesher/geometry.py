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
        # relations
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
        self.curves = list()
        self.surfaces = list()
        self.solids = list()

        self.length_unit = length_unit
        self.length_unit_factor = self._get_length_unit_factor

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
        old_factor = self.length_unit_factor
        new_factor = self._get_length_unit_factor(length_unit)
        scale = old_factor / new_factor

        centers = [
            self._solids_centers,
            self._surfaces_centers,
            self._curves_centers,
            self._points_centers
        ]

        for center in centers:
            for key, value in center.items():
                center[key] = value * scale

        for key, value in self._curves_lengths.items():
            self._curves_lengths[key] = value * scale
        
        for key, value in self._surfaces_areas.items():
            self._surfaces_areas[key] = value * (scale**2)

        for key, value in self._solids_volumes.items():
            self._solids_volumes[key] = value * (scale**3)

        self.length_unit = length_unit 
        self.length_unit_factor = new_factor

    def points_to_curves(self, *point_ids: int) -> Iterator[int]:
        for point_id in point_ids:
            for curve_id in self._curves_to_points.inverse.get(point_id, []):
                yield curve_id

    def points_to_surfaces(self, *point_ids: int) -> Iterator[int]:
        for curve_id in self.points_to_curves(*point_ids):
            for surface_id in self._surfaces_to_curves.inverse.get(curve_id, []):
                yield surface_id

    def points_to_solids(self, *point_ids: int) -> Iterator[int]:
        for curve_id in self.points_to_curves(*point_ids):
            for surface_id in self._surfaces_to_curves.inverse.get(curve_id, []):
                for solid_id in self._solids_to_surfaces.inverse.get(surface_id, []):
                    yield solid_id

    def curves_to_points(self, *curve_ids: int) -> Iterator[int]:
        for curve_id in curve_ids:
            for point_id in self._curves_to_points.get(curve_id, []):
                yield point_id

    def curves_to_surfaces(self, *curve_ids: int) -> Iterator[int]:
        for curve_id in curve_ids:
            for surface_id in self._surfaces_to_curves.inverse.get(curve_id, []):
                yield surface_id

    def curves_to_solids(self, *curve_ids: int) -> Iterator[int]:
        for surface_id in self.curves_to_surfaces(*curve_ids):
            for solid_id in self._solids_to_surfaces.inverse.get(surface_id, []):
                yield solid_id

    def surfaces_to_curves(self, *surface_ids: int) -> Iterator[int]:
        for surface_id in surface_ids:
            for curve_id in self._surfaces_to_curves.get(surface_id, []):
                yield curve_id

    def surfaces_to_points(self, *surface_ids: int) -> Iterator[int]:
        for curve_id in self.surfaces_to_curves(*surface_ids):
            for point_id in self._curves_to_points.get(curve_id, []):
                yield point_id

    def surfaces_to_solids(self, *surface_ids: int) -> Iterator[int]:
        for surface_id in surface_ids:
            for solid_id in self._solids_to_surfaces.inverse.get(surface_id, []):
                yield solid_id

    def solids_to_points(self, *volume_ids: int) -> Iterator[int]:
        for surface_id in self.solids_to_surfaces(*volume_ids):
            for curve_id in self._surfaces_to_curves.get(surface_id, []):
                for point_id in self._curves_to_points.get(curve_id, []):
                    yield point_id

    def solids_to_curves(self, *volume_ids: int) -> Iterator[int]:
        for surface_id in self.solids_to_surfaces(*volume_ids):
            for curve_id in self._surfaces_to_curves.get(surface_id, []):
                yield curve_id

    def solids_to_surfaces(self, *volume_ids: int) -> Iterator[int]:
        for volume_id in volume_ids:
            for surface_id in self._solids_to_surfaces.get(volume_id, []):
                yield surface_id

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

    def arc_length(self, *curve_ids: int) -> float:
        return sum(self._curves_lengths[curve_id] for curve_id in curve_ids)

    def surface_area(self, *surface_ids: int) -> float:
        return sum(self._surfaces_areas[surface_id] for surface_id in surface_ids)

    def volume(self, *volume_ids: int) -> float:
        return sum(self._solids_volumes[volume_id] for volume_id in volume_ids)

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
                self.solids.append(tag)

            elif dim == 2:
                self._surfaces_areas[tag] = mass * (self.length_unit_factor**2)
                self._surfaces_to_curves[tag] = tuple(downwards)
                self.surfaces.append(tag)

            elif dim == 1:
                self._curves_lengths[tag] = mass * (self.length_unit_factor**1)
                self._curves_to_points[tag] = tuple(downwards)
                self.curves.append(tag)

    def _get_length_unit_factor(self, length_unit: LengthUnits) -> float:
        if length_unit == "milimeter":
            return 1e-3
        elif length_unit == "inch":
            return 0.0254
        else:
            raise ValueError(f'Invalid length unit "{length_unit}"')
