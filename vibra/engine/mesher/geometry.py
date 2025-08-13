from collections import defaultdict
import gmsh
import numpy as np
from vibra.utils.bidict import bidict

class Geometry:
    def __init__(self):
        self.geometry_imported = True
        
        self.points_coords = dict()        
        self.solids_to_surfaces = bidict() #3d -> 2d    
        self.surfaces_to_curves = bidict() #2d -> 1d     
        self.curves_to_points = bidict() #1d -> 0d

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

    def read_file(self, file_path : str):
        gmsh.initialize()
        gmsh.open(file_path)

        gmsh.model.occ.synchronize()

        self.process_geometry_information()
        self.process_downwards_adjacencies_from_entities()
        gmsh.finalize()


    def process_downwards_adjacencies_from_entities(self):
        """This method processes the downwards adjacencies
        from the geometric entities.
        """

        self.solids_to_surfaces.clear()
        self.surfaces_to_curves.clear()
        self.curves_to_points.clear()

        for dim, tag in gmsh.model.getEntities():
            _, downwards = gmsh.model.getAdjacencies(dim, tag)
            downwards = [int(_id) for _id in downwards]

            if dim == 3:
                self.solids_to_surfaces[tag] = tuple(downwards)

            elif dim == 2:
                self.surfaces_to_curves[tag] = tuple(downwards)

            elif dim == 1:
                self.curves_to_points[tag] = tuple(downwards)
        
    def process_geometry_information(self):
        self.clear_geometry_data()

        labels = ["points", "lines", "surfaces", "volumes"]

        unit_factor = 1e-3
        for dim, tag in gmsh.model.getEntities():
            label = labels[dim]
            self.geometry_information[label].append(tag)

            if dim == 0:
                continue

            value = 0.0
            if self.geometry_imported:
                value = gmsh.model.occ.getMass(dim, tag)

            if dim == 3:
                self.solids_volumes[tag] = value * (unit_factor**3)

            elif dim == 2:
                self.surfaces_areas[tag] = value * (unit_factor**2)

            elif dim == 1:
                self.curves_lengths[tag] = value * (unit_factor**1)

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

        self.geometry_information = defaultdict(list)
