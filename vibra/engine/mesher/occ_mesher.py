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

        vertex_mapper = self._map_vertices(shape)
        edge_mapper = self._map_edges(shape)
        face_mapper = self._map_faces(shape)
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

        coordinates = []
        edges_connectivity = []
        faces_connectivity = []

        line_indices = []
        surface_indices = []

        visited_points = set()
        visited_faces = set()
        visited_edges = set()
        visited_solids = set()

        volume_to_surfaces = defaultdict(set)
        surface_to_lines = defaultdict(set)
        line_to_points = defaultdict(set)

        # TODO: update the nomenclature, it is very wrong
        for solid in self._iterate_solids(shape):
            solid_index = solid_mapper.FindIndex(solid)
            if solid_index in visited_solids:
                continue
            visited_solids.add(solid_index)

            for face in self._iterate_faces(solid):
                face_index = face_mapper.FindIndex(face)
                volume_to_surfaces[solid_index].add(face_index)
                if face_index in visited_faces:
                    continue
                visited_faces.add(face_index)

                triangulation = BRep_Tool.Triangulation_s(face, loc)
                coordinate_shift = len(coordinates)

                for i in range(triangulation.NbNodes()):
                    coordinates.append(triangulation.Node(i + 1).Coord())

                for triangle in triangulation.Triangles():
                    triangle_indexes = np.array(triangle.Get())
                    faces_connectivity.append(triangle_indexes + coordinate_shift - 1)
                    surface_indices.append(face_index)

                for edge in self._iterate_edges(face):
                    edge_index = edge_mapper.FindIndex(edge)
                    surface_to_lines[face_index].add(edge_index)
                    if edge_index in visited_edges:
                        continue
                    visited_edges.add(edge_index)

                    polygon = BRep_Tool.PolygonOnTriangulation_s(edge, triangulation, loc)
                    for a, b in pairwise(range(polygon.Nodes().Length())):
                        index_a = polygon.Node(a + 1) + coordinate_shift - 1
                        index_b = polygon.Node(b + 1) + coordinate_shift - 1
                        edges_connectivity.append((index_a, index_b))
                        line_indices.append(edge_index)

                    for vertex in self._iterate_vertices(edge):
                        vertex_index = vertex_mapper.FindIndex(vertex)
                        visited_points.add(vertex_index)
                        line_to_points[edge_index].add(vertex_index)

        mesh = Mesh()
        coordinates = np.array(coordinates) * mesh.get_length_unit_factor()
        node_indices = np.arange(len(coordinates)).reshape(-1, 1)
        nodal_coordinates = np.concatenate(
            [node_indices, coordinates],
            axis=1,
        )

        edge_indices = np.arange(len(edges_connectivity)).reshape(-1, 1)
        line_indices = np.array(line_indices).reshape(-1, 1)
        whatever = np.zeros_like(line_indices)
        lines_connectivity = np.concatenate(
            [
                edge_indices,
                line_indices,
                whatever,
                whatever,
                edges_connectivity,
            ],
            axis=1,
        )

        face_indices = np.arange(len(faces_connectivity)).reshape(-1, 1)
        surface_indices = np.array(surface_indices).reshape(-1, 1)
        whatever = np.zeros_like(surface_indices)
        faces_connectivity = np.concatenate(
            [
                face_indices,
                surface_indices,
                whatever,
                whatever,
                faces_connectivity,
            ],
            axis=1,
        )

        mesh.set_mesh_data(
            nodal_coordinates,
            lines_connectivity,
            faces_connectivity,
            solids_connectivity=np.zeros((0, 4)),
        )

        mesh.geometry_information.update(
            {
                "points": list(visited_points),
                "lines": list(visited_edges),
                "surfaces": list(visited_faces),
                "volumes": list(visited_solids),
            }
        )

        mesh.surfaces_from_volume.update({i: list(j) for i, j in volume_to_surfaces.items()})
        mesh.lines_from_surface.update({i: list(j) for i, j in surface_to_lines.items()})
        mesh.points_from_line.update({i: list(j) for i, j in line_to_points.items()})
        mesh.process_upwards_adjacencies()

        # This is a temporary workaround.
        # Since this information does not depend on a mesh we can store it in a separated class.
        # But for now I am doing it the lazy way so I can get things to work.
        gi = GeometryInfo().read_file(self.path)
        mesh.area_from_surfaces = gi._surfaces_areas
        mesh.volume_from_bodies = gi._solids_volumes

        return mesh, gi

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

    def _iterate_edges(self, shape):
        for i in self._iterate_entities(shape, TopAbs_EDGE):
            yield TopoDS.Edge(i)

    def _iterate_faces(self, shape):
        for i in self._iterate_entities(shape, TopAbs_FACE):
            yield TopoDS.Face(i)

    def _iterate_solids(self, shape):
        for i in self._iterate_entities(shape, TopAbs_SOLID):
            yield TopoDS.Solid(i)

    def _iterate_vertices(self, shape):
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
