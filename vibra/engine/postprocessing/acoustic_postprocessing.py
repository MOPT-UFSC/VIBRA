from __future__ import annotations

import logging
from functools import cache

# from time import perf_counter
from typing import Optional

import numpy as np

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.postprocessing.acoustic_post_solution_dataclass import NodalParticleVelocities
from vibra.engine.solution import HarmonicSolution, Solution
from vibra.interface.viewer_3d.plot_setup import PressurePlotType
from vibra.utils.lazy_array import LazyArray
from vibra.utils.signal_processing import process_multiple_iffts_from_one_sided_spectrum_signals


class AcousticPostprocessing:
    def __init__(self, model: Model):
        if not isinstance(model, Model):
            raise ValueError("The model argument must be of type Model.")

        self.model = model

        self.waveforms = np.array([], dtype=float)

    @property
    def mesh(self) -> Optional[Mesh]:
        return self.model.mesh

    @property
    def solution(self) -> Optional[Solution]:
        return self.model.solution

    @property
    def acoustic_element_2d(self):
        if self.model.acoustic_element_2d is None:
            self.model.set_acoustic_elements()
        return self.model.acoustic_element_2d

    @property
    def acoustic_element_3d(self):
        if self.model.acoustic_element_3d is None:
            self.model.set_acoustic_elements()
        return self.model.acoustic_element_3d

    @cache
    def get_min_max_values_of_pressures(self, column: int, plot_type: str, is_modal: bool = False):
        """
        This method returns the minimum and maximum pressure values
        of selected frequency used in the animation processing.

        Parameters
        ----------
        column: int value relative to frequency column index.

        Returns
        -------
        p_min, p_max: float values for minimum and maximum pressures,

        """

        if is_modal:
            nodal_solution = self.solution.modal_shapes
        else:
            nodal_solution = self.solution.nodal_solution

        if isinstance(nodal_solution, LazyArray) and not nodal_solution.is_valid():
            return None

        data = nodal_solution[:, column]

        amplitudes = np.abs(data)
        phases = np.angle(data)

        p_min = 1
        p_max = 0

        divisions = 36
        thetas = np.linspace(0, 2 * np.pi, divisions + 1, endpoint=True)

        if plot_type == "absolute_values":
            return 0, max(np.abs(data))

        if plot_type == "real_values":
            return min(np.real(data)), max(np.real(data))

        if plot_type == "imag_values":
            return min(np.imag(data)), max(np.imag(data))

        for theta in thetas:
            pressures = amplitudes * np.cos(theta + phases)

            if plot_type == "absolute_animation":
                pressures = np.abs(pressures)

            p_min_i = min(pressures)
            p_max_i = max(pressures)

            p_min = min(p_min, p_min_i)
            p_max = max(p_max, p_max_i)

        if plot_type == "absolute_animation":
            p_min = 0

        if plot_type == "non_absolute_animation":
            max_value = np.max(np.abs([p_min, p_max]))
            p_min = -max_value
            p_max = max_value

        return p_min, p_max

    def compute_acoustic_pressure_field(
        self,
        index: int,
        phase_rad: float,
        plot_type: PressurePlotType,
        is_modal: bool = False,
    ):
        if self.solution is None:
            return

        if is_modal:
            nodal_solution = self.solution.modal_shapes
        else:
            nodal_solution = self.solution.nodal_solution

        if isinstance(nodal_solution, LazyArray) and not nodal_solution.is_valid():
            return

        if nodal_solution.shape[1] < index:
            return

        # selected nodal solution
        _nodal_solution = nodal_solution[:, index]

        amplitudes = np.abs(_nodal_solution)
        phases = np.angle(_nodal_solution)
        delta = -phases[np.argmax(amplitudes)]

        acoustic_pressures = amplitudes * np.cos(phases + phase_rad + delta)
        match plot_type:
            case PressurePlotType.ABSOLUTE_VALUES:
                acoustic_pressures = np.abs(_nodal_solution)
            case PressurePlotType.REAL_VALUES:
                acoustic_pressures = np.real(_nodal_solution)
            case PressurePlotType.IMAG_VALUES:
                acoustic_pressures = np.imag(_nodal_solution)
            case PressurePlotType.ABSOLUTE_ANIMATION:
                acoustic_pressures = np.abs(acoustic_pressures)

        min_value, max_value = self.get_min_max_values_of_pressures(index, plot_type, is_modal)

        return acoustic_pressures, min_value, max_value, np.imag(_nodal_solution).any()

    def compute_acoustic_transient_pressure_field(
        self,
        time_index: int,
        plot_type: PressurePlotType,
        reduced_loop_time: float | None = None,
    ):

        time_vector, self.waveforms = self.compute_multiple_ifft()

        if reduced_loop_time is None:
            n = time_vector.size
        else:
            n = np.sum(time_vector <= reduced_loop_time)

        # cache the minimum and maximum values of the nodal pressure waveforms
        min_max_values = self.get_acoustic_waveforms_minimum_and_maximum_values(int(n))
        acoustic_pressures = self.waveforms[:, time_index].flatten()

        match plot_type:
            case PressurePlotType.ABSOLUTE_ANIMATION:
                acoustic_pressures = np.abs(acoustic_pressures)
                min_value = 0
                max_value = np.max(np.abs(min_max_values))

            case _:
                min_value, max_value = min_max_values

        return time_vector[:n], acoustic_pressures, min_value, max_value

    @cache
    def compute_multiple_ifft(self) -> tuple[np.ndarray, np.ndarray]:
        assert isinstance(self.solution, HarmonicSolution)
        assert self.solution.analysis_id.is_acoustic()  # for now, I guess

        # t0 = perf_counter()
        logging.info("Computing multiple iffts... [25/100]")
        time_vector, waveforms = process_multiple_iffts_from_one_sided_spectrum_signals(
            self.solution.frequencies,
            self.solution.nodal_solution,
            dc_included=False,
        )

        logging.info("Computing multiple iffts... [100/100]")

        # dt = perf_counter() - t0
        # print(f"Elapsed time to process ifft: {dt: .6f} s")

        return time_vector, waveforms

    @cache
    def get_acoustic_waveforms_minimum_and_maximum_values(self, N: float):
        _waveforms = self.waveforms[:, :N]
        return (_waveforms.min(), _waveforms.max())

    def compute_particle_velocity(
        self,
        component_label: str,
        node_id: int | None = None,
        surface_id: int | None = None,
        volume_id: int | None = None,
    ) -> np.ndarray:

        if isinstance(node_id, int):
            surface_ids = self.mesh.get_surfaces_from_node(node_id)
            if np.unique(surface_ids).size != 1:
                print(f"The surfaces {surface_ids} contains the node: {node_id}")

            surface_id = surface_ids[0]

        particle_velocities_data = self.get_particle_velocity_from_surface(surface_id, volume_id=volume_id)
        particle_velocities_Vj: dict = getattr(particle_velocities_data, component_label)

        if isinstance(node_id, int):
            return particle_velocities_Vj.get(node_id)

        else:
            array_particle_velocities_Vj = np.array(list(particle_velocities_Vj.values()), dtype=complex)
            return np.average(array_particle_velocities_Vj, axis=0)

    def compute_acoustic_impedance(self, node_id: int | None = None, surface_id: int | None = None, volume_id: int | None = None):

        frequencies = self.model.frequencies
        zeros = np.zeros_like(frequencies, dtype=complex)

        if isinstance(node_id, int):
            surface_ids = self.mesh.get_surfaces_from_node(node_id)
            if np.unique(surface_ids).size != 1:
                return zeros, None
            else:
                surface_id = surface_ids[0]

        elif isinstance(surface_id, int):
            nodes = self.mesh.get_nodes_from_surface(surface_id)

        else:
            return zeros, None

        particle_velocities_data = self.get_particle_velocity_from_surface(surface_id, volume_id=volume_id)

        if isinstance(node_id, int):
            pressure = self.solution.nodal_solution[node_id, :]
            particle_velocities_Vn: dict = getattr(particle_velocities_data, "Vn")
            particle_velocity = particle_velocities_Vn.get(node_id)
            return pressure / particle_velocity

        else:
            pressures = self.solution.nodal_solution[nodes, :]
            surface_impedance = pressures / particle_velocities_data.Vn_array()
            return np.average(surface_impedance, axis=0)

    def compute_surface_absorption_coefficient(self, surface_id: int | None = None, volume_id: int | None = None):

        frequencies = self.model.frequencies
        aux_zeros = np.zeros_like(frequencies, dtype=complex)

        rho, speed_of_sound = self.model.get_fluid_properties_from_surface(surface_id)
        Z0 = rho * speed_of_sound

        Zs = self.compute_acoustic_impedance(surface_id=surface_id, volume_id=volume_id)

        if not Zs.any():
            return aux_zeros

        # R is the sound reflection coefficient
        R = (Zs - Z0) / (Zs + Z0)

        # alpha is the sound absorption coefficient
        alpha = 1 - (np.abs(R)) ** 2

        return alpha

    def get_particle_velocity_from_surface(self, surface_id: int, volume_id: int | None = None) -> NodalParticleVelocities:
        """
        This method computes the nodal average particle velocity in the selected surface.

        Parameters
        ----------
        surface_id: int
            The selected surface ID.

        rho: float
            The fluid density related to the selected surface.

        Returns
        -------

        particle_velocities: dict
            A dictionary with the normal particle velocity and its components in
            the x, y, and z directions, computed in the selected surface.
        """

        frequencies = self.model.frequencies
        zeros = np.zeros_like(frequencies, dtype=complex)

        rho, _ = self.model.get_fluid_properties_from_volume(volume_id)
        if rho is None:
            return zeros, None

        element_3d = self.acoustic_element_3d

        if element_3d.connectivity is None:
            element_3d.reorder_connect()

        data_normals = self.mesh.get_surface_nodal_normals(surface_id, volume_id)

        map_elements_to_nodes, filtered_nodes = self.mesh.get_solid_elements_connected_to_nodes(surface_id=surface_id, return_nodes=True)

        node_ids = self.mesh.get_nodes_from_surface(surface_id)
        map_elements_to_nodes, filtered_nodes = self.mesh.get_solid_elements_connected_to_nodes(node_ids=node_ids, return_nodes=True)

        # map_elements_to_nodes, filtered_nodes = aelf.mesh.get_solid_elements_connected_to_nodes(
        #     surface_id=surface_id, return_nodes=True)

        # Load all frequency solutions to optimize multiple load on the `process_particle_velocity` method below.
        node_to_index = dict(zip(filtered_nodes, np.arange(filtered_nodes.size, dtype=int)))
        solution = self.solution.nodal_solution[filtered_nodes, :]

        pv_data = dict()
        for node_id, solid_element_ids in map_elements_to_nodes.items():
            Vk = 0.0
            for element_id in solid_element_ids:
                connect = element_3d.connectivity[element_id, 1:]
                indexes = np.array([node_to_index.get(node) for node in connect])
                enodal_pressures = solution[indexes, :]
                Vk += element_3d.process_particle_velocity(
                    element_id,
                    node_id,
                    rho,
                    frequencies,
                    nodal_pressures=enodal_pressures,
                    solution=None,
                )

            pv_data[node_id] = Vk / len(solid_element_ids)

        ## Uncomment the line below to plot the average normals at the nodes
        self.mesh.set_nodal_normals_data(surface_id, data_normals)

        ## Only for validation purposes
        # output_data = np.zeros((len(ordered_nodes), 4), dtype=float)
        # output_data[:, 0] = ordered_nodes

        # for row, node_id in enumerate(ordered_nodes):
        #     output_data[row, 1:] =  self.assembler.model.mesh.nodal_normals_data[node_id]

        # fname = f"nodal_normals_data_surface_{surface_id}.dat"
        # header = "Node index || x-axis component [m] || y-axis component [m] || z-axis component [m]"
        # np.savetxt(fname, output_data, fmt=["%i", "%.16f", "%.16f", "%.16f"], delimiter=",", header=header)

        return self.nodal_particle_velocity_post_process(pv_data, data_normals)

    def nodal_particle_velocity_post_process(self, input_particle_velocity_data: dict, nodal_normals: np.ndarray):

        nodal_particle_velocities = NodalParticleVelocities()

        for key in input_particle_velocity_data.keys():
            particle_velocity = input_particle_velocity_data.get(key)
            if particle_velocity is None:
                continue

            nodal_particle_velocities.Vx[key] = particle_velocity[0, :]
            nodal_particle_velocities.Vy[key] = particle_velocity[1, :]
            nodal_particle_velocities.Vz[key] = particle_velocity[2, :]
            nodal_particle_velocities.Vn[key] = particle_velocity.T @ nodal_normals[key]

        nodal_particle_velocities.nodal_normals = nodal_normals

        return nodal_particle_velocities

    def compute_transmission_loss(
        self,
        input_surface_id: int,
        output_surface_id: int,
        surface_integration: bool = True,
    ):
        """
        This method compute the acoustic transmission loss between two selected surfaces.

        Parameters
        ----------
        input_surface_id: int
            The input surface ID.

        output_surface_id: int
            The output surface ID.

        surface_integration: bool, optional
            It controls whether the sound power will be calculated using surface integration
            or through the summation of the product of nodal sound intensity and nodal area.

        Returns
        -------
        frequencies: np.ndarray
            The vector of valid frequencies.

        transmission_loss: np.ndarray
            The vector of computed transmission loss values in dB.

        """

        frequencies = self.model.frequencies

        logging.info("Processing the transmission loss... [10/100]")
        nodes_input = np.sort(self.mesh.get_nodes_from_surface(input_surface_id))
        nodes_output = np.sort(self.mesh.get_nodes_from_surface(output_surface_id))

        logging.info("Processing the transmission loss... [20/100]")
        # P_in = self.solution.nodal_solution[nodes_input, :]
        P_out = self.solution.nodal_solution[nodes_output, :]

        logging.info("Processing the transmission loss... [40/100]")

        if not surface_integration:
            A_in = self.mesh.surface_area_from_element_integration.get(input_surface_id)
            A_out = self.mesh.surface_area_from_element_integration.get(output_surface_id)

            # print(f"A_in: {A_in} [m²]")
            # print(f"A_out: {A_out} [m²]")

            nodal_areas_in = np.zeros(len(nodes_input), dtype=float)
            for i, node in enumerate(nodes_input):
                areas = self.mesh.nodal_area[node]
                nodal_areas_in[i] = sum(areas)

            # _nodal_areas_in = np.array([nodes_input, nodal_areas_in * (A_in / np.sum(nodal_areas_in))]).T
            # np.savetxt(f"nodal_areas_surface_{input_surface_id}.dat", _nodal_areas_in, fmt=["%i", "%.16f"], delimiter=",", header="Node index || Nodal area [m2]")

            nodal_areas_out = np.zeros(len(nodes_output), dtype=float)
            for i, node in enumerate(nodes_output):
                areas = self.mesh.nodal_area[node]
                nodal_areas_out[i] = sum(areas)

            # _nodal_areas_out = np.array([nodes_output, nodal_areas_out * (A_out / np.sum(nodal_areas_out))]).T
            # # np.savetxt(f"nodal_areas_surface_{output_surface_id}.dat", _nodal_areas_out, fmt=["%i", "%.16f"], delimiter=",", header="Node index || Nodal area [m2]")

            Aeff_in = nodal_areas_in.reshape(-1, 1) * (A_in / np.sum(nodal_areas_in))
            Aeff_out = nodal_areas_out.reshape(-1, 1) * (A_out / np.sum(nodal_areas_out))

            # Aeff_in = np.ones((nodes_input.size, 1), dtype=float) * (A_in / nodes_input.size)
            # Aeff_out = np.ones((nodes_output.size, 1), dtype=float) * (A_out / nodes_output.size)

            volumes_in = self.mesh.volumes_from_surface.get(input_surface_id)
            if volumes_in is None:
                return None, None

            volumes_out = self.mesh.volumes_from_surface.get(output_surface_id)
            if volumes_out is None:
                return None, None

            # if isinstance(volumes_in, list) and len(volumes_in) == 1:
            #     volume_in = volumes_in[0]

            if isinstance(volumes_out, list) and len(volumes_out) == 1:
                volume_out = volumes_out[0]

            # logging.info("Processing the transmission loss... [50/100]")
            # input_pv_data = self.get_particle_velocity_from_surface(input_surface_id, volume_id=volume_in)

            logging.info("Processing the transmission loss... [60/100]")
            output_pv_data = self.get_particle_velocity_from_surface(output_surface_id, volume_id=volume_out)

        logging.info("Processing the transmission loss... [70/100]")
        Zo_in = self.model.get_surface_impedance(input_surface_id)
        if Zo_in is None:
            return None, None

        Zo_out = self.model.get_surface_impedance(output_surface_id)
        if Zo_out is None:
            return None, None

        logging.info("Processing the transmission loss... [80/100]")
        (P_downstream, V_downstream) = self.model.get_downstream_pressure_and_particle_velocity(input_surface_id)
        if P_downstream is None or V_downstream is None:
            return None, None

        logging.info("Processing the transmission loss... [90/100]")
        if surface_integration:
            ## compute the sound power through surface integration
            W_in = self.integrate_surface_sound_power(input_surface_id, P_downstream, np.conj(P_downstream / Zo_in))
            W_out = self.integrate_surface_sound_power(output_surface_id, P_out, np.conj(P_out / Zo_out))

        else:
            ## compute the sound power through summation of the product of nodal sound intensity by nodal area
            # input sound intensity calculation
            I_in = np.abs(np.real(P_downstream * np.conjugate(V_downstream)) / 2)

            # output sound intensity calculation
            V_out = output_pv_data.Vn_array()
            I_out = np.real(P_out * np.conjugate(V_out)) / 2

            # NOTE: be careful of using the calculated particle velocity in the sound power
            # integration. If the element shape functions are linear, the particle velocity
            # will be constant in the element. This results is not consitent with the physics,
            # therefore, you should use 'richer' elements with the quadratic shape functions
            # to get more representative results.

            # V_in = -input_pv_data.Vn_array()
            # P_downstream = (P_in + Zo_in * V_in) / 2
            # V_downstream = P_downstream / Zo_in

            # I_in = np.real(P_downstream * np.conjugate(V_downstream)) / 2
            # I_out = np.real(P_out * np.conjugate(V_out)) / 2

            # compute the transmission loss using nodal areas
            W_in = 10 * np.log10(np.sum(I_in * Aeff_in, axis=0))
            W_out = 10 * np.log10(np.sum(I_out * Aeff_out, axis=0))

        transmission_loss = W_in - W_out

        if frequencies[0] == 0:
            frequencies = frequencies[1:]
            transmission_loss = transmission_loss[1:]

        return frequencies, transmission_loss

    def integrate_surface_sound_power(
        self, surface_id: int, pressures: np.ndarray, particle_velocities: np.ndarray, dB_scale: bool = True
    ) -> np.ndarray:
        """
        This method integrates the sound power intensity over the selected surface.

        Parameters
        ----------
            surface_id: int
                The identifier of selected surface.

            pressures: np.ndarray
                The acoustic pressures from selected suraface.

            particle_velocities: np.ndarray
                The acoustic pressures from selected suraface.

        Returns
        -------
        sound_power: np.ndarray
            The sound power level in dB if dB_scale is True or the sound power in watts otherwise.
        """

        nodes = np.sort(self.mesh.get_nodes_from_surface(surface_id))
        surface_connectivities = self.mesh.get_connectivity_from_surface(surface_id)

        number_nodes = len(nodes)
        map_nodes = dict(zip(nodes, np.arange(number_nodes)))

        if len(pressures.shape) == 1:
            pressures = np.tile(pressures, (number_nodes, 1))

        if len(particle_velocities.shape) == 1:
            particle_velocities = np.tile(particle_velocities, (number_nodes, 1))

        element_2d = self.acoustic_element_2d

        sound_power = 0.0
        for i, e_connect in enumerate(surface_connectivities):
            node_indexes = [map_nodes.get(node) for node in e_connect]
            L_sv = pressures[node_indexes, :].T.reshape(-1, 1, element_2d.DOF_PER_ELEMENT)
            R_sv = particle_velocities[node_indexes, :].T.reshape(-1, element_2d.DOF_PER_ELEMENT, 1)

            normalized_data = element_2d.elementary_sound_power(e_connect, L_sv, R_sv)
            sound_power += np.real(normalized_data) / 2

        if dB_scale:
            return 10 * np.log10(sound_power / 1e-12)

        return sound_power

    def compute_noise_reduction(self, input_surface_id: int, output_surface_id: int):
        """
        This method compute the acoustic noise reduction between two selected surfaces.

        Parameters
        ----------

        input_surface_id: int
            The input surface ID.

        output_surface_id: int
            The output surface ID.

        Returns
        -------

        frequencies: np.ndarray
            The vector of valid frequencies.

        noise_reduction: np.ndarray
            The vector of computed noise reduction values in dB.

        """

        frequencies = self.model.frequencies
        rows_input = self.mesh.get_nodes_from_surface(input_surface_id)
        rows_output = self.mesh.get_nodes_from_surface(output_surface_id)

        P_in = np.average(self.solution.nodal_solution[rows_input, :], axis=0)
        P_out = np.average(self.solution.nodal_solution[rows_output, :], axis=0)

        # the zero_shift constant is summed to avoid zero values either in P_input2 or P_output2 variables
        zero_shift = 1e-12

        Prms_out2 = np.real(P_out * np.conjugate(P_out)) / 2 + zero_shift
        Prms_in2 = np.real(P_in * np.conjugate(P_in)) / 2 + zero_shift

        noise_reduction = 10 * np.log10(Prms_in2 / Prms_out2)

        if frequencies[0] == 0:
            frequencies = frequencies[1:]
            noise_reduction = noise_reduction[1:]

        return frequencies, noise_reduction


def plot_graph(matrix):
    """ """
    import matplotlib.pyplot as plt

    plt.ion()
    plt.cla()
    plt.spy(matrix, color=(0.25, 0.25, 0.25))
    plt.show()
