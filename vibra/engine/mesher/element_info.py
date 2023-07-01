from dataclasses import dataclass

from vibra.engine.mesher import gmsh_constants


@dataclass
class ElementInfo:
    algorithm_2d: int
    algorithm_3d: int
    subdivision_algorithm: int
    recombination_algorithm: int

    recombine_all: bool
    second_order_incomplete: bool
    element_order: int


TETRAHEDRON_4 = ElementInfo(
    algorithm_2d=gmsh_constants.DELAUNAY_2D,
    algorithm_3d=gmsh_constants.DELAUNAY_3D,
    subdivision_algorithm=gmsh_constants.NO_SUBDIVISION,
    recombination_algorithm=gmsh_constants.SIMPLE_RECOMBINATION,
    recombine_all=False,
    second_order_incomplete=False,
    element_order=1,
)

TETRAHEDRON_10 = ElementInfo(
    algorithm_2d=gmsh_constants.DELAUNAY_2D,
    algorithm_3d=gmsh_constants.DELAUNAY_3D,
    subdivision_algorithm=gmsh_constants.NO_SUBDIVISION,
    recombination_algorithm=gmsh_constants.SIMPLE_RECOMBINATION,
    recombine_all=False,
    second_order_incomplete=False,
    element_order=2,
)

HEXAHEDRON_8 = ElementInfo(
    algorithm_2d=gmsh_constants.QUASI_STRUCTURED_QUADS_2D,
    algorithm_3d=gmsh_constants.DELAUNAY_3D,
    subdivision_algorithm=gmsh_constants.ALL_HEXAHEDRA_SUBDIVISION,
    recombination_algorithm=gmsh_constants.BLOSSOM_FULL_QUAD_RECOMBINATION,
    recombine_all=True,
    second_order_incomplete=False,
    element_order=1,
)

HEXAHEDRON_20 = ElementInfo(
    algorithm_2d=gmsh_constants.QUASI_STRUCTURED_QUADS_2D,
    algorithm_3d=gmsh_constants.DELAUNAY_3D,
    subdivision_algorithm=gmsh_constants.ALL_HEXAHEDRA_SUBDIVISION,
    recombination_algorithm=gmsh_constants.BLOSSOM_FULL_QUAD_RECOMBINATION,
    recombine_all=True,
    second_order_incomplete=True,
    element_order=2,
)

DEFAULT = TETRAHEDRON_4