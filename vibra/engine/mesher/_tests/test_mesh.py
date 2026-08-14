from itertools import combinations
from pathlib import Path

import gmsh
import numpy as np

from vibra import PROJECT_DIR
from vibra.engine.mesher.element_setup import GMSH_HEX8, GMSH_HEX20, GMSH_TET4, GMSH_TET10
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import ElementTopology, LocalMeshSizeControlSetup, MeshSetup


def test_tetrahedron_4_mesh():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/cylinder.step")
    mesh_test_path = str(PROJECT_DIR / "validation_files/data/mesh_info/cilinder_tet4/")

    mesh_setup = MeshSetup(
        minimum_element_size=30,
        maximum_element_size=80,
        custom_element_setup=GMSH_TET4,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)
    assert mesh.element_topology == ElementTopology("tetrahedral", "linear")

    _compare_mesh(
        mesh,
        mesh_test_path,
    )


def test_tetrahedron_10_mesh():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/tetrahedron.step")
    mesh_test_path = str(PROJECT_DIR / "validation_files/data/mesh_info/tetrahedron_tet10/")

    mesh_setup = MeshSetup(
        minimum_element_size=30,
        maximum_element_size=80,
        custom_element_setup=GMSH_TET10,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)
    assert mesh.element_topology == ElementTopology("tetrahedral", "quadratic")

    _compare_mesh(
        mesh,
        mesh_test_path,
    )


def test_hexahedron_8_mesh():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/cylinder.step")

    mesh_setup = MeshSetup(
        minimum_element_size=30,
        maximum_element_size=80,
        custom_element_setup=GMSH_HEX8,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)
    assert mesh.element_topology == ElementTopology("hexahedral", "linear")


def test_hexahedron_20_mesh():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/parallelepiped.step")

    mesh_setup = MeshSetup(
        minimum_element_size=300,
        maximum_element_size=300,
        custom_element_setup=GMSH_HEX20,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)
    assert mesh.element_topology == ElementTopology("hexahedral", "quadratic")


def test_local_mesh_size_control_coarsening():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/tetrahedron_double_volume.step")

    mesh_setup = MeshSetup(
        maximum_element_size=20,
        merge_connected_volumes=False,
        local_mesh_size_control_parameters=[LocalMeshSizeControlSetup("volumes", 40, [1])],
        custom_element_setup=GMSH_TET4,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)

    mean_edges = _mean_edge_length_per_volume(mesh)
    assert mean_edges[1] > mean_edges[2] * 1.2
    assert mean_edges[2] < 30


def test_local_mesh_size_control_coarsening_connected():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/tetrahedron_double_volume.step")

    mesh_setup = MeshSetup(
        maximum_element_size=20,
        local_mesh_size_control_parameters=[LocalMeshSizeControlSetup("volumes", 40, [1])],
        custom_element_setup=GMSH_TET4,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)

    mean_edges = _mean_edge_length_per_volume(mesh)
    assert mean_edges[1] > mean_edges[2] * 1.2
    assert mean_edges[2] < 30


def test_local_mesh_size_control_refines():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/tetrahedron_double_volume.step")

    mesh_setup = MeshSetup(
        maximum_element_size=20,
        merge_connected_volumes=False,
        local_mesh_size_control_parameters=[LocalMeshSizeControlSetup("volumes", 5, [2])],
        custom_element_setup=GMSH_TET4,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)

    mean_edges = _mean_edge_length_per_volume(mesh)
    assert mean_edges[2] < mean_edges[1] * 0.9


def test_disconnected_surfaces_keep_volumes_disconnected():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/tetrahedron_double_volume.step")

    mesh_setup = MeshSetup(
        maximum_element_size=20,
        merge_connected_volumes=True,
        disconnected_surfaces=[1],
        custom_element_setup=GMSH_TET4,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)

    surfaces = sorted(mesh.geometry_information["surfaces"])
    twin_surface = surfaces[-1]

    assert twin_surface not in {1, 2, 3, 4, 5, 6, 7}
    assert mesh.volumes_from_surface[1] == [2]
    assert mesh.volumes_from_surface[twin_surface] == [1]

    nodes_from_volumes = _nodes_from_volumes(mesh)
    shared_nodes = set(nodes_from_volumes[1]) & set(nodes_from_volumes[2])
    assert not shared_nodes

    solids_from_surface_1 = {
        mesh.face_to_solid_element[i]
        for i in range(mesh.faces_connectivity.shape[0])
        if mesh.faces_connectivity[i, 1] == 1
    }
    solids_from_surface_twin = {
        mesh.face_to_solid_element[i]
        for i in range(mesh.faces_connectivity.shape[0])
        if mesh.faces_connectivity[i, 1] == twin_surface
    }
    assert solids_from_surface_1
    assert solids_from_surface_twin
    assert {_volume_of_solid(mesh, solid) for solid in solids_from_surface_1} == {2}
    assert {_volume_of_solid(mesh, solid) for solid in solids_from_surface_twin} == {1}

    assert np.isclose(mesh.area_from_surfaces[1], mesh.area_from_surfaces[twin_surface])


