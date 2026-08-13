from pathlib import Path
from typing import Literal

import gmsh
import numpy as np

from vibra.utils.bidict import bidict

LengthUnits = Literal["millimeter", "inch"]


class Geometry:
    def __init__(
        self,
        path: str | Path | None = None,
        length_unit: LengthUnits = "millimeter",
    ):
        self._solids_to_surfaces = bidict()
        self._surfaces_to_curves = bidict()
        self._curves_to_points = bidict()

        self._solids_centers = dict()
        self._surfaces_centers = dict()
        self._curves_centers = dict()
        self._points_centers = dict()

        self._surfaces_normals = dict()
        self._curves_normals = dict()
        self._points_normals = dict()

        self._surfaces_areas = dict()
        self._curves_lengths = dict()
        self._solids_volumes = dict()

        self._straight_curves = set()
        self._straight_surfaces = set()

        # About geometry information
        self.points = list()
        self.curves = list()
        self.surfaces = list()
        self.solids = list()

        self.length_unit = length_unit
        self.length_unit_factor = self._get_length_unit_factor(length_unit)

        self.set_length_unit(length_unit)
        if path is not None:
            self.read_file(path)

    def read_file(self, file_path: str):
        # allowed to run in a secondary thread
        gmsh.initialize("", False, interruptible=False)

        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", 0)  # all available threads

        gmsh.open(file_path)

        gmsh.model.occ.synchronize()

        self._process_geometry_information()
        self._process_curves_normals()
        self._process_points_normals()

        gmsh.finalize()

    def clear(self):
        self._solids_to_surfaces.clear()
        self._surfaces_to_curves.clear()
        self._curves_to_points.clear()

        self._solids_centers.clear()
        self._surfaces_centers.clear()
        self._curves_centers.clear()
        self._points_centers.clear()

        self._surfaces_normals.clear()
        self._curves_normals.clear()
        self._points_normals.clear()

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
            self._points_centers,
        ]

        for center in centers:
            for key, value in center.items():
                if value.any():
                    center[key] = value * scale

        for key, value in self._curves_lengths.items():
            if value:
                self._curves_lengths[key] = value * scale

        for key, value in self._surfaces_areas.items():
            if value:
                self._surfaces_areas[key] = value * (scale**2)

        for key, value in self._solids_volumes.items():
            if value:
                self._solids_volumes[key] = value * (scale**3)

        self.length_unit = length_unit
        self.length_unit_factor = new_factor

    def points_to_curves(self, *point_ids: int) -> set[int]:
        """Get all curves connected to the given points."""
        curves_set = set()
        for point_id in point_ids:
            for points_tuple, curve_id in self._curves_to_points.inverse.items():
                if point_id in points_tuple:
                    curves_set.add(curve_id[0])
        return curves_set

    def points_to_surfaces(self, *point_ids: int) -> set[int]:
        """Get all surfaces connected to the given points."""
        surfaces_set = set()
        for curve_id in self.points_to_curves(*point_ids):
            for curves_tuple, surface_id in self._surfaces_to_curves.inverse.items():
                if curve_id in curves_tuple:
                    surfaces_set.add(surface_id[0])
        return surfaces_set

    def points_to_solids(self, *point_ids: int) -> set[int]:
        """Get all solids connected to the given points."""
        solids_set = set()
        for surface_id in self.points_to_surfaces(*point_ids):
            for surfaces_tuple, solid_id in self._solids_to_surfaces.inverse.items():
                if surface_id in surfaces_tuple:
                    solids_set.add(solid_id[0])
        return solids_set

    def curves_to_points(self, *curve_ids: int) -> set[int]:
        """Get all points connected to the given curves."""
        points_set = set()
        for curve_id in curve_ids:
            for point_id in self._curves_to_points.get(curve_id, []):
                points_set.add(point_id)
        return points_set

    def curves_to_surfaces(self, *curve_ids: int) -> set[int]:
        """Get all surfaces connected to the given curves."""
        surfaces_set = set()
        for curve_id in curve_ids:
            for curves_tuple, surface_id in self._surfaces_to_curves.inverse.items():
                if curve_id in curves_tuple:
                    surfaces_set.add(surface_id[0])
        return surfaces_set

    def curves_to_solids(self, *curve_ids: int) -> set[int]:
        """Get all solids connected to the given curves."""
        solids_set = set()
        for surface_id in self.curves_to_surfaces(*curve_ids):
            for surfaces_tuple, solid_id in self._solids_to_surfaces.inverse.items():
                if surface_id in surfaces_tuple:
                    solids_set.add(solid_id[0])
        return solids_set

    def surfaces_to_curves(self, *surface_ids: int) -> set[int]:
        """Get all curves connected to the given surfaces."""
        curves_set = set()
        for surface_id in surface_ids:
            for curve_id in self._surfaces_to_curves.get(surface_id, []):
                curves_set.add(curve_id)
        return curves_set

    def surfaces_to_points(self, *surface_ids: int) -> set[int]:
        """Get all points connected to the given surfaces."""
        points_set = set()
        for curve_id in self.surfaces_to_curves(*surface_ids):
            for point_id in self._curves_to_points.get(curve_id, []):
                points_set.add(point_id)
        return points_set

    def surfaces_to_solids(self, *surface_ids: int) -> set[int]:
        """Get all solids connected to the given surfaces."""
        solids_set = set()
        for surface_id in surface_ids:
            for surfaces_tuple, solid_id in self._solids_to_surfaces.inverse.items():
                if surface_id in surfaces_tuple:
                    solids_set.add(solid_id[0])
        return solids_set

    def solids_to_points(self, *volume_ids: int) -> set[int]:
        """Get all points connected to the given solids."""
        points_set = set()
        for surface_id in self.solids_to_surfaces(*volume_ids):
            for curve_id in self._surfaces_to_curves.get(surface_id, []):
                for point_id in self._curves_to_points.get(curve_id, []):
                    points_set.add(point_id)
        return points_set

    def solids_to_curves(self, *volume_ids: int) -> set[int]:
        """Get all curves connected to the given solids."""
        curves_set = set()
        for surface_id in self.solids_to_surfaces(*volume_ids):
            for curve_id in self._surfaces_to_curves.get(surface_id, []):
                curves_set.add(curve_id)
        return curves_set

    def solids_to_surfaces(self, *volume_ids: int) -> set[int]:
        """Get all surfaces connected to the given solids."""
        surfaces_set = set()
        for volume_id in volume_ids:
            for surface_id in self._solids_to_surfaces.get(volume_id, []):
                surfaces_set.add(surface_id)
        return surfaces_set

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
        """Process and store geometry information (length, areas, volumes, centers, etc.) from the Gmsh model."""
        self.clear()

        for dim, tag in gmsh.model.getEntities():
            _, downwards = gmsh.model.getAdjacencies(dim, tag)
            downwards = [int(_id) for _id in downwards]

            mass = gmsh.model.occ.getMass(dim, tag)

            if dim == 3:
                self._solids_volumes[tag] = mass * (self.length_unit_factor**3)
                self._solids_to_surfaces[tag] = tuple(downwards)
                self.solids.append(tag)

                center, _ = self.process_center_element(dim, tag)
                self._solids_centers[tag] = center

            elif dim == 2:
                self._surfaces_areas[tag] = mass * (self.length_unit_factor**2)
                self._surfaces_to_curves[tag] = tuple(downwards)
                self.surfaces.append(tag)

                center, uv_mid = self.process_center_element(dim, tag)
                self._surfaces_centers[tag] = center

                normal = gmsh.model.getNormal(tag, uv_mid)
                curvature = gmsh.model.getCurvature(dim, tag, uv_mid)

                self._surfaces_normals[tag] = normal

                if np.any(np.isclose(curvature, 0, atol=1e-8)):
                    self._straight_surfaces.add(tag)

            elif dim == 1:
                self._curves_lengths[tag] = mass * (self.length_unit_factor**1)
                self._curves_to_points[tag] = tuple(downwards)
                self.curves.append(tag)

                center, uv_mid = self.process_center_element(dim, tag)
                center = (
                    gmsh.model.get_value(dim, tag, uv_mid) * self.length_unit_factor
                )
                curvature = gmsh.model.getCurvature(dim, tag, uv_mid)

                self._curves_centers[tag] = center
                if np.any(np.isclose(curvature, 0, atol=1e-8)):
                    self._straight_curves.add(tag)

            elif dim == 0:
                self.points.append(tag)
                center, uv_mid = self.process_center_element(dim, tag)
                center = (
                    gmsh.model.get_value(dim, tag, uv_mid) * self.length_unit_factor
                )
                self._points_centers[tag] = center

    def _process_curves_normals(self):
        for curve in self.curves:
            center_coord = self._curves_centers[curve]
            adjacent_surfaces = set(self.curves_to_surfaces(curve))

            normals_sum = np.zeros(3)
            for surface in adjacent_surfaces:
                center_uv = gmsh.model.get_parametrization(2, surface, center_coord)
                normals_sum += gmsh.model.get_normal(surface, center_uv)

            self._curves_normals[curve] = normals_sum / np.linalg.norm(normals_sum)

    def _process_points_normals(self):
        for point in self.points:
            center_coord = self._points_centers[point]
            adjacent_surfaces = set(self.points_to_surfaces(point))

            normals_sum = np.zeros(3)
            for surface in adjacent_surfaces:
                center_uv = gmsh.model.get_parametrization(2, surface, center_coord)
                normals_sum += gmsh.model.get_normal(surface, center_uv)

            self._points_normals[point] = normals_sum / np.linalg.norm(normals_sum)

    def process_center_element(self, dim: int, tag: int) -> np.ndarray:
        """Process the center of an element based on its dimension."""
        if dim != 3:
            uv_min, uv_max = gmsh.model.get_parametrization_bounds(dim, tag)
            uv_mid = (uv_min + uv_max) / 2
            center = gmsh.model.get_value(dim, tag, uv_mid) * self.length_unit_factor
            
        else:
            center = np.asarray(gmsh.model.occ.getCenterOfMass(dim, tag)) * self.length_unit_factor
            uv_mid = None
        
        return center, uv_mid

    def _get_length_unit_factor(self, length_unit: LengthUnits) -> float:
        if length_unit == "millimeter":
            return 1e-3
        elif length_unit == "inch":
            return 0.0254
        else:
            raise ValueError(f'Invalid length unit "{length_unit}"')
