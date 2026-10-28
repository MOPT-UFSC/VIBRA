from itertools import pairwise
from pathlib import Path

import numpy as np
from OCP.Bnd import Bnd_Box
from OCP.BOPAlgo import BOPAlgo_Builder, BOPAlgo_GlueEnum
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepGProp import BRepGProp
from OCP.BRepLProp import BRepLProp_SLProps
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.collections import IndexedMap_TopoDS_Shape_TopTools_ShapeMapHasher as TopTools_IndexedMapOfShape
from OCP.GeomAbs import GeomAbs_Line, GeomAbs_Plane
from OCP.GProp import GProp_GProps
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_REVERSED, TopAbs_SOLID, TopAbs_VERTEX
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

        # TODO: improve the performance of these loops
        for solid in self._iterate_solids(shape):
            solid_index = solid_mapper.FindIndex(solid)
            if duplicated(SOLID, solid_index):
                continue

            geometry_info.solids.append(solid_index)
            geometry_info._solids_volumes[solid_index] = self._solid_volume(solid)
            geometry_info._solids_centers[solid_index] = self._solid_center(solid)
            geometry_info._bounding_solids[solid_index] = self._bounding_box(solid)

            for surface in self._iterate_surfaces(solid):
                surface_index = surface_mapper.FindIndex(surface)

                if not duplicated(SOLID, SURFACE, solid_index, surface_index):
                    geometry_info._solids_to_surfaces[solid_index].append(surface_index)

                if duplicated(SURFACE, surface_index):
                    continue

                geometry_info.surfaces.append(surface_index)
                geometry_info._surfaces_areas[surface_index] = self._surface_area(surface)
                geometry_info._surfaces_centers[surface_index] = self._surface_center(surface)
                geometry_info._surfaces_normals[surface_index] = self._surface_normal(surface)
                geometry_info._bounding_surfaces[surface_index] = self._bounding_box(surface)
                if self._is_straight_surface(surface):
                    geometry_info._straight_surfaces.add(surface_index)

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
                    geometry_info._curves_lengths[curve_index] = self._curve_length(curve)
                    geometry_info._curves_centers[curve_index] = self._curve_center(curve)
                    geometry_info._bounding_curves[curve_index] = self._bounding_box(curve)
                    if self._is_straight_curve(curve):
                        geometry_info._straight_curves.add(curve_index)

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

                        if duplicated(POINT, point_index):
                            continue

                        geometry_info.points.append(point_index)
                        geometry_info._points_centers[point_index] = self._point_center(point)

        geometry_info._create_inverse_maps()
        geometry_info._process_curves_normals()
        geometry_info._process_points_normals()

        mesh = Mesh()
        mesh.set_mesh_data(
            np.array(nodal_coordinates),
            np.array(edges_connectivity),
            np.array(faces_connectivity),
            solids_connectivity=np.zeros((0, 4)),
        )

        return mesh, geometry_info

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
        return self._fragment(shape)

    def _read_iges(self, path: str | Path):
        from OCP.IGESControl import IGESControl_Reader

        reader = IGESControl_Reader()
        status = reader.ReadFile(str(path))

        if status != IFSelect_RetDone:
            raise ValueError("File could not be read")

        reader.TransferRoots()
        shape = reader.OneShape()
        return self._fragment(shape)

    def _fragment(self, shape):
        builder = BOPAlgo_Builder()
        for solid in self._iterate_solids(shape):
            builder.AddArgument(solid)
        builder.SetGlue(BOPAlgo_GlueEnum.BOPAlgo_GlueShift)
        builder.Perform()

        result = builder.Shape()
        if builder.HasErrors():
            return shape

        return result

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

    def _solid_volume(self, shape) -> float:
        props = GProp_GProps()
        BRepGProp.VolumeProperties_s(shape, props)
        return props.Mass() * 1e-9

    def _surface_area(self, shape) -> float:
        props = GProp_GProps()
        BRepGProp.SurfaceProperties_s(shape, props)
        return props.Mass() * 1e-6

    def _curve_length(self, shape) -> float:
        props = GProp_GProps()
        BRepGProp.LinearProperties_s(shape, props)
        return props.Mass() * 1e-3

    def _solid_center(self, shape) -> np.ndarray:
        props = GProp_GProps()
        BRepGProp.VolumeProperties_s(shape, props)
        return np.array(props.CentreOfMass().Coord()) * 1e-3

    def _surface_center(self, shape) -> np.ndarray:
        surface = BRepAdaptor_Surface(shape)
        u_mid = (surface.FirstUParameter() + surface.LastUParameter()) / 2
        v_mid = (surface.FirstVParameter() + surface.LastVParameter()) / 2
        return np.array(surface.Value(u_mid, v_mid).Coord()) * 1e-3

    def _curve_center(self, shape) -> np.ndarray:
        curve = BRepAdaptor_Curve(shape)
        u_mid = (curve.FirstParameter() + curve.LastParameter()) / 2
        return np.array(curve.Value(u_mid).Coord()) * 1e-3

    def _point_center(self, shape) -> np.ndarray:
        return np.array(BRep_Tool.Pnt_s(shape).Coord()) * 1e-3

    def _is_straight_surface(self, shape) -> bool:
        return BRepAdaptor_Surface(shape).GetType() == GeomAbs_Plane

    def _is_straight_curve(self, shape) -> bool:
        return BRepAdaptor_Curve(shape).GetType() == GeomAbs_Line

    def _surface_normal(self, shape) -> np.ndarray:
        surface = BRepAdaptor_Surface(shape)
        u_mid = (surface.FirstUParameter() + surface.LastUParameter()) / 2
        v_mid = (surface.FirstVParameter() + surface.LastVParameter()) / 2

        props = BRepLProp_SLProps(surface, u_mid, v_mid, 1, 1e-6)
        normal = np.array(props.Normal().Coord())

        if shape.Orientation() == TopAbs_REVERSED:
            normal *= -1

        return normal

    def _bounding_box(self, shape) -> tuple[float, float, float, float, float, float]:
        bbox = Bnd_Box()
        bbox.SetGap(1e-6)
        BRepBndLib.Add_s(shape, bbox, False)
        return (
            bbox.GetXMin() * 1e-3,
            bbox.GetYMin() * 1e-3,
            bbox.GetZMin() * 1e-3,
            bbox.GetXMax() * 1e-3,
            bbox.GetYMax() * 1e-3,
            bbox.GetZMax() * 1e-3,
        )
