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

        BRepMesh_IncrementalMesh(
            theShape=shape,
            theLinDeflection=deflection,
            isRelative=False,
            theAngDeflection=deflection,
            isInParallel=True,
        )

        loc = TopLoc_Location()

        for face in iterate_faces(shape):
            triangulation = BRep_Tool.Triangulation(face, loc)

            for a, b, c in extract_triangle_coords(triangulation):
                pass

            for edge in iterate_edges(face):
                pass

        return shape


def extract_triangle_coords(triangulation):
    for i in range(1, triangulation.NbTriangles() + 1):
        triangle = triangulation.Triangle(i)
        a, b, c = triangle.Get()

        node_a = triangulation.Node(a)
        node_b = triangulation.Node(b)
        node_c = triangulation.Node(c)

        yield (
            (node_a.X(), node_a.Y(), node_a.Z()),
            (node_b.X(), node_b.Y(), node_b.Z()),
            (node_c.X(), node_c.Y(), node_c.Z()),
        )


def extract_edge_coords(edge, triangulation):
    loc = TopLoc_Location()
    poly = BRep_Tool.PolygonOnTriangulation(edge, triangulation, loc)

    if poly is None:
        return ()

    indices = poly.Nodes()
    for i in range(1, indices.Length() + 1):
        node = triangulation.Node(indices.Value(i))
        yield (node.X(), node.Y(), node.Z())


def _iterate_entities(shape, entity_type):
    explorer = TopExp_Explorer(shape, entity_type)
    while explorer.More():
        yield explorer.Current()
        explorer.Next()


def _map_repetitions(shape, entity_type):
    indexed_map = TopTools_IndexedMapOfShape()
    topexp.MapShapes(shape, TopAbs_EDGE, entity_type)
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
