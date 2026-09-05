
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vibra.engine.model import Model

from collections import defaultdict
from time import perf_counter

import numpy as np

from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material


class ModelDomainsProcessor:
    def __init__(self, model: "Model"):

        self.model = model

        self.reset()

    def reset(self):
        self.volumes_of_domain = {}
        self.surfaces_of_domain = {}
        self.lines_of_domain = {}
        self.points_of_domain = {}
        self.fluid_structure_interfaces = {}

        self.nodes_of_domain = {}
        self.elements_of_domain = {}

        self.structural_dofs_shift = 0
        self.acoustic_dofs_shift = 0

        self.acoustic_dofs_indices = None
        self.structural_dofs_indices = None


    @property
    def mesh(self):
        return self.model.mesh


    @property
    def properties(self):
        return self.model.properties


    def map_model_domains(self):
        """
        This method maps all entities of each domain.
        """

        all_ids = defaultdict(list)
        volumes_of_domain = defaultdict(list)

        self.volumes_of_domain.clear()
        self.surfaces_of_domain.clear()
        self.lines_of_domain.clear()
        self.points_of_domain.clear()

        for vol_id in self.mesh.elements_from_volume:

            fluid = self.properties._get_property("fluid", volume=vol_id)
            if isinstance(fluid, Fluid):
                all_ids["volumes"].append(vol_id)
                volumes_of_domain["acoustic"].append(int(vol_id))
                continue

            material = self.properties._get_property("material", volume=vol_id)
            if isinstance(material, Material):
                all_ids["volumes"].append(vol_id)
                volumes_of_domain["structural"].append(int(vol_id))

        for domain in ["acoustic", "structural"]:
            surfaces_of_domain = set()
            lines_of_domain = set()
            points_of_domain = set()
            _volumes_of_domain = volumes_of_domain.get(domain, [])

            for vol_id in _volumes_of_domain:
                surface_ids = self.mesh.surfaces_from_volume.get(vol_id, [])
                surfaces_of_domain |= set(surface_ids)

                for surf_id in surface_ids:
                    line_ids = self.mesh.lines_from_surface.get(surf_id, [])
                    lines_of_domain |= set(line_ids)

                    for line_id in line_ids:
                        point_ids = self.mesh.points_from_line.get(line_id, [])
                        points_of_domain |= set(point_ids)

            all_ids["surfaces"].extend(surfaces_of_domain)
            all_ids["lines"].extend(surfaces_of_domain)
            all_ids["points"].extend(surfaces_of_domain)

            self.volumes_of_domain[domain] = sorted(_volumes_of_domain)
            self.surfaces_of_domain[domain] = sorted(surfaces_of_domain)
            self.lines_of_domain[domain] = sorted(lines_of_domain)
            self.points_of_domain[domain] = sorted(points_of_domain)

        self.volumes_of_domain["both"] = [int(_id) for _id in np.unique([all_ids.get("volumes", [])])]
        self.surfaces_of_domain["both"] = [int(_id) for _id in np.unique([all_ids.get("surfaces", [])])]
        self.lines_of_domain["both"] = [int(_id) for _id in np.unique([all_ids.get("lines", [])])]
        self.points_of_domain["both"] = [int(_id) for _id in np.unique([all_ids.get("points", [])])]


    def map_fluid_structure_interfaces(self):
        """
        This method maps the fluid-structure interfaces.
        """
        self.fluid_structure_interfaces.clear()
        for surface_id, vol_ids in self.mesh.volumes_from_surface.items():
            if len(vol_ids) == 1:
                continue

            acoustic_volumes = self.volumes_of_domain.get("acoustic", [])
            structural_volumes = self.volumes_of_domain.get("structural", [])

            vol_a, vol_b = vol_ids
            if vol_a in acoustic_volumes and vol_b in structural_volumes:
                fluid_volume = vol_a
                structure_volume = vol_b

            elif vol_b in acoustic_volumes and vol_a in structural_volumes:
                fluid_volume = vol_b
                structure_volume = vol_a

            else:
                continue

            self.fluid_structure_interfaces[surface_id] = {
                "fluid_volume" : fluid_volume,
                "structure_volume" : structure_volume,
                }


    def map_nodes_and_elements_by_domain(self):
        """
        This method groups the nodes and elements for acoustic and structural domains.
        """
        self.nodes_of_domain.clear()
        self.elements_of_domain.clear()
        for domain, vol_ids in self.volumes_of_domain.items():
            rows = np.isin(self.mesh.solids_connectivity[:, 1], vol_ids)
            self.nodes_of_domain[domain] = np.unique(self.mesh.solids_connectivity[rows, 4:])
            self.elements_of_domain[domain] = np.unique(self.mesh.solids_connectivity[rows, 0])


    def process_nodes_mappings_by_domain(self):
        """
        This method maps the nodes of each domain to a continuous list of indices.
        """

        acoustic_nodes: np.ndarray = self.nodes_of_domain.get("acoustic", np.ndarray([]))
        structural_nodes: np.ndarray = self.nodes_of_domain.get("structural", np.ndarray([]))

        # the total number of nodes (per domain)
        self.number_acoustic_nodes = len(acoustic_nodes)
        self.number_structural_nodes = len(structural_nodes)

        # the total number of nodes
        total_nodes = len(self.mesh.nodal_coordinates)

        # map the nodes of each domain sequentially
        self.structural_nodes_mapping = np.full(total_nodes, -1, dtype=int)
        self.acoustic_nodes_mapping = np.full(total_nodes, -1, dtype=int)

        for index, node_id in enumerate(acoustic_nodes):
            self.acoustic_nodes_mapping[node_id] = index

        for index, node_id in enumerate(structural_nodes):
            self.structural_nodes_mapping[node_id] = index

        print(f"Number of acoustic nodes: {self.number_acoustic_nodes}")
        print(f"Number of structural nodes: {self.number_structural_nodes}")


    def process_element_mappings_by_domain(self):
        """
        This method maps the elements of each domain to a continuous list of indices.
        """

        acoustic_elements: np.ndarray = self.elements_of_domain.get("acoustic", np.ndarray([]))
        structural_elements: np.ndarray = self.elements_of_domain.get("structural", np.ndarray([]))

        # the total number of elements (per domain)
        self.number_3d_acoustic_elements = len(acoustic_elements)
        self.number_3d_structural_elements = len(structural_elements)

        # the total number of elements
        total_elements = len(self.mesh.solids_connectivity)

        # map the elements of each domain sequentially
        self.structural_elements_mapping = np.full(total_elements, -1, dtype=int)
        self.acoustic_elements_mapping = np.full(total_elements, -1, dtype=int)

        for index, element_id in enumerate(acoustic_elements):
            self.acoustic_elements_mapping[element_id] = index

        for index, element_id in enumerate(structural_elements):
            self.structural_elements_mapping[element_id] = index

        print(f"Number of acoustic elements: {self.number_3d_acoustic_elements}")
        print(f"Number of structural elements: {self.number_3d_structural_elements}")


    def process_dof_by_domain(self):
        """
        This method processes the DOF indices arrays of each domain.
        """

        if self.model.acoustic_element_3d is None:
            self.model.set_acoustic_elements()

        if self.model.structural_element_3d is None:
            self.model.set_structural_elements()

        # number of dof per node for each domain
        dof_act = self.model.acoustic_element_3d.dof_per_node
        dof_str = self.model.structural_element_3d.dof_per_node

        self.total_act_dofs = dof_act * self.number_acoustic_nodes
        self.total_str_dofs = dof_str * self.number_structural_nodes
        self.total_dof = self.total_act_dofs + self.total_str_dofs

        # define the dof shifts for each domain
        self.structural_dofs_shift = 0
        self.acoustic_dofs_shift = self.total_str_dofs

        # process the structural dofs (continuous nodes sequence + dofs shift)
        nodes_str_seq = np.arange(self.number_structural_nodes, dtype=int).reshape(-1, 1)
        structural_dofs_indices = dof_str * nodes_str_seq + np.arange(dof_str) + self.structural_dofs_shift
        self.structural_dofs_indices = structural_dofs_indices.flatten()

        # process the acoustic dofs (continuous nodes sequence + dofs shift)
        nodes_act_seq = np.arange(self.number_acoustic_nodes, dtype=int).reshape(-1, 1)
        acoustic_dofs_indices = dof_act * nodes_act_seq + np.arange(dof_act) + self.acoustic_dofs_shift
        self.acoustic_dofs_indices = acoustic_dofs_indices.flatten()

        print(f"Number of acoustic DOF: {self.total_act_dofs}")
        print(f"Number of structural DOF: {self.total_str_dofs}")
        print(f"Total number of DOF: {self.total_dof}")

        # TODO: to be removed after validation has been done
        # data = np.array([self.acoustic_nodes_mapping, self.structural_nodes_mapping]).T
        # np.savetxt("nodes_mappings.dat", data, delimiter=",", fmt="%i")

        # all_indices = np.arange(self.total_dof, dtype=int)
        # all_indices_conc = np.sort(np.append(self.structural_dofs_indices, self.acoustic_dofs_indices))
        # data = np.array([all_indices, all_indices_conc], dtype=int).T
        # np.savetxt("dof_indices.dat", data, delimiter=",", fmt="%i")
        # print(np.allclose(all_indices, all_indices_conc))

        # mask = np.isin(all_indices, str_dof_indices, invert=True)
        # act_dof_indices = all_indices[mask]

        # print(total_dof, str_dof_indices.size, act_dof_indices.size)

        # return total_dof, str_dof_indices, act_dof_indices


    def get_dofs_shift(self, domain: str):
        return self.acoustic_dofs_shift if domain == "acoustic" else self.structural_dofs_shift


    def update_domains_mappings(self):
        t0 = perf_counter()
        self.map_model_domains()
        dt1 = perf_counter() - t0

        t0 = perf_counter()
        self.map_fluid_structure_interfaces()
        dt2 = perf_counter() - t0

        t0 = perf_counter()
        self.map_nodes_and_elements_by_domain()
        dt3 = perf_counter() - t0

        t0 = perf_counter()
        self.process_nodes_mappings_by_domain()
        dt4 = perf_counter() - t0

        t0 = perf_counter()
        self.process_element_mappings_by_domain()
        dt5 = perf_counter() - t0

        t0 = perf_counter()
        self.process_dof_by_domain()
        dt6 = perf_counter() - t0

        print(f"Elapsed time to 'map_model_domains': {dt1 : .6f} s")
        print(f"Elapsed time to 'map_fluid_structure_interfaces': {dt2 : .6f} s")
        print(f"Elapsed time to 'map_nodes_and_elements_by_domain': {dt3 : .6f} s")
        print(f"Elapsed time to 'process_nodes_mappings_by_domain': {dt4 : .6f} s")
        print(f"Elapsed time to 'process_element_mappings_by_domain': {dt5 : .6f} s")
        print(f"Elapsed time 'process_dof_by_domain': {dt6 : .6f} s")
