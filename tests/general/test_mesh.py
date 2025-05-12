import numpy as np
import pytest
from pathlib import Path

from vibra.engine.mesher.element_type import (
    HEXAHEDRON_8,
    HEXAHEDRON_20,
    TETRAHEDRON_4,
    TETRAHEDRON_10,
)
from vibra.engine.mesher.mesh import Mesh


def test_tetrahedron_4_mesh():
    mesh = Mesh().load_cad(
        "data/examples/geometry_files/cilindro.step",
        minimum_element_size=30,
        maximum_element_size=80,
        threads=1,
        element_type=TETRAHEDRON_4,
    )

    _compare_mesh(
        mesh,
        "tests/general/mesh_info/cilinder_tet4/",
    )

@pytest.mark.skip
def test_tetrahedron_10_mesh():
    mesh = Mesh().load_cad(
        "data/examples/geometry_files/tetrahedron.step",
        minimum_element_size=30,
        maximum_element_size=80,
        threads=1,
        element_type=TETRAHEDRON_10,
        gmsh_gui=True
    )

    _compare_mesh(
        mesh,
        "tests/general/mesh_info/tetrahedron_tet10/",
    )

@pytest.mark.skip
def test_hexahedron_8_mesh():
    mesh = Mesh().load_cad(
        "data/examples/geometry_files/cilindro.step",
        minimum_element_size=30,
        maximum_element_size=80,
        threads=1,
        element_type=HEXAHEDRON_8,
    )

    _compare_mesh(
        mesh,
        "tests/general/mesh_info/cilinder_hex8/",
    )

@pytest.mark.skip
def test_hexahedron_20_mesh():
    mesh = Mesh().load_cad(
        "data/examples/geometry_files/parallelepiped.step",
        minimum_element_size=300,
        maximum_element_size=300,
        threads=1,
        element_type=HEXAHEDRON_20,
    )

    _compare_mesh(
        mesh,
        "tests/general/mesh_info/parallelepiped_hex20/",
    )


def _compare_mesh(mesh: Mesh, mesh_path: Path | str):
    mesh_path = Path(mesh_path)

    if not mesh_path.exists():
        mesh_path.mkdir(parents=True)
        mesh.export_nodal_coordinates(mesh_path / "nodal_coordinates.dat")
        mesh.export_line_elements_connectivity(mesh_path / "lines_connectivity.dat")
        mesh.export_face_elements_connectivity(mesh_path / "faces_connectivity.dat")
        mesh.export_solid_elements_connectivity(mesh_path / "solids_connectivity.dat")

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

    assert np.allclose(expected_nodal_coordinates, mesh.nodal_coordinates)
    assert np.allclose(expected_lines_connectivity, mesh.lines_connectivity)
    assert np.allclose(expected_faces_connectivity, mesh.faces_connectivity)
    assert np.allclose(expected_solids_connectivity, mesh.solids_connectivity)
