from pathlib import Path

import gmsh
import numpy as np

from vibra import PROJECT_DIR
from vibra.engine.mesher.element_setup import GMSH_HEX8, GMSH_HEX20, GMSH_TET4, GMSH_TET10
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import ElementTopology, MeshSetup


def test_tetrahedron_4_mesh():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/cylinder.step")
    mesh_test_path = str(PROJECT_DIR / "validation_files/data/mesh_info/cilinder_tet4/")

    mesh_setup = MeshSetup(
        minimum_element_size=30,
        maximum_element_size=80,
        custom_element_setup=GMSH_TET4,
    )
    mesh = Mesh().new_load_cad(geometry_path, mesh_setup, threads=1)
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
    mesh = Mesh().new_load_cad(geometry_path, mesh_setup, threads=1)
    assert mesh.element_topology == ElementTopology("tetrahedral", "quadratic")

    _compare_mesh(
        mesh,
        mesh_test_path,
    )


def test_hexahedron_8_mesh():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/cylinder.step")
    mesh_test_path = str(PROJECT_DIR / "validation_files/data/mesh_info/cilinder_hex8/")

    mesh_setup = MeshSetup(
        minimum_element_size=30,
        maximum_element_size=80,
        custom_element_setup=GMSH_HEX8,
    )
    mesh = Mesh().new_load_cad(geometry_path, mesh_setup, threads=1)
    assert mesh.element_topology == ElementTopology("hexahedral", "linear")

    # hexahedral mesh is not deterministic =(
    # _compare_mesh(
    #     mesh,
    #     mesh_test_path,
    # )


def test_hexahedron_20_mesh():
    geometry_path = str(PROJECT_DIR / "data/examples/geometry_files/parallelepiped.step")
    mesh_test_path = str(PROJECT_DIR / "validation_files/data/mesh_info/parallelepiped_hex20/")

    mesh_setup = MeshSetup(
        minimum_element_size=300,
        maximum_element_size=300,
        custom_element_setup=GMSH_HEX20,
    )
    mesh = Mesh().new_load_cad(geometry_path, mesh_setup, threads=1)
    assert mesh.element_topology == ElementTopology("hexahedral", "quadratic")

    # hexahedral mesh is not deterministic =(
    # _compare_mesh(
    #     mesh,
    #     mesh_test_path,
    # )


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
