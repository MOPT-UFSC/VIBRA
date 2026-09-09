from __future__ import annotations

import logging
from collections import defaultdict
from functools import cache
from time import perf_counter
from typing import Literal

import numpy as np

from vibra.engine.model import Model
from vibra.engine.postprocessing.structural_post_solution_dataclass import NodalStresses
from vibra.engine.solution import HarmonicSolution, LazyHarmonicSolution, ModalSolution
from vibra.interface.viewer_3d.plot_setup import DisplacementFieldPlotSetupFrequency, StressPlotType, StressType

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
            r_min = min(r_min, r_min_i)

            r_max_i = np.max(u_xyz)
            r_max = max(r_max, r_max_i)

        if data_type in ["u_sum", "v_sum", "a_sum"]:
            return 0.0, r_max

        if np.abs(r_min) != np.abs(r_max):
            max_abs = np.max(np.abs([r_min, r_max]))
            r_min = -max_abs
            r_max = max_abs

        return r_min, r_max


    @cache
    def get_max_min_values_for_stress_data(self, data_complex: tuple[complex], data_type: str) -> list[float, float]:
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

        s_min = 1
        s_max = 0

        divisions = 36
        thetas = np.linspace(0, 2 * np.pi, divisions + 1, endpoint=True)

        if data_type == "absolute_values":
            return 0, max(np.abs(data_complex))

        if data_type == "real_values":
            return min(np.real(data_complex)), max(np.real(data_complex))

        if data_type == "imag_values":
            return min(np.imag(data_complex)), max(np.imag(data_complex))

        for theta in thetas:
            pressures = amplitudes * np.cos(theta + phases)

            if data_type == "absolute_animation":
                pressures = np.abs(pressures)

            s_min_i = min(pressures)
            s_max_i = max(pressures)

            s_min = min(s_min, s_min_i)
            s_max = max(s_max, s_max_i)

        if data_type == "absolute_animation":
            s_min = 0

        if data_type == "non_absolute_animation":
            max_value = np.max(np.abs([s_min, s_max]))
            s_min = -max_value
            s_max = max_value

        return s_min, s_max


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


    def compute_structural_response_field_for_stress_plot(
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

        min_value, max_value = self.get_max_min_values_of_selected_data(tuple(data_complex), data_type)

        return current_solution, max_value


    @cache
    def recover_nodal_averaged_structural_stresses(
            self,
            node_ids : int | list[int] | None = None,
            surface_ids: int | list[int] | None = None,
            volume_ids: list[int] | None = None,
            ) -> np.ndarray | None:
        """
        This method computes the nodal averaged.

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
        avg_nodal_stresses: np.ndarray
            A 3D array in which each plane stores the averaged nodal stresses, so that each row
            contains a stress (Sx, Sy, Sz, Txy, Txz, Tyz) and the columns represent the frequencies.

        """

        logging.info("Recovering the structural stresses... (1/3)")

        t0 = perf_counter()

        element_3d = self.structural_element_3d

        if element_3d.connectivities is None:
            element_3d.reorder_connect()

        if all(item is None for item in (node_ids, surface_ids, volume_ids)):
            node_ids = self.model.domains_processor.nodes_of_domain.get("structural", [])

        elif isinstance(node_ids, int):
            node_ids = [node_ids]

        elif not isinstance(node_ids, np.ndarray | list):

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

            node_ids = np.unique(node_ids)

        if not isinstance(node_ids, np.ndarray | list):
            print("Invalid node ids")
            return

        logging.info("Recovering the structural stresses... (2/3)")
        element_ids = self.model.get_solid_elements_from_nodes(node_ids, "structural")

        dt = perf_counter() - t0
        print(f"Time 1: {dt} s")

        t0 = perf_counter()

        # initialize variables
        n_nodes = len(node_ids)
        n_el = len(element_ids)
        n_freq = len(self.model.frequencies)

        avg_nodal_stresses = np.zeros((n_nodes, 6, n_freq), dtype=complex)
        _, counts = np.unique(self.mesh.solids_connectivity[element_ids, 4:], return_counts=True)

        corner_indices = element_3d.corner_nodes_indices
        midside_data = element_3d.midside_nodes_indices
        is_quadratic = np.any(midside_data)

        if is_quadratic:
            midside_indices = midside_data[:, 0]
            ind_1 = midside_data[:, 1]
            ind_2 = midside_data[:, 2]

        # initialize logging variable
        last_progress = 0

        for i, element_id in enumerate(element_ids):

            progress = int((100 * (i / n_el) // 5) * 5)
            if progress != last_progress:
                logging.info(f"Recovering the structural stresses... [{progress}/100]")

            # process the extrapolated nodal stresses
            enodal_stresses = element_3d.process_stresses_at_integration_points(
                element_id,
                solution = self.solution.structural_solution,
                extrapolate=True,
                )

            # map the node indexes
            connect = element_3d.connectivities[element_id, :]
            _connect = self.model.get_mapped_nodes(connect, "structural")

            avg_nodal_stresses[_connect[corner_indices], :, :] += enodal_stresses

            if is_quadratic:
                avg_nodal_stresses[_connect[midside_indices], :, :] += (enodal_stresses[ind_1, :, :] + enodal_stresses[ind_2, :, :]) / 2

        # average the nodal stresses
        avg_nodal_stresses /= counts.reshape(-1, 1, 1)

        dt = perf_counter() - t0
        print(f"Time 2: {dt} s")

        return avg_nodal_stresses


    def recover_element_structural_stresses(
            self,
            node_ids : int | list[int] | None = None,
            surface_ids: int | list[int] | None = None,
            volume_ids: list[int] | None = None,
            ) -> np.ndarray | None:
        """
        This method computes the nodal stresses for each element.

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
        element_stress_data: dict
            A dictionary whose keys are the element_id and the values are the nodal
            stresses for each element (3D array with dimensions: n_nodes x 6 x Nf).

        """

        logging.info("Recovering the structural stresses... (1/3)")

        t0 = perf_counter()

        element_3d = self.structural_element_3d

        if element_3d.connectivities is None:
            element_3d.reorder_connect()

        if all(item is None for item in (node_ids, surface_ids, volume_ids)):
            node_ids = self.model.domains_processor.nodes_of_domain.get("structural", [])

        elif isinstance(node_ids, int):
            node_ids = [node_ids]

        elif not isinstance(node_ids, np.ndarray | list):

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

            node_ids = np.unique(node_ids)

        if not isinstance(node_ids, np.ndarray | list):
            print("Invalid node ids")
            return

        logging.info("Recovering the structural stresses... (2/3)")
        element_ids = self.model.get_solid_elements_from_nodes(node_ids, "structural")

        dt = perf_counter() - t0
        print(f"Time 1: {dt} s")

        t0 = perf_counter()

        # initialize variables
        n_el = len(element_ids)
        element_stress_data = {}

        midside_data = element_3d.midside_nodes_indices
        is_quadratic = np.any(midside_data)

        if is_quadratic:
            ind_1 = midside_data[:, 1]
            ind_2 = midside_data[:, 2]

        # initialize logging variable
        last_progress = 0

        for i, element_id in enumerate(element_ids):

            progress = int((100 * (i / n_el) // 5) * 5)
            if progress != last_progress:
                logging.info(f"Recovering the structural stresses... [{progress}/100]")

            # process the extrapolated nodal stresses
            enodal_stresses = element_3d.process_stresses_at_integration_points(
                element_id,
                solution = self.solution.structural_solution,
                extrapolate=True,
                )

            # map the node indexes
            if is_quadratic:
                midside_stresses = (enodal_stresses[ind_1, :, :] + enodal_stresses[ind_2, :, :]) / 2
                element_stress_data[element_id] = np.append(enodal_stresses, midside_stresses, axis=0)
            else:
                element_stress_data[element_id] = enodal_stresses

        dt = perf_counter() - t0
        print(f"Time 2: {dt} s")

        return element_stress_data


    def compute_structural_stresses_field(
        self,
        column: int,
        phase_rad: float,
        stress_type: StressType,
        data_type: StressPlotType,
    ):

        t0 = perf_counter()
        avg_nodal_stresses = self.recover_nodal_averaged_structural_stresses()
        if avg_nodal_stresses is None:
            return
        dt = perf_counter() - t0
        print(f"Time to compute nodal stresses: {dt} s")

        t0 = perf_counter()
        n_nodes = len(avg_nodal_stresses)

        # initialize the stress vector
        stress_vector = np.zeros(n_nodes, dtype=complex)

        for index, nodal_stresses in enumerate(avg_nodal_stresses):
            stress_vector[index] = nodal_stresses[stress_type, column]

        amplitudes = np.abs(stress_vector)
        phases = np.angle(stress_vector)
        delta = -phases[np.argmax(amplitudes)]

        stress_values = amplitudes * np.cos(phases + phase_rad + delta)

        match data_type:
            case StressPlotType.ABSOLUTE_VALUES:
                stress_values = np.abs(stress_vector)
            case StressPlotType.REAL_VALUES:
                stress_values = np.real(stress_vector)
            case StressPlotType.IMAG_VALUES:
                stress_values = np.imag(stress_vector)
            case StressPlotType.ABSOLUTE_ANIMATION:
                stress_values = np.abs(stress_values)

        # convert stresses to MPa
        stress_vector /= 1e6
        stress_values /= 1e6

        dt = perf_counter() - t0
        print(f"Time to post-process the nodal stresses (A): {dt} s")

        t0 = perf_counter()

        min_value, max_value = self.get_max_min_values_for_stress_data(tuple(stress_vector), data_type)
        symmetric_animation = not np.imag(stress_vector).any()

        dt = perf_counter() - t0
        print(f"Time to post-process the nodal stresses (B): {dt} s")

        return stress_values, min_value, max_value, symmetric_animation


    def compute_advanced_structural_stresses_field(
        self,
        column: int,
        phase_rad: float,
        stress_type: StressType,
        data_type: StressPlotType,
    ):

        t0 = perf_counter()
        avg_nodal_stresses = self.recover_nodal_averaged_structural_stresses()
        if avg_nodal_stresses is None:
            return
        dt = perf_counter() - t0
        print(f"Time to compute nodal stresses: {dt} s")

        t0 = perf_counter()
        n_nodes = len(avg_nodal_stresses)

        # initialize the stress vector
        stress_vector = np.zeros(n_nodes, dtype=complex)

        for index, nodal_stresses in enumerate(avg_nodal_stresses):

            # evaluate the stresses at a specific time/phase (phase_rad = omega * t)
            sigma_x, sigma_y, sigma_z, tau_xy, tau_xz, tau_yz = compute_phase_shifted_values(nodal_stresses[:, column], phase_rad)

            if stress_type == StressType.VON_MISES_STRESS:
                stress_vector[index] = np.sqrt((1/2) * (
                    (sigma_x-sigma_y)**2 + 
                    (sigma_y-sigma_z)**2 + 
                    (sigma_z-sigma_x)**2 +
                    6 * (tau_xy**2 + tau_xz**2 + tau_yz**2)
                    ))

            else:

                # compute the stress tensor at a specific time/phase (phase_rad = omega * t)
                stress_tensor = np.array([
                    [sigma_x, tau_xy, tau_xz], 
                    [tau_xy, sigma_y, tau_yz],
                    [tau_xz, tau_yz, sigma_z],
                    ], dtype=complex)

                # compute the maximum principal stresses
                eigen_values = np.linalg.eigvalsh(stress_tensor)

                # order the maximum principal stresses (sigma_1 >= sigma_2 >= sigma_3)
                sigma_1, sigma_2, sigma_3 = sorted(eigen_values, reverse=True)

                if stress_type == StressType.MAXIMUM_PRINCIPAL_STRESS_1:
                    stress_vector[index] = sigma_1

                elif stress_type == StressType.MAXIMUM_PRINCIPAL_STRESS_2:
                    stress_vector[index] = sigma_2
                
                elif stress_type == StressType.MAXIMUM_PRINCIPAL_STRESS_3:
                    stress_vector[index] = sigma_3

                elif stress_type == StressType.TRESCA_STRESS:
                    stress_vector[index] = sigma_1 - sigma_3

        # copy the estress vector
        stress_values = stress_vector.copy()

        match data_type:
            case StressPlotType.ABSOLUTE_VALUES:
                stress_values = np.abs(stress_vector)
            case StressPlotType.REAL_VALUES:
                stress_values = np.real(stress_vector)
            case StressPlotType.IMAG_VALUES:
                stress_values = np.imag(stress_vector)
            case StressPlotType.ABSOLUTE_ANIMATION:
                stress_values = np.abs(stress_values)

        # convert stresses to MPa
        stress_vector /= 1e6
        stress_values /= 1e6

        dt = perf_counter() - t0
        print(f"Time to post-process the nodal stresses (A): {dt} s")

        t0 = perf_counter()

        min_value, max_value = self.get_max_min_values_for_stress_data(tuple(stress_vector), data_type)

        # force the processing of all animation frames
        symmetric_animation = False

        dt = perf_counter() - t0
        print(f"Time to post-process the nodal stresses (B): {dt} s")

        return stress_values, min_value, max_value, symmetric_animation


    ##TODO: remove as soon as the stresses recovering has been validated
    def recover_nodal_averaged_structural_stresses_ref(
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


    # TODO: remove if not used
    def nodal_stresses_post_process(self, input_stresses_data: np.ndarray):

        nodal_stresses = NodalStresses()

        nodal_stresses.sigma_x = input_stresses_data[:, 0, :]
        nodal_stresses.sigma_y = input_stresses_data[:, 1, :]
        nodal_stresses.sigma_z = input_stresses_data[:, 2, :]
        nodal_stresses.tau_xy = input_stresses_data[:, 3, :]
        nodal_stresses.tau_xz = input_stresses_data[:, 4, :]
        nodal_stresses.tau_yz = input_stresses_data[:, 5, :]

        return nodal_stresses

        ## Only for validation purposes
        # output_data = np.zeros((len(ordered_nodes), 4), dtype=float)
        # output_data[:, 0] = ordered_nodes

        # for row, node_id in enumerate(ordered_nodes):
        #     output_data[row, 1:] =  self.assembler.model.mesh.nodal_normals_data[node_id]

        # fname = f"nodal_normals_data_surface_{surface_id}.dat"
        # header = "Node index || x-axis component [m] || y-axis component [m] || z-axis component [m]"
        # np.savetxt(fname, output_data, fmt=["%i", "%.16f", "%.16f", "%.16f"], delimiter=",", header=header)


def compute_phase_shifted_values(values: np.ndarray[complex], phase_rad: float):
    return values.real * np.cos(phase_rad) -  values.imag * np.sin(phase_rad)