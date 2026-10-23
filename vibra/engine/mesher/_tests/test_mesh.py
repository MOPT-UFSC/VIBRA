from itertools import combinations
from pathlib import Path

import gmsh
import numpy as np

from vibra import PROJECT_DIR
from vibra.engine.mesher.geometry_info import GeometryInfo
from vibra.engine.mesher.gmsh_constants import GMSH_HEX8, GMSH_HEX20, GMSH_TET4, GMSH_TET10
from vibra.engine.mesher.gmsh_mesher import GmshMesher
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import ElementTopology, LocalMeshSizeControlSetup
from vibra.engine.serialization.file_helpers import read_json, write_json


def test_tetrahedron_4_mesh():
    geometry_path = str(PROJECT_DIR / "examples/geometry_files/cylinder.step")
    mesh_test_path = str(PROJECT_DIR / "validation_files/data/mesh_info/cilinder_tet4/")

    mesher = GmshMesher(geometry_path)
    mesher.setup.minimum_element_size = 30
    mesher.setup.maximum_element_size = 80
    mesher.setup.custom_element_setup = GMSH_TET4

    mesh, geometry_info = mesher.generate(threads=1)
    assert mesh.element_topology == ElementTopology("tetrahedral", "linear")

    _compare_mesh(
        mesh,
        geometry_info,
        mesh_test_path,
    )


def test_tetrahedron_10_mesh():
    geometry_path = str(PROJECT_DIR / "examples/geometry_files/tetrahedron.step")
    mesh_test_path = str(PROJECT_DIR / "validation_files/data/mesh_info/tetrahedron_tet10/")

    mesher = GmshMesher(geometry_path)
    mesher.setup.minimum_element_size = 30
    mesher.setup.maximum_element_size = 80
    mesher.setup.custom_element_setup = GMSH_TET10

    mesh, geometry_info = mesher.generate(threads=1)
    assert mesh.element_topology == ElementTopology("tetrahedral", "quadratic")

    _compare_mesh(
        mesh,
        geometry_info,
        mesh_test_path,
    )


def test_hexahedron_8_mesh():
    geometry_path = str(PROJECT_DIR / "examples/geometry_files/cylinder.step")

    mesher = GmshMesher(geometry_path)
    mesher.setup.minimum_element_size = 30
    mesher.setup.maximum_element_size = 80
    mesher.setup.custom_element_setup = GMSH_HEX8

    mesh, _ = mesher.generate(threads=1)
    assert mesh.element_topology == ElementTopology("hexahedral", "linear")


def test_hexahedron_20_mesh():
    geometry_path = str(PROJECT_DIR / "examples/geometry_files/parallelepiped.step")

    mesher = GmshMesher(geometry_path)
    mesher.setup.minimum_element_size = 300
    mesher.setup.maximum_element_size = 300
    mesher.setup.custom_element_setup = GMSH_HEX20

    mesh, _ = mesher.generate(threads=1)
    assert mesh.element_topology == ElementTopology("hexahedral", "quadratic")


def test_local_mesh_size_control_coarsening():
    geometry_path = str(PROJECT_DIR / "examples/geometry_files/tetrahedron_double_volume.step")

    mesher = GmshMesher(geometry_path)
    mesher.setup.maximum_element_size = 20
    mesher.setup.merge_connected_volumes = False
    mesher.setup.local_mesh_size_control_parameters = [LocalMeshSizeControlSetup("volumes", 40, [1])]
    mesher.setup.custom_element_setup = GMSH_TET4

    mesh, _ = mesher.generate(threads=1)

    mean_edges = _mean_edge_length_per_volume(mesh)
    assert mean_edges[1] > mean_edges[2] * 1.2
    assert mean_edges[2] < 30


def test_local_mesh_size_control_coarsening_connected():
    geometry_path = str(PROJECT_DIR / "examples/geometry_files/tetrahedron_double_volume.step")

    mesher = GmshMesher(geometry_path)
    mesher.setup.maximum_element_size = 20
    mesher.setup.local_mesh_size_control_parameters = [LocalMeshSizeControlSetup("volumes", 40, [1])]
    mesher.setup.custom_element_setup = GMSH_TET4

    mesh, _ = mesher.generate(threads=1)

    mean_edges = _mean_edge_length_per_volume(mesh)
    assert mean_edges[1] > mean_edges[2] * 1.2
    assert mean_edges[2] < 30


