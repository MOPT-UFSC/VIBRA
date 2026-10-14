from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import IntEnum
from typing import Self

import gmsh
import numpy as np

from vibra.engine.mesher.mesh import Mesh

logger = logging.getLogger(__name__)


class GmshCommon:
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
    class ElementSetup:
        algorithm_2d: GmshCommon.MeshAlgorithms2D
        algorithm_3d: GmshCommon.MeshAlgorithms3D
        subdivision_algorithm: GmshCommon.SubdivisionAlgorithms
        recombination_algorithm: GmshCommon.RecombinationAlgorithms
        recombine_all: bool
        second_order_incomplete: bool
        element_order: int
        dimensions: int

        def copy(self) -> Self:
            return self.__class__(**self.__dict__)

    def _create_mesh_from_gmsh_state(self) -> Mesh:
        mesh = Mesh()

        indices, coords, _parametric_coords = gmsh.model.mesh.get_nodes(includeBoundary=True)
        indices = np.array(indices) - 1
        coords = np.array(coords)

        nodal_coordinates = np.zeros((np.max(indices) + 1, 4))
        nodal_coordinates[indices, 1:] = coords.reshape(-1, 3) * mesh.get_length_unit_factor()
        nodal_coordinates[indices, :1] = indices.reshape(-1, 1)

        dim_to_data = {}
        for el_type in gmsh.model.mesh.get_element_types():
            _el_name, dim, _order, num_nodes, _, _ = gmsh.model.mesh.get_element_properties(el_type)
            element_tags, node_tags = gmsh.model.mesh.get_elements_by_type(el_type)

            element_indices = np.arange(len(element_tags)).reshape(-1, 1)
            entity_tags = np.zeros_like(element_indices)
            element_types = np.full_like(element_indices, el_type)
            nodes_per_element = np.full_like(element_indices, num_nodes)
            connectivity = np.array(node_tags).reshape(-1, num_nodes) - 1

            element_tags = np.array(element_tags)
            for _, entity_tag in gmsh.model.get_entities(dim):
                _, entity_element_tags, _ = gmsh.model.mesh.get_elements(dim, entity_tag)
                entity_tags[np.isin(element_tags, entity_element_tags)] = entity_tag

            data = np.concatenate(
                [
                    element_indices,
                    entity_tags,
                    element_types,
                    nodes_per_element,
                    connectivity,
                ],
                axis=1,
            ).astype(int)
            dim_to_data[dim] = data

        mesh.set_mesh_data(
            nodal_coordinates=nodal_coordinates,
            lines_connectivity=dim_to_data.get(1, np.zeros((0, 4), dtype=int)),
            faces_connectivity=dim_to_data.get(2, np.zeros((0, 4), dtype=int)),
            solids_connectivity=dim_to_data.get(3, np.zeros((0, 4), dtype=int)),
        )

        if mesh.suppressed_volumes:
            self.remove_disconnected_nodes()

        # logging.info("Post-processing mesh... [68/100]")
        mesh.process_mesh_related_mappings("Post-processing")
        # mesh.map_face_elements_to_solid_elements()

        logger.info("Post-processing mesh... [80/100]")
        mesh.process_disconnected_nodes_criterion()

        logger.info("Post-processing mesh... [90/100]")
        mesh.process_collapsed_elements_data_criterion()

        return mesh


GMSH_TET4 = GmshCommon.ElementSetup(
    algorithm_2d=GmshCommon.MeshAlgorithms2D.DELAUNAY_2D,
    algorithm_3d=GmshCommon.MeshAlgorithms3D.HXT_3D,
    subdivision_algorithm=GmshCommon.SubdivisionAlgorithms.NO_SUBDIVISION,
    recombination_algorithm=GmshCommon.RecombinationAlgorithms.SIMPLE_RECOMBINATION,
    recombine_all=False,
    second_order_incomplete=False,
    element_order=1,
    dimensions=3,
)

GMSH_TET10 = GmshCommon.ElementSetup(
    algorithm_2d=GmshCommon.MeshAlgorithms2D.DELAUNAY_2D,
    algorithm_3d=GmshCommon.MeshAlgorithms3D.HXT_3D,
    subdivision_algorithm=GmshCommon.SubdivisionAlgorithms.NO_SUBDIVISION,
    recombination_algorithm=GmshCommon.RecombinationAlgorithms.SIMPLE_RECOMBINATION,
    recombine_all=False,
    second_order_incomplete=False,
    element_order=2,
    dimensions=3,
)

GMSH_HEX8 = GmshCommon.ElementSetup(
    algorithm_2d=GmshCommon.MeshAlgorithms2D.QUASI_STRUCTURED_QUADS_2D,
    algorithm_3d=GmshCommon.MeshAlgorithms3D.DELAUNAY_3D,
    subdivision_algorithm=GmshCommon.SubdivisionAlgorithms.ALL_HEXAHEDRA_SUBDIVISION,
    recombination_algorithm=GmshCommon.RecombinationAlgorithms.BLOSSOM_FULL_QUAD_RECOMBINATION,
    recombine_all=True,
    second_order_incomplete=False,
    element_order=1,
    dimensions=3,
)

GMSH_HEX20 = GmshCommon.ElementSetup(
    algorithm_2d=GmshCommon.MeshAlgorithms2D.QUASI_STRUCTURED_QUADS_2D,
    algorithm_3d=GmshCommon.MeshAlgorithms3D.DELAUNAY_3D,
    subdivision_algorithm=GmshCommon.SubdivisionAlgorithms.ALL_HEXAHEDRA_SUBDIVISION,
    recombination_algorithm=GmshCommon.RecombinationAlgorithms.BLOSSOM_FULL_QUAD_RECOMBINATION,
    recombine_all=True,
    second_order_incomplete=True,
    element_order=2,
    dimensions=3,
)

GMSH_VISUAL_MESH = GmshCommon.ElementSetup(
    algorithm_2d=GmshCommon.MeshAlgorithms2D.DELAUNAY_2D,
    algorithm_3d=GmshCommon.MeshAlgorithms3D.HXT_3D,
    subdivision_algorithm=GmshCommon.SubdivisionAlgorithms.NO_SUBDIVISION,
    recombination_algorithm=GmshCommon.RecombinationAlgorithms.SIMPLE_RECOMBINATION,
    recombine_all=False,
    second_order_incomplete=False,
    element_order=1,
    dimensions=2,
)

DEFAULT_ELEMENT_SETUP = GMSH_TET4