def test_disconnected_surfaces_skips_single_volume_surfaces():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/tetrahedron_double_volume.step")

    mesh_setup = MeshSetup(
        maximum_element_size=20,
        merge_connected_volumes=True,
        disconnected_surfaces=[2],
        custom_element_setup=GMSH_TET4,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)

    assert sorted(mesh.geometry_information["surfaces"]) == [1, 2, 3, 4, 5, 6, 7]
    nodes_from_volumes = _nodes_from_volumes(mesh)
    assert set(nodes_from_volumes[1]) & set(nodes_from_volumes[2])


def test_multiple_disconnected_surfaces_simultaneously():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/decoupling_cavity_cylindrical.STEP")

    reference_setup = MeshSetup(
        maximum_element_size=40,
        merge_connected_volumes=True,
        custom_element_setup=GMSH_TET4,
    )
    reference_mesh = Mesh().load_cad(geometry_path, reference_setup, threads=1)
    original_surfaces = set(reference_mesh.geometry_information["surfaces"])

    disconnected_surfaces = [1, 8, 12, 13]
    mesh_setup = MeshSetup(
        maximum_element_size=40,
        merge_connected_volumes=True,
        disconnected_surfaces=disconnected_surfaces,
        custom_element_setup=GMSH_TET4,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)

    twin_surfaces = [surface_id for surface_id in mesh.geometry_information["surfaces"] if surface_id not in original_surfaces]
    assert len(twin_surfaces) == len(disconnected_surfaces)

    node_index = {int(node): i for i, node in enumerate(mesh.nodal_coordinates[:, 0])}
    coords = mesh.nodal_coordinates

    def _face_element_geometry(surface_id: int) -> set[tuple]:
        rows = mesh.faces_connectivity[mesh.faces_connectivity[:, 1] == surface_id]
        geometry = set()
        for connect in rows[:, 4:]:
            points = sorted(tuple(np.round(coords[node_index[int(node)], 1:], 6)) for node in connect)
            geometry.add(tuple(points))
        return geometry

    for surface_id, twin_surface_id in zip(disconnected_surfaces, twin_surfaces):
        assert _face_element_geometry(surface_id) == _face_element_geometry(twin_surface_id)

        surface_nodes = set(mesh.faces_connectivity[mesh.faces_connectivity[:, 1] == surface_id, 4:].flatten().astype(int))
        twin_nodes = set(mesh.faces_connectivity[mesh.faces_connectivity[:, 1] == twin_surface_id, 4:].flatten().astype(int))
        assert not (surface_nodes & twin_nodes)

    assert not mesh.disconnected_nodes_data


def test_disconnected_surfaces_cross_interfaces_do_not_orphan_nodes():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/decoupling_cavity_cylindrical.STEP")

    disconnected_surfaces = [8, 31]
    mesh_setup = MeshSetup(
        maximum_element_size=40,
        merge_connected_volumes=True,
        disconnected_surfaces=disconnected_surfaces,
        custom_element_setup=GMSH_TET4,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)

    reference_setup = MeshSetup(
        maximum_element_size=40,
        merge_connected_volumes=True,
        custom_element_setup=GMSH_TET4,
    )
    reference_mesh = Mesh().load_cad(geometry_path, reference_setup, threads=1)
    original_surfaces = set(reference_mesh.geometry_information["surfaces"])

    twin_surfaces = [surface_id for surface_id in mesh.geometry_information["surfaces"] if surface_id not in original_surfaces]
    assert len(twin_surfaces) == len(disconnected_surfaces)

    for surface_id, twin_surface_id in zip(disconnected_surfaces, twin_surfaces):
        assert _face_element_geometry(mesh, surface_id) == _face_element_geometry(mesh, twin_surface_id)

        surface_nodes = set(mesh.faces_connectivity[mesh.faces_connectivity[:, 1] == surface_id, 4:].flatten().astype(int))
        twin_nodes = set(mesh.faces_connectivity[mesh.faces_connectivity[:, 1] == twin_surface_id, 4:].flatten().astype(int))
        assert not (surface_nodes & twin_nodes)

    assert not mesh.disconnected_nodes_data


