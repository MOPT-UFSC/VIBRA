
from vibra import app
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

from copy import deepcopy
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

        # self.properties._set_property("acoustic_dofs_decoupling", dict(), surface=6)

        surfaces_to_decouple = list()
        for (property, surface_id) in self.properties.surface_properties.keys():
            if property == "acoustic_dofs_decoupling":
                surfaces_to_decouple.append(surface_id)

        max_surface_id = max(self.mesh.nodes_from_surfaces.keys())

        self.decouple_info.clear()
        for surf_id in surfaces_to_decouple:
            max_surface_id += 1
            vol_ids = self.mesh.volumes_from_surface[surf_id]
            self.decouple_info[vol_ids[0]] = {
                                              "surface_id" : surf_id,
                                              "new_surface_id" : int(max_surface_id)
                                              }


    def update_nodal_coordinates(self):
        """
        """
        self.gathering_decoupling_information()

        if not self.decouple_info:
            return

        max_node_id = max(self.mesh.cache_nodal_coordinates[:, 0])
        shift_value = max_node_id + 1

        self.nodes_mapping.clear()
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
        # from pprint import pprint
        # pprint(self.nodes_mapping)
        # keys = list(self.nodes_mapping.keys())
        # values = list(self.nodes_mapping.values())
        # out_data = np.array([keys, values], dtype=int).T
        # np.savetxt("out_data.dat", out_data, delimiter=",", fmt="%i, %i")


    def get_new_line_ids(self, line_ids: list[int]):
        """
        """
        max_line_id = max(list(self.mesh.geometry_information.get("curves")))
        shifted_line_ids = np.arange(len(line_ids), dtype=int) + int(max_line_id + 1)
        return list(shifted_line_ids)


    def get_new_point_ids(self, point_ids: list[int]):
        """
        """
        max_point_id = max(list(self.mesh.geometry_information.get("points")))
        shifted_point_ids = np.arange(len(point_ids), dtype=int) + int(max_point_id + 1)
        return list(shifted_point_ids)


    def get_nodes_from_lines_that_bound_decoupled_surfaces(self):
        """
        """

        nodes_from_lines = list()
        valid_surface_ids = list()

        #TODO: verify the necessity of updating the geometry-related data
        for vol_id, data in self.decouple_info.items():
            data: dict
            surf_id = data.get("surface_id")
            # new_surf_id = data.get("new_surface_id")
            valid_surface_ids.extend(self.mesh.surfaces_from_volume[vol_id])
            valid_surface_ids.remove(surf_id)

            # self.mesh.volumes_from_surface[surf_id].remove(vol_id)
            # self.mesh.volumes_from_surface[new_surf_id] = [vol_id]

            # surfaces_from_volume = list(deepcopy(self.mesh.surfaces_from_volume[vol_id]))
            # surfaces_from_volume.remove(surf_id)
            # surfaces_from_volume.append(new_surf_id)
            # self.mesh.surfaces_from_volume[vol_id] = np.sort((surfaces_from_volume))

            lines_from_surface = self.mesh.lines_from_surface[surf_id]
            # new_line_ids = self.get_new_line_ids(lines_from_surface)

            for i, line_id in enumerate(lines_from_surface):
                nodes_from_lines.extend(self.mesh.nodes_from_lines[line_id])
                # points_from_line = deepcopy(self.mesh.points_from_line[line_id])
                # self.mesh.points_from_line[new_line_ids[i]] = self.get_new_point_ids(points_from_line)

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
        for j, node_id in enumerate(values):
            if node_id in self.nodes_mapping.keys():
                output_values[j] = self.nodes_mapping[node_id]

        return output_values
    

    def modify_the_connectivities_from_lines(self, surface_id: int):
        """
        """

        cols = self.mesh.lines_connectivity.shape[1]
        lines_from_surface = self.mesh.lines_from_surface[surface_id]
        new_line_ids = self.get_new_line_ids(lines_from_surface)

        for i, line_id in enumerate(lines_from_surface):

            new_line_id = new_line_ids[i]
            line_connectivity = self.mesh.cache_connectivity_from_lines[line_id]
            new_connectivity = np.zeros_like(line_connectivity, dtype=int)

            for j, connect in enumerate(line_connectivity):
                new_connectivity[j, :] = self.update_connectivity(connect)

            self.mesh.connectivity_from_lines[new_line_id] = new_connectivity
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


    def update_all_connectivity_related_attributes(self):
        """
        """

        if not self.decouple_info:
            return

        for elem3d_id, vol_id, _, _, *connect_3d in deepcopy(self.mesh.cache_solids_connectivity):
            if vol_id in self.decouple_info.keys():
                self.mesh.solids_connectivity[elem3d_id, 4:] = self.update_connectivity(connect_3d)

        valid_surface_ids, nodes_from_bound_lines = self.get_nodes_from_lines_that_bound_decoupled_surfaces()
        for elem2d_id, surf_id, _, _, *connect_2d in self.mesh.cache_faces_connectivity:
            if surf_id not in valid_surface_ids:
                continue

            if np.isin(nodes_from_bound_lines, connect_2d).any():
                self.mesh.faces_connectivity[elem2d_id, 4:] = self.update_connectivity(connect_2d)

        for surface_id in self.mesh.nodes_from_surfaces.keys():
            for data in self.decouple_info.values():
                data: dict
                if surface_id == data.get("surface_id"):
                    new_surface_id = data.get("new_surface_id")
                    self.modify_the_connectivities_from_lines(surface_id)
                    self.modify_the_connectivities_from_surfaces(surface_id, new_surface_id)
                    break

        self.mesh.process_mesh_related_mappings()


    def process_dofs_decoupling(self):
        """
        """
        self.update_nodal_coordinates()
        self.update_all_connectivity_related_attributes()