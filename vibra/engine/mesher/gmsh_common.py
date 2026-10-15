from __future__ import annotations

import logging

import gmsh
import numpy as np

from vibra.engine.mesher.mesh import Mesh

logger = logging.getLogger(__name__)


class GmshCommon:
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
            mesh.remove_disconnected_nodes()

        # logging.info("Post-processing mesh... [68/100]")
        mesh.process_mesh_related_mappings("Post-processing")
        # mesh.map_face_elements_to_solid_elements()

        logger.info("Post-processing mesh... [80/100]")
        mesh.process_disconnected_nodes_criterion()

        logger.info("Post-processing mesh... [90/100]")
        mesh.process_collapsed_elements_data_criterion()

        return mesh
