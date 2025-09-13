import logging
from functools import cache

import numpy as np

from typing import Literal, TYPE_CHECKING

from vibra.engine.solvers import ModalSolver, HarmonicSolver

if TYPE_CHECKING:
    from vibra.project_files.project import Project

AcousticPlotTypes = Literal[
    "absolute_animation",
    "non_absolute_animation",
    "absolute_values",
    "real_values",
    "imag_values",
]


class AcousticPostprocessing:
    def __init__(self, project: 'Project'=None, acoustic_modal_solver: ModalSolver=None, acoustic_harmonic_solver: HarmonicSolver=None):
        if all(v is None for v in [project, acoustic_modal_solver, acoustic_harmonic_solver]):  
            raise ValueError("At least one of 'project', 'acoustic_modal_solver', or 'acoustic_harmonic_solver' must be provided.")
        self.project = project
        self.acoustic_modal_solver = acoustic_modal_solver
        self.acoustic_harmonic_solver = acoustic_harmonic_solver

    @property
    def harmonic_solver(self):
        if self.project is not None:
            return self.project.acoustic_harmonic_solver
        return self.acoustic_harmonic_solver

    @property
    def modal_solver(self):
        if self.project is not None:
            return self.project.acoustic_modal_solver
        return self.acoustic_modal_solver

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
            data = self.modal_solver.solution[:, column]
        else:
            data = self.harmonic_solver.solution[:, column]

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

            if p_min_i < p_min:
                p_min = p_min_i
            if p_max_i > p_max:
                p_max = p_max_i

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
        plot_type: AcousticPlotTypes,
        is_modal: bool = False
    ):

        if is_modal:
            solver = self.modal_solver
        else:
            solver = self.harmonic_solver

        if solver.solution is None:
            return None

        selected_mode_shape = solver.solution[:, index]
        amplitudes = np.abs(selected_mode_shape)
        phases = np.angle(selected_mode_shape)
        delta = -phases[np.argmax(amplitudes)]
        acoustic_pressures = amplitudes * np.cos(phases + phase_rad + delta)
        if plot_type == "absolute_values":
            acoustic_pressures = np.abs(selected_mode_shape)
        elif plot_type == "real_values":
            acoustic_pressures = np.real(selected_mode_shape)
        elif plot_type == "imag_values":
            acoustic_pressures = np.imag(selected_mode_shape)
        elif plot_type == "absolute_animation":
            acoustic_pressures = np.abs(acoustic_pressures)

        min_value, max_value = self.get_min_max_values_of_pressures(index, plot_type, is_modal)

        return acoustic_pressures, min_value, max_value, np.imag(selected_mode_shape).any()

    def compute_particle_velocity(
         self,
         component_label: str,
         node_id: int | None = None,
         surface_id: int | None = None,
    ):
        frequencies = self.harmonic_solver.assembler.frequencies
        zeros = np.zeros_like(frequencies, dtype=complex)

        if isinstance(node_id, int):
            surface_ids = self.harmonic_solver.assembler.model.mesh.get_surfaces_from_node(node_id)
            if np.unique(surface_ids).size != 1:
                return zeros, None
            surface_id = surface_ids[0]

        rho, _ = self.harmonic_solver.assembler.model.get_fluid_properties_from_surface(surface_id, frequencies)
        if rho is None:
            return zeros, None

        particle_velocities_data = self.get_particle_velocity_from_surface(surface_id, rho)
        particle_velocities_Vj = particle_velocities_data.get(component_label)
        if not isinstance(particle_velocities_Vj, dict):
            return zeros, None

        if isinstance(node_id, int):
            return particle_velocities_Vj.get(node_id)

        else:
            array_particle_velocities_Vj = np.array(list(particle_velocities_Vj.values()), dtype=complex)
            return np.average(array_particle_velocities_Vj, axis=0)

    def compute_acoustic_impedance(self, node_id: int | None = None, surface_id: int | None = None):
        frequencies = self.harmonic_solver.assembler.frequencies
        aux_zeros = np.zeros_like(frequencies, dtype=complex)

        if isinstance(node_id, int):
            surface_ids = self.harmonic_solver.assembler.model.mesh.get_surfaces_from_node(node_id)
            if np.unique(surface_ids).size != 1:
                return aux_zeros, None

            surface_id = surface_ids[0]

        elif isinstance(surface_id, int):
            nodes = self.harmonic_solver.assembler.model.mesh.get_nodes_from_surface(surface_id)

        else:
            return aux_zeros, None

        rho, _ = self.harmonic_solver.assembler.model.get_fluid_properties_from_surface(surface_id, frequencies)
        if rho is None:
            return aux_zeros, None
        particle_velocities_data = self.get_particle_velocity_from_surface(surface_id, rho)
        particle_velocities_Vj = particle_velocities_data.get("Vn")

        if not isinstance(particle_velocities_Vj, dict):
            return aux_zeros, None

        if isinstance(node_id, int):
            pressure = self.harmonic_solver.solution[node_id, :]
            particle_velocity = particle_velocities_Vj.get(node_id)
            return pressure / particle_velocity

        else:
            pressures = self.harmonic_solver.solution[nodes, :]
            array_particle_velocities_Vj = np.array(list(particle_velocities_Vj.values()), dtype=complex)
            surface_impedance = pressures / array_particle_velocities_Vj
            return np.average(surface_impedance, axis=0)
        
    def compute_surface_absorption_coefficient(
        self, 
        surface_id: int | None = None,
    ):

        frequencies = self.harmonic_solver.assembler.frequencies
        aux_zeros = np.zeros_like(frequencies, dtype=complex)

        rho, speed_of_sound = self.harmonic_solver.assembler.model.get_fluid_properties_from_surface(surface_id, frequencies)
        Z0 = rho * speed_of_sound

        Zs = self.compute_acoustic_impedance(surface_id=surface_id)
        if not Zs.any():
            return aux_zeros
        # R is the sound reflection coefficient
        R = (Zs - Z0) / (Zs + Z0)

        # alpha is the sound absorption coefficient
        alpha = 1 - (np.abs(R))**2

        return alpha
    def get_particle_velocity_from_surface(self, surface_id: int, rho: float | np.ndarray):
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

        frequencies = self.harmonic_solver.assembler.model.frequencies
        element_3d = self.harmonic_solver.assembler.model.acoustic_element_3d

        if element_3d is None:
            self.harmonic_solver.assembler.define_acoustic_elements()
            element_3d = self.harmonic_solver.assembler.element_3d
        
        if element_3d.connectivity is None:
            element_3d.reorder_connect()

        data_normals = self.harmonic_solver.assembler.model.mesh.get_average_normals_for_surface_nodes(surface_id)
        map_elements_to_nodes, filtered_nodes = self.harmonic_solver.assembler.model.mesh.get_solid_elements_connected_to_nodes(
            surface_id=surface_id, return_nodes=True)
        
        # Load all frequency solutions to optimize multiple load on the `process_particle_velocity` method below.
        node_to_index = dict(zip(filtered_nodes, np.arange(filtered_nodes.size, dtype=int)))
        solution = self.harmonic_solver.solution[filtered_nodes, :]

        pv_data = dict()
        for node_id, solid_element_ids in map_elements_to_nodes.items():

            Vk = 0.
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

        Vx = dict()
        Vy = dict()
        Vz = dict()
        Vn = dict()
        particle_velocities = dict()

        for i, _node_id in enumerate(np.sort(list(pv_data.keys()))):
            Vx[_node_id] = pv_data[_node_id][0, :]
            Vy[_node_id] = pv_data[_node_id][1, :]
            Vz[_node_id] = pv_data[_node_id][2, :]
            Vn[_node_id] = pv_data[_node_id].T @ data_normals[_node_id]

        particle_velocities["Vx"] = Vx
        particle_velocities["Vy"] = Vy
        particle_velocities["Vz"] = Vz
        particle_velocities["Vn"] = Vn
        particle_velocities["nodal_normals"] = data_normals

        ## Uncomment the line below to plot the average normals at the nodes
        # self.assembler.model.mesh.set_nodal_normals_data(data_normals)

        ## Only for validation purposes
        # output_data = np.zeros((len(ordered_nodes), 4), dtype=float)
        # output_data[:, 0] = ordered_nodes

        # for row, node_id in enumerate(ordered_nodes):
        #     output_data[row, 1:] =  self.assembler.model.mesh.nodal_normals_data[node_id]

        # fname = f"nodal_normals_data_surface_{surface_id}.dat"
        # header = "Node index || x-axis component [m] || y-axis component [m] || z-axis component [m]"
        # np.savetxt(fname, output_data, fmt=["%i", "%.16f", "%.16f", "%.16f"], delimiter=",", header=header)

        return particle_velocities

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

        model = self.harmonic_solver.assembler.model
        frequencies = self.harmonic_solver.assembler.model.frequencies

        nodes_input = np.sort(model.mesh.get_nodes_from_surface(input_surface_id))
        nodes_output = np.sort(model.mesh.get_nodes_from_surface(output_surface_id))

        P_in = self.harmonic_solver.solution[nodes_input, :]
        P_out = self.harmonic_solver.solution[nodes_output, :]

        logging.info("Processing the transmission loss... [40/100]")

        if not surface_integration:

            A_in = model.mesh.surface_area_from_element_integration.get(input_surface_id)
            A_out = model.mesh.surface_area_from_element_integration.get(output_surface_id)

            # print(f"A_in: {A_in} [m²]")
            # print(f"A_out: {A_out} [m²]")

            nodal_areas_in = np.zeros(len(nodes_input), dtype=float)
            for i, node in enumerate(nodes_input):
                areas = model.mesh.nodal_area[node]
                nodal_areas_in[i] = sum(areas)

            # _nodal_areas_in = np.array([nodes_input, nodal_areas_in * (A_in / np.sum(nodal_areas_in))]).T
            # np.savetxt(f"nodal_areas_surface_{input_surface_id}.dat", _nodal_areas_in, fmt=["%i", "%.16f"], delimiter=",", header="Node index || Nodal area [m2]")

            nodal_areas_out = np.zeros(len(nodes_output), dtype=float)
            for i, node in enumerate(nodes_output):
                areas = model.mesh.nodal_area[node]
                nodal_areas_out[i] = sum(areas)

            # _nodal_areas_out = np.array([nodes_output, nodal_areas_out * (A_out / np.sum(nodal_areas_out))]).T
            # # np.savetxt(f"nodal_areas_surface_{output_surface_id}.dat", _nodal_areas_out, fmt=["%i", "%.16f"], delimiter=",", header="Node index || Nodal area [m2]")

            Aeff_in = nodal_areas_in.reshape(-1, 1) * (A_in / np.sum(nodal_areas_in))
            Aeff_out = nodal_areas_out.reshape(-1, 1) * (A_out / np.sum(nodal_areas_out))

            rho_in, _ = model.get_fluid_properties_from_surface(input_surface_id, frequencies)
            if rho_in is None:
                return None, None

            rho_out, _ = model.get_fluid_properties_from_surface(output_surface_id, frequencies)
            if rho_out is None:
                return None, None

            logging.info("Processing the transmission loss... [50/100]")
            input_pv_data = self.get_particle_velocity_from_surface(input_surface_id, rho_in)

            logging.info("Processing the transmission loss... [60/100]")
            output_pv_data = self.get_particle_velocity_from_surface(output_surface_id, rho_out)

        logging.info("Processing the transmission loss... [70/100]")
        Zo_in = model.get_surface_impedance(input_surface_id)
        if Zo_in is None:
            return None, None

        Zo_out = model.get_surface_impedance(output_surface_id)
        if Zo_out is None:
            return None, None

        logging.info("Processing the transmission loss... [80/100]")
        (P_downstream, V_downstream) = model.get_downstream_pressure_and_particle_velocity(input_surface_id)
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
            V_out = np.array(list(output_pv_data["Vn"].values()), dtype=complex)
            I_out = np.real(P_out * np.conjugate(V_out)) / 2

            # NOTE: be careful of using the calculated particle velocity in the sound power
            # integration. If the element shape functions are linear, the particle velocity
            # will be constant in the element. This results is not consitent with the physics,
            # therefore, you should use 'richer' elements with the quadratic shape functions
            # to get more representative results.

            # V_in = -np.array(list(input_pv_data["Vn"].values()), dtype=complex)
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
            self,
            surface_id: int,
            pressures: np.ndarray,
            particle_velocities: np.ndarray,
            dB_scale: bool = True
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

        assembler = self.harmonic_solver.assembler

        nodes = np.sort(assembler.model.mesh.get_nodes_from_surface(surface_id))
        surface_connectivities = assembler.model.mesh.get_connectivity_from_surface(surface_id)

        number_nodes = len(nodes)
        map_nodes = dict(zip(nodes, np.arange(number_nodes)))

        if len(pressures.shape) == 1:
            pressures = np.tile(pressures, (number_nodes, 1))

        if len(particle_velocities.shape) == 1:
            particle_velocities = np.tile(particle_velocities, (number_nodes, 1))

        element_2d = self.harmonic_solver.assembler.element_2d
        if element_2d is None:
            assembler.define_acoustic_elements()
            element_2d = assembler.element_2d

        sound_power = 0.
        for i, e_connect in enumerate(surface_connectivities):
            node_indexes = [map_nodes.get(node) for node in e_connect]
            L_sv = pressures[node_indexes, :].T.reshape(-1, 1, 3)
            R_sv = particle_velocities[node_indexes, :].T.reshape(-1, 3, 1)

            normalized_data = element_2d.elementary_sound_power(e_connect, L_sv, R_sv)
            sound_power += np.real(normalized_data) / 2

        if dB_scale:
            return 10 * np.log10(sound_power / 1e-12)

        return sound_power

    def compute_noise_reduction(
            self, 
            input_surface_id: int, 
            output_surface_id: int
            ):
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

        frequencies = self.harmonic_solver.assembler.model.frequencies
        rows_input = self.harmonic_solver.assembler.model.mesh.get_nodes_from_surface(input_surface_id)
        rows_output = self.harmonic_solver.assembler.model.mesh.get_nodes_from_surface(output_surface_id)

        P_in = np.average(self.harmonic_solver.solution[rows_input, :], axis=0)
        P_out = np.average(self.harmonic_solver.solution[rows_output, :], axis=0)

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
    """
    """
    import matplotlib.pyplot as plt
    plt.ion()
    plt.cla()
    plt.spy(matrix, color=(0.25,0.25,0.25))
    plt.show()
