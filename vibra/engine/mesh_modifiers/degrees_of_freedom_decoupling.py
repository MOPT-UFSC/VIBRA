
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

from collections import defaultdict
from copy import deepcopy
from time import time

import logging
import numpy as np


class DegreesOfFreedomDecoupling:
    def __init__(self, model: "Model"):
        self.model = model
        self.mesh = model.mesh
        self.geometry = model.geometry
        self.properties = model.properties

        self.initialize()


    def initialize(self):
        self.decouple_info = dict()
        self.nodes_mapping = dict()
        self.surfaces_mapping = dict()
        self.lines_mapping = dict()
        self.points_mapping = dict()


    def gathering_decoupling_information(self):
        """ This method gathers all existing decoupling 
            information from surface properties.
        """
        self.decouple_info.clear()
        self.nodes_mapping.clear()

        if self.mesh.cache_nodal_coordinates is None:
            return

        max_surface_id = max(self.geometry.surfaces) if self.geometry.surfaces else 0

        for key, data in self.properties.surface_properties.items():
            (property, surface_id) = key
            if property == "degrees_of_freedom_decoupling":

                data: dict
                max_surface_id += 1
                vol_id =  data.get("volume_to_decouple")

                if isinstance(vol_id, int):    
                    self.decouple_info[surface_id] = vol_id


    def process_mappings_for_all_new_entities(self):
        """ This method performs the mappings between the existing entities
            in relation to the new entities that will be created.
        """
        self.surfaces_mapping = self.get_new_surfaces_mapping()
        self.lines_mapping = self.get_new_lines_mapping()
        self.points_mapping = self.get_new_points_mapping()


    def update_surface_property_with_new_surface_id(self):
        """ This method inserts the ID of the new surface into the
            degrees_of_freedom_decoupling surface property data.
        """
        property = "degrees_of_freedom_decoupling"
        for surface_id in self.decouple_info.keys():

            new_surface_id = self.surfaces_mapping.get(surface_id, -1)
            if new_surface_id == -1:
                continue

            data = self.properties._get_property(property, surface=surface_id)
            if isinstance(data, dict):
                aux_data = deepcopy(data)
                aux_data.update(new_surface_id=int(new_surface_id))
                self.properties.surface_properties[property, surface_id] = aux_data


    def get_new_points_mapping(self):
        """ This method returns a dictionary that maps all point IDs from
            decoupling surfaces in relation to the new point IDs that will be created.

            Returns
            -------
            point_ids_mapping : dict
                a dictionary in which keys are the point IDs from the decoupling surface, and
                the values are the new point IDs.

        """
        surface_ids = list(self.decouple_info.keys())
        point_ids = list(self.geometry.surfaces_to_points(*surface_ids))

        max_point_id = max(self.geometry.points) if self.geometry.points else 0
        new_point_ids = np.arange(len(point_ids), dtype=int) + max_point_id + 1
        point_ids_mapping = dict(zip(point_ids, new_point_ids.tolist()))

        return point_ids_mapping


    def get_new_lines_mapping(self):
        """ This method returns a dictionary that maps all line IDs from
            decoupling surfaces in relation to the new line IDs that will be created.

            Returns
            -------
            lines_mapping : dict
                a dictionary in which keys are the line IDs from the decoupling surface, and
                the values are the new line IDs.

        """
        surface_ids = list(self.decouple_info.keys())
        line_ids = list(self.geometry.surfaces_to_curves(*surface_ids))

        max_line_id = max(self.geometry.curves) if self.geometry.curves else 0
        new_line_ids = np.arange(len(line_ids), dtype=int) + max_line_id + 1
        lines_mapping = dict(zip(line_ids, new_line_ids.tolist()))

        return lines_mapping


    def get_new_surfaces_mapping(self):
        """ 
        This method returns a dictionary that maps all surface IDs from decoupling
        surfaces in relation to the new surface IDs that will be created.

        Returns
        -------
        surfaces_mapping : dict
            a dictionary in which keys are the surface IDs from the decoupling surface, and
            the values are the new surface IDs.

        """
        surface_ids = list(self.decouple_info.keys())
        max_surface_id = max(self.geometry.surfaces) if self.geometry.surfaces else 0
        new_surface_ids = np.arange(len(surface_ids), dtype=int) + max_surface_id + 1
        surfaces_mapping = dict(zip(surface_ids, new_surface_ids.tolist()))

        return surfaces_mapping


    def get_nodes_from_new_surface(self, surface_id: int):
        """ 
        This method processes the Node IDs from new surface.

        Parameters
        ----------
        surface_id: int
            The input surface ID.

        Returns
        -------
        new_surface_nodes: list
            A list of node IDs from new surface ID.

        """
        new_surface_nodes = list()
        for node_id in self.mesh.get_nodes_from_surface(surface_id):

            new_node_id = self.nodes_mapping.get(node_id)
            if new_node_id is None:
                continue

            new_surface_nodes.append(new_node_id)

        new_surface_nodes = list(set(new_surface_nodes))

        return new_surface_nodes


    def update_nodal_coordinates(self):
        """ This method processes the indexes and nodal coordinates relative to
            the new nodes, modifying the nodal_coordinates, nodes_from_surface, 
            and nodes_from_volume attributes.
        """
        self.gathering_decoupling_information()
        if not self.decouple_info:
            return

        logging.info("Processing degress of freedom decoupling... [35/100]")

        # process the mappings for new surfaces, lines, and points
        self.process_mappings_for_all_new_entities()

        # update the corresponding surface property
        self.update_surface_property_with_new_surface_id()

        max_node_id = max(self.mesh.cache_nodal_coordinates[:, 0])
        shift_value = max_node_id + 1

        # reset the nodal coordinates from cache data
        nodal_coordinates = deepcopy(self.mesh.cache_nodal_coordinates)

        # process all non-repeated nodes from decoupled surfaces
        nodes_from_surfaces = set()
        for surface_id in self.decouple_info.keys():
            nodes = self.mesh.get_nodes_from_surface(surface_id, from_cache=True)
            nodes_from_surfaces |= set(nodes)

        nodes_from_surfaces = list(nodes_from_surfaces)

        # create the twin nodes indexes
        twin_nodes = np.arange(0, len(nodes_from_surfaces), dtype=int) + int(shift_value)

        # process the nodes mapping
        self.nodes_mapping = dict(zip(nodes_from_surfaces, twin_nodes))

        # insert the nodal coordinates of twin nodes
        coords_from_twin_nodes = np.zeros((len(nodes_from_surfaces), 4), dtype=float)
        coords_from_twin_nodes[:, 0 ] = twin_nodes
        coords_from_twin_nodes[:, 1:] = self.mesh.nodal_coordinates[nodes_from_surfaces, 1:] 

        # append the twin nodes data in the nodal coordinates matrix
        self.mesh.nodal_coordinates = np.append(nodal_coordinates, coords_from_twin_nodes, axis=0)


    def export_nodes_mapping(self):
        """"
        This method exports the nodes mapping in a text file format.
        It is meant for decoupling validation purposes.
        """
        a = np.array(list(self.nodes_mapping.keys()))
        b = np.array(list(self.nodes_mapping.values()))
        ind = np.argsort(a)
        array = np.array([a[ind], b[ind]], dtype=int).T
        np.savetxt("nodes_mapping.dat", array, delimiter=",", fmt="%i")


    def get_surfaces_and_nodes_from_lines_that_bound_decoupling_surfaces(self):
        """ This method returns the lines that bound decoupling
            surfaces, and the nodes associated with these lines.
        """
        nodes_from_lines = set()
        valid_surface_ids = set()

        for surface_id, vol_id in self.decouple_info.items():
            all_surfaces_from_vol = self.geometry.solids_to_surfaces(vol_id)
            valid_surface_ids.update(all_surfaces_from_vol - {surface_id})

            curves_on_surface = self.geometry.surfaces_to_curves(surface_id)
            for curve_id in curves_on_surface:
                nodes = self.mesh.get_nodes_from_line(curve_id, from_cache=True)
                if nodes is not None:
                    nodes_from_lines.update(nodes)

        return list(valid_surface_ids), list(nodes_from_lines)

    def get_line_element_tag_and_nodes_number(self, input_line_id: int):
        """ Returns the 1D element tag and the number of 
            nodes per element.

            Parameters
            ----------
            input_line_id: int
                Represents the line ID.

            Return
            ------
            tag: int
                The 1D element type tag.

            n_nodes: int
                The number of nodes from 1D element.
        """        
        for _, line_id, tag, n_nodes, *_ in self.mesh.lines_connectivity:
            if line_id == input_line_id:
                return tag, n_nodes


    def get_surface_element_tag_and_nodes_number(self, input_surface_id: int):
        """ Returns the 2D element tag and the number of 
            nodes per element.

            Parameters
            ----------
            input_surface_id: int
                Represents the surface ID.

            Return
            ------
            tag: int
                The 2D element type tag.

            n_nodes: int
                The number of nodes from 2D element.
        """
        for _, surf_id, tag, n_nodes, *_ in self.mesh.faces_connectivity:
            if surf_id == input_surface_id:
                return tag, n_nodes


    def update_nodes_from_array(self, values: np.ndarray):
        """ This method returns an array whose elements are modified
            based on the nodes mapping previously processed.

            Parameters
            ----------
            values: np.ndarray
                The input array containing the node IDs.

            Returns
            -------
            output_values: np.ndarray
                The output array with mapped elements.
        """
        output_values = values.copy()
        nodes_to_map = self.nodes_mapping.keys()

        for j, node_id in enumerate(values):
            if node_id in nodes_to_map:
                output_values[j] = self.nodes_mapping[node_id]

        return output_values


    def modify_the_connectivities_from_lines(self, surface_id: int):
        """ Modifies the connectivities from 1D elements, the
            nodes from lines and connectivity from lines.

            Parameters
            ----------
            surface_id: int
                Represents the surface ID.

        """

        cols = self.mesh.lines_connectivity.shape[1]
        lines_from_surface = self.mesh.lines_from_surface[surface_id]

        for i, line_id in enumerate(lines_from_surface):

            line_connectivity = self.mesh.get_connectivity_from_line(line_id, from_cache=True)
            new_connectivity = np.zeros_like(line_connectivity, dtype=int)

            for j, connect in enumerate(line_connectivity):
                new_connectivity[j, :] = self.update_nodes_from_array(connect)

            new_line_id = self.lines_mapping.get(line_id)
            etag, nodes_per_element = self.get_line_element_tag_and_nodes_number(line_id)

            rows = new_connectivity.shape[0]
            ones = np.ones(rows, dtype=int)
            last_index = self.mesh.lines_connectivity[-1, 0]
            element_ids = int(last_index + 1) + np.arange(new_connectivity.shape[0])

            connectivity_to_append = np.zeros((rows, cols), dtype=int)
            connectivity_to_append[:, 0 ] = element_ids
            connectivity_to_append[:, 1 ] = ones * int(new_line_id)
            connectivity_to_append[:, 2 ] = ones * int(etag)
            connectivity_to_append[:, 3 ] = ones * int(nodes_per_element)
            connectivity_to_append[:, 4:] = new_connectivity

            self.mesh.lines_connectivity = np.append(self.mesh.lines_connectivity, connectivity_to_append, axis=0)


    def modify_the_connectivities_from_surfaces(self, surface_id: int):
        """ Modifies the connectivities from 2D elements, the
            nodes from surfaces and connectivity from surfaces.

            Parameters
            ----------
            surface_id: int
                Represents the surface ID.

        """

        cols = self.mesh.faces_connectivity.shape[1]
        face_connectivity = self.mesh.get_connectivity_from_surface(surface_id, from_cache=True)
        new_connectivity = np.zeros_like(face_connectivity, dtype=int)

        for j, connect in enumerate(face_connectivity):
            new_connectivity[j, :] = self.update_nodes_from_array(connect)

        new_surface_id = self.surfaces_mapping.get(surface_id)
        etag, nodes_per_element = self.get_surface_element_tag_and_nodes_number(surface_id)

        rows = new_connectivity.shape[0]
        ones = np.ones(rows, dtype=int)
        last_index = self.mesh.faces_connectivity[-1, 0]
        element_ids = int(last_index + 1) + np.arange(new_connectivity.shape[0])

        connectivity_to_append = np.zeros((rows, cols), dtype=int)
        connectivity_to_append[:, 0 ] = element_ids
        connectivity_to_append[:, 1 ] = ones * int(new_surface_id)
        connectivity_to_append[:, 2 ] = ones * int(etag)
        connectivity_to_append[:, 3 ] = ones * int(nodes_per_element)
        connectivity_to_append[:, 4:] = new_connectivity

        self.mesh.faces_connectivity = np.append(self.mesh.faces_connectivity, connectivity_to_append, axis=0)


    def get_lines_from_unmodified_surfaces(self):
        """ Returns the lines from unmodified surfaces, i.e.,
            all lines from non-decoupled surfaces.
        """
        line_ids = set()
        lines_nodes = set()
        for surface_id, vol_id in self.decouple_info.items():
            decoupling_curves = self.geometry.surfaces_to_curves(surface_id)
            surfaces_in_volume = self.geometry.solids_to_surfaces(vol_id)

            for surf_id in surfaces_in_volume:
                if surf_id == surface_id:
                    continue
                line_ids.update(self.geometry.surfaces_to_curves(surf_id))
            
            line_ids -= decoupling_curves

        for line_id in line_ids:
            nodes = self.mesh.get_nodes_from_line(line_id, from_cache=True)
            if nodes is not None:
                lines_nodes.update(nodes)

        return list(line_ids), list(lines_nodes)


    def update_all_connectivity_related_attributes(self):
        """ This method performs all necessary updates in
            the connectivity-related attributes.
        """
        if not self.decouple_info:
            return

        logging.info("Processing degress of freedom decoupling... [50/100]")

        # reset the attributes from cache data
        self.mesh.solids_connectivity = deepcopy(self.mesh.cache_solids_connectivity)
        self.mesh.faces_connectivity = deepcopy(self.mesh.cache_faces_connectivity)
        self.mesh.lines_connectivity = deepcopy(self.mesh.cache_lines_connectivity)

        volume_ids = list(self.decouple_info.values())
        node_ids = list(self.nodes_mapping.keys())

        rows_3d = np.sum(np.isin(self.mesh.cache_solids_connectivity[:, 4:], node_ids), axis=1) >= 1
        for elem3d_id, vol_id, _, _, *connect_3d in self.mesh.cache_solids_connectivity[rows_3d, :]:
            if vol_id in volume_ids:
                self.mesh.solids_connectivity[elem3d_id, 4:] = self.update_nodes_from_array(connect_3d)

        valid_surface_ids, nodes_from_bound_lines = self.get_surfaces_and_nodes_from_lines_that_bound_decoupling_surfaces()
        rows_2d = np.sum(np.isin(self.mesh.cache_faces_connectivity[:, 4:], nodes_from_bound_lines), axis=1) >= 1
        for elem2d_id, surf_id, _, _, *connect_2d in self.mesh.cache_faces_connectivity[rows_2d, :]:
            if surf_id in valid_surface_ids:
                self.mesh.faces_connectivity[elem2d_id, 4:] = self.update_nodes_from_array(connect_2d)

        valid_line_ids, lines_nodes = self.get_lines_from_unmodified_surfaces()
        rows_1d = np.sum(np.isin(self.mesh.cache_lines_connectivity[:, 4:], lines_nodes), axis=1) >= 1
        for elem1d_id, line_id, _, _, *connect_1d in self.mesh.cache_lines_connectivity[rows_1d, :]:
            if line_id in valid_line_ids:
                self.mesh.lines_connectivity[elem1d_id, 4:] = self.update_nodes_from_array(connect_1d)

        for surf_id in self.mesh.geometry_information.get("surfaces"):
            for surface_id in self.decouple_info.keys():
                if surf_id == surface_id:
                    self.modify_the_connectivities_from_lines(surface_id)
                    self.modify_the_connectivities_from_surfaces(surface_id)
                    break

        self.update_nodes_from_points()
        self.mesh.process_mesh_related_mappings("Post-processing")


    def update_nodes_from_points(self):
        """ This method updates the nodes from created points.
        """
        for point_id, new_point_id in self.points_mapping.items():
            node_from_point = self.mesh.nodes_from_points.get(point_id)
            if node_from_point is None:
                continue

            new_node_id = self.nodes_mapping.get(node_from_point)
            if new_node_id is None:
                continue
        
            self.mesh.nodes_from_points[new_point_id] = int(new_node_id)
            self.mesh.points_from_nodes[int(new_node_id)] = new_point_id


    def mimetize_the_fluid_from_decoupling_surfaces(self):
        """ This method applies the same fluid from decoupling
            surfaces to their twin surfaces, respectively.
        """

        logging.info("Processing degress of freedom decoupling... [100/100]")

        for surface_id in self.decouple_info.keys():
            new_surface_id = self.surfaces_mapping.get(surface_id)

            fluid = self.model.properties._get_property("fluid", surface=surface_id)
            if fluid is None:
                continue

            fluid_id = self.model.properties._get_property("fluid_id", surface=surface_id)
            self.model.properties._set_property("fluid", fluid, surface=new_surface_id)
            self.model.properties._set_property("fluid_id", fluid_id, surface=new_surface_id)


    def update_geometry_related_information(self):
        """ This method updates the geometry-related information,
            precisely, the number of each entity and the properties 
            associated with them, beyond the upward and downward
            adjacencies from entities.
        """
        if not self.decouple_info:
            return

        logging.info("Processing degress of freedom decoupling... [90/100]")

        # Groups surfaces to be decoupled by their parent volume.
        temp_decouple_map = defaultdict(list)
        for surf_id, vol_id in self.decouple_info.items():
            temp_decouple_map[vol_id].append(surf_id)

        # For each volume, replaces the old shared surface IDs with the new,
        # independent surface IDs in its definition.
        for vol_id, decoupled_surf_ids in temp_decouple_map.items():
            original_surfaces = set(self.geometry.solids_to_surfaces(vol_id))
            surfaces_to_keep = original_surfaces - set(decoupled_surf_ids)
            newly_added_surfaces = {self.surfaces_mapping[sid] for sid in decoupled_surf_ids}
            updated_surfaces = surfaces_to_keep | newly_added_surfaces
            self.geometry._solids_to_surfaces[vol_id] = tuple(sorted(list(updated_surfaces)))

        
        # Iterates through the original shared surfaces to create the new,
        # independent geometric entities (surfaces, curves, and points).
        for surf_id in self.decouple_info.keys():
            new_surf_id = self.surfaces_mapping[surf_id]
            self.geometry.surfaces.append(new_surf_id)
            self.geometry._surfaces_areas[new_surf_id] = self.geometry.surface_area(surf_id)

            original_curves = self.geometry.surfaces_to_curves(surf_id)
            new_curve_ids = [self.lines_mapping[cid] for cid in original_curves]
            self.geometry._surfaces_to_curves[new_surf_id] = tuple(new_curve_ids)

            for i, curve_id in enumerate(original_curves):
                new_curve_id = new_curve_ids[i]
                if new_curve_id not in self.geometry.curves:
                    self.geometry.curves.append(new_curve_id)
                    self.geometry._curves_lengths[new_curve_id] = self.geometry.arc_length(curve_id)

                original_points = self.geometry.curves_to_points(curve_id)
                new_point_ids = [self.points_mapping[pid] for pid in original_points]
                self.geometry._curves_to_points[new_curve_id] = tuple(new_point_ids)

                for point_id in new_point_ids:
                    if point_id not in self.geometry.points:
                        self.geometry.points.append(point_id)

    def process_degrees_of_freedom_decoupling(self):
        """ This method processes all required actions to decouple
            degrees of freedom of connected volumes.
        """
        t0 = time()
        self.update_nodal_coordinates()
        self.update_all_connectivity_related_attributes()
        self.update_geometry_related_information()
        self.mimetize_the_fluid_from_decoupling_surfaces()
        dt = time() - t0
        print(f"Elapsed time to process the degrees of freedom decoupling {dt : .6f} s")


def maps_values_to_keys(input_data: dict):
    """ This function returns a dictionary that maps the 
        values of the original dictionary to its keys.

        Parameters
        ----------
        input_data: dict,
            The input dictionary to be reversed.

        Returns
        -------
        output_data: dict,
            The reversed output dictionary.

    """

    output_data = defaultdict(list)

    for key, values in input_data.items():
        for value in values:
            output_data[value].append(key)

    return output_data