from itertools import pairwise
from pathlib import Path

import numpy as np
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.collections import IndexedMap_TopoDS_Shape_TopTools_ShapeMapHasher as TopTools_IndexedMapOfShape
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCP.TopExp import TopExp, TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS

from vibra.engine.geometry.geometry import GeometryInfo
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

    def generate(self, threads: int = 0) -> Mesh:
        if self.path is None:
            message = "Geometry not defined"
            context = (
                "The geometry file has not been defined yet."
                "Import a supported CAD file format to proceed."
                "\n\n"
                "Suported file formats: *.iges and *.step"
            )
            raise IncompleteSetupError(message, context=context)

        match self.path.suffix.lower():
            case ".step" | ".stp":
                shape = self._read_step(self.path)
            case ".iges" | ".igs":
                shape = self._read_iges(self.path)
            case _:
                message = f"Unsupported file format: '{self.path.suffix}'.\n Supported formats are: *.step, *.stp, *.iges, *.igs"
                raise ValueError(message)

        edge_mapper = self._map_edges(shape)
        face_mapper = self._map_faces(shape)

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

        visited_faces = set()
        visited_edges = set()

        for face in self._iterate_faces(shape):
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
                faces_connectivity.append(triangle_indexes + coordinate_shift - 1)
                surface_indices.append(face_index)

            for edge in self._iterate_edges(face):
                edge_index = edge_mapper.FindIndex(edge)
                if edge_index in visited_edges:
                    continue
                visited_edges.add(edge_index)

                polygon = BRep_Tool.PolygonOnTriangulation_s(edge, triangulation, loc)
                for a, b in pairwise(range(polygon.Nodes().Length())):
                    index_a = polygon.Node(a + 1) + coordinate_shift - 1
                    index_b = polygon.Node(b + 1) + coordinate_shift - 1
                    edges_connectivity.append((index_a, index_b))
                    line_indices.append(edge_index)

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

        # This is a temporary workaround.
        # Since this information does not depend on a mesh we can store it in a separated class.
        # But for now I am doing it the lazy way so I can get things to work.
        gi = GeometryInfo().read_file(self.path)
        mesh.surfaces_from_volume = gi._solids_to_surfaces
        mesh.lines_from_surface = gi._surfaces_to_curves
        mesh.points_from_line = gi._curves_to_points
        mesh.volumes_from_surface = gi._surfaces_to_solids
        mesh.surfaces_from_line = gi._curves_to_surfaces
        mesh.lines_from_point = gi._points_to_curves
        mesh.length_from_lines = gi._curves_lengths
        mesh.area_from_surfaces = gi._surfaces_areas
        mesh.volume_from_bodies = gi._solids_volumes

        return mesh

    def _iterate_entities(self, shape, entity_type):
        explorer = TopExp_Explorer(shape, entity_type)
        while explorer.More():
            yield explorer.Current()
            explorer.Next()

    def _map_repetitions(self, shape, entity_type):
        indexed_map = TopTools_IndexedMapOfShape()
        TopExp.MapShapes_s(shape, entity_type, indexed_map)
        return indexed_map

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

    def _map_edges(self, shape):
        return self._map_repetitions(shape, TopAbs_EDGE)

    def _map_faces(self, shape):
        return self._map_repetitions(shape, TopAbs_FACE)
