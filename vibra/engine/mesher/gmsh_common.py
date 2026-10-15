from __future__ import annotations

import logging
from typing import Literal

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

    def _compute_gmsh_quality_parameters(self):
        quality_bins = {
            "gamma": (0.7, 0.15),
            "volume": (1e-3, 0),
            "minSJ": (0.3, 0.1),
            "aspectRatio": (4, 1.5),
        }

        logger.info("Computing mesh quality metrics... [10/100]")
        _, element_tags, _ = gmsh.model.mesh.get_elements(3, -1)
        if not element_tags:
            return

        # process the mesh quality metrics
        elements = element_tags[0]
        N_elem = len(elements)
        N_param = len(quality_bins.keys())
        quality_table = np.zeros((N_elem, N_param), dtype=float)

        logger.info("Computing mesh quality metrics... [25/100]")
        min_edge_quals = gmsh.model.mesh.getElementQualities(elements, "minEdge")
        max_edge_quals = gmsh.model.mesh.getElementQualities(elements, "maxEdge")

        logger.info("Computing mesh quality metrics... [40/100]")
        quality_table[:, 0] = gmsh.model.mesh.get_element_qualities(elements, "gamma")
        quality_table[:, 1] = gmsh.model.mesh.get_element_qualities(elements, "volume")
        quality_table[:, 2] = gmsh.model.mesh.get_element_qualities(elements, "minSJ")
        quality_table[:, 3] = max_edge_quals / min_edge_quals  # aspect ratio

        MeshQualityParams = Literal["gamma", "volume", "minSJ", "aspectRatio"]

        # compute the mesh quality statistics
        logger.info("Computing mesh quality metrics... [70/100]")
        quality_statistics: dict[MeshQualityParams, list[float]] = {}
        for i, parameter in enumerate(quality_bins.keys()):
            column = quality_table[:, i]
            worst = np.max(column) if (parameter == "aspectRatio") else np.min(column)
            quality_statistics[parameter] = [worst, np.mean(column), np.std(column)]

        # compute the bad elements
        logger.info("Computing mesh quality metrics... [85/100]")
        bad_elements: dict[MeshQualityParams, np.ndarray] = {}
        for j, parameter in enumerate(quality_bins.keys()):
            limit = quality_bins.get(parameter)
            if parameter == "aspectRatio":
                bad_elements[parameter] = np.where(quality_table[:, j] > limit[0])[0]
            else:
                bad_elements[parameter] = np.where(quality_table[:, j] < limit[1])[0]

        # compute the histogram data
        logger.info("Computing mesh quality metrics... [95/100]")
        histograms_data: dict[MeshQualityParams, dict] = {}
        for i, parameter in enumerate(quality_bins.keys()):
            column = quality_table[:, i]
            bins = np.linspace(np.min(column), np.max(column), 30)
            hist, bin_edges = np.histogram(column, bins=bins)

            histograms_data[parameter] = [
                hist,
                bin_edges,
                np.percentile(column, 5),
                np.percentile(column, 95),
            ]

        return {
            "statistics": quality_statistics,
            "bad_elements": bad_elements,
            "histograms_data": histograms_data,
        }

    def _process_geometry_information(self, mesh: Mesh):
        mesh.clear_geometry_data()

        unit_factor = mesh.get_length_unit_factor()
        labels = ["points", "lines", "surfaces", "volumes"]

        for dim, tag in gmsh.model.getEntities():
            if gmsh.model.getVisibility(dim, tag) == 0:
                continue

            label = labels[dim]
            mesh.geometry_information[label].append(tag)

            if dim == 0:
                continue

            value = 0.0
            if mesh.geometry_imported:
                value = gmsh.model.occ.getMass(dim, tag)

            if dim == 3:
                mesh.volume_from_bodies[tag] = value * (unit_factor**3)

            elif dim == 2:
                mesh.area_from_surfaces[tag] = value * (unit_factor**2)
                if mesh.area_from_surfaces[tag] == 0:
                    continue

                uv_min, uv_max = gmsh.model.getParametrizationBounds(dim, tag)
                uv_mid = (uv_min + uv_max) / 2
                center = gmsh.model.getValue(dim, tag, uv_mid) * unit_factor
                mesh.surfaces_centers[tag] = center

            elif dim == 1:
                mesh.length_from_lines[tag] = value * (unit_factor**1)
