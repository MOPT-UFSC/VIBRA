
from vibra import app
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

from collections import defaultdict
from copy import deepcopy
from time import time

import numpy as np


class DofsDecoupling:
    def __init__(self, model: "Model"):
        self.model = model
        self.mesh = model.mesh
        self.properties = model.properties

        self.initialize()


    def initialize(self):
        self.decouple_info = dict()
        self.nodes_mapping = dict()


    def gathering_decoupling_information(self):
        """
        """
        self.decouple_info.clear()
        self.nodes_mapping.clear()
        if self.mesh.cache_nodal_coordinates is None:
            return

        max_surface_id = int(np.max(self.mesh.cache_faces_connectivity[:, 1]))

        for key, data in self.properties.surface_properties.items():
            (property, surface_id) = key
            if property == "acoustic_dofs_decoupling":

                data: dict
                max_surface_id += 1
                vol_id =  data.get("volume_to_decouple")

                if isinstance(vol_id, int):    
                    self.decouple_info[vol_id] = {
                                                  "surface_id" : surface_id,
                                                  "new_surface_id" : int(max_surface_id),
                                                  }

                    aux_data = deepcopy(data)
                    aux_data.update(new_surface_id=int(max_surface_id))
                    self.properties.surface_properties[key] = aux_data


    def update_nodal_coordinates(self):
        """
        """
        self.gathering_decoupling_information()
        if not self.decouple_info:
            return

        max_node_id = max(self.mesh.cache_nodal_coordinates[:, 0])
        shift_value = max_node_id + 1

        nodal_coordinates = deepcopy(self.mesh.cache_nodal_coordinates)

        for vol_id, data in self.decouple_info.items():
            data: dict

            # update the nodes from surface
            nodes_from_surface = self.mesh.nodes_from_surfaces[data.get("surface_id")]
            twin_nodes = np.arange(0, len(nodes_from_surface), dtype=int) + int(shift_value)

            # add the twin nodes from the new surface
            self.mesh.nodes_from_surfaces[data.get("new_surface_id")] = twin_nodes
            shift_value += len(nodes_from_surface)

            # update the nodes from volume
            nodes_from_volume = deepcopy(self.mesh.nodes_from_volumes[vol_id])
            self.mesh.nodes_from_volumes[vol_id] = self.update_connectivity(nodes_from_volume)

            # process the nodes mapping
            for k, node_id in enumerate(nodes_from_surface):
                self.nodes_mapping[node_id] = twin_nodes[k]

            # insert the nodal coordinates of twin nodes
            coords_from_twin_nodes = np.zeros((len(nodes_from_surface), 4), dtype=float)
            coords_from_twin_nodes[:, 0 ] = twin_nodes
            coords_from_twin_nodes[:, 1:] = self.mesh.nodal_coordinates[nodes_from_surface, 1:] 
            nodal_coordinates = np.append(nodal_coordinates, coords_from_twin_nodes, axis=0)

        self.mesh.nodal_coordinates = nodal_coordinates


    def get_new_line_ids(self, line_ids: list[int]):
        """
        """
        max_line_id = np.max(self.mesh.cache_lines_connectivity[:, 1])
        shifted_line_ids = np.arange(len(line_ids), dtype=int) + int(max_line_id + 1)
        return shifted_line_ids


    def get_new_point_ids(self, point_ids: list[int]):
        """
        """
        #TODO: modify this criterion
        max_point_id = max(list(self.mesh.geometry_information.get("points")))
        shifted_point_ids = np.arange(len(point_ids), dtype=int) + int(max_point_id + 1)
        return list(shifted_point_ids)


    def get_nodes_from_lines_that_bound_decoupled_surfaces(self):
        """
        """
        surfaces_from_volume = deepcopy(self.mesh.cache_surfaces_from_volume)
        lines_from_surface = deepcopy(self.mesh.cache_lines_from_surface)

        nodes_from_lines = list()
        valid_surface_ids = list()

        for vol_id, data in self.decouple_info.items():

            data: dict
            valid_surface_ids.extend(surfaces_from_volume[vol_id])
            surface_id = data.get("surface_id")
            valid_surface_ids.remove(surface_id)

            for i, line_id in enumerate(lines_from_surface[surface_id]):
                nodes_from_lines.extend(self.mesh.nodes_from_lines[line_id])

        nodes_from_lines = list(set(nodes_from_lines))

        return valid_surface_ids, nodes_from_lines


    def get_line_element_tag_and_nodes_number(self, input_line_id: int):
        for _, line_id, tag, n_nodes, *_ in self.mesh.lines_connectivity:
            if line_id == input_line_id:
                return tag, n_nodes


    def get_surface_element_tag_and_nodes_number(self, surface_id: int):
        for _, surf_id, tag, n_nodes, *_ in self.mesh.faces_connectivity:
            if surf_id == surface_id:
                return tag, n_nodes


    def update_connectivity(self, values: np.ndarray):
        """
        """
        output_values = values.copy()
        nodes_to_map = self.nodes_mapping.keys()

        for j, node_id in enumerate(values):
            if node_id in nodes_to_map:
                output_values[j] = self.nodes_mapping[node_id]

        return output_values
    

    def modify_the_connectivities_from_lines(self, surface_id: int):
        """
        """

        cols = self.mesh.lines_connectivity.shape[1]
        lines_from_surface = self.mesh.lines_from_surface[surface_id]
        new_line_ids = self.get_new_line_ids(lines_from_surface)

        for i, line_id in enumerate(lines_from_surface):

            line_connectivity = self.mesh.cache_connectivity_from_lines[line_id]
            new_connectivity = np.zeros_like(line_connectivity, dtype=int)

            for j, connect in enumerate(line_connectivity):
                new_connectivity[j, :] = self.update_connectivity(connect)

            new_line_id = int(new_line_ids[i])
            self.mesh.connectivity_from_lines[new_line_id] = new_connectivity
            self.mesh.nodes_from_lines[new_line_id] = np.array([*set(new_connectivity.flatten())], dtype=int)

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


    def modify_the_connectivities_from_surfaces(self, surface_id: int, new_surface_id: int):
        """
        """

        cols = self.mesh.faces_connectivity.shape[1]
        face_connectivity = self.mesh.cache_connectivity_from_surfaces[surface_id]
        new_connectivity = np.zeros_like(face_connectivity, dtype=int)

        for j, connect in enumerate(face_connectivity):
            new_connectivity[j, :] = self.update_connectivity(connect)

        self.mesh.connectivity_from_surfaces[new_surface_id] = new_connectivity
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


    def get_lines_from_valid_surfaces(self):
        """
        """
        line_ids = list()
        for vol_id, data in self.decouple_info.items():
            data: dict
            surf_id = data.get("surface_id")
            if surf_id is None:
                return

            for surface_id in self.mesh.cache_surfaces_from_volume[vol_id]:
                if surf_id == surface_id:
                    continue

                line_ids.extend(self.mesh.cache_lines_from_surface[surface_id])

        return list(set(line_ids))


    def update_all_connectivity_related_attributes(self):
        """
        """
        t0 = time()
        if not self.decouple_info:
            return

        # reset the attributes with the aid of cache data
        self.mesh.solids_connectivity = deepcopy(self.mesh.cache_solids_connectivity)
        self.mesh.faces_connectivity = deepcopy(self.mesh.cache_faces_connectivity)
        self.mesh.lines_connectivity = deepcopy(self.mesh.cache_lines_connectivity)

        volume_ids = list(self.decouple_info.keys())
        for elem3d_id, vol_id, _, _, *connect_3d in self.mesh.cache_solids_connectivity:
            if vol_id in volume_ids:
                self.mesh.solids_connectivity[elem3d_id, 4:] = self.update_connectivity(connect_3d)

        valid_surface_ids, nodes_from_bound_lines = self.get_nodes_from_lines_that_bound_decoupled_surfaces()
        for elem2d_id, surf_id, _, _, *connect_2d in self.mesh.cache_faces_connectivity:
            if surf_id not in valid_surface_ids:
                continue

            if np.isin(nodes_from_bound_lines, connect_2d).any():
                self.mesh.faces_connectivity[elem2d_id, 4:] = self.update_connectivity(connect_2d)

        lines_from_valid_surfaces = self.get_lines_from_valid_surfaces()
        for elem1d_id, line_id, _, _, *connect_1d in self.mesh.cache_lines_connectivity:
            if line_id in lines_from_valid_surfaces:
                if np.isin(nodes_from_bound_lines, connect_1d).any():
                    self.mesh.lines_connectivity[elem1d_id, 4:] = self.update_connectivity(connect_1d)

        for surface_id in self.mesh.nodes_from_surfaces.keys():
            for data in self.decouple_info.values():
                data: dict
                if surface_id == data.get("surface_id"):
                    new_surface_id = data.get("new_surface_id")
                    self.modify_the_connectivities_from_lines(surface_id)
                    self.modify_the_connectivities_from_surfaces(surface_id, new_surface_id)
                    break

        self.mesh.process_mesh_related_mappings()

        dt = time() - t0
        print(f"Elapsed time to update connectivities: {dt} s")


    def apply_fluid_at_new_surface(self, surface_id: int, new_surface_id: int):

        fluid = self.model.properties._get_property("fluid", surface=surface_id)
        self.model.properties._set_property("fluid", fluid, surface=new_surface_id)

        fluid_id = self.model.properties._get_property("fluid_id", surface=surface_id)
        self.model.properties._set_property("fluid_id", fluid_id, surface=new_surface_id)


    def update_geometry_related_information(self):
        """
        """
        surfaces_from_volume = deepcopy(self.mesh.cache_surfaces_from_volume)
        lines_from_surface = deepcopy(self.mesh.cache_lines_from_surface)
        points_from_line = deepcopy(self.mesh.cache_points_from_line)

        geometry_information = deepcopy(self.mesh.geometry_information)
        area_from_surface = geometry_information.get("area_from_surface")
        length_from_curve = geometry_information.get("length_from_curve")

        for vol_id, data in self.decouple_info.items():
            data: dict

            surf_id = data.get("surface_id")
            new_surf_id = data.get("new_surface_id")
            self.apply_fluid_at_new_surface(surf_id, new_surf_id)

            surfaces_from_volume = set(surfaces_from_volume[vol_id])
            surfaces_from_volume -= set({surf_id})
            surfaces_from_volume |= set({new_surf_id})
            self.mesh.surfaces_from_volume[vol_id] = np.sort(list(surfaces_from_volume))

            surface_ids = set(geometry_information["surfaces"])
            surface_ids |= set({new_surf_id})
            self.mesh.geometry_information["surfaces"] = list(surface_ids)

            self.mesh.geometry_information["area_from_surface"].update({new_surf_id : area_from_surface[surf_id]})

            lines_from_surface = lines_from_surface[surf_id]
            new_line_ids = self.get_new_line_ids(lines_from_surface)
            self.mesh.lines_from_surface[new_surf_id] = new_line_ids

            line_ids = set(geometry_information["curves"])
            for i, line_id in enumerate(lines_from_surface):
                new_line_id = int(new_line_ids[i])
                line_ids |= set({new_line_id})
                self.mesh.geometry_information["length_from_curve"].update({new_line_id : length_from_curve[line_id]})
                self.mesh.points_from_line[new_line_id] = self.get_new_point_ids(points_from_line[line_id])

            self.mesh.geometry_information["curves"] = list(line_ids)

        if self.decouple_info:
            self.mesh.volumes_from_surface = maps_values_to_keys(deepcopy(self.mesh.surfaces_from_volume))
            self.mesh.surfaces_from_line = maps_values_to_keys(deepcopy(self.mesh.lines_from_surface))
            self.mesh.lines_from_point = maps_values_to_keys(deepcopy(self.mesh.points_from_line))


    def process_dofs_decoupling(self):
        """
        """
        self.update_nodal_coordinates()
        self.update_all_connectivity_related_attributes()
        self.update_geometry_related_information()


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