def test_local_mesh_size_control_refines():
    geometry_path = str(PROJECT_DIR / "examples/geometry_files/tetrahedron_double_volume.step")

    mesher = GmshMesher(geometry_path)
    mesher.setup.maximum_element_size = 20
    mesher.setup.merge_connected_volumes = False
    mesher.setup.local_mesh_size_control_parameters = [LocalMeshSizeControlSetup("volumes", 5, [2])]
    mesher.setup.custom_element_setup = GMSH_TET4

    mesh, _ = mesher.generate(threads=1)

    mean_edges = _mean_edge_length_per_volume(mesh)
    assert mean_edges[2] < mean_edges[1] * 0.9


def _mean_edge_length_per_volume(mesh: Mesh) -> dict[int, float]:
    node_index = {int(node): i for i, node in enumerate(mesh.nodal_coordinates[:, 0])}
    coords = mesh.nodal_coordinates[:, 1:]

    mean_edges = {}
    for volume_id in mesh.all_volume_ids():
        rows = mesh.solids_connectivity[mesh.solids_connectivity[:, 1] == volume_id]
        lengths = []
        for connect in rows[:, 4:]:
            for a, b in combinations(connect, 2):
                lengths.append(np.linalg.norm(coords[node_index[int(a)]] - coords[node_index[int(b)]]))
        mean_edges[volume_id] = float(np.mean(lengths))

    return mean_edges


def _compare_mesh(mesh: Mesh, geometry_info: GeometryInfo, mesh_path: Path | str):
    mesh_path = Path(mesh_path)
    mappings = {
        "face_to_solid_element": dict(mesh.face_to_solid_element),
        "line_from_element": dict(mesh.elements_from_line),
        "surface_from_element": dict(mesh.elements_from_surface),
        "volume_from_element": dict(mesh.elements_from_volume),
    }
    geometry = {
        "surfaces_from_volume": dict(mesh.surfaces_from_volume),
        "lines_from_surface": dict(mesh.lines_from_surface),
        "points_from_line": dict(mesh.points_from_line),
        "volumes_from_surface": dict(mesh.volumes_from_surface),
        "surfaces_from_line": dict(mesh.surfaces_from_line),
        "lines_from_point": dict(mesh.lines_from_point),
        "face_elements_connected_to_nodes": dict(mesh.face_elements_connected_to_nodes),
        "length_from_lines": dict(mesh.length_from_lines),
        "area_from_surfaces": dict(mesh.area_from_surfaces),
        "volume_from_bodies": dict(mesh.volume_from_bodies),
    }

    if not mesh_path.exists():
        mesh_path.mkdir(parents=True)
        mesh.export_nodal_coordinates(mesh_path / "nodal_coordinates.dat")
        mesh.export_line_elements_connectivity(mesh_path / "lines_connectivity.dat")
        mesh.export_face_elements_connectivity(mesh_path / "faces_connectivity.dat")
        mesh.export_solid_elements_connectivity(mesh_path / "solids_connectivity.dat")
        write_json(mesh_path / "mappings.json", mappings)
        write_json(mesh_path / "geometry.json", geometry)
        assert False

    expected_nodal_coordinates = np.loadtxt(
        mesh_path / "nodal_coordinates.dat",
        delimiter=",",
        skiprows=1,
    )
    expected_lines_connectivity = np.loadtxt(
        mesh_path / "lines_connectivity.dat",
        delimiter=",",
        skiprows=1,
    )
    expected_faces_connectivity = np.loadtxt(
        mesh_path / "faces_connectivity.dat",
        delimiter=",",
        skiprows=1,
    )
    expected_solids_connectivity = np.loadtxt(
        mesh_path / "solids_connectivity.dat",
        delimiter=",",
        skiprows=1,
    )
    expected_mappings = read_json(mesh_path / "mappings.json")
    expected_geometry = read_json(mesh_path / "geometry.json")

    if gmsh.isInitialized():
        gmsh.finalize()

    assert np.allclose(expected_nodal_coordinates, mesh.nodal_coordinates)
    assert np.allclose(expected_lines_connectivity, mesh.lines_connectivity)
    assert np.allclose(expected_faces_connectivity, mesh.faces_connectivity)
    assert np.allclose(expected_solids_connectivity, mesh.solids_connectivity)

    assert expected_mappings == _normalize(mappings)
    assert expected_geometry == _normalize(geometry)

    if (expected_solids_connectivity.size != 0) and (mesh.solids_connectivity.size != 0):
        assert np.allclose(expected_solids_connectivity, mesh.solids_connectivity)


def _normalize(obj):
    """
    JSON converts all keys to strings. To compare dicts we need to match this behaviour.
    """
    if isinstance(obj, dict):
        return {str(k): _normalize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_normalize(item) for item in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    return obj
