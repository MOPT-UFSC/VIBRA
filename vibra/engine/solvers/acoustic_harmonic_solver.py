
from vibra.engine.solvers.linear_solver import SolverType, initialize_solver
from vibra.engine import AnalysisID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler

import logging
import numpy as np

from functools import cache
from scipy.sparse import triu
from time import time

class AcousticHarmonicSolver:
    def __init__(self, assembler: "AcousticAssembler", **kwargs):
        self.assembler = assembler
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


    def solve(self, print_log: bool = False):
        """ 
        This method solves the acoustic harmonic analysis using the
        direct method for both damped and undamped problems.

        Parameter
        ---------
        print_log: bool, optional
            This argument controls the printing of the solution steps to the terminal.
        """

        logging.info(f"Solving harmonic analysis (direct method)... [10/100]")

        self.get_min_max_values_of_pressures.cache_clear()

        # mass and stiffness matrices
        M = self.assembler.mass_matrix
        K = self.assembler.stiffness_matrix

        # damping matrices
        C_imp = self.assembler.damping_matrix
        C_visc = self.assembler.visc_damping_matrix
        
        # mass flow load vector
        Q = self.assembler.mass_flow_vectors

        # the viscous-related source term is temporary disabled
        Q_visc = self.assembler.Qvisc_damping_matrix * 0
        
        is_pm_active = self.assembler.model.porous_material_properties
        is_vt_active = self.assembler.model.viscous_thermal_model_properties

        # frequencies vector [in hertz]
        frequencies = self.assembler.model.frequencies

        # process the prescribed and unprescribed indexes
        self.unprescribed_indexes, self.prescribed_indexes = self.assembler.get_matrices_dropping_indexes()

        # process the prescribed values
        self.prescribed_values, self.array_prescribed_values = self.assembler.get_prescribed_dofs_values()

        rows = K.shape[0]
        cols = len(frequencies)
        solution = np.zeros((rows, cols), dtype=complex)

        frequency_dependent = is_pm_active or is_vt_active

        for i, freq in enumerate(frequencies):

            logging.info(f"Solution step {i+1} and frequency {freq} Hz [{i}/{len(frequencies)}]")

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")

            # create the frequency vector
            omega = 2 * np.pi * freq

            # define the damping matrix [C]
            C = C_imp + C_visc

            if i == 0:

                # define the prescribed dofs-related load vector
                F_eq = self.get_prescribed_pressure_model_excitation()

                # computes the load vector F for omega = 1
                F = Q_visc @ Q[:, i] - 1j * Q[:, i] - F_eq

                # computes the A matrix for omega = 1
                A = K - M + 1j * C

                is_A_complex = np.any(np.imag(A.data))
                is_F_complex = np.any(np.imag(F)) or np.any(np.imag(F_eq))
                is_complex = is_A_complex or is_F_complex

                # initialize the solver based on data types
                linear_solver = initialize_solver(SolverType.PARDISO, is_complex=is_complex, is_symmetric=True)
                del A, F

            else:
                self.assembler.assemble_global_damping_matrix_2d_elements(index=i)
                C_imp = self.assembler.damping_matrix

                if frequency_dependent:
                    self.assembler.assemble_global_mass_matrix(index=i)
                    self.assembler.assemble_global_stiffness_matrix(index=i)
                    M = self.assembler.mass_matrix
                    K = self.assembler.stiffness_matrix

                # update the prescribed dofs-related load vector for each frequency step
                F_eq = self.get_prescribed_pressure_model_excitation(index=i, matrices_updated=frequency_dependent)

            A = K - (omega**2) * M + 1j * omega * C
            F = Q_visc @ Q[:, i] - 1j * omega * Q[:, i] - F_eq

            if not is_complex:
                A.data = np.real(A.data)
                F = np.real(F)

            # convert the symmetric matrix [A] into an upper triangular matrix to enhance the solver's
            # performance and reduce the amount of memory required to compute the solution
            A = triu(A, format="csr")

            # compute the solution for each frequency step
            solution[:, i] = linear_solver.solve(A, F)

            # clear the memory and delete some variables to reduce the memory usage
            linear_solver.clear_memory()
            del A, F

        logging.info(f"Solving harmonic analysis (direct method)... [99/100]")

        # reinsert the prescribed degrees of freedom into the solution vector
        self.solution = self.reinsert_the_prescribed_degrees_of_freedoom(solution)

        return self.solution


    def reinsert_the_prescribed_degrees_of_freedoom(self, solution: np.ndarray):
        """
        This method reinsert the value of the prescribed degree of freedom in the solution array.

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


    def get_prescribed_pressure_model_excitation(self, index: int = 0, matrices_updated: bool = False):
        """
        This method computes the equivalent loads resulting from the degrees of freedom 
        prescription to compound the acoustic model excitation vector.

        Parameters
        ----------
        index: int, optional
            An integer values that represents the frequency index.
        
        matrices_updated: bool, optional
            Controls when the sliced matrices will be updated.

        Returns
        -------
        F_eq: np.ndarray
            The equivalent acoustic load vector of complex numbers in which
            each column corresponds to a frequency step of analysis.
        """

        if len(self.prescribed_values) == 0:
            return 0.

        if index == 0 or matrices_updated:
            self.Kr = (self.assembler.stiffness_matrix_r.toarray())[self.unprescribed_indexes, :]
            self.Mr = (self.assembler.mass_matrix_r.toarray())[self.unprescribed_indexes, :]
            self.Cr = (self.assembler.damping_matrix_r.toarray())[self.unprescribed_indexes, :]
            self.Cr_visc = (self.assembler.visc_damping_matrix_r.toarray())[self.unprescribed_indexes, :]

        Kr_add = np.sum((self.Kr * self.array_prescribed_values[:, index]), axis=1)
        Mr_add = np.sum((self.Mr * self.array_prescribed_values[:, index]), axis=1)
        Cr_add = np.sum(((self.Cr + self.Cr_visc) * self.array_prescribed_values[:, index]), axis=1)

        frequencies = self.assembler.model.frequencies
        omega = 2 * np.pi * frequencies[index]

        F_Kadd = Kr_add
        F_Madd = -(omega**2) * Mr_add 
        F_Cadd = 1j * omega * Cr_add
        F_eq = F_Kadd + F_Madd + F_Cadd

        return F_eq


    def get_particle_velocity_from_surface(self, surface_id: int, rho: float | np.ndarray, TL=False):
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
        element_3d, element_2d = self.assembler.get_element()
        element_3d.reorder_connect()

        node_ids = self.assembler.model.mesh.nodes_from_surfaces[surface_id]
        solid_elements_connected_to_nodes = self.assembler.model.mesh.get_solid_elements_connected_to_nodes(node_ids)
        face_elements_connected_to_nodes = self.assembler.model.mesh.get_face_elements_connected_to_nodes(node_ids, surface_id)

        data_vp = dict()
        data_normals = dict()

        for node_id, solid_element_ids in solid_elements_connected_to_nodes.items():

            if TL:
                face_elem_connect = self.assembler.model.mesh.face_elements_connected_to_nodes[node_id]
            else:
                face_elem_connect = face_elements_connected_to_nodes[node_id, surface_id]

            n = 0.
            for face_connect in face_elem_connect:
                n += element_2d.get_element_face_normal(face_connect)
                # print(node_id, face_connect, element_2d.get_element_face_normal(face_connect))

            data_normals[node_id] = n / len(face_elem_connect)
            # print(node_id, len(face_elem_connect),  data_normals[node_id])

            Vk = 0.
            for solid_element_id in solid_element_ids:
                Vk += element_3d.process_particle_velocity(solid_element_id, node_id, rho, frequencies, self.solution)

            data_vp[node_id] = Vk / len(solid_element_ids)

        Vx = dict()
        Vy = dict()
        Vz = dict()
        Vn = dict()
        particle_velocities = dict()

        ordered_nodes = np.sort(list(data_vp.keys()))

        for i, _node_id in enumerate(ordered_nodes):
            Vx[_node_id] = data_vp[_node_id][0, :]
            Vy[_node_id] = data_vp[_node_id][1, :]
            Vz[_node_id] = data_vp[_node_id][2, :]
            Vn[_node_id] = data_vp[_node_id].T @ data_normals[_node_id]

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


    def get_transmission_loss(self, input_surface_id: int, output_surface_id: int):
        """ 
        This method compute the acoustic transmission loss between two selected surfaces.

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

        transmission_loss: np.ndarray
            The vector of computed transmission loss values in dB.

        """

        model = self.assembler.model
        frequencies = self.assembler.model.frequencies

        nodes_input = model.mesh.nodes_from_surfaces[input_surface_id]
        nodes_output = model.mesh.nodes_from_surfaces[output_surface_id]

        nodes_input = np.sort(nodes_input)
        nodes_output = np.sort(nodes_output)

        P_in = self.solution[nodes_input, :]
        P_out = self.solution[nodes_output, :]

        # volume_out = model.mesh.volumes_from_surface[output_surface_id][0]
        # volume_in = model.mesh.volumes_from_surface[input_surface_id][0]

        # fluid_out, _ = model.properties._get_property("fluid", volume=volume_out)
        # fluid_in, _ = model.properties._get_property("fluid", volume=volume_in)

        # rho_out = fluid_out.fluid_density
        # c0_out = fluid_out.speed_of_sound

        # rho_in = fluid_in.fluid_density
        # c0_in = fluid_in.speed_of_sound

        A_in = model.mesh.surface_area_from_element_integration[input_surface_id]
        A_out = model.mesh.surface_area_from_element_integration[output_surface_id]

        # print(f"A_in: {A_in} [m²]")
        # print(f"A_out: {A_out} [m²]")

        logging.info("Processing the transmission loss... [40/100]")

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
        # np.savetxt(f"nodal_areas_surface_{output_surface_id}.dat", _nodal_areas_out, fmt=["%i", "%.16f"], delimiter=",", header="Node index || Nodal area [m2]")

        Aeff_in = nodal_areas_in.reshape(-1, 1) * (A_in / np.sum(nodal_areas_in))
        Aeff_out = nodal_areas_out.reshape(-1, 1) * (A_out / np.sum(nodal_areas_out))

        rho_in = model.get_fluid_density_for_particle_velocity_calculation(input_surface_id, frequencies)
        if rho_in is None:
            return None, None

        rho_out = model.get_fluid_density_for_particle_velocity_calculation(output_surface_id, frequencies)
        if rho_out is None:
            return None, None

        logging.info("Processing the transmission loss... [50/100]")
        input_pv_data = self.get_particle_velocity_from_surface(input_surface_id, rho_in)

        logging.info("Processing the transmission loss... [90/100]")
        output_pv_data = self.get_particle_velocity_from_surface(output_surface_id, rho_out)

        # Transmission loss
        surf_velocity = model.properties._get_property("surface_velocity", surface=input_surface_id)
        if isinstance(surf_velocity, dict):
            if "real_values" in surf_velocity.keys():
                real_values = np.array(surf_velocity["real_values"])
                imag_values = np.array(surf_velocity["imag_values"])
                V_in = real_values + 1j * imag_values

            elif "values" in surf_velocity.keys():
                V_in = surf_velocity["values"]

        else:
            return None, None

        specific_impedance = model.properties._get_property("specific_impedance", surface=input_surface_id)
        if isinstance(specific_impedance, dict):
            if "real_values" in specific_impedance.keys():
                real_values = np.array(specific_impedance["real_values"])
                imag_values = np.array(specific_impedance["imag_values"])
                Zo_in = real_values + 1j * imag_values

            elif "anechoic_termination" in specific_impedance.keys():

                pm_active, rho_eff_pm, C_eff_pm = model.is_porous_material_model_active(input_surface_id)
                tv_active, rho_eff_tv, C_eff_tv = model.is_viscous_thermal_model_active(input_surface_id)

                if pm_active:
                    density = rho_eff_pm
                    speed_of_sound = C_eff_pm

                elif tv_active:
                    density = rho_eff_tv
                    speed_of_sound = C_eff_tv

                else:
                    fluid = model.properties._get_property("fluid", surface=input_surface_id)
                    density = fluid.fluid_density
                    speed_of_sound = fluid.speed_of_sound

                Zo_in = density * speed_of_sound

            elif "values" in surf_velocity.keys():
                Zo_in = specific_impedance["values"]

        else:
            return None, None

        ## INPUT SOUND INTENSITY CALCULATION

        P_downstream = V_in * Zo_in / 2
        V_downstream = P_downstream / Zo_in
        I_in = np.abs(np.real(P_downstream * np.conjugate(V_downstream)) / 2)

        # V_in = -np.array(list(input_pv_data["Vn"].values()), dtype=complex)
        # P_downstream = (P_in + Zo_in * V_in) / 2
        # V_downstream = P_downstream / Zo_in
        # I_in = np.real(P_downstream * np.conjugate(V_downstream)) / 2

        ## OUTPUT SOUND INTENSITY CALCULATION

        V_out = np.array(list(output_pv_data["Vn"].values()), dtype=complex)
        I_out = np.real(P_out * np.conjugate(V_out)) / 2

        # Aeff_in = A_in * np.ones((len(nodes_input), 1), dtype=float) / len(nodes_input)
        # Aeff_out = A_out * np.ones((len(nodes_output), 1), dtype=float) / len(nodes_output)

        W_in = 10 * np.log10(np.sum(I_in * Aeff_in, axis=0))
        W_out = 10 * np.log10(np.sum(I_out * Aeff_out, axis=0))

        transmission_loss = W_in - W_out

        if frequencies[0] == 0:
            frequencies = frequencies[1:]
            transmission_loss = transmission_loss[1:]

        return frequencies, transmission_loss


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
        rows_input = self.assembler.model.mesh.nodes_from_surfaces[input_surface_id]
        rows_output = self.assembler.model.mesh.nodes_from_surfaces[output_surface_id]

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