from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Iterator, Literal

import gmsh
import numpy as np

LengthUnits = Literal["millimeter", "inch"]


class Geometry:
    def __init__(
        self,
        path: str | Path | None = None,
        length_unit: LengthUnits = "millimeter",
    ):
        self._solids_to_surfaces = defaultdict()
        self._surfaces_to_curves = defaultdict()
        self._curves_to_points = defaultdict()

        self._surfaces_to_solids = defaultdict()
        self._curves_to_surfaces = defaultdict()
        self._points_to_curves = defaultdict()

        self._cache_solids_to_surfaces = defaultdict()
        self._cache_surfaces_to_curves = defaultdict()
        self._cache_curves_to_points = defaultdict()

        self._solids_centers = defaultdict()
        self._surfaces_centers = defaultdict()
        self._curves_centers = defaultdict()
        self._points_centers = defaultdict()

        self._surfaces_normals = defaultdict()
        self._curves_normals = defaultdict()
        self._points_normals = defaultdict()

        self._surfaces_areas = defaultdict()
        self._curves_lengths = defaultdict()
        self._solids_volumes = defaultdict()

        self._bounding_lines = defaultdict()
        self._bounding_surfaces = defaultdict() 
        self._bounding_solids = defaultdict() 

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

        volumes_list = gmsh.model.getEntities(3)
        gmsh.model.occ.fragment(volumes_list, volumes_list)
        gmsh.model.occ.synchronize()

        self._process_geometry_information()
        self._process_curves_normals()
        self._process_points_normals()
        gmsh.finalize()

    def clear(self):
        self._solids_to_surfaces.clear()
        self._surfaces_to_curves.clear()
        self._curves_to_points.clear()

        self._surfaces_to_solids.clear()
        self._curves_to_surfaces.clear()
        self._points_to_curves.clear()

        self._cache_solids_to_surfaces.clear()
        self._cache_surfaces_to_curves.clear()
        self._cache_curves_to_points.clear()

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

        self._bounding_lines.clear()
        self._bounding_surfaces.clear()
        self._bounding_solids.clear()

        self._straight_curves.clear()
        self._straight_surfaces.clear()

        self.points.clear()
        self.curves.clear()
        self.surfaces.clear()
        self.solids.clear()

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
            curves_set.update(self._points_to_curves.get(point_id, []))
        return curves_set

    def points_to_surfaces(self, *point_ids: int) -> set[int]:
        """Get all surfaces connected to the given points."""
        connected_curves = self.points_to_curves(*point_ids)
        return self.curves_to_surfaces(*connected_curves)

    def points_to_solids(self, *point_ids: int) -> set[int]:
        """Get all solids connected to the given points."""
        connected_surfaces = self.points_to_surfaces(*point_ids)
        return self.surfaces_to_solids(*connected_surfaces)

    def curves_to_points(self, *curve_ids: int) -> set[int]:
        """Get all points connected to the given curves."""
        points_set = set()
        for curve_id in curve_ids:
            points_set.update(self._curves_to_points.get(curve_id, []))
        return points_set

    def curves_to_surfaces(self, *curve_ids: int) -> set[int]:
        """Get all surfaces connected to the given curves."""
        surfaces_set = set()
        for curve_id in curve_ids:
            surfaces_set.update(self._curves_to_surfaces.get(curve_id, []))
        return surfaces_set

    def curves_to_solids(self, *curve_ids: int) -> set[int]:
        """Get all solids connected to the given curves."""
        connected_surfaces = self.curves_to_surfaces(*curve_ids)
        return self.surfaces_to_solids(*connected_surfaces)

    def surfaces_to_curves(self, *surface_ids: int) -> set[int]:
        """Get all curves connected to the given surfaces."""
        curves_set = set()
        for surface_id in surface_ids:
            curves_set.update(self._surfaces_to_curves.get(surface_id, []))
        return curves_set

    def surfaces_to_points(self, *surface_ids: int) -> set[int]:
        """Get all points connected to the given surfaces."""
        connected_curves = self.surfaces_to_curves(*surface_ids)
        return self.curves_to_points(*connected_curves)

    def surfaces_to_solids(self, *surface_ids: int) -> set[int]:
        """Get all solids connected to the given surfaces."""
        solids_set = set()
        for surface_id in surface_ids:
            solids_set.update(self._surfaces_to_solids.get(surface_id, []))
        return solids_set

    def solids_to_points(self, *volume_ids: int) -> set[int]:
        """Get all points connected to the given solids."""
        connected_curves = self.solids_to_curves(*volume_ids)
        return self.curves_to_points(*connected_curves)

    def solids_to_curves(self, *volume_ids: int) -> set[int]:
        """Get all curves connected to the given solids."""
        connected_surfaces = self.solids_to_surfaces(*volume_ids)
        return self.surfaces_to_curves(*connected_surfaces)

    def solids_to_surfaces(self, *volume_ids: int) -> set[int]:
        """Get all surfaces connected to the given solids."""
        surfaces_set = set()
        for volume_id in volume_ids:
            surfaces_set.update(self._solids_to_surfaces.get(volume_id, []))
        return surfaces_set

    def is_curve_straight(self, curve_id: int) -> bool:
        return curve_id in self._straight_curves

    def is_surface_straight(self, surface_id: int) -> bool:
        return surface_id in self._straight_surfaces

    def are_there_volumes_in_geometry(self) -> bool:
        return bool(self.solids)

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
        """Process and store geometry information (lenghts, areas, volumes, centers, etc.) from the Gmsh model."""
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

                bounding_solids_coords = np.asarray(gmsh.model.getBoundingBox(dim, tag)) * self.length_unit_factor
                self._bounding_solids[tag] = bounding_solids_coords

            elif dim == 2:
                self._surfaces_areas[tag] = mass * (self.length_unit_factor**2)
                self._surfaces_to_curves[tag] = tuple(downwards)
                self.surfaces.append(tag)

                center, uv_mid = self.process_center_element(dim, tag)
                self._surfaces_centers[tag] = center

                normal = gmsh.model.getNormal(tag, uv_mid)
                curvature = gmsh.model.getCurvature(dim, tag, uv_mid)
                self._surfaces_normals[tag] = normal

                bounding_surf_coords = np.asarray(gmsh.model.getBoundingBox(dim, tag)) * self.length_unit_factor
                self._bounding_surfaces[tag] = bounding_surf_coords

                if np.allclose(curvature, 0):
                    self._straight_surfaces.add(tag)

            elif dim == 1:
                self._curves_lengths[tag] = mass * (self.length_unit_factor**1)
                self._curves_to_points[tag] = tuple(downwards)
                self.curves.append(tag)

                center, uv_mid = self.process_center_element(dim, tag)
                curvature = gmsh.model.getCurvature(dim, tag, uv_mid)
                self._curves_centers[tag] = center

                bounding_lines_coords = np.asarray(gmsh.model.getBoundingBox(dim, tag)) * self.length_unit_factor
                self._bounding_lines[tag] = bounding_lines_coords

                if np.allclose(curvature, 0):
                    self._straight_curves.add(tag)

            elif dim == 0:
                self.points.append(tag)
                center, uv_mid = self.process_center_element(dim, tag)
                self._points_centers[tag] = center

        self._create_inverse_maps()

    def _process_curves_normals(self):
        """
        This is not a mathematically rigorous concept.

        It is just a quick and dirty way to find a vector pointing
        outwards of a geometry in the location of the curve center.

        It may be used for many purposes, such as positioning symbols, for example.
        """

        for curve in self.curves:
            adjacent_surfaces = self.curves_to_surfaces(curve)

            if not adjacent_surfaces:
                continue

            normals_sum = np.zeros(3)

            # First try to get normals from the surfaces
            for surf_id in adjacent_surfaces:
                normals_sum += self._surfaces_normals[surf_id]

            if np.allclose(normals_sum, 0):
                # If the sum of the surface normals is zero, estimate the "curve normal"
                # by summing the vectors that point to each adjacent surface center.
                curve_center = self.curve_center(curve)
                for surf_id in adjacent_surfaces:
                    surf_center = self.surface_center(surf_id)
                    vector = curve_center - surf_center
                    normals_sum += vector / np.linalg.norm(vector)

            # normalize the sum
            norm = np.linalg.norm(normals_sum)
            if norm > 1e-9:
                normals_sum /= norm

            self._curves_normals[curve] = normals_sum

    def _process_points_normals(self):
        """
        This is not a mathematically rigorous concept.

        It is just a quick and dirty way to find a vector pointing
        outwards of a geometry in the location of the point center.

        It may be used for many purposes, such as positioning symbols, for example.
        """

        for point in self.points:
            adjacent_curves = self.points_to_curves(point)

            if not adjacent_curves:
                continue

            normals_sum = np.zeros(3)

            for curve_id in adjacent_curves:
                normals_sum += self._curves_normals[curve_id]

            if np.allclose(normals_sum, 0):
                # If the sum of the curve normals is zero, estimate the "point normal"
                # by summing the vectors that point to each adjacent curve center.
                point_center = self.point_center(point)
                for curve_id in adjacent_curves:
                    curve_center = self.curve_center(curve_id)
                    vector = point_center - curve_center
                    normals_sum += vector / np.linalg.norm(vector)

            # normalize the sum
            norm = np.linalg.norm(normals_sum)
            if norm > 1e-9:
                normals_sum /= norm

            self._points_normals[point] = normals_sum

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

    def _create_inverse_maps(self):
        surfaces_to_solids = defaultdict(list)

        for solid, surfaces in self._solids_to_surfaces.items():
            for surface in surfaces:
                surfaces_to_solids[surface].append(solid)
        self._surfaces_to_solids = {surf: tuple(sol) for surf, sol in surfaces_to_solids.items()}

        curves_to_surfaces = defaultdict(list)
        for surface, curves in self._surfaces_to_curves.items():
            for curve in curves:
                curves_to_surfaces[curve].append(surface)
        self._curves_to_surfaces = {curv: tuple(surf) for curv, surf in curves_to_surfaces.items()}

        points_to_curves = defaultdict(list)
        for curve, points in self._curves_to_points.items():
            for point in points:
                points_to_curves[point].append(curve)
        self._points_to_curves = {point: tuple(curv) for point, curv in points_to_curves.items()}

    def _get_length_unit_factor(self, length_unit: LengthUnits) -> float:
        if length_unit == "millimeter":
            return 1e-3
        elif length_unit == "inch":
            return 0.0254
        else:
            raise ValueError(f'Invalid length unit "{length_unit}"')


def cache_geometry_information(self):
    self._cache_solids_to_surfaces = deepcopy(self._solids_to_surfaces)
    self._cache_surfaces_to_curves = deepcopy(self._surfaces_to_curves)
    self._cache_curves_to_points = deepcopy(self._curves_to_points)


def restore_data_from_cache(self):
    self._solids_to_surfaces = deepcopy(self._cache_solids_to_surfaces)
    self._surfaces_to_curves = deepcopy(self._cache_surfaces_to_curves)
    self._curves_to_points = deepcopy(self._cache_curves_to_points)

    self._cache_solids_to_surfaces.clear()
    self._cache_surfaces_to_curves.clear()
    self._cache_curves_to_points.clear()

    # To be continued

