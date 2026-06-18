from __future__ import annotations

from dataclasses import dataclass

from vibra.engine.mesher.gmsh_constants import (
    MeshAlgorithms2D,
    MeshAlgorithms3D,
    RecombinationAlgorithms,
    SubdivisionAlgorithms,
)


@dataclass
class ElementSetup:
    algorithm_2d: MeshAlgorithms2D
    algorithm_3d: MeshAlgorithms3D
    subdivision_algorithm: SubdivisionAlgorithms
    recombination_algorithm: RecombinationAlgorithms
    recombine_all: bool
    second_order_incomplete: bool
    element_order: int
    dimensions: int

    def copy(self) -> ElementSetup:
        return ElementSetup(**self.__dict__)


GMSH_TET4 = ElementSetup(
    algorithm_2d=MeshAlgorithms2D.DELAUNAY_2D,
    algorithm_3d=MeshAlgorithms3D.HXT_3D,
    subdivision_algorithm=SubdivisionAlgorithms.NO_SUBDIVISION,
    recombination_algorithm=RecombinationAlgorithms.SIMPLE_RECOMBINATION,
    recombine_all=False,
    second_order_incomplete=False,
    element_order=1,
    dimensions=3,
)

GMSH_TET10 = ElementSetup(
    algorithm_2d=MeshAlgorithms2D.DELAUNAY_2D,
    algorithm_3d=MeshAlgorithms3D.HXT_3D,
    subdivision_algorithm=SubdivisionAlgorithms.NO_SUBDIVISION,
    recombination_algorithm=RecombinationAlgorithms.SIMPLE_RECOMBINATION,
    recombine_all=False,
    second_order_incomplete=False,
    element_order=2,
    dimensions=3,
)

GMSH_HEX8 = ElementSetup(
    algorithm_2d=MeshAlgorithms2D.QUASI_STRUCTURED_QUADS_2D,
    algorithm_3d=MeshAlgorithms3D.DELAUNAY_3D,
    subdivision_algorithm=SubdivisionAlgorithms.ALL_HEXAHEDRA_SUBDIVISION,
    recombination_algorithm=RecombinationAlgorithms.BLOSSOM_FULL_QUAD_RECOMBINATION,
    recombine_all=True,
    second_order_incomplete=False,
    element_order=1,
    dimensions=3,
)

GMSH_HEX20 = ElementSetup(
    algorithm_2d=MeshAlgorithms2D.QUASI_STRUCTURED_QUADS_2D,
    algorithm_3d=MeshAlgorithms3D.DELAUNAY_3D,
    subdivision_algorithm=SubdivisionAlgorithms.ALL_HEXAHEDRA_SUBDIVISION,
    recombination_algorithm=RecombinationAlgorithms.BLOSSOM_FULL_QUAD_RECOMBINATION,
    recombine_all=True,
    second_order_incomplete=True,
    element_order=2,
    dimensions=3,
)

GMSH_VISUAL_MESH = ElementSetup(
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