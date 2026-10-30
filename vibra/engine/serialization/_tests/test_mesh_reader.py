from pathlib import Path

import gmsh
import numpy as np

from vibra import PROJECT_DIR
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import ElementTopology
from vibra.engine.serialization.mesh_reader import MeshReader


def test_tetrahedron_4_mesh():
    path = str(PROJECT_DIR / "validation_files/data/Comsol/tet4_linear/rectangular_cavities_tet4_40x30_mm.nas")
    mesh_test_path = str(PROJECT_DIR / "validation_files/data/nastran_mesh_info/tetrahedron_tet4/")

    mesh = MeshReader(path).read_mesh()

    assert mesh.element_topology == ElementTopology("tetrahedral", "linear")
    _compare_mesh(
        mesh,
        mesh_test_path,
    )


def test_tetrahedron_10_mesh():
    path = str(PROJECT_DIR / "validation_files/data/Comsol/tet10_lagrange/rectangular_cavities_tet10_50x30_mm.nas")
    mesh_test_path = str(PROJECT_DIR / "validation_files/data/nastran_mesh_info/tetrahedron_tet10/")

    mesh = MeshReader(path).read_mesh()

    assert mesh.element_topology == ElementTopology("tetrahedral", "quadratic")
    _compare_mesh(
        mesh,
        mesh_test_path,
    )


def test_hexahedron_8_mesh():
    path = str(PROJECT_DIR / "validation_files/data/Comsol/hex8_linear/rectangular_cavities_hex8_40x30_mm.nas")
    mesh_test_path = str(PROJECT_DIR / "validation_files/data/nastran_mesh_info/tetrahedron_hex8/")

    mesh = MeshReader(path).read_mesh()
    assert mesh.element_topology == ElementTopology("hexahedral", "linear")
    _compare_mesh(
        mesh,
        mesh_test_path,
    )


def test_hexahedron_20_mesh():
    path = str(PROJECT_DIR / "validation_files/data/Comsol/hex20_lagrange/rectangular_cavities_hex20_40x30_mm.nas")
    mesh_test_path = str(PROJECT_DIR / "validation_files/data/nastran_mesh_info/tetrahedron_hex20/")

    mesh = MeshReader(path).read_mesh()

    assert mesh.element_topology == ElementTopology("hexahedral", "quadratic")
    _compare_mesh(
        mesh,
        mesh_test_path,
    )


def _compare_mesh(mesh: Mesh, mesh_path: Path | str):
    mesh_path = Path(mesh_path)
    mappings = {
        "face_to_solid_element": mesh.face_to_solid_element.items(),
        "line_from_element": mesh.elements_from_line.items(),
        "surface_from_element": mesh.elements_from_surface.items(),
        "volume_from_element": mesh.elements_from_volume.items(),
    }
    geometry = {
        "surfaces_from_volume": mesh.surfaces_from_volume.items(),
        "lines_from_surface": mesh.lines_from_surface.items(),
        "points_from_line": mesh.points_from_line.items(),
        "volumes_from_surface": mesh.volumes_from_surface.items(),
        "surfaces_from_line": mesh.surfaces_from_line.items(),
        "lines_from_point": mesh.lines_from_point.items(),
        "face_elements_connected_to_nodes": mesh.face_elements_connected_to_nodes.items(),
        "length_from_lines": mesh.length_from_lines.items(),
        "area_from_surfaces": mesh.area_from_surfaces.items(),
        "volume_from_bodies": mesh.volume_from_bodies.items(),
    }

    if not mesh_path.exists():
        mesh_path.mkdir(parents=True)
        mesh.export_nodal_coordinates(mesh_path / "nodal_coordinates.dat")
        mesh.export_line_elements_connectivity(mesh_path / "lines_connectivity.dat")
        mesh.export_face_elements_connectivity(mesh_path / "faces_connectivity.dat")
        mesh.export_solid_elements_connectivity(mesh_path / "solids_connectivity.dat")
        (mesh_path / "mappings.dat").write_text(str(mappings))  # saving the str of the dict
        (mesh_path / "geometry.dat").write_text(str(geometry))  # saving the str of the dict
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
    expected_geometry = (mesh_path / "geometry.dat").read_text()

    if gmsh.isInitialized():
        gmsh.finalize()

    assert np.allclose(expected_nodal_coordinates, mesh.nodal_coordinates)
    assert np.allclose(expected_lines_connectivity, mesh.lines_connectivity)
    assert np.allclose(expected_faces_connectivity, mesh.faces_connectivity)
    assert np.allclose(expected_solids_connectivity, mesh.solids_connectivity)
    assert expected_mappings == str(mappings)
    assert expected_geometry == str(geometry)

    if (expected_solids_connectivity.size != 0) and (mesh.solids_connectivity.size != 0):
        assert np.allclose(expected_solids_connectivity, mesh.solids_connectivity)
