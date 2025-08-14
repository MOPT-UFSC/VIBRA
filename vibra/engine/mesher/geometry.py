from collections import defaultdict
import gmsh
import numpy as np
from vibra.utils.bidict import bidict

class Geometry:
    def __init__(self, **kwargs):
        self.length_unit = kwargs.get("length_unit", "milimeter")
        self.geometry_qf = kwargs.get("geometry_qf", 1.0)

        self.geometry_imported = True
        
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

    def read_file(self, file_path : str):
        gmsh.initialize()
        gmsh.open(file_path)

        gmsh.model.occ.synchronize()

        self.process_geometry_information()
        gmsh.finalize()

        
    def process_geometry_information(self):
        self.clear_geometry_data()

        unit_factor = self.get_length_unit_factor()
        for dim, tag in gmsh.model.getEntities():
            _, downwards = gmsh.model.getAdjacencies(dim, tag)
            downwards = [int(_id) for _id in downwards]

            if dim == 0:
                self.points.append(tag)
                continue

            value = 0.0
            if self.geometry_imported:
                value = gmsh.model.occ.getMass(dim, tag)

            if dim == 3:
                self.solids_volumes[tag] = value * (unit_factor**3)
                self.solids_to_surfaces[tag] = tuple(downwards)
                self.volumes.append(tag)

            elif dim == 2:
                self.surfaces_areas[tag] = value * (unit_factor**2)
                self.surfaces_to_curves[tag] = tuple(downwards)
                self.surfaces.append(tag)

            elif dim == 1:
                self.curves_lengths[tag] = value * (unit_factor**1)
                self.curves_to_points[tag] = tuple(downwards)
                self.lines.append(tag)

    def clear_geometry_data(self):
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



    def set_length_unit(self, length_unit: str = "milimeter"):
        self.length_unit = length_unit
    
    def get_length_unit_factor(self):
        if self.length_unit == "milimeter":
            return 1e-3
        elif self.length_unit == "inch":
            return 0.0254
        else:
            return 1