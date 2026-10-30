from dataclasses import dataclass
from enum import IntEnum
from typing import Self


class MeshAlgorithms2D(IntEnum):
    MESH_ADAPT_2D = 1
    AUTOMATIC_2D = 2
    INITIAL_MESH_ONLY_2D = 3
    DELAUNAY_2D = 5
    FRONTAL_DELAUNAY_2D = 6
    BAMG_2D = 7
    FRONTAL_DELAUNAY_FOR_QUADS_2D = 8
    PACKING_OF_PARALLELOGRAMS_2D = 9
    QUASI_STRUCTURED_QUADS_2D = 11


class MeshAlgorithms3D(IntEnum):
    DELAUNAY_3D = 1
    INITIAL_MESH_ONLY_3D = 3
    FRONTAL_3D = 4
    MMG_3D = 7
    RTREE_3D = 9
    HXT_3D = 10


class RecombinationAlgorithms(IntEnum):
    SIMPLE_RECOMBINATION = 0
    BLOSSOM_RECOMBINATION = 1
    SIMPLE_FULL_QUAD_RECOMBINATION = 2
    BLOSSOM_FULL_QUAD_RECOMBINATION = 3


class SubdivisionAlgorithms(IntEnum):
    NO_SUBDIVISION = 0
    ALL_QuadrangleS_SUBDIVISION = 1
    ALL_HEXAHEDRA_SUBDIVISION = 2
    BARYCENTRIC_SUBDIVISION = 3


@dataclass
class GmshElementSetup:
    algorithm_2d: MeshAlgorithms2D
    algorithm_3d: MeshAlgorithms3D
    subdivision_algorithm: SubdivisionAlgorithms
    recombination_algorithm: RecombinationAlgorithms
    recombine_all: bool
    second_order_incomplete: bool
    element_order: int
    dimensions: int

    def copy(self) -> Self:
        return GmshElementSetup(**self.__dict__)


GMSH_TET4 = GmshElementSetup(
    algorithm_2d=MeshAlgorithms2D.DELAUNAY_2D,
    algorithm_3d=MeshAlgorithms3D.HXT_3D,
    subdivision_algorithm=SubdivisionAlgorithms.NO_SUBDIVISION,
    recombination_algorithm=RecombinationAlgorithms.SIMPLE_RECOMBINATION,
    recombine_all=False,
    second_order_incomplete=False,
    element_order=1,
    dimensions=3,
)

GMSH_TET10 = GmshElementSetup(
    algorithm_2d=MeshAlgorithms2D.DELAUNAY_2D,
    algorithm_3d=MeshAlgorithms3D.HXT_3D,
    subdivision_algorithm=SubdivisionAlgorithms.NO_SUBDIVISION,
    recombination_algorithm=RecombinationAlgorithms.SIMPLE_RECOMBINATION,
    recombine_all=False,
    second_order_incomplete=False,
    element_order=2,
    dimensions=3,
)

GMSH_HEX8 = GmshElementSetup(
    algorithm_2d=MeshAlgorithms2D.QUASI_STRUCTURED_QUADS_2D,
    algorithm_3d=MeshAlgorithms3D.DELAUNAY_3D,
    subdivision_algorithm=SubdivisionAlgorithms.ALL_HEXAHEDRA_SUBDIVISION,
    recombination_algorithm=RecombinationAlgorithms.BLOSSOM_FULL_QUAD_RECOMBINATION,
    recombine_all=True,
    second_order_incomplete=False,
    element_order=1,
    dimensions=3,
)

GMSH_HEX20 = GmshElementSetup(
    algorithm_2d=MeshAlgorithms2D.QUASI_STRUCTURED_QUADS_2D,
    algorithm_3d=MeshAlgorithms3D.DELAUNAY_3D,
    subdivision_algorithm=SubdivisionAlgorithms.ALL_HEXAHEDRA_SUBDIVISION,
    recombination_algorithm=RecombinationAlgorithms.BLOSSOM_FULL_QUAD_RECOMBINATION,
    recombine_all=True,
    second_order_incomplete=True,
    element_order=2,
    dimensions=3,
)

GMSH_VISUAL_MESH = GmshElementSetup(
    algorithm_2d=MeshAlgorithms2D.DELAUNAY_2D,
    algorithm_3d=MeshAlgorithms3D.HXT_3D,
    subdivision_algorithm=SubdivisionAlgorithms.NO_SUBDIVISION,
    recombination_algorithm=RecombinationAlgorithms.SIMPLE_RECOMBINATION,
    recombine_all=False,
    second_order_incomplete=False,
    element_order=1,
    dimensions=2,
)

DEFAULT_ELEMENT_SETUP = GMSH_TET4
