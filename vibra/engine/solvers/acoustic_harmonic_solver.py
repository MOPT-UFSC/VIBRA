import logging
import os
import json
import numpy as np
from scipy.sparse.linalg import spsolve
from scipy.sparse import triu
#
# os.environ["OMP_DYNAMIC"] = "FALSE"
# os.environ["OMP_THREAD_LIMIT"] = "8"
# os.environ["OMP_NUM_THREADS"] = "4"
# 

from pypardiso.pardiso_wrapper import PyPardisoSolver

from functools import cache

from vibra.utils.progress_status import ProgressStatus


class AcousticHarmonicSolver:
    def __init__(self, assembler, analysis_data=None):
        #
        self.assembler = assembler
        #
        self.reset_variables()
        self.load_analysis_data(analysis_data)

    def reset_variables(self):
        self.analysis_type = None
        self.frequencies = None
        self.dissipation_model = None
        self.modal_shape = None
        self.solution = None
        self.loads = None

    def load_analysis_data(self, analysis_data):
        if analysis_data is not None:
            if analysis_data["analysis_id"] == 3:
                self.analysis_type = "acoustic"
                if "frequencies" in analysis_data.keys():
                    self.frequencies = analysis_data["frequencies"]

    def load_dissipation_model(self, data):
        self.dissipation_model = data

    @cache
    def get_max_min_values_of_pressures(self, column):
        """ This method returns the minimum and maximum pressure values
            of selected frequency for animation purposes.

            Parameters:
            -----------
            column: int value relative to frequency column index.

            Returns:
            -----------
            p_min, p_max: float values for minimum and maximum pressures,

        """
        data = self.solution[:, column]

        amplitudes = np.abs(data)
        phases = np.angle(data)

        p_min = 1
        p_max = 0
        thetas = np.arange(0, 360, 2) * (np.pi / 180)

        for theta in thetas:
            pressures = amplitudes * np.cos(phases + theta)

            p_min_i = min(pressures)
            p_max_i = max(pressures)

            if p_min_i < p_min:
                p_min = p_min_i
            if p_max_i > p_max:
                p_max = p_max_i

        return p_min, p_max

    def solve(self, print_log=False):
        """ """
        self.get_max_min_values_of_pressures.cache_clear()

        # Note: use mtype=3 for full symmetric complex matrix and mtype=6 for upper triangular complex matrix
        ps = PyPardisoSolver(mtype=6)
        #
        self.unprescribed_indexes, self.prescribed_indexes = self.assembler.get_matrices_dropping_indexes()
        #
        M = self.assembler.mass_matrix
        K = self.assembler.stiffness_matrix
        #
        C_imp = self.assembler.damping_matrix
        C_visc = self.assembler.visc_damping_matrix
        Q = self.assembler.mass_flow_vectors
        Q_visc = self.assembler.Qvisc_damping_matrix*0
        # np.savetxt("mass_flow_vectors.dat", Q)
        #
        # self.plot_graph(M)
        
        condition_1 = self.assembler.model.lrf_properties 
        condition_2 = self.assembler.model.porous_material_properties
        condition_3 = self.assembler.model.viscous_thermal_model_properties

        if condition_1 or condition_2 or condition_3:
            freq_dependent = True
        else:
            freq_dependent = False
            F_eq = self.get_prescribed_pressure_model_excitation()

        rows = K.shape[0]
        cols = len(self.frequencies)
        solution = np.zeros((rows, cols), dtype=complex)
        #
        logging.info( "Solving harmonic analysis..." + ProgressStatus(0, len(self.frequencies)))

        for i, freq in enumerate(self.frequencies):

            message = f"Solution step {i+1} and frequency {freq} Hz"
            logging.info( message + ProgressStatus(i, len(self.frequencies)))

            if print_log:
                print(f"Solution step {i} -> frequency {freq} Hz")
            
            omega = 2 * np.pi * freq

            if freq_dependent:

                self.assembler.assemble_global_mass_matrix(index=i)
                self.assembler.assemble_global_stiffness_matrix(index=i)

                F_eq = self.get_prescribed_pressure_model_excitation(freq_dependent=True, index=i)

                M = self.assembler.mass_matrix
                K = self.assembler.stiffness_matrix

                F = Q_visc @ Q[:, i] - 1j * omega * Q[:, i] - F_eq

            else:

                F = Q_visc @ Q[:, i] - 1j * omega * Q[:, i] - F_eq[:, i]

            C = C_imp[i] + C_visc
            A = K - (omega**2) * M + 1j * omega * C

            A = triu(A, format="csr")
            # ps.factorize(A)

            # solution[:, i] = spsolve(A, F)
            solution[:, i] = ps.solve(A, F)
            ps.free_memory(everything=True)
            del A, F

        self.solution = self._reinsert_prescribed_dofs(solution)

        return self.solution

    def _reinsert_prescribed_dofs(self, solution):
        """
        This method reinsert the value of the prescribed degree of freedom in the solution.

        Parameters
        ----------
        solution : array
            Solution data from the direct method, modal superposition or modal shapes from modal analysis.

        Returns
        ----------
        array
            Solution of all the degrees of freedom.
        """
        rows = solution.shape[0] + len(self.prescribed_indexes)
        cols = solution.shape[1]

        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[self.unprescribed_indexes, :] = solution

        if len(self.prescribed_indexes) > 0:
            full_solution[self.prescribed_indexes, :] = self.array_prescribed_values[:, 0:cols]

        return full_solution
    
    def get_prescribed_pressure_model_excitation(self, freq_dependent=False, index=0):
        """
        This method adds the effects of prescribed acoustic pressure into mass flow global vector.

        Returns
        ----------
        array
            F_eq. Each column corresponds to a frequency of analysis.
        """

        # logging.info("Processing prescribed pressure model excitation..." + ProgressStatus(0, len(self.frequencies)))
        self.prescribed_values, self.array_prescribed_values = self.assembler.get_prescribed_values()
        #
        Kr = (self.assembler.stiffness_matrix_r.toarray())[self.unprescribed_indexes, :]
        Mr = (self.assembler.mass_matrix_r.toarray())[self.unprescribed_indexes, :]
        Cr_visc = (self.assembler.visc_damping_matrix_r.toarray())[self.unprescribed_indexes, :]

        # logging.info( "Processing prescribed pressure model excitation..." + ProgressStatus(10, len(self.frequencies)))

        rows = Kr.shape[0]
        if freq_dependent:
            cols = 1
            F_eq = np.zeros(rows, dtype=complex)
        else:
            cols = len(self.frequencies)
            F_eq = np.zeros((rows,cols), dtype=complex)

        nf = len(self.frequencies)
        aux_ones = np.ones(nf, dtype=complex)

        if len(self.prescribed_values) != 0:

            # list_prescribed_values = list()

            # for value in self.prescribed_values:
            #     if isinstance(value, complex):
            #         list_prescribed_values.append(aux_ones*value)
            #     elif isinstance(value, np.ndarray):
            #         list_prescribed_values.append(value)
      
            # self.array_prescribed_values = np.array(list_prescribed_values)

            if freq_dependent:
                # logging.info("Processing prescribed pressure model excitation..." + ProgressStatus(index + 10, len(self.frequencies) + 10))

                Cr = (self.assembler.damping_matrix_r[index].toarray())[self.unprescribed_indexes, :]
                #
                Kr_add = np.sum((Kr * self.array_prescribed_values[:, index]), axis=1)
                Mr_add = np.sum((Mr * self.array_prescribed_values[:, index]), axis=1)
                Cr_add = np.sum(((Cr + Cr_visc) * self.array_prescribed_values[:, index]), axis=1)
                #
                omega = 2*np.pi*self.frequencies[index]
                F_Kadd = Kr_add
                F_Madd = (-(omega**2))*Mr_add 
                F_Cadd = 1j*omega*Cr_add
                F_eq = F_Kadd + F_Madd + F_Cadd
            
            else:
               
                for i, freq in enumerate(self.frequencies):
                    #
                    logging.info("Processing prescribed pressure model excitation..." + ProgressStatus(i + 10, len(self.frequencies) + 10))

                    Cr = (self.assembler.damping_matrix_r[i].toarray())[self.unprescribed_indexes, :]
                    #
                    Kr_add = np.sum((Kr * self.array_prescribed_values[:, i]), axis=1)
                    Mr_add = np.sum((Mr * self.array_prescribed_values[:, i]), axis=1)
                    Cr_add = np.sum(((Cr + Cr_visc) * self.array_prescribed_values[:, i]), axis=1)
                    #
                    omega = 2*np.pi*freq
                    F_Kadd = Kr_add
                    F_Madd = (-(omega**2))*Mr_add 
                    F_Cadd = 1j*omega*Cr_add
                    F_eq[:, i] = F_Kadd + F_Madd + F_Cadd

                logging.info("Processing prescribed pressure model excitation..." + ProgressStatus(100, 100))

        return F_eq


    def get_particle_velocity_from_surface(self, surface_id: int, rho: float | np.ndarray):
        """ Process the nodal average particle velocity to selected surface.
            Returns the partcicle velocity in components x, y, z and normal
        """

        element_3d, element_2d = self.assembler.get_element()
        element_3d.reorder_connect()

        node_ids = self.assembler.model.mesh.nodes_from_surfaces[surface_id]
        solid_elements_connected_to_nodes = self.assembler.model.mesh.get_solid_elements_connected_to_nodes(node_ids)
        face_elements_connected_to_nodes = self.assembler.model.mesh.get_face_elements_connected_to_nodes(node_ids, surface_id)

        # fluid = self.assembler.model.properties.get_fluid(surface=surface_id)
        # rho = fluid.fluid_density

        data_vp = dict()
        data_normals = dict()

        for node_id, solid_element_ids in solid_elements_connected_to_nodes.items():

            n = 0.
            face_elem_connect = face_elements_connected_to_nodes[node_id, surface_id]

            for face_connect in face_elem_connect:
                n += element_2d.get_element_face_normal(face_connect)
                # print(node_id, face_connect, element_2d.get_element_face_normal(face_connect))

            data_normals[node_id] = n / len(face_elem_connect)
            # print(node_id, len(face_elem_connect),  data_normals[node_id])

            Vk = 0.
            for solid_element_id in solid_element_ids:
                Vk += element_3d.process_particle_velocity(solid_element_id, node_id, rho, self.frequencies, self.solution)

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

        return particle_velocities


    def get_transmission_loss(self, input_surface_id, output_surface_id):
        """ Returns the transmission loss.
        
        """
        
        nodes_input = self.assembler.model.mesh.nodes_from_surfaces[input_surface_id]
        nodes_output = self.assembler.model.mesh.nodes_from_surfaces[output_surface_id]

        nodes_input = np.sort(nodes_input)
        nodes_output = np.sort(nodes_output)

        P_in = self.solution[nodes_input, :]
        P_out = self.solution[nodes_output, :]

        volume_out = self.assembler.model.mesh.volume_from_surface[output_surface_id][0]
        volume_in = self.assembler.model.mesh.volume_from_surface[input_surface_id][0]

        fluid_out, _ = self.assembler.model.get_fluid(volume=volume_out)
        fluid_in, _ = self.assembler.model.get_fluid(volume=volume_in)

        rho_out = fluid_out.fluid_density
        c0_out = fluid_out.speed_of_sound

        rho_in = fluid_in.fluid_density
        c0_in = fluid_in.speed_of_sound

        A_in = self.assembler.model.mesh.surface_area_from_element_integration[input_surface_id]
        A_out = self.assembler.model.mesh.surface_area_from_element_integration[output_surface_id]

        # print(f"A_in: {A_in} [m²]")
        # print(f"A_out: {A_out} [m²]")

        logging.info("Processing the transmission loss..." + ProgressStatus(40, 100))

        out_data = dict()
        list_nodes_in = list()
        nodal_areas_in = np.zeros(len(nodes_input), dtype=float)
        for i, node in enumerate(nodes_input):
            areas = self.assembler.model.mesh.nodal_area[node]
            nodal_areas_in[i] = sum(areas)
            out_data[node] = sum(areas)
            # print("input: ", i, node)
            list_nodes_in.append(node)

        list_nodes_out = list()
        nodal_areas_out = np.zeros(len(nodes_output), dtype=float)
        for i, node in enumerate(nodes_output):
            areas = self.assembler.model.mesh.nodal_area[node]
            nodal_areas_out[i] = sum(areas)
            out_data[node] = sum(areas)
            # print("output: ", i, node)
            list_nodes_out.append(node)

        # with open("areas_data.json", "w") as file:
        #     json.dump(out_data, file, indent=2)

        # print("\n")
        # for i in [177, 178, 8818]:
        #     ratio = out_data[i] / np.sum(nodal_areas_in)
        #     print(f"Node #{i+1} - area: {ratio*A_in} [m²]")

        # print("\n")
        # for i in [340, 341, 8904]:
        #     ratio = out_data[i] / np.sum(nodal_areas_out)
        #     print(f"Node #{i+1} - area: {ratio*A_out} [m²]")

        Aeff_in = nodal_areas_in.reshape(-1, 1) * (A_in / np.sum(nodal_areas_in))
        Aeff_out = nodal_areas_out.reshape(-1, 1) * (A_out / np.sum(nodal_areas_out))

        input_rho = self.assembler.model.get_fluid_density_for_particle_velocity_calculation(input_surface_id, self.frequencies)
        if input_rho is None:
            return np.zeros_like(self.frequencies, dtype=complex)

        output_rho = self.assembler.model.get_fluid_density_for_particle_velocity_calculation(output_surface_id, self.frequencies)
        if output_rho is None:
            return np.zeros_like(self.frequencies, dtype=complex)

        logging.info("Processing the transmission loss..." + ProgressStatus(50, 100))
        input_particle_velocities = self.get_particle_velocity_from_surface(input_surface_id, input_rho)

        logging.info("Processing the transmission loss..." + ProgressStatus(90, 100))
        output_particle_velocities = self.get_particle_velocity_from_surface(output_surface_id, output_rho)

        # Transmission loss
        surf_velocity = self.assembler.model.properties.get_surface_velocity(input_surface_id)
        if surf_velocity is None:
            return None, None, None

        real_values = np.array(surf_velocity["real_values"])
        imag_values = np.array(surf_velocity["imag_values"])
        V_in = real_values + 1j * imag_values

        P_in = V_in * rho_in * c0_in / 4
        I_in = np.abs(np.real(P_in * np.conjugate(V_in)) / 2)

        # V_in = np.array(list(input_particle_velocities["Vn"].values()), dtype=complex)
        # I_in = -np.real(P_in * np.conjugate(V_in)) / 2

        V_out = np.array(list(output_particle_velocities["Vn"].values()), dtype=complex)
        I_out = np.real(P_out * np.conjugate(V_out)) / 2

        # Vx = np.array(list(input_particle_velocities["Vx"].values()), dtype=complex)
        # print(np.array([np.average(V_in, axis=0), np.average(Vx, axis=0)]).T)

        # print(f"I_in: {np.average(I_in, axis=0)}")
        # print(f"I_out: {np.average(I_out, axis=0)}")
        # I_in_out = np.array([np.average(I_in, axis=0), np.average(I_out, axis=0)], dtype=float).T
        # print(f"Sound intensities: {I_in_out}")

        W_in = 10*np.log10(np.sum(I_in * Aeff_in, axis=0))
        W_out = 10*np.log10(np.sum(I_out * Aeff_out, axis=0))

        TL = W_in - W_out

        diff = 10*np.log10(np.sum(I_out * Aeff_out, axis=0)) - 10*np.log10(np.sum(I_out * A_out/len(nodes_output), axis=0))

        if self.frequencies[0] == 0:
            return self.frequencies[1:], TL[1:], diff[1:]
        else:
            return self.frequencies, TL, diff

    def get_noise_reduction(self, input_surface_id, output_surface_id):
        """ Returns the transmission loss.

        """

        rows_input = self.assembler.model.mesh.nodes_from_surfaces[input_surface_id]
        rows_output = self.assembler.model.mesh.nodes_from_surfaces[output_surface_id]

        P_in = np.average(self.solution[rows_input,:], axis=0)
        P_out = np.average(self.solution[rows_output,:], axis=0)

        # the zero_shift constant is summed to avoid zero values either in P_input2 or P_output2 variables
        zero_shift = 1e-12

        Prms_out2 = np.real(P_out*np.conjugate(P_out)) / 2 + zero_shift
        Prms_in2 = np.real(P_in*np.conjugate(P_in)) / 2 + zero_shift

        NR = 10*np.log10(Prms_in2/Prms_out2)

        if 0 in self.frequencies:
            return self.frequencies[1:], NR[1:]

        return self.frequencies, NR


    def plot_graph(self, matrix):
        """
        """
        import matplotlib.pyplot as plt
        plt.ion()
        plt.cla()
        plt.spy(matrix, color=(0.25,0.25,0.25))
        plt.show()