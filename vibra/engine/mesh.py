import logging
from collections import defaultdict
from pathlib import Path

import gmsh
import numpy as np

from vibra.utils.progress_status import ProgressStatus

# Meshing algorithms
MESH_ADAPT = 1
DELAUNAY = 5
FRONTAL = 6


class Mesh:
    def __init__(self):
        self.points = []
        self.lines = []
        self.faces = []

        self.points_entities = dict()
        self.line_entities = dict()
        self.face_entities = dict()

    def set_points(self, points):
        self.points = np.array(points)

    def set_lines(self, lines):
        self.lines = np.array(lines)

    def set_faces(self, faces):
        self.faces = np.array(faces)

    def set_entities(self, dim, tag, indexes):
        if dim == 0:
            self.points_entities[tag] = set(indexes)
        elif dim == 1:
            self.line_entities[tag] = set(indexes)
        elif dim == 2:
            self.face_entities[tag] = set(indexes)
        else:
            NotImplemented

    @classmethod
    def from_file(cls, path, *, size=0, threads=1):
        path = Path(path)

        logging.info("Importing geometry" + ProgressStatus(0, 10))
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.open(str(path))

        if size > 0:
            gmsh.option.setNumber("Mesh.MeshSizeMin", size)
            gmsh.option.setNumber("Mesh.MeshSizeMax", size)
        else:
            gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.05)

        gmsh.option.setNumber("Mesh.Algorithm", DELAUNAY)
        gmsh.option.setNumber("General.NumThreads", threads)

        logging.info("Creating visualization mesh" + ProgressStatus(1, 10))
        gmsh.model.mesh.generate(dim=2)

        logging.info("Extracting mesh data" + ProgressStatus(8, 10))
        indexes, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
        total_nodes = int(np.max(indexes))
        points = np.zeros(total_nodes * 3).reshape(-1, 3)
        points[indexes - 1] = coords.reshape(-1, 3)

        lines = []
        faces = []
        entities = defaultdict(list)

        for dim, tag in gmsh.model.getEntities():
            *_, _points = gmsh.model.mesh.getElements(dim, tag)

            if _points:
                _points = _points[0]
            else:
                continue

            if dim == 0:
                entities[dim, tag].append(tag - 1)

            elif dim == 1:
                offset = len(lines)
                for i, (a, b) in enumerate(_points.reshape(-1, 2) - 1):
                    lines.append((a, b))
                    entities[dim, tag].append(i + offset)

            elif dim == 2:
                offset = len(faces)

                # I am assuming all the faces are triangles
                for i, (a, b, c) in enumerate(_points.reshape(-1, 3) - 1):
                    faces.append((a, b, c))
                    entities[dim, tag].append(i + offset)

            else:
                NotImplemented

        mesh = Mesh()
        mesh.set_points(points)
        mesh.set_lines(lines)
        mesh.set_faces(faces)

        for (dim, tag), indexes in entities.items():
            mesh.set_entities(dim, tag, indexes)

        return mesh
