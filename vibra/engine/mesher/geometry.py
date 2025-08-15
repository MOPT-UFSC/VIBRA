from collections import defaultdict
import gmsh
import numpy as np
from vibra.utils.bidict import bidict
from typing import Literal
from pathlib import Path

LengthUnits = Literal["milimeter", "inch"]


class Geometry:
    def __init__(
        self,
        path: str | Path | None = None,
        length_unit: LengthUnits = "milimeter",
    ):
        # connectivity
        self.points_coords = dict()
        self.solids_to_surfaces = bidict()
        self.surfaces_to_curves = bidict()
        self.curves_to_points = bidict()

        # centers
        self.solids_centers = dict()
        self.surfaces_centers = dict()
        self.curves_centers = dict()

        # normals
        self.surfaces_normals = dict()
        self.curves_normals = dict()
        self.points_normals = dict()

        # areas
        self.surfaces_areas = dict()
        self.curves_lengths = dict()
        self.solids_volumes = dict()

        self.straight_solids = dict()
        self.straight_lines = dict()
        self.straight_curves = dict()

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
        self.points_coords.clear()
        self.solids_to_surfaces.clear()
        self.surfaces_to_curves.clear()
        self.curves_to_points.clear()

        # centers
        self.solids_centers.clear()
        self.surfaces_centers.clear()
        self.curves_centers.clear()

        # normals
        self.surfaces_normals.clear()
        self.curves_normals.clear()
        self.points_normals.clear()

        # areas
        self.surfaces_areas.clear()
        self.curves_lengths.clear()

        self.solids_volumes.clear()

        self.straight_solids.clear()
        self.straight_lines.clear()
        self.straight_curves.clear()

    def set_length_unit(self, length_unit: LengthUnits):
        self.length_unit = length_unit
        self.length_unit_factor = self._get_length_unit_factor(length_unit)

        # You should not modify the lenght unit after reading the geometry
        # because it is misleading unless you correct all values.
        # TODO: replace this clear by a function that converts all length units.
        self.clear()

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
                self.solids_volumes[tag] = mass * (self.length_unit_factor**3)
                self.solids_to_surfaces[tag] = tuple(downwards)
                self.volumes.append(tag)

            elif dim == 2:
                self.surfaces_areas[tag] = mass * (self.length_unit_factor**2)
                self.surfaces_to_curves[tag] = tuple(downwards)
                self.surfaces.append(tag)

            elif dim == 1:
                self.curves_lengths[tag] = mass * (self.length_unit_factor**1)
                self.curves_to_points[tag] = tuple(downwards)
                self.lines.append(tag)

    def _get_length_unit_factor(self, length_unit: LengthUnits) -> float:
        if length_unit == "milimeter":
            return 1e-3
        elif length_unit == "inch":
            return 0.0254
        else:
            raise ValueError(f'Invalid length unit "{length_unit}"')
