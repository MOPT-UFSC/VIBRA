import warnings 

from dataclasses import dataclass

from vibra.engine.mesher import gmsh_constants

warnings.warn("The file element_type is deprecated, use element_setup instead", DeprecationWarning)

@dataclass
class ElementType:
    element_type: str
    shape_function: str
    algorithm_2d: int
    algorithm_3d: int
    subdivision_algorithm: int
    recombination_algorithm: int
    recombine_all: bool
    second_order_incomplete: bool
    element_order: int
    dimensions: int


TETRAHEDRON_4 = ElementType(
    element_type = "tetrahedral",
    shape_function = "linear",
    algorithm_2d = gmsh_constants.DELAUNAY_2D,
    algorithm_3d = gmsh_constants.HXT_3D,
    subdivision_algorithm = gmsh_constants.NO_SUBDIVISION,
    recombination_algorithm = gmsh_constants.SIMPLE_RECOMBINATION,
    recombine_all = False,
    second_order_incomplete = False,
    element_order = 1,
    dimensions = 3,
)

TETRAHEDRON_10 = ElementType(
    element_type = "tetrahedral",
    shape_function = "quadratic",
    algorithm_2d = gmsh_constants.DELAUNAY_2D,
    algorithm_3d = gmsh_constants.HXT_3D,
    subdivision_algorithm = gmsh_constants.NO_SUBDIVISION,
    recombination_algorithm = gmsh_constants.SIMPLE_RECOMBINATION,
    recombine_all = False,
    second_order_incomplete = False,
    element_order = 2,
    dimensions = 3,
)

HEXAHEDRON_8 = ElementType(
    element_type = "hexahedral",
    shape_function = "linear",
    algorithm_2d = gmsh_constants.QUASI_STRUCTURED_QUADS_2D,
    algorithm_3d = gmsh_constants.DELAUNAY_3D,
    subdivision_algorithm = gmsh_constants.ALL_HEXAHEDRA_SUBDIVISION,
    recombination_algorithm = gmsh_constants.BLOSSOM_FULL_QUAD_RECOMBINATION,
    recombine_all = True,
    second_order_incomplete = False,
    element_order = 1,
    dimensions = 3,
)

HEXAHEDRON_20 = ElementType(
    element_type = "hexahedral",
    shape_function = "quadratic",
    algorithm_2d = gmsh_constants.QUASI_STRUCTURED_QUADS_2D,
    algorithm_3d = gmsh_constants.DELAUNAY_3D,
    subdivision_algorithm = gmsh_constants.ALL_HEXAHEDRA_SUBDIVISION,
    recombination_algorithm = gmsh_constants.BLOSSOM_FULL_QUAD_RECOMBINATION,
    recombine_all = True,
    second_order_incomplete = True,
    element_order = 2,
    dimensions = 3,
)

DEFAULT_ELEMENT_TYPE = TETRAHEDRON_4