def test_disconnected_surfaces_decouple_corner_nodes_of_three_volumes():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/decoupling_cavity_complex.STEP")

    disconnected_surfaces = [40, 41, 42, 43, 44, 46, 60, 63, 65, 74]
    mesh_setup = MeshSetup(
        maximum_element_size=40,
        merge_connected_volumes=True,
        disconnected_surfaces=disconnected_surfaces,
        custom_element_setup=GMSH_TET4,
    )
    mesh = Mesh().load_cad(geometry_path, mesh_setup, threads=1)

    reference_setup = MeshSetup(
        maximum_element_size=40,
        merge_connected_volumes=True,
        custom_element_setup=GMSH_TET4,
    )
    reference_mesh = Mesh().load_cad(geometry_path, reference_setup, threads=1)
    original_surfaces = set(reference_mesh.geometry_information["surfaces"])

    twin_surfaces = [surface_id for surface_id in mesh.geometry_information["surfaces"] if surface_id not in original_surfaces]
    assert len(twin_surfaces) == len(disconnected_surfaces)

    for surface_id, twin_surface_id in zip(disconnected_surfaces, twin_surfaces):
        assert _face_element_geometry(mesh, surface_id) == _face_element_geometry(mesh, twin_surface_id)

        surface_nodes = set(mesh.faces_connectivity[mesh.faces_connectivity[:, 1] == surface_id, 4:].flatten().astype(int))
        twin_nodes = set(mesh.faces_connectivity[mesh.faces_connectivity[:, 1] == twin_surface_id, 4:].flatten().astype(int))
        assert not (surface_nodes & twin_nodes)

    nodes_from_volumes = _nodes_from_volumes(mesh)
    assert not set(nodes_from_volumes[1]) & set(nodes_from_volumes[4])
    assert not set(nodes_from_volumes[1]) & set(nodes_from_volumes[4]) & set(nodes_from_volumes[6])
    assert not set(nodes_from_volumes[3]) & set(nodes_from_volumes[4]) & set(nodes_from_volumes[5]) & set(nodes_from_volumes[6])

    assert not mesh.disconnected_nodes_data


def _face_element_geometry(mesh: Mesh, surface_id: int) -> set[tuple]:
    node_index = {int(node): i for i, node in enumerate(mesh.nodal_coordinates[:, 0])}
    coords = mesh.nodal_coordinates
    rows = mesh.faces_connectivity[mesh.faces_connectivity[:, 1] == surface_id]
    geometry = set()
    for connect in rows[:, 4:]:
        points = sorted(tuple(np.round(coords[node_index[int(node)], 1:], 6)) for node in connect)
        geometry.add(tuple(points))
    return geometry


def _volume_of_solid(mesh: Mesh, solid_id: int) -> int:
    row = mesh.solids_connectivity[mesh.solids_connectivity[:, 0] == solid_id]
    return int(row[0, 1])


def _nodes_from_volumes(mesh: Mesh) -> dict[int, set[int]]:
    nodes_from_volumes = {volume_id: set() for volume_id in mesh.all_solid_ids()}
    for row in mesh.solids_connectivity:
        nodes_from_volumes[int(row[1])].update(int(n) for n in row[4:])
    return nodes_from_volumes


def _mean_edge_length_per_volume(mesh: Mesh) -> dict[int, float]:
    node_index = {int(node): i for i, node in enumerate(mesh.nodal_coordinates[:, 0])}
    coords = mesh.nodal_coordinates[:, 1:]

    mean_edges = {}
    for volume_id in mesh.all_solid_ids():
        rows = mesh.solids_connectivity[mesh.solids_connectivity[:, 1] == volume_id]
        lengths = []
        for connect in rows[:, 4:]:
            for a, b in combinations(connect, 2):
                lengths.append(np.linalg.norm(coords[node_index[int(a)]] - coords[node_index[int(b)]]))
        mean_edges[volume_id] = float(np.mean(lengths))

    return mean_edges


def _compare_mesh(mesh: Mesh, mesh_path: Path | str):
    mesh_path = Path(mesh_path)
    mappings = dict(
        face_to_solid_element=mesh.face_to_solid_element.items(),
        # line_from_element=mesh.line_from_element.items(),
        # surface_from_element=mesh.surface_from_element.items(),
        # volume_from_element=mesh.volume_from_element.items(),
    )

    if not mesh_path.exists():
        mesh_path.mkdir(parents=True)
        mesh.export_nodal_coordinates(mesh_path / "nodal_coordinates.dat")
        mesh.export_line_elements_connectivity(mesh_path / "lines_connectivity.dat")
        mesh.export_face_elements_connectivity(mesh_path / "faces_connectivity.dat")
        mesh.export_solid_elements_connectivity(mesh_path / "solids_connectivity.dat")
        (mesh_path / "mappings.dat").write_text(str(mappings))  # saving the str of the dict
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
    expected_mappings = (mesh_path / "mappings.dat").read_text()

    if gmsh.isInitialized():
        gmsh.finalize()

    assert np.allclose(expected_nodal_coordinates, mesh.nodal_coordinates)
    assert np.allclose(expected_lines_connectivity, mesh.lines_connectivity)
    assert np.allclose(expected_faces_connectivity, mesh.faces_connectivity)
    assert np.allclose(expected_solids_connectivity, mesh.solids_connectivity)
    assert expected_mappings == str(mappings)

    if (expected_solids_connectivity.size != 0) and (mesh.solids_connectivity.size != 0):
        assert np.allclose(expected_solids_connectivity, mesh.solids_connectivity)
