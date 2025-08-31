
from vibra.engine import AnalysisID
from vibra.engine.solvers.linear_solver import SolverType, initialize_solver
from vibra.engine.properties.fluid import Fluid

from typing import TYPE_CHECKING

from vibra.project_files.lazy_hdf5_matrix import LazyHDF5MatrixWriter, LazyHDF5MatrixLoader
from vibra.project_files.project_file import ProjectFile

if TYPE_CHECKING:
    from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler

import logging
import numpy as np

from functools import cache
from scipy.sparse import triu
from time import time

class AcousticHarmonicSolver:
    def __init__(self, assembler: "AcousticAssembler", project_file: ProjectFile | None = None, **kwargs):
        self.assembler = assembler
        self.project_file = project_file
        self.reset_variables()


    def reset_variables(self):
        self.loads = None
        self.solution = None
        self.dissipation_model = None
        self.analysis_type = "acoustic"


    def load_dissipation_model(self, data):
        self.dissipation_model = data


    @cache
    def get_min_max_values_of_pressures(self, column: int, plot_type: str):
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
    
        data = self.solution[:, column]

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


    def solve(self, print_log: bool = False, is_resume: bool = False):
        """ 
        This method solves the acoustic harmonic analysis using the
        direct method for both damped and undamped problems.

        Parameter
        ---------
        print_log: bool, optional
            This argument controls the printing of the solution steps to the terminal.
        """

        logging.info(f"Solving harmonic analysis (direct method)... [10/100]")

        frequencies = self.assembler.model.frequencies

        if self.project_file:
            num_rows = self.assembler.total_dofs
            solution = self.project_file.get_solution_writer(num_rows, frequencies, dtype=complex, is_resume=is_resume)
        else:
            num_rows = self.assembler.stiffness_matrix.shape[0]
            solution = np.zeros((num_rows, len(frequencies)), dtype=complex)

        self.compute_frequency_sweep(solution, print_log, is_resume)

        logging.info(f"Solving harmonic analysis (direct method)... [99/100]")
        if isinstance(solution, LazyHDF5MatrixWriter):
            solution.close()
            self.solution = self.project_file.get_solution_loader()
        else:
            # reinsert the prescribed degrees of freedom into the solution vector
            self.solution = self.reinsert_the_prescribed_dofs_into_solution_matrix(solution)

        return self.solution

    def compute_frequency_sweep(self, solution, print_log, is_resume):
        self.get_min_max_values_of_pressures.cache_clear()

        # mass and stiffness matrices
        M = self.assembler.mass_matrix
        K = self.assembler.stiffness_matrix

        # damping matrices
        C_imp = self.assembler.damping_matrix
        C_visc = self.assembler.visc_damping_matrix

        # mass flow load vector
        f_Q = self.assembler.mass_flow_vectors

        # frequencies vector [in hertz]
        frequencies = self.assembler.model.frequencies

        # process the prescribed and unprescribed indexes
        self.unprescribed_indexes, self.prescribed_indexes = self.assembler.get_matrices_dropping_indexes()

        # process the prescribed values
        self.prescribed_values, self.array_prescribed_values = self.assembler.get_prescribed_dofs_values()
        frequency_dependent = self.assembler.frequency_dependent
        for i, freq in enumerate(frequencies):
            logging.info(f"Solution step {i + 1} and frequency {freq} Hz [{i + 1}/{len(frequencies)}]")
            
            if is_resume and i != 0 and isinstance(solution, LazyHDF5MatrixWriter) and solution.has_column(i):
                continue

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            # create the frequency vector
            omega = 2 * np.pi * freq

            if i == 0:

                # compute the mass source load vector
                f_Qms = self.assembler.compute_mass_source_load_vector(1)

                # compute the prescribed dofs-related load vector
                f_eq = self.get_prescribed_pressure_model_excitation()

                # compute the load vector f for omega = 1
                f = f_Qms - 1j * f_Q[:, i] - f_eq

                # compose the damping matrix [C]
                C = C_imp + C_visc

                # computes the A matrix for omega = 1
                A = K - M + 1j * C

                is_A_complex = np.any(np.imag(A.data))
                is_f_complex = np.any(np.imag(f)) or np.any(np.imag(f_eq)) or np.any(np.imag(f_Qms))
                is_complex = is_A_complex or is_f_complex

                # initialize the solver based on data types
                linear_solver = initialize_solver(SolverType.PARDISO, is_complex=is_complex, is_symmetric=True)
                del A, f
                if is_resume and isinstance(solution, LazyHDF5MatrixWriter) and solution.has_column(i):
                    continue

            else:

                # update the damping matrix [C]
                self.assembler.assemble_global_damping_matrix_2d_elements(index=i)
                C_imp = self.assembler.damping_matrix
                C = C_imp + C_visc

                if frequency_dependent:

                    # reassemble the global mass and stiffness matrices
                    factor_K, factor_M = self.assembler.compute_global_matrices_factors(index=i)
                    self.assembler.assemble_global_mass_matrix(factor_M)
                    self.assembler.assemble_global_stiffness_matrix(factor_K)

                    M = self.assembler.mass_matrix
                    K = self.assembler.stiffness_matrix

                    # reassemble the mass source matrices
                    self.assembler.assemble_mass_source_matrices_from_surfaces(index=i)
                    self.assembler.assemble_mass_source_matrices_from_volumes(index=i)

                # update the prescribed dofs-related load vector for each frequency step
                f_eq = self.get_prescribed_pressure_model_excitation(index=i)

            # compute the mass source load vector
            f_Qms = self.assembler.compute_mass_source_load_vector(omega, index=i)

            # define the linear system equation terms [A]{x} = {f}
            A = K - (omega**2) * M + 1j * omega * C
            f = f_Qms - 1j * omega * f_Q[:, i] - f_eq

            if not is_complex:
                A.data = np.real(A.data)
                f = np.real(f)

            # convert the symmetric matrix [A] into an upper triangular matrix to enhance the solver's
            # performance and reduce the amount of memory required to compute the solution
            A = triu(A, format="csr")

            # compute the solution for each frequency step
            solution_freq = linear_solver.solve(A, f)
            if isinstance(solution, LazyHDF5MatrixWriter):
                # reinsert the prescribed degrees of freedom into the solution vector
                solution_freq = self.reinsert_the_prescribed_dofs_into_solution_freq(solution_freq, i)

            solution[:, i] = solution_freq

            # clear the memory and delete some variables to reduce the memory usage
            linear_solver.clear_memory()
            del A, f

    def reinsert_the_prescribed_dofs_into_solution_matrix(self, solution: np.ndarray):
        """
        This method reinserts the value of the prescribed degree of freedom in the solution array.

        Parameters
        ----------
        solution : np.ndarray
            Solution data obtained from harmonic analysis using the direct method.

        Returns
        -------
        full_solution: np.ndarray
            An array that contains the solution of all the degrees of freedom.
        """
        rows = solution.shape[0] + len(self.prescribed_indexes)
        cols = solution.shape[1]

        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[self.unprescribed_indexes, :] = solution

        if len(self.prescribed_indexes):
            full_solution[self.prescribed_indexes, :] = self.array_prescribed_values[:, 0:cols]

        return full_solution

    def reinsert_the_prescribed_dofs_into_solution_freq(self, solution: np.ndarray, freq_index: int):
        """
        This method reinserts the value of the prescribed degree of freedom in the solution array.

        Parameters
        ----------
        solution : np.ndarray
            Solution data obtained from harmonic analysis using the direct method.
        freq_index: int
            Frequency index related to the input solution.

        Returns
        -------
        full_solution: np.ndarray
            An array that contains the solution of all the degrees of freedom.
        """
        rows = solution.shape[0] + len(self.prescribed_indexes)

        full_solution = np.zeros(rows, dtype=complex)
        full_solution[self.unprescribed_indexes] = solution

        if len(self.prescribed_indexes):
            full_solution[self.prescribed_indexes] = self.array_prescribed_values[:, freq_index]

        return full_solution

    def get_prescribed_pressure_model_excitation(self, index: int = 0):
        """
        This method computes the equivalent loads resulting from the degrees of freedom 
        prescription to compound the acoustic model excitation vector.

        Parameters
        ----------
        index: int, optional
            An integer values that represents the frequency index.

        Returns
        -------
        F_eq: np.ndarray
            The equivalent acoustic load vector of complex numbers in which
            each column corresponds to a frequency step of analysis.
        """

        if len(self.prescribed_values) == 0:
            return 0.

        frequencies = self.assembler.model.frequencies
        omega = 2 * np.pi * frequencies[index]

        values = self.array_prescribed_values[:, index]

        self.Kr = self.assembler.stiffness_matrix_r
        self.Mr = self.assembler.mass_matrix_r
        self.Cr = self.assembler.damping_matrix_r
        self.Cr_visc = self.assembler.visc_damping_matrix_r

        Kr_add = self.Kr @ values
        Mr_add = self.Mr @ values
        Cr_add = (self.Cr + self.Cr_visc) @ values

        F_Kadd = Kr_add
        F_Madd = -(omega**2) * Mr_add 
        F_Cadd = 1j * omega * Cr_add
        F_eq = F_Kadd + F_Madd + F_Cadd

        return F_eq[self.unprescribed_indexes]


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

        frequencies = self.assembler.model.frequencies
        element_3d = self.assembler.model.acoustic_element_3d

        if element_3d is None:
            self.assembler.define_acoustic_elements()
            element_3d = self.assembler.element_3d
            element_3d.reorder_connect()

        data_normals = self.assembler.model.mesh.get_average_normals_for_surface_nodes(surface_id)
        solid_elements_connected_to_nodes = self.assembler.model.mesh.get_solid_elements_connected_to_nodes(surface_id=surface_id)

        pv_data = dict()

        # Load all frequency solutions to optimize multiple load on the `process_particle_velocity` method below.
        nodal_pressures = self.solution[:, :]
        for node_id, solid_element_ids in solid_elements_connected_to_nodes.items():

            Vk = 0.
            for solid_element_id in solid_element_ids:
                Vk += element_3d.process_particle_velocity(solid_element_id, node_id, rho, frequencies, nodal_pressures)

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


    def get_transmission_loss(self, input_surface_id: int, output_surface_id: int, surface_integration: bool = True):
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

        model = self.assembler.model
        frequencies = self.assembler.model.frequencies

        nodes_input = np.sort(model.mesh.get_nodes_from_surface(input_surface_id))
        nodes_output = np.sort(model.mesh.get_nodes_from_surface(output_surface_id))

        P_in = self.solution[nodes_input, :]
        P_out = self.solution[nodes_output, :]

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
        Zo_in = self.get_surface_impedance(input_surface_id)
        if Zo_in is None:
            return None, None

        Zo_out = self.get_surface_impedance(output_surface_id)
        if Zo_out is None:
            return None, None

        logging.info("Processing the transmission loss... [80/100]")
        (P_downstream, V_downstream) = self.get_downstream_pressure_and_particle_velocity(input_surface_id)
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

            # compute the transmission loss using an alternative surface integration
            # W_in = self.integrate_surface_sound_power_from_nodal_sound_intensity(input_surface_id, I_in)
            # W_out = self.integrate_surface_sound_power_from_nodal_sound_intensity(output_surface_id, I_out)

        transmission_loss = W_in - W_out

        if frequencies[0] == 0:
            frequencies = frequencies[1:]
            transmission_loss = transmission_loss[1:]

        return frequencies, transmission_loss


    def get_surface_impedance(self, surface_id: int) -> float | complex | np.ndarray:
        """
        It returs the acoustic impedance of selected surface.

        Parameter
        ---------
        surface_id: int
            The selected surface ID.

        Returns
        -------
        impedance: np.ndarray, float or None
            The acoustic impedance of selected surface.
        """

        impedance = None
        model = self.assembler.model

        si_data = model.properties._get_property("specific_impedance", surface=surface_id)
        pw_data = model.properties._get_property("incident_plane_wave", surface=surface_id)

        if isinstance(si_data, dict):
            if "real_values" in si_data.keys():
                real_values = np.array(si_data["real_values"])
                imag_values = np.array(si_data["imag_values"])
                impedance = real_values + 1j * imag_values

            elif "anechoic_termination" in si_data.keys():
                rho_eff_pm, C_eff_pm = model.get_porous_material_model_effective_properties(surface_id)
                rho_eff_tv, C_eff_tv = model.get_viscous_thermal_model_effective_properties(surface_id)

                if isinstance(rho_eff_pm, np.ndarray):
                    density = rho_eff_pm
                    speed_of_sound = C_eff_pm

                elif isinstance(rho_eff_tv, np.ndarray):
                    density = rho_eff_tv
                    speed_of_sound = C_eff_tv

                else:

                    fluid = model.properties._get_property("fluid", surface=surface_id)
                    if not isinstance(fluid, Fluid):
                        return None

                    density = fluid.fluid_density
                    speed_of_sound = fluid.speed_of_sound

                impedance = density * speed_of_sound

            elif "values" in si_data.keys():
                impedance = si_data["values"][0]

        elif isinstance(pw_data, dict):
            rho_eff_pm, C_eff_pm = model.get_porous_material_model_effective_properties(surface_id)
            rho_eff_tv, C_eff_tv = model.get_viscous_thermal_model_effective_properties(surface_id)

            if isinstance(rho_eff_pm, np.ndarray):
                density = rho_eff_pm
                speed_of_sound = C_eff_pm

            elif isinstance(rho_eff_tv, np.ndarray):
                density = rho_eff_tv
                speed_of_sound = C_eff_tv

            else:
                fluid = model.properties._get_property("fluid", surface=surface_id)
                if not isinstance(fluid, Fluid):
                    return None

                density = fluid.fluid_density
                speed_of_sound = fluid.speed_of_sound

            impedance = density * speed_of_sound

        return impedance


    def get_downstream_pressure_and_particle_velocity(self, surface_id: int):
        """
        This method computes the downstream pressure and particle velocity
        from the model acoustic excitation.

        Parameters
        ----------
        surface_id: int
            The input surface ID.

        Returns
        -------
        P_downstream: np.ndarray
            The downstream pressure vector or matrix.

        V_downstream: np.ndarray
            The downstream velocity vector or matrix.
        """

        model = self.assembler.model
        frequencies = self.assembler.model.frequencies

        Zo_in = self.get_surface_impedance(surface_id)
        if Zo_in is None:
            return None, None

        pw_data = model.properties._get_property("incident_plane_wave", surface=surface_id)
        sv_data = model.properties._get_property("surface_velocity", surface=surface_id)

        if not (pw_data or sv_data):
            return None, None

        if isinstance(pw_data, dict):
            values = pw_data.get("values")[0]
            _wave_vector = pw_data.get("wave_vector")
            wave_vector = np.array(_wave_vector, dtype=float)

            if isinstance(values, complex | float):
                P_inc = values * np.ones_like(frequencies, dtype=complex)
            else:
                P_inc = values

            node_normals = model.mesh.get_stacked_normals_for_surface_elements(surface_id)
            avg_normal = np.average(node_normals, axis=0).flatten()

            P_downstream = P_inc * (avg_normal @ wave_vector)
            V_downstream = -P_downstream / Zo_in

        if isinstance(sv_data, dict):
            if "real_values" in sv_data.keys():
                real_values = np.array(sv_data["real_values"])
                imag_values = np.array(sv_data["imag_values"])
                V_in = real_values + 1j * imag_values

            elif "values" in sv_data.keys():
                V_in = sv_data["values"]

            P_downstream = V_in * Zo_in / 2
            V_downstream = P_downstream / Zo_in

        return P_downstream, V_downstream


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

        nodes = np.sort(self.assembler.model.mesh.get_nodes_from_surface(surface_id))
        surface_connectivities = self.assembler.model.mesh.get_connectivity_from_surface(surface_id)

        number_nodes = len(nodes)
        map_nodes = dict(zip(nodes, np.arange(number_nodes)))

        if len(pressures.shape) == 1:
            pressures = np.tile(pressures, (number_nodes, 1))

        if len(particle_velocities.shape) == 1:
            particle_velocities = np.tile(particle_velocities, (number_nodes, 1))

        element_2d = self.assembler.element_2d
        if element_2d is None:
            self.assembler.define_acoustic_elements()
            element_2d = self.assembler.element_2d

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


    def integrate_surface_sound_power_from_nodal_sound_intensity(  
                                                                 self, 
                                                                 surface_id: int,
                                                                 sound_intensities: np.ndarray,
                                                                 dB_scale: bool = True
                                                                 ) -> np.ndarray:
        """
        This method integrates the sound power intensity over the selected surface.

        Parameters
        ----------
            surface_id: int
                The identifier of selected surface.

            sound_intensities: np.ndarray
                The acoustic sound intensities from selected suraface.

        Returns
        -------
        sound_power: np.ndarray
            The sound power level in dB if dB_scale is True or the sound power in watts otherwise.
        """

        nodes = np.sort(self.assembler.model.mesh.get_nodes_from_surface(surface_id))
        surface_connectivities = self.assembler.model.mesh.get_connectivity_from_surface(surface_id)

        number_nodes = len(nodes)
        map_nodes = dict(zip(nodes, np.arange(number_nodes)))

        if len(sound_intensities.shape) == 1:
            sound_intensities = np.tile(sound_intensities, (number_nodes, 1))

        element_2d = self.assembler.element_2d
        if element_2d is None:
            self.assembler.define_acoustic_elements()
            element_2d = self.assembler.element_2d

        sound_power = 0.
        for i, e_connect in enumerate(surface_connectivities):
            node_indexes = [map_nodes.get(node) for node in e_connect]
            sound_intensity = sound_intensities[node_indexes, :]
            normalized_data = element_2d.elementary_sound_power_from_sound_intensity(e_connect, sound_intensity)
            sound_power += np.sum(np.real(normalized_data) / 2, axis=0)

        if dB_scale:
            return 10 * np.log10(sound_power / 1e-12)

        return sound_power


    def get_noise_reduction(self, input_surface_id, output_surface_id):
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
        frequencies = self.assembler.model.frequencies
        rows_input = self.assembler.model.mesh.get_nodes_from_surface(input_surface_id)
        rows_output = self.assembler.model.mesh.get_nodes_from_surface(output_surface_id)

        P_in = np.average(self.solution[rows_input,:], axis=0)
        P_out = np.average(self.solution[rows_output,:], axis=0)

        # the zero_shift constant is summed to avoid zero values either in P_input2 or P_output2 variables
        zero_shift = 1e-12

        Prms_out2 = np.real(P_out*np.conjugate(P_out)) / 2 + zero_shift
        Prms_in2 = np.real(P_in*np.conjugate(P_in)) / 2 + zero_shift

        noise_reduction = 10*np.log10(Prms_in2/Prms_out2)

        if frequencies[0] == 0:
            frequencies = frequencies[1:]
            noise_reduction = noise_reduction[1:]

        return frequencies, noise_reduction


    def plot_graph(self, matrix):
        """
        """
        import matplotlib.pyplot as plt
        plt.ion()
        plt.cla()
        plt.spy(matrix, color=(0.25,0.25,0.25))
        plt.show()