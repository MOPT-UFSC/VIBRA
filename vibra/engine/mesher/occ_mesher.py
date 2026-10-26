from collections import defaultdict
from itertools import pairwise
from pathlib import Path

import numpy as np
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.collections import IndexedMap_TopoDS_Shape_TopTools_ShapeMapHasher as TopTools_IndexedMapOfShape
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID, TopAbs_VERTEX
from OCP.TopExp import TopExp, TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS

from vibra.engine.mesher.geometry_info import GeometryInfo
from vibra.engine.mesher.mesh import Mesh
from vibra.errors import IncompleteSetupError


class OccMesher:
    def __init__(self, path: str | Path | None = None):
        self.reset()
        if path is not None:
            self.set_path(path)

    def reset(self):
        self.path: Path | None = None
        self.deflection: float = 0.5

    def set_path(self, path: str | Path):
        self.path = Path(path).expanduser()

    def generate(self, threads: int = 0) -> tuple[Mesh, GeometryInfo]:
        if self.path is None:
            message = "Geometry not defined"
            context = (
                "The geometry file has not been defined yet."
                "Import a supported CAD file format to proceed."
                "\n\n"
                "Suported file formats: *.iges and *.step"
            )
            raise IncompleteSetupError(message, context=context)

        shape = self._read_geometry_file(self.path)
        point_mapper = self._map_vertices(shape)
        curve_mapper = self._map_edges(shape)
        surface_mapper = self._map_faces(shape)
        solid_mapper = self._map_solids(shape)

        # For some reason I can not use named args =(
        BRepMesh_IncrementalMesh(
            shape,
            self.deflection,
            False,  # is relative
            self.deflection,
            True,  # in parallel
        )
        loc = TopLoc_Location()
        _visited = set()

        def duplicated(*args):
            if args in _visited:
                return True
            _visited.add(args)
            return False

        WHATEVER = 0
        SOLID = 3
        SURFACE = 2
        CURVE = 1
        POINT = 0

        geometry_info = GeometryInfo()
        nodal_coordinates = []
        edges_connectivity = []
        faces_connectivity = []

        # TODO: update the nomenclature, it is very wrong
        for solid in self._iterate_solids(shape):
            solid_index = solid_mapper.FindIndex(solid)
            if duplicated(SOLID, solid_index):
                continue

            geometry_info.solids.append(solid_index)

            for surface in self._iterate_surfaces(solid):
                surface_index = surface_mapper.FindIndex(surface)

                if not duplicated(SOLID, SURFACE, solid_index, surface_index):
                    geometry_info._solids_to_surfaces[solid_index].append(surface_index)

                if duplicated(SURFACE, surface_index):
                    continue

                geometry_info.surfaces.append(surface_index)

                triangulation = BRep_Tool.Triangulation_s(surface, loc)
                coordinate_shift = len(nodal_coordinates)

                for index in range(triangulation.NbNodes()):
                    x, y, z = (val * 1e-3 for val in triangulation.Node(index + 1).Coord())
                    nodal_coordinates.append((len(nodal_coordinates), x, y, z))

                for triangle in triangulation.Triangles():
                    _connectivity = np.array(triangle.Get()) + coordinate_shift - 1
                    _row = (
                        len(faces_connectivity),
                        surface_index,
                        WHATEVER,
                        WHATEVER,
                        *_connectivity,
                    )
                    faces_connectivity.append(_row)

                for curve in self._iterate_curves(surface):
                    curve_index = curve_mapper.FindIndex(curve)

                    if not duplicated(SURFACE, CURVE, surface_index, curve_index):
                        geometry_info._surfaces_to_curves[surface_index].append(curve_index)

                    if duplicated(CURVE, curve_index):
                        continue

                    geometry_info.curves.append(curve_index)

                    polygon = BRep_Tool.PolygonOnTriangulation_s(curve, triangulation, loc)
                    for a, b in pairwise(range(polygon.Nodes().Length())):
                        _row = (
                            len(edges_connectivity),
                            curve_index,
                            WHATEVER,
                            WHATEVER,
                            polygon.Node(a + 1) + coordinate_shift - 1,
                            polygon.Node(b + 1) + coordinate_shift - 1,
                        )
                        edges_connectivity.append(_row)

                    for point in self._iterate_points(curve):
                        point_index = point_mapper.FindIndex(point)

                        if not duplicated(CURVE, POINT, curve_index, point_index):
                            geometry_info._curves_to_points[curve_index].append(point_index)

                        if not duplicated(POINT, point_index):
                            geometry_info.points.append(point_index)

        geometry_info._create_inverse_maps()

        mesh = Mesh()
        mesh.set_mesh_data(
            np.array(nodal_coordinates),
            np.array(edges_connectivity),
            np.array(faces_connectivity),
            solids_connectivity=np.zeros((0, 4)),
        )

        return mesh, GeometryInfo().read_file(self.path)

    def _iterate_entities(self, shape, entity_type):
        explorer = TopExp_Explorer(shape, entity_type)
        while explorer.More():
            yield explorer.Current()
            explorer.Next()

    def _map_repetitions(self, shape, entity_type):
        indexed_map = TopTools_IndexedMapOfShape()
        TopExp.MapShapes_s(shape, entity_type, indexed_map)
        return indexed_map

    def _read_geometry_file(self, path: Path):
        match path.suffix.lower():
            case ".step" | ".stp":
                return self._read_step(path)
            case ".iges" | ".igs":
                return self._read_iges(path)
            case _:
                message = f"Unsupported file format: '{path.suffix}'.\n Supported formats are: *.step, *.stp, *.iges, *.igs"
                raise ValueError(message)

    def _read_step(self, path: str | Path):
        from OCP.STEPControl import STEPControl_Reader

        reader = STEPControl_Reader()
        status = reader.ReadFile(str(path))

        if status != IFSelect_RetDone:
            raise ValueError("File could not be read")

        reader.TransferRoots()
        shape = reader.OneShape()
        return shape

    def _read_iges(self, path: str | Path):
        from OCP.IGESControl import IGESControl_Reader

        reader = IGESControl_Reader()
        status = reader.ReadFile(str(path))

        if status != IFSelect_RetDone:
            raise ValueError("File could not be read")

        reader.TransferRoots()
        shape = reader.OneShape()
        return shape

    def _iterate_curves(self, shape):
        for i in self._iterate_entities(shape, TopAbs_EDGE):
            yield TopoDS.Edge(i)

    def _iterate_surfaces(self, shape):
        for i in self._iterate_entities(shape, TopAbs_FACE):
            yield TopoDS.Face(i)

    def _iterate_solids(self, shape):
        for i in self._iterate_entities(shape, TopAbs_SOLID):
            yield TopoDS.Solid(i)

    def _iterate_points(self, shape):
        for i in self._iterate_entities(shape, TopAbs_VERTEX):
            yield TopoDS.Vertex(i)

    def _map_edges(self, shape):
        return self._map_repetitions(shape, TopAbs_EDGE)

    def _map_faces(self, shape):
        return self._map_repetitions(shape, TopAbs_FACE)

    def _map_solids(self, shape):
        return self._map_repetitions(shape, TopAbs_SOLID)

    def _map_vertices(self, shape):
        return self._map_repetitions(shape, TopAbs_VERTEX)
