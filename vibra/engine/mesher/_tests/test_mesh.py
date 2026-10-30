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


def test_detect_refinement_need():
    mesh = Mesh(length_unit="millimeter")
    mesh.length_from_lines = {1: 0.002, 2: 0.02, 3: 0.001}
    mesh.area_from_surfaces = {10: 1e-6, 11: 1.4e-6, 12: 5e-6, 13: 0.0}
    mesh.surfaces_from_line = {1: [10, 12], 2: [12], 3: [10, 11, 12]}

    result = mesh.detect_refinement_need(5)

    assert result["line_ids"] == [1, 3]
    assert result["surface_ids"] == [10, 11]
    assert result["surface_areas"] == {10: 1e-6, 11: 1.4e-6}
    assert result["refinement_length"] == 0.001
    assert [group["line_id"] for group in result["groups"]] == [1, 3]


def test_detect_refinement_need_with_adjacent_lines():
    mesh = Mesh(length_unit="millimeter")
    mesh.length_from_lines = {1: 0.001, 2: 0.002, 3: 0.02, 4: 0.01}
    mesh.area_from_surfaces = {10: 1e-6, 11: 2e-6, 12: 3e-6}
    mesh.surfaces_from_line = {1: [10], 2: [10], 3: [11], 4: [12]}
    mesh.points_from_line = {1: [1, 2], 2: [2, 3], 3: [3, 4], 4: [5, 6]}
    mesh.lines_from_point = {1: [1], 2: [1, 2], 3: [2, 3], 4: [3], 5: [4], 6: [4]}

    result_without_adjacent = mesh.detect_refinement_need(5, adjacent_factor=None)
    assert result_without_adjacent["line_ids"] == [1, 2]

    result_with_adjacent = mesh.detect_refinement_need(5, adjacent_factor=25)
    assert result_with_adjacent["line_ids"] == [1, 2, 3]


def test_group_refinement_sizes():
    mesh = Mesh(length_unit="millimeter")
    groups = [
        {"line_id": 1, "line_length": 0.00008, "surface_ids": [10]},
        {"line_id": 2, "line_length": 0.00009, "surface_ids": [10, 11]},
        {"line_id": 3, "line_length": 0.002, "surface_ids": [10, 20]},
        {"line_id": 4, "line_length": 0.004, "surface_ids": [21]},
    ]

    bins = mesh.group_refinement_sizes(groups, max_bins=5, merge_ratio=1.5)

    assert [bin_data["surface_ids"] for bin_data in bins] == [[10, 11], [20], [21]]
    assert [bin_data["element_size"] for bin_data in bins] == [0.000085, 0.002, 0.004]
    assert bins[0]["line_length_sum"] == 0.00017

    merged_bins = mesh.group_refinement_sizes(groups, max_bins=2, merge_ratio=1.5)

    assert len(merged_bins) == 2
    assert [bin_data["surface_ids"] for bin_data in merged_bins] == [[10, 11], [20, 21]]
    assert merged_bins[1]["element_size"] == 0.003

    multiplied_bins = mesh.group_refinement_sizes(groups, max_bins=5, merge_ratio=1.5, size_multiplier=2.0)

    assert [bin_data["element_size"] for bin_data in multiplied_bins] == [0.00017, 0.004, 0.008]


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
