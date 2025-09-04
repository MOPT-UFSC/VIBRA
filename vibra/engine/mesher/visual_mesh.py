import numpy as np
from pathlib import Path
from time import perf_counter
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone

from OCC.Core.TopExp import TopExp_Explorer, topexp
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.TopoDS import topods
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GCPnts import GCPnts_QuasiUniformDeflection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from OCC.Core.TopTools import TopTools_IndexedMapOfShape

from OCC.Core.Poly import Poly_Triangulation, Poly_Triangle

from itertools import pairwise
from typing import Iterator

import matplotlib.pyplot as plt
import numpy as np


class VisualMesh:
    def __init__(self):
        self.clear()

    def clear(self):
        self.coords = np.zeros((0, 3))
        self.vertices = np.zeros((0, 1))
        self.segments = np.zeros((0, 2))
        self.triangles = np.zeros((0, 3))

    def load_file(self, path: str | Path, deflection: float = 0.5):
        shape = _read_step(path)

        edge_mapper = map_edges(shape)
        face_mapper = map_faces(shape)

        # For some reason I can not use named args =(
        BRepMesh_IncrementalMesh(
            shape,
            deflection,
            False,  # is relative
            deflection,
            True,  # in parallel
        )

        loc = TopLoc_Location()

        coords = list()
        segments = list()
        triangles = list()

        visited_faces = set()
        visited_edges = set()

        triangle: Poly_Triangle

        for face in iterate_faces(shape):
            face_index = face_mapper.FindIndex(face)
            if face_index in visited_faces:
                continue
            visited_faces.add(face_index)

            triangulation = BRep_Tool.Triangulation(face, loc)
            coord_shift = len(coords)

            for i in range(triangulation.NbNodes()):
                coords.append(triangulation.Node(i + 1).Coord())

            for triangle in triangulation.Triangles():
                triangle_indexes = np.array(triangle.Get())
                triangles.append(triangle_indexes + coord_shift - 1)

            for edge in iterate_edges(face):
                edge_index = edge_mapper.FindIndex(edge)
                if edge_index in visited_edges:
                    continue
                visited_edges.add(edge_index)

                polygon = BRep_Tool.PolygonOnTriangulation(edge, triangulation, loc)
                indexes = polygon.Nodes()
                for a, b in pairwise(range(indexes.Length())):
                    index_a = indexes.Value(a + 1) + coord_shift - 1
                    index_b = indexes.Value(b + 1) + coord_shift - 1
                    segments.append((index_a, index_b))

        self.coords = np.array(coords)
        self.segments = np.array(segments)
        self.triangles = np.array(triangles)


def _iterate_entities(shape, entity_type):
    explorer = TopExp_Explorer(shape, entity_type)
    while explorer.More():
        yield explorer.Current()
        explorer.Next()


def _map_repetitions(shape, entity_type):
    indexed_map = TopTools_IndexedMapOfShape()
    topexp.MapShapes(shape, entity_type, indexed_map)
    return indexed_map


def _read_step(path: str | Path):
    reader = STEPControl_Reader()
    status = reader.ReadFile(path)

    if status != IFSelect_RetDone:
        raise ValueError("File could not be read")

    reader.TransferRoots()
    shape = reader.OneShape()
    return shape


def iterate_edges(shape):
    yield from _iterate_entities(shape, TopAbs_EDGE)


def iterate_faces(shape):
    yield from _iterate_entities(shape, TopAbs_FACE)


def map_edges(shape):
    return _map_repetitions(shape, TopAbs_EDGE)


def map_faces(shape):
    return _map_repetitions(shape, TopAbs_FACE)
