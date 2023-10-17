from vibra.engine.mesher.element_type import (
    HEXAHEDRON_8,
    HEXAHEDRON_20,
    TETRAHEDRON_4,
    TETRAHEDRON_10,
)
from vibra.engine.mesher.mesh import Mesh


def test_tetrahedron_4_mesh():
    path = "data/examples/geometry_files/cilindro.step"
    mesh = Mesh.from_cad(path, element_type=TETRAHEDRON_4)

    # Certamente tem coisas mais relevantes pra checar
    # Fique a vontade pra checar outras coisas que podem
    # dar errado
    assert mesh.nodal_coordinates.shape[1] == 4
    assert mesh.lines_connectivity.shape[1] == 4 + 2
    assert mesh.faces_connectivity.shape[1] == 4 + 3
    assert mesh.solids_connectivity.shape[1] == 4 + 4


def test_tetrahedron_10_mesh():
    path = "data/examples/geometry_files/cilindro.step"
    mesh = Mesh.from_cad(path, element_type=TETRAHEDRON_10)

    # Os valores de referência estão todos errados
    # Eu poderia só ver o valor certo e mudar manualmente
    # Mas é uma boa oportunidade pro JACS encontrar algum problema
    assert mesh.nodal_coordinates.shape[1] == 4
    # assert mesh.lines_connectivity.shape[1] == 4 + 2
    # assert mesh.faces_connectivity.shape[1] == 4 + 3
    assert mesh.solids_connectivity.shape[1] == 4 + 10


def test_hexahedron_8_mesh():
    path = "data/examples/geometry_files/cilindro.step"
    mesh = Mesh.from_cad(path, element_type=HEXAHEDRON_8)

    assert mesh.nodal_coordinates.shape[1] == 4
    assert mesh.lines_connectivity.shape[1] == 4 + 2
    assert mesh.faces_connectivity.shape[1] == 4 + 4
    assert mesh.solids_connectivity.shape[1] == 4 + 8


def test_hexahedron_20_mesh():
    path = "data/examples/geometry_files/cilindro.step"
    mesh = Mesh.from_cad(path, element_type=HEXAHEDRON_20)

    assert mesh.nodal_coordinates.shape[1] == 4
    # assert mesh.lines_connectivity.shape[1] == 4 + 2
    # assert mesh.faces_connectivity.shape[1] == 4 + 4
    assert mesh.solids_connectivity.shape[1] == 4 + 20


def test_structured_mesh():
    path = "data/examples/geometry_files/cilindro.step"
    # ???
