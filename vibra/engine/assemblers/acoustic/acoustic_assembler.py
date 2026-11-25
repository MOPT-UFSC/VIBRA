import logging
import sys
from time import perf_counter

import numpy as np
from scipy.sparse import block_array, coo_matrix, csr_matrix
from tqdm import tqdm

from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.engine.assemblers.acoustic.acoustic_excitations_assembler import AcousticExcitationsAssembler
from vibra.engine.assemblers.acoustic.acoustic_impedances_assembler import AcousticImpedancesAssembler
from vibra.engine.model import Model
from vibra.engine.properties.fluid import Fluid


class AcousticAssembler:
    def __init__(self, model : Model):

        self.model = model
        self.properties = model.properties

        self.reset()

        self.excitations_assembler = AcousticExcitationsAssembler(self)
        self.impedances_assembler = AcousticImpedancesAssembler(self)


    def reset(self):

        self.frequencies = None
        self.frequency_dependent = False

        self.number_frequencies = 1
        self.prescribed_values = np.array([])
        self.prescribed_dof_indices = None
        self.unprescribed_dof_indices = None
        self.fluid_properties_from_volume = {}

        self.element_1d = None
        self.element_2d = None
        self.element_3d = None

        # global matrices and excitation vector
        self.reset_global_matrices_attributes()
        self.reset_reduced_matrices_attributes()


    def reset_global_matrices_attributes(self):
        self.rows = None
        self.cols = None
        self.int3d_NtN = None
        self.int3d_BtB = None
        self.mass_matrix = None
        self.stiffness_matrix = None

        self.damping_matrix_2d = None
        self.damping_matrix_3d: None
        self.visc_load_matrix: None


    def reset_reduced_matrices_attributes(self):
        self.mass_matrix_r = None
        self.stiffness_matrix_r = None
        self.damping_matrix_r = None


    @property
    def number_3d_elements(self):
        return self.model.domains_processor.number_3d_acoustic_elements


    @property
    def acoustic_dofs_indices(self):
        return self.model.domains_processor.acoustic_dofs_indices


    def define_acoustic_elements(self):
        self.model.set_acoustic_elements()
        self.element_1d = self.model.acoustic_element_1d
        self.element_2d = self.model.acoustic_element_2d
        self.element_3d = self.model.acoustic_element_3d


    def update_number_of_frequencies(self):
        analysis_setup = self.model.analysis_setup
        if isinstance(analysis_setup, HarmonicAnalysisSetup):
            self.frequencies = analysis_setup.get_frequencies()
            self.number_frequencies = len(self.frequencies)

        else:
            self.frequencies = None
            self.number_frequencies = 1

    def is_assembled(self):
        return (self.stiffness_matrix is not None) and (self.mass_matrix is not None)


    def process_prescribed_dof_values(self):
        """
        This method returns all the values of the acoustic degrees of freedom with prescribed pressure boundary conditions.

        Returns
        -------
        array
            Values of the acoustic degrees of freedom with prescribed pressure boundary conditions.

        See also
        --------
        process_prescribed_indices : Indexes of the acoustic degrees of freedom with prescribed pressure boundary conditions.

        process_unprescribed_indices : Indexes of the acoustic free degrees of freedom.
        """

        prescribed_dof_values = []

        aux_ones = np.ones(self.number_frequencies, dtype=np.complex128)

        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property != "acoustic_pressure":
                continue

            if "values" in data:
                complex_values = data["values"]

            else:
                real_values = np.array(data["real_values"])
                imag_values = np.array(data["imag_values"])
                complex_values = real_values + 1j * imag_values

            nodes = self.model.mesh.get_nodes_from_surface(surface_id)
            if nodes is None:
                continue

            for _ in nodes:
                for _complex_values in complex_values:
                    if isinstance(_complex_values, np.ndarray):
                        _values = _complex_values[self.model.solution_steps_mask]
                    else:
                        _values = _complex_values

                    prescribed_dof_values.append(_values)

        # TODO: implement same structure for lines
        # TODO: refactor this method

        prescribed_dof = []

        for value in prescribed_dof_values:
            if isinstance(value, complex):
                prescribed_dof.append(aux_ones * value)
            elif isinstance(value, np.ndarray):
                if len(value) == 1:
                    prescribed_dof.append(aux_ones * value)
                else: 
                    prescribed_dof.append(value[0:self.number_frequencies])

        self.prescribed_values = np.array(prescribed_dof)


    def process_prescribed_indices(self):
        """
        Returns the prescribed dof indices.
        """
        prescribed_dof_indices = []
        for key in self.properties.surface_properties:
            property, surface_id = key
            if property != "acoustic_pressure":
                continue

            nodes = self.model.mesh.get_nodes_from_surface(surface_id)
            if nodes is None:
                continue

            global_dofs = self.model.get_dof_indices_from_nodes(nodes, "acoustic")
            prescribed_dof_indices.extend(global_dofs[:, 0])

        self.prescribed_dof_indices = prescribed_dof_indices


    def process_unprescribed_indices(self):
        """ 
        Returns the unprescribed dof indices.
        """
        all_indices = np.arange(self.model.domains_processor.total_act_dofs, dtype=np.int32)
        self.unprescribed_dof_indices = np.delete(all_indices, self.prescribed_dof_indices)


    def process_dofs_indices(self):
        self.process_prescribed_indices()
        self.process_unprescribed_indices()
        self.process_prescribed_dof_values()


    def get_fluid_properties_from_surface(self, surface_id: int):

        volumes_from_surface = self.model.mesh.volumes_from_surface[surface_id]
        if len(volumes_from_surface) != 1:
            return None, None
        
        volume_id = volumes_from_surface[0]
        pm_properties = self.model.porous_material_properties.get(volume_id)
        vt_properties = self.model.viscous_thermal_model_properties.get(volume_id)

        if isinstance(pm_properties, dict):
            density = pm_properties.get("rho_eff")
            speed_of_sound = pm_properties.get("C_eff")

        elif isinstance(vt_properties, dict):
            density = vt_properties.get("rho_eff")
            speed_of_sound = vt_properties.get("C_eff")

        else:
            fluid = self.model.properties._get_property("fluid", volume=volume_id)
            if not isinstance(fluid, Fluid):
                return None, None

            proportional_damping = self.model.properties._get_property("proportional_damping", volume=volume_id)
            density = self.properties.get_fluid_density(fluid, proportional_damping)
            speed_of_sound = self.properties.get_speed_of_sound(fluid, proportional_damping)

        return density, speed_of_sound


    def get_value_in_array_form(
            self, 
            value: float | np.ndarray, 
            ravel: bool = False, 
            filter_frequencies: bool=True,
            ) -> np.ndarray:
        """
        This method returns, for a given input value, an output vector with 
        the same length as the frequencies vector.

        Parameters
        ----------
        value: float or np.ndarray
            The input value to be converted in array with
            the same length as the frequencies vector.
        
        ravel: bool, optional
            Controls whether the output vector will be flattened or not.

        Returns
        -------
        output_vector: np.ndarray
            The output vector with the same length as the frequencies
            vector.
        """

        aux_ones = np.ones((1, self.number_frequencies), dtype=np.complex128)

        if isinstance(value, complex | float):
            output_vector = value * aux_ones

        elif isinstance(value, np.ndarray):
            if value.shape[0] == 1:
                output_vector = value * aux_ones

            elif len(value.shape) == 1:
                output_vector = value.reshape(1, -1)

            else:
                output_vector = value

        if filter_frequencies:
            # filter values based on the solution steps mask
            if output_vector.shape[1] - self.number_frequencies:
                if self.model.solution_steps_mask:
                    output_vector = output_vector[:, self.model.solution_steps_mask]

        return output_vector.ravel() if ravel else output_vector


    def compute_data_to_assemble_global_matrices(self, reorder: bool = True):
        """ 
        This method processes the data required to assemble the global matrices
        based on the stacked elementary matrices.

        Parameters
        ----------
        reorder: bool, optional
            Control when the connectivity matrix will be reordered.
        """

        self.rows, self.cols, _ = self.element_3d.generate_ind_rows_cols(reorder=reorder)

        logging.info("Processing the elementary matrices data... [25/100]")
        self.int3d_BtB, self.int3d_NtN = self.element_3d.stacked_elementary_matrices_NtN_BtB()

        if self.model.stop_processing:
            return True

        logging.info("Processing the elementary matrices data... [85/100]")
        self.fluid_properties_from_volume, self.frequency_dependent = self.model.map_fluid_properties_to_volumes()

        logging.info("Processing the elementary matrices data... [95/100]")
        self.process_dofs_indices()

        if self.model.reduced_memory_mode:
            self.write_global_matrices_array_data()


    def compute_data_to_assemble_global_matrices_using_loop(self, reorder: bool = True):
        """ 
        This method processes the data required to assemble the global matrices
        sweeping all solid elements.

        Parameters
        ----------
        reorder: bool, optional
            Control when the connectivity matrix will be reordered.
        """

        dof = self.element_3d.dof_per_element
        self.int3d_BtB = np.zeros((self.number_3d_elements, dof, dof), dtype=np.complex128)
        self.int3d_NtN = np.zeros((self.number_3d_elements, dof, dof), dtype=np.complex128)

        self.rows, self.cols, _ = self.element_3d.generate_ind_rows_cols(reorder=reorder)

        last_progress = 0
        for index, element_id in enumerate(self.model.domains_processor.elements_of_domain.get("acoustic", [])):

            if self.model.stop_processing:
                return True

            progress = int(100 * (index / self.number_3d_elements))
            if progress != last_progress:
                logging.info(f"Processing the elementary matrices data... [{progress}/100]")

            last_progress = progress

            Ke, Me = self.element_3d.elementary_matrices(element_id)
            self.int3d_BtB[index, :, :] = Ke
            self.int3d_NtN[index, :, :] = Me

        logging.info("Processing the elementary matrices data... [85/100]")
        self.fluid_properties_from_volume, self.frequency_dependent = self.model.map_fluid_properties_to_volumes()

        logging.info("Processing the elementary matrices data... [95/100]")
        self.process_dofs_indices()

        if self.model.reduced_memory_mode:
            self.write_global_matrices_array_data()


    def compute_global_matrices_factors(self, index: int = 0):
        """
        This method calculates the global mass and stiffness matrix factors.

        Parameters
        ----------
        index: int, optional
            The frequency index.

        Returns
        -------
        factor_K: np.ndarray
            The global stiffness matrix factor.

        factor_M: np.ndarray
            The global mass matrix factor.
        """

        factor_K = np.zeros(self.number_3d_elements, complex)
        factor_M = np.zeros(self.number_3d_elements, complex)

        factor_Cvisc = np.zeros(self.number_3d_elements, complex)
        factor_fvisc = np.zeros(self.number_3d_elements, complex)

        for vol_id in self.model.domains_processor.volumes_of_domain.get("acoustic", []):

            fluid_data = self.fluid_properties_from_volume.get(vol_id)
            if not isinstance(fluid_data, dict):
                continue

            rho_f = fluid_data.get("rho_f")[index]
            C_f = fluid_data.get("C_f")[index]
            mu_0 = fluid_data.get("mu_0")
            rho_0 = fluid_data.get("rho_0")
            C_0 = fluid_data.get("C_0")

            # 3D elements of the volume
            element_ids = self.model.mesh.elements_from_volume.get(vol_id)

            # auxiliar vector
            aux_ones = np.ones(len(element_ids), dtype=float)

            # convert the element indices
            _element_ids = self.model.domains_processor.acoustic_elements_mapping[element_ids]

            factor_K[_element_ids] = aux_ones / (rho_f)
            factor_M[_element_ids] = aux_ones / (rho_f * C_f**2)
            factor_Cvisc[_element_ids] = ((4 * mu_0) / (3 * ((rho_0 * C_0)**2)))
            factor_fvisc[_element_ids] = ((4 * mu_0) / (3 * (rho_0**2)))

        factor_K = factor_K.reshape(-1, 1, 1)
        factor_M = factor_M.reshape(-1, 1, 1)
        factor_Cvisc = factor_Cvisc.reshape(-1, 1, 1)
        factor_fvisc = factor_fvisc.reshape(-1, 1, 1)

        return factor_K, factor_M, factor_Cvisc, factor_fvisc


    def assemble_global_mass_matrix(self, factor_M: np.ndarray):
        """
        This method assembles the global mass matrix.

        Parameters
        ----------
        factor_M: np.ndarray
            An array containing all elementary mass factors in stacked form.
        """

        data_M = self.int3d_NtN * factor_M
        M = coo_matrix((data_M.ravel(), (self.rows, self.cols)), shape=self.model.gm_shape).tocsr()

        if self.model.drop_domain:
            idx = self.acoustic_dofs_indices
            M = M[idx, :][:, idx]

        if not self.model.reduced_memory_mode:
            self.mass_matrix = M

        return M


    def assemble_global_stiffness_matrix(self, factor_K: np.ndarray):
        """
        This method assembles the global stiffness matrix.

        Parameters
        ----------
        factor_K: np.ndarray
            An array containing all elementary stiffness factors in stacked form.
        """

        data_K = self.int3d_BtB * factor_K
        K = coo_matrix((data_K.ravel(), (self.rows, self.cols)), shape=self.model.gm_shape).tocsr()

        if self.model.drop_domain:
            idx = self.acoustic_dofs_indices
            K = K[idx, :][:, idx]

        if not self.model.reduced_memory_mode:
            self.stiffness_matrix = K

        return K


    def assemble_global_mass_and_stiffness_matrices(self, factor_M: np.ndarray, factor_K: np.ndarray):
        """
        This method assembles the global mass matrix.
        """

        data_M = self.int3d_NtN * factor_M
        data_K = self.int3d_BtB * factor_K

        M = coo_matrix((data_M.ravel(), (self.rows, self.cols)), shape=self.model.gm_shape).tocsr()
        K = coo_matrix((data_K.ravel(), (self.rows, self.cols)), shape=self.model.gm_shape).tocsr()

        if self.model.drop_domain:
            idx = self.acoustic_dofs_indices
            M = M[idx, :][:, idx]
            K = K[idx, :][:, idx]

        if not self.model.reduced_memory_mode:
            self.mass_matrix = M
            self.stiffness_matrix = K

        return M, K


    def process_global_matrices_data(self, reorder: bool = True, stacked_matrices: bool = True, print_log: bool = False):
        """
        This method assembles the global matrices of the acoustic model.
        """

        if not self.model.volumes_of_domain:
            self.model.domains_processor.update_domains_mappings()

        logging.info("Processing data to assemble global matrices... [10/100]")
        self.define_acoustic_elements()
        self.update_number_of_frequencies()

        logging.info("Processing data to assemble global matrices... [20/100]")
        t0 = perf_counter()
        if stacked_matrices:
            self.compute_data_to_assemble_global_matrices(reorder=reorder)
        else:
            self.compute_data_to_assemble_global_matrices_using_loop(reorder=reorder, print_log=print_log)
        dt = perf_counter() - t0
        if print_log:
            print(f"Elapsed time to gather data to assemble global matrices: {dt : .6f} [s]")

        if self.model.stop_processing:
            return

        logging.info("Processing data to assemble damping matrix... [40/100]")
        t0 = perf_counter()
        self.impedances_assembler.compute_data_to_assemble_damping_matrix()
        dt = perf_counter() - t0
        if print_log:
            print(f"Elapsed time to gather data to assemble damping matrices: {dt : .6f} [s]")


    def process_global_matrices_data_and_excitations(self, reorder: bool = True, stacked_matrices: bool = True, print_log: bool = False):
        """
        This method assembles the global matrices and excitations of the acoustic model.
        """
        self.process_global_matrices_data(reorder = reorder, stacked_matrices = stacked_matrices, print_log = print_log)        
        self.excitations_assembler.assemble_model_excitations()


    def assemble_global_matrices_CMK(self, index: int=0):
        """
        Use this method to reassemble the global matrices for a specific solution step.

        Parameter
        ---------
        index: int
            The solution step index of interest.

        """

        if any(item is None for item in [self.rows, self.cols, self.int3d_NtN, self.int3d_BtB]):
            self.load_global_matrices_data()

        logging.info("Assembling global matrices... [55/100]")
        # process the global matrices factors
        factor_K, factor_M, factor_Cvisc, factor_fvisc = self.compute_global_matrices_factors(index=index)

        logging.info("Assembling global matrices... [65/100]")
        # assemble the global mass and stiffness matrices
        M, K = self.assemble_global_mass_and_stiffness_matrices(factor_M, factor_K)

        # assemble global damping matrix
        logging.info("Assembling global matrices... [75/100]")
        self.damping_matrix_2d = self.impedances_assembler.assemble_global_damping_matrix_2d_elements()

        logging.info("Assembling global matrices... [95/100]")
        self.damping_matrix_3d, self.visc_load_matrix = self.impedances_assembler.assemble_global_damping_matrix_3d_elements(factor_Cvisc, factor_fvisc)

        C = self.damping_matrix_2d + self.damping_matrix_3d

        return C, M, K


    def exists_a_non_zero_prescribed_value(self, index: int):
        """
        This method checks if there is a non-zero prescribed dof value.
        """
        if self.prescribed_values.size == 0:
            return False

        return np.any(self.prescribed_values[:, index])


    def process_reduced_global_matrices(self, C: csr_matrix, M: csr_matrix, K: csr_matrix):
        """
        """
        # prescribed indexes
        idx = self.prescribed_dof_indices

        self.damping_matrix_r = C[:, idx]
        self.mass_matrix_r = M[:, idx]
        self.stiffness_matrix_r = K[:, idx]


    def compute_load_vector(self, index: int) -> np.ndarray:
        """
        Use this method to compute the acoustic load vector.

        Parameters
        ----------
        freq: float
            The frequency value in Hz.
        
        index: int
            The column index.

        Return
        ------
        load_vector: np.ndarray
            The acoustic load vector

        """

        logging.info("Computing the load vector... [95/100]")

        if self.frequency_dependent:

            # reassemble the mass source matrices
            self.excitations_assembler.assemble_mass_source_matrices_from_surfaces(index=index)
            self.excitations_assembler.assemble_mass_source_matrices_from_volumes(index=index)

        # create the frequency vector
        freq = self.frequencies[index]
        omega = 2 * np.pi * freq

        # # update the prescribed dof-related load vector for each frequency step
        # f_eq = self.excitations_assembler.get_prescribed_pressure_model_excitation(index=index)

        # mass source-related load vector
        f_ms = self.excitations_assembler.compute_mass_source_load_vector(omega, index=index)

        # mass flow vector
        mass_flow_vector = self.excitations_assembler.mass_flow_vector

        # viscous damping-related load vector
        f_visc = self.visc_load_matrix @ mass_flow_vector[:, index]

        # mass flow-related load vector
        f_mf = 1j * omega * mass_flow_vector[:, index]

        # compute the load vector {f}
        load_vector = f_ms + f_visc - f_mf - self.f_eq

        if self.model.reduced_memory_mode:
            del f_ms, f_visc, f_mf
            self.f_eq = None

        if self.prescribed_dof_indices:
            return load_vector[self.unprescribed_dof_indices]

        return load_vector


    def compute_dynamic_stiffness_matrix(self, freq: float, index: int) -> csr_matrix:
        """
        Use this method to compute the global acoustic dynamic stiffness matrix.

        Parameters
        ----------
        freq: float
            The frequency value in Hz.

        index: int
            The column index.

        Return
        ------
        Kd: csr_matrix
            The global acoustic dynamic stiffness matrix.

        """

        if index == 0 or self.frequency_dependent or self.model.reduced_memory_mode:
            C, M, K = self.assemble_global_matrices_CMK(index)

        else:
            self.damping_matrix_2d = self.impedances_assembler.assemble_global_damping_matrix_2d_elements(index=index)
            C = self.damping_matrix_2d + self.damping_matrix_3d
            M = self.mass_matrix
            K = self.stiffness_matrix

        # compute the dynamic stiffness matrix Kd
        omega = 2 * np.pi * freq
        Kd = -(omega**2) * M + (1j * omega) * C + K

        if self.prescribed_values.any():
            self.f_eq = Kd[:, self.prescribed_dof_indices] @ self.prescribed_values[:, index]
        else:
            self.f_eq = 0.

        if self.model.reduced_memory_mode:
            self.reset_global_matrices_attributes()

        if self.prescribed_dof_indices:
            Kd = Kd[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]

        return Kd


    def build_eigenproblem_system(self):

        _, M, K = self.assemble_global_matrices_CMK()

        C_imp = self.damping_matrix_2d

        if self.prescribed_dof_indices:
            idx = self.unprescribed_dof_indices
            M = M[idx, :][:, idx]
            K = K[idx, :][:, idx]
            C_imp = C_imp[idx, :][:, idx]

        is_complex = np.any(np.iscomplex(K.data)) or np.any(np.iscomplex(M.data)) or np.any(np.iscomplex(C_imp.data))
        if not is_complex:
            K.data = np.real(K.data)
            M.data = np.real(M.data)
            C_imp.data = np.real(C_imp.data)

        if np.any(C_imp.data):
            B = block_array([[M, None], [None, M]], format="csr")
            A = block_array([[None, M], [-K, -C_imp]], format="csr")

            return A, B, False

        return K, M, True


    def reinsert_the_prescribed_dof(self, solution: np.ndarray, modal_analysis=False):
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

        rows = len(solution) + len(self.prescribed_dof_indices)
        cols = solution.shape[1]

        full_solution = np.zeros((rows, cols), dtype=np.complex128)
        full_solution[self.unprescribed_dof_indices, :] = solution

        if len(self.prescribed_dof_indices):
            if modal_analysis:
                full_solution[self.prescribed_dof_indices, :] = np.zeros((len(self.prescribed_values), cols))
            else:
                full_solution[self.prescribed_dof_indices, :] = self.prescribed_values[:, 0:cols]

        return full_solution


    def reinsert_the_prescribed_dof_into_solution_freq(self, solution: np.ndarray, freq_index: int):
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

        rows = len(solution) + len(self.prescribed_dof_indices)

        full_solution = np.zeros(rows, dtype=np.complex128)
        full_solution[self.unprescribed_dof_indices] = solution

        if len(self.prescribed_dof_indices):
            full_solution[self.prescribed_dof_indices] = self.prescribed_values[:, freq_index]

        return full_solution


    def write_global_matrices_array_data(self):

        print()
        print("Allocated RAM for acoustic global matrices")
        print(f"data K -> {self.get_size_in_GB(self.int3d_BtB) : .4f} GB")
        print(f"data M -> {self.get_size_in_GB(self.int3d_NtN) : .4f} GB")
        print(f"rows I -> {self.get_size_in_GB(self.rows) : .4f} GB")
        print(f"cols J -> {self.get_size_in_GB(self.cols) : .4f} GB")

        logging.info("Writing the global matrices data... [25/100]")
        self.model.array_writer("acoustic_rows_indices.npy", self.rows)

        logging.info("Writing the global matrices data... [50/100]")
        self.model.array_writer("acoustic_cols_indices.npy", self.cols)

        logging.info("Writing the global matrices data... [75/100]")
        self.model.array_writer("acoustic_int3d_NtN.npy", self.int3d_NtN)

        logging.info("Writing the global matrices data... [98/100]")
        self.model.array_writer("acoustic_int3d_BtB.npy", self.int3d_BtB)


    def load_global_matrices_data(self):
        self.rows = self.model.array_reader("acoustic_rows_indices.npy")
        self.cols = self.model.array_reader("acoustic_cols_indices.npy")
        self.int3d_NtN = self.model.array_reader("acoustic_int3d_NtN.npy")
        self.int3d_BtB = self.model.array_reader("acoustic_int3d_BtB.npy")


    def get_size_in_GB(self, data: np.ndarray):
        return sys.getsizeof(data) / (1024**3)