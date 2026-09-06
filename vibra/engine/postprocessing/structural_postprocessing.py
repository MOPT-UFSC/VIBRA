from __future__ import annotations

from collections import defaultdict
from functools import cache
from time import time
from typing import Literal

import numpy as np

from vibra.engine import AnalysisID
from vibra.engine.model import Model
from vibra.engine.postprocessing.structural_post_solution_dataclass import NodalStresses
from vibra.engine.solution import HarmonicSolution, LazyHarmonicSolution, ModalSolution

DataTypes = Literal["u_sum", "u_x", "u_y", "u_z", "v_svm", "v_x", "v_y", "v_z", "a_sum", "a_x", "a_y", "a_z"]


class StructuralPostprocessing:
    def __init__(self, model: Model):
        if not isinstance(model, Model):
            raise ValueError("The model argument must be of type Model.")

        self.model = model

    @property
    def mesh(self):
        return self.model.mesh

    @property
    def solution(self):
        return self.model.solution

    @property
    def structural_element_2d(self):
        if self.model.structural_element_2d is None:
            self.model.set_structural_elements()
        return self.model.structural_element_2d

    @property
    def structural_element_3d(self):
        if self.model.structural_element_3d is None:
            self.model.set_structural_elements()
        return self.model.structural_element_3d

    @cache
    def get_max_min_values_of_selected_data(self, data_complex: tuple[complex], data_type: str) -> list[float, float]:
        """
        This method returns the minimum and maximum values of selected frequency for animation purposes.

        Parameters
        ----------
        data_complex: a tuple of complex values in which the phase sweep will be applied.

        data_type: a string of type DataTypes that represents the data to be processed.

        Return
        ------
        r_min, r_max: float values for minimum and maximum displacements,

        """
        if not data_complex:
            return

        amplitudes = np.abs(data_complex)
        phases = np.angle(data_complex)

        r_min = 1
        r_max = 0
        thetas = np.arange(0, 360, 2) * (np.pi / 180)

        for theta in thetas:
            results = (amplitudes * np.cos(phases + theta)).reshape(-1, 3)

            if data_type in ["u_x", "v_x", "a_x"]:
                u_xyz = results * np.array([1.0, 0.0, 0.0])
            elif data_type in ["u_y", "v_y", "a_y"]:
                u_xyz = results * np.array([0.0, 1.0, 0.0])
            elif data_type in ["u_z", "v_z", "a_z"]:
                u_xyz = results * np.array([0.0, 0.0, 1.0])
            else:
                u_xyz = np.linalg.norm(results, axis=1)

            r_min_i = np.min(u_xyz)
            if r_min_i < r_min:
                r_min = r_min_i

            r_max_i = np.max(u_xyz)
            if r_max_i > r_max:
                r_max = r_max_i

        if data_type in ["u_sum", "v_sum", "a_sum"]:
            return 0.0, r_max

        if np.abs(r_min) != np.abs(r_max):
            max_abs = np.max(np.abs([r_min, r_max]))
            r_min = -max_abs
            r_max = max_abs

        return r_min, r_max

    def compute_structural_response_field(
        self,
        column: int,
        phase_rad: float,
        data_type: DataTypes,
        n_diff: int = 0,
        unit_scale_factor: float = 1.0,
        is_modal: bool = False,
    ):
        if not isinstance(self.solution, ModalSolution | HarmonicSolution):
            return

        if isinstance(self.solution, LazyHarmonicSolution) and not self.solution.is_valid():
            return

        if is_modal:
            modal_shapes = self.solution.structural_modal_shapes
            data_complex = modal_shapes[self.solution.displacement_dof, column].copy()
        else:
            nodal_solution = self.solution.structural_solution
            data_complex = nodal_solution[self.solution.displacement_dof, column].copy()

        if unit_scale_factor != 1.0:
            data_complex *= unit_scale_factor

        if self.model.analysis_id.is_harmonic():
            freq = self.model.frequencies[column]
            data_complex *= (1j * 2 * np.pi * freq)**n_diff

        amplitudes = np.abs(data_complex)
        phases = np.angle(data_complex)
        delta = -phases[np.argmax(amplitudes)]

        phase_shifted_data = amplitudes * np.cos(phases + phase_rad + delta)
        current_solution = phase_shifted_data.reshape(-1, 3).copy()

        if data_type in ["u_sum", "v_sum", "a_sum"]:
            color_scalars = np.linalg.norm(current_solution, axis=1)
            phase_shifted_data = current_solution.copy()

        elif data_type in ["u_x", "v_x", "a_x"]:
            color_scalars = current_solution[:, 0]
            phase_shifted_data = current_solution * np.array([1.0, 0.0, 0.0])

        elif data_type in ["u_y", "v_y", "a_y"]:
            color_scalars = current_solution[:, 1]
            phase_shifted_data = current_solution * np.array([0.0, 1.0, 0.0])

        elif data_type in ["u_z", "v_z", "a_z"]:
            color_scalars = current_solution[:, 2]
            phase_shifted_data = current_solution * np.array([0.0, 0.0, 1.0])

        min_value, max_value = self.get_max_min_values_of_selected_data(tuple(data_complex), data_type)

        return phase_shifted_data, color_scalars, min_value, max_value, np.imag(data_complex).any()

    def get_structural_stresses(
            self,
            node_ids : int | list[int] | None = None,
            surface_ids: int | list[int] | None = None,
            volume_ids: list[int] | None = None,
            ):
        """
        This method computes the nodal averaged stresses and the nodal stresses
        for each element.

        Parameters
        ----------
        node_ids: int, list[int], None. (default None)
            The selected node IDs.

        surface_ids: int, list[int], None. (default None)
            The selected surface IDs.

        volume_ids: int, list[int], None. (default None)
            The selected volume IDss.

        Return
        ------
        avg_nodal_stresses_data: dict
            A dictionary whose keys are the node_ids and the values are the averaged
            nodal stresses.

        nodal_stresses_data: dict
            A dictionary whose keys are the tuples in the form (element_id, node_id)
            and the values are the nodal stresses for each element.

        """

        t0 = time()

        element_3d = self.structural_element_3d

        if element_3d.connectivities is None:
            element_3d.reorder_connect()

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        if not isinstance(node_ids, np.ndarray | list):

            node_ids = []
            if isinstance(surface_ids, int):
                surface_ids = [surface_ids]

            if isinstance(surface_ids, list):
                for surface_id in surface_ids:
                    surface_nodes = self.mesh.get_nodes_from_surface(surface_id)
                    node_ids.extend(surface_nodes)

            if isinstance(volume_ids, int):
                volume_ids = [volume_ids]

            if isinstance(volume_ids, list):
                for volume_id in volume_ids:
                    volume_nodes = self.mesh.get_nodes_from_volume(volume_id)
                    node_ids.extend(volume_nodes)

        if not node_ids:
            print("Invalid node ids")
            return {}, {}

        node_ids = np.unique(node_ids)
        element_ids = self.mesh.get_solid_elements_from_nodes(node_ids)

        dt = time() - t0
        print(f"Time 1: {dt} s")

        t0 = time()

        # local_dofs = np.arange(element_3d.dof_per_node, dtype=int)
        # dofs_indices = element_nodes.reshape(-1, 1) * element_3d.dof_per_node + local_dofs

        # # Load all frequency solutions to optimize multiple load
        # node_to_index = dict(zip(element_nodes, np.arange(element_nodes.size, dtype=int)))
        # solution = self.solution.nodal_solution[dofs_indices.flatten(), :]

        nodal_stresses_data = {}

        avg_den = defaultdict(int)
        avg_nodal_stresses_data = defaultdict(float)

        corner_indices = element_3d.corner_nodes_indices
        midside_indices_map = element_3d.midside_nodes_indices_map

        for element_id in element_ids:
            connect = element_3d.connectivities[element_id, :]
            # indices = np.array([node_to_index.get(node) for node in connect], dtype=int)
            # dofs_indices = indices.reshape(-1, 1) * element_3d.dof_per_node + local_dofs
            # dofs_indices = dofs_indices.flatten()

            element_stresses = element_3d.process_stresses_at_integration_points(
                element_id,
                nodal_solution = None, #self.solution.nodal_solution[dofs_indices, :]
                solution = self.solution.structural_solution,
                )

            enodal_stresses = element_3d.extrapolate_stresses_to_nodes(element_stresses)

            for i, e_node in enumerate(connect):
                avg_den[e_node] += 1

                if i in corner_indices:
                    avg_nodal_stresses_data[e_node] += enodal_stresses[:, i, :]
                    nodal_stresses_data[(element_id, e_node)] = enodal_stresses[:, i, :]

                else:

                    (index_1, index_2) = midside_indices_map.get(i)
                    avg_stress = (enodal_stresses[:, index_1, :] + enodal_stresses[:, index_2, :]) / 2

                    avg_nodal_stresses_data[e_node] += avg_stress
                    nodal_stresses_data[(element_id, e_node)] = avg_stress

        for _node_id, den in avg_den.items():
            avg_nodal_stresses_data[_node_id] /= den

        dt = time() - t0
        print(f"Time 2: {dt} s")

        return avg_nodal_stresses_data, nodal_stresses_data

    def get_structural_stresses_ref(
            self,
            node_ids : int | list[int] | None = None,
            surface_ids: int | list[int] | None = None,
            volume_ids: list[int] | None = None,
            ):
        """
        This method computes the nodal averaged stresses and the nodal stresses
        for each element.

        Parameters
        ----------
        node_ids: int, list[int], None. (default None)
            The selected node IDs.

        surface_ids: int, list[int], None. (default None)
            The selected surface IDs.

        volume_ids: int, list[int], None. (default None)
            The selected volume IDss.

        Return
        ------
        avg_nodal_stresses_data: dict
            A dictionary whose keys are the node_ids and the values are the averaged
            nodal stresses.

        nodal_stresses_data: dict
            A dictionary whose keys are the tuples in the form (element_id, node_id)
            and the values are the nodal stresses for each element.
        """

        mesh = self.model.mesh
        element_3d = self.model.structural_element_3d

        # if element_3d is None:
        #     self.harmonic_solver.assembler.define_structural_elements()
        #     element_3d = self.harmonic_solver.assembler.element_3d

        if element_3d.connectivities is None:
            element_3d.reorder_connect()

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        if not isinstance(node_ids, np.ndarray | list):

            node_ids = []
            if isinstance(surface_ids, int):
                surface_ids = [surface_ids]

            if isinstance(surface_ids, list):
                for surface_id in surface_ids:
                    surface_nodes = mesh.get_nodes_from_surface(surface_id)
                    node_ids.extend(surface_nodes)

            if isinstance(volume_ids, int):
                volume_ids = [volume_ids]

            if isinstance(volume_ids, list):
                for volume_id in volume_ids:
                    volume_nodes = mesh.get_nodes_from_volume(volume_id)
                    node_ids.extend(volume_nodes)

        if not node_ids:
            print("Invalid node ids")
            return {}, {}

        node_ids = np.unique(node_ids)

        map_elements_to_nodes, filtered_nodes = mesh.get_solid_elements_connected_to_nodes(
            node_ids=node_ids, return_nodes=True)

        local_dofs = np.arange(element_3d.dof_per_node, dtype=int)
        dofs_indices = filtered_nodes.reshape(-1, 1) * element_3d.dof_per_node + local_dofs

        # Load all frequency solutions to optimize multiple load on the `process_particle_velocity` method below.
        node_to_index = dict(zip(filtered_nodes, np.arange(filtered_nodes.size, dtype=int)))
        solution = self.solution.structural_solution[dofs_indices.flatten(), :]

        nodal_stresses_data = {}
        avg_nodal_stresses_data = defaultdict(float)

        for node_id, solid_element_ids in map_elements_to_nodes.items():

            n_el = len(solid_element_ids)

            for element_id in solid_element_ids:
                connect = element_3d.connectivities[element_id, :]
                indices = np.array([node_to_index.get(node) for node in connect], dtype=int)

                dofs_indices = indices.reshape(-1, 1) * element_3d.dof_per_node + local_dofs
                dofs_indices = dofs_indices.flatten()

                element_stresses = element_3d.process_stresses_at_integration_points(
                    element_id,
                    nodal_solution = solution[dofs_indices, :]
                    )

                nodal_stresses = element_3d.extrapolate_stresses_to_nodes(element_stresses)
                for i, e_node in enumerate(connect):
                    nodal_stresses_data[(element_id, e_node)] = nodal_stresses[:, i, :]

                avg_nodal_stresses_data[node_id] += nodal_stresses_data[(element_id, node_id)] / n_el

        return avg_nodal_stresses_data, nodal_stresses_data


    def nodal_stresses_post_process(self, input_stresses_data: dict):

        nodal_stresses = NodalStresses()

        for key in input_stresses_data.keys():
            stresses = input_stresses_data.get(key)
            if stresses is None:
                continue

            nodal_stresses.sigma_x[key] = stresses[0, :]
            nodal_stresses.sigma_y[key] = stresses[1, :]
            nodal_stresses.sigma_z[key] = stresses[2, :]
            nodal_stresses.tau_xy[key] = stresses[3, :]
            nodal_stresses.tau_xz[key] = stresses[4, :]
            nodal_stresses.tau_yz[key] = stresses[5, :]

        return nodal_stresses


        ## Only for validation purposes
        # output_data = np.zeros((len(ordered_nodes), 4), dtype=float)
        # output_data[:, 0] = ordered_nodes

        # for row, node_id in enumerate(ordered_nodes):
        #     output_data[row, 1:] =  self.assembler.model.mesh.nodal_normals_data[node_id]

        # fname = f"nodal_normals_data_surface_{surface_id}.dat"
        # header = "Node index || x-axis component [m] || y-axis component [m] || z-axis component [m]"
        # np.savetxt(fname, output_data, fmt=["%i", "%.16f", "%.16f", "%.16f"], delimiter=",", header=header)
