from itertools import pairwise
from pathlib import Path
from time import perf_counter
from typing import Iterator

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCP.TopTools import TopTools_IndexedMapOfShape
from OCP.TopExp import TopExp_Explorer, TopExp
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS


class VisualMesh:
    def __init__(self):
        self.clear()

    def clear(self):
        self.coordinates = np.zeros((0, 3))
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

        coordinates = list()
        segments = list()
        triangles = list()

        visited_faces = set()
        visited_edges = set()

        for face in iterate_faces(shape):
            face_index = face_mapper.FindIndex(face)
            if face_index in visited_faces:
                continue
            visited_faces.add(face_index)

            triangulation = BRep_Tool.Triangulation_s(face, loc)
            coordinate_shift = len(coordinates)

            for i in range(triangulation.NbNodes()):
                coordinates.append(triangulation.Node(i + 1).Coord())

            for triangle in triangulation.Triangles():
                triangle_indexes = np.array(triangle.Get())
                triangles.append(triangle_indexes + coordinate_shift - 1)

            for edge in iterate_edges(face):
                edge_index = edge_mapper.FindIndex(edge)
                if edge_index in visited_edges:
                    continue
                visited_edges.add(edge_index)

                polygon = BRep_Tool.PolygonOnTriangulation_s(edge, triangulation, loc)
                for a, b in pairwise(range(polygon.Nodes().Length())):
                    index_a = polygon.Node(a + 1) + coordinate_shift - 1
                    index_b = polygon.Node(b + 1) + coordinate_shift - 1
                    segments.append((index_a, index_b))

        self.coordinates = np.array(coordinates)
        self.segments = np.array(segments)
        self.triangles = np.array(triangles)


def _iterate_entities(shape, entity_type):
    explorer = TopExp_Explorer(shape, entity_type)
    while explorer.More():
        yield explorer.Current()
        explorer.Next()


def _map_repetitions(shape, entity_type):
    indexed_map = TopTools_IndexedMapOfShape()
    TopExp.MapShapes_s(shape, entity_type, indexed_map)
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
    for i in _iterate_entities(shape, TopAbs_EDGE):
        yield TopoDS.Edge_s(i)


def iterate_faces(shape):
    for i in _iterate_entities(shape, TopAbs_FACE):
        yield TopoDS.Face_s(i)


def map_edges(shape):
    return _map_repetitions(shape, TopAbs_EDGE)


def map_faces(shape):
    return _map_repetitions(shape, TopAbs_FACE)
