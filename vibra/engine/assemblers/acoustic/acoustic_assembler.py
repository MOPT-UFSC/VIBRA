import logging
import sys
from time import time

import numpy as np
from scipy.sparse import block_array, csr_matrix
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

        # global matrices
        self.stiffness_matrix = None
        self.stiffness_matrix_r = None
        self.mass_matrix = None
        self.mass_matrix_r = None
        self.damping_matrix = None
        self.damping_matrix_r = None
        self.visc_damping_matrix = None
        self.visc_damping_matrix_r = None

        self.visc_load_matrix = None
        self.mass_flow_vector = None

        self.frequencies = None
        self.frequency_dependent = False

        self.number_frequencies = 1
        self.prescribed_values = []
        self.prescribed_dof_indices = None
        self.unprescribed_dof_indices = None
        self.fluid_properties_from_volume = {}

        self.element_1d = None
        self.element_2d = None
        self.element_3d = None


    @property
    def number_3d_elements(self):
        return self.model.number_3d_acoustic_elements


    @property
    def acoustic_dofs(self):
        return self.model.acoustic_dofs_indices


    @property
    def acoustic_ndofs(self):
        return len(self.model.acoustic_dofs_indices)

    @property
    def total_dofs(self):
        return self.model.total_dof


    @property
    def gm_shape(self):
        return (self.model.total_dof, self.model.total_dof)


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


    def get_prescribed_dof_values(self):
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

        global_prescribed = []
        list_prescribed_dof = []

        aux_ones = np.ones(self.number_frequencies, dtype=complex)

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

                    global_prescribed.append(_values)

        # TODO: implement same structure for lines
        # TODO: refactor this method

        try:

            for value in global_prescribed:
                if isinstance(value, complex):
                    list_prescribed_dof.append(aux_ones * value)
                elif isinstance(value, np.ndarray):
                    if len(value) == 1:
                       list_prescribed_dof.append(aux_ones * value)
                    else: 
                        list_prescribed_dof.append(value[0:self.number_frequencies])

            array_prescribed_values = np.array(list_prescribed_dof)

        except Exception as _error_log:
            print(str(_error_log))

        return global_prescribed, array_prescribed_values


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

            _nodes = self.model.fluid_node_mapping[nodes]

            global_dofs = self.model.get_acoustic_global_dof_from_nodes(_nodes)
            prescribed_dof_indices.extend(global_dofs)

        self.prescribed_dof_indices = prescribed_dof_indices


    def process_unprescribed_indices(self):
        """ 
        Returns the unprescribed dof indices.
        """
        all_indices = np.arange(self.model.total_act_dofs, dtype=int)
        self.unprescribed_dof_indices = np.delete(all_indices, self.prescribed_dof_indices)


    def process_dofs_indices(self):
        self.process_prescribed_indices()
        self.process_unprescribed_indices()


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
            flatten: bool = False, 
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
        
        flatten: bool, optional
            Controls whether the output vector will be flattened or not.

        Returns
        -------
        output_vector: np.ndarray
            The output vector with the same length as the frequencies
            vector.
        """

        aux_ones = np.ones((1, self.number_frequencies), dtype=complex)

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

        return output_vector.flatten() if flatten else output_vector


    def compute_data_to_assemble_global_matrices(self, reorder: bool = True):
        """ 
        This method processes the data required to assemble the global matrices
        based on the stacked elementary matrices.

        Parameters
        ----------
        reorder: bool, optional
            Control when the connectivity matrix will be reordered.
        """

        self.ind_rows, self.ind_cols, _ = self.element_3d.generate_ind_rows_cols(reorder=reorder)

        logging.info("Processing the elementary matrices data... [25/100]")
        self.int3d_BtB, self.int3d_NtN = self.element_3d.stacked_elementary_matrices_NtN_BtB()

        if self.model.stop_processing:
            return True

        logging.info("Processing the elementary matrices data... [85/100]")
        self.fluid_properties_from_volume, self.frequency_dependent = self.model.map_fluid_properties_to_volumes()

        logging.info("Processing the elementary matrices data... [95/100]")
        self.process_dofs_indices()


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
        self.int3d_BtB = np.zeros((self.number_3d_elements, dof, dof), dtype=complex)
        self.int3d_NtN = np.zeros((self.number_3d_elements, dof, dof), dtype=complex)

        self.ind_rows, self.ind_cols, _ = self.element_3d.generate_ind_rows_cols(reorder=reorder)

        last_progress = 0
        for index, element_id in enumerate(self.model.elements_per_domain.get("acoustic", [])):

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

        for vol_id, elements_from_volume in self.model.mesh.elements_from_volume.items():
            fluid_data = self.fluid_properties_from_volume.get(vol_id)
            if not isinstance(fluid_data, dict):
                continue

            rho_f = fluid_data.get("rho_f")[index]
            C_f = fluid_data.get("C_f")[index]
            mu_0 = fluid_data.get("mu_0")
            rho_0 = fluid_data.get("rho_0")
            C_0 = fluid_data.get("C_0")

            aux_ones = np.ones(elements_from_volume.size, dtype=float)

            factor_K[elements_from_volume] = aux_ones / (rho_f)
            factor_M[elements_from_volume] = aux_ones / (rho_f * C_f**2)
            factor_Cvisc[elements_from_volume] = ((4 * mu_0) / (3 * ((rho_0 * C_0)**2)))
            factor_fvisc[elements_from_volume] = ((4 * mu_0) / (3 * (rho_0**2)))

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
        self.mass_matrix = csr_matrix((data_M.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        if self.model.drop_domain:
            self.mass_matrix = self.mass_matrix[self.acoustic_dofs, :][:, self.acoustic_dofs]

        self.mass_matrix_r = self.mass_matrix[:, self.prescribed_dof_indices]

        if self.prescribed_dof_indices:
            self.mass_matrix = self.mass_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def assemble_global_stiffness_matrix(self, factor_K: np.ndarray):
        """
        This method assembles the global stiffness matrix.

        Parameters
        ----------
        factor_K: np.ndarray
            An array containing all elementary stiffness factors in stacked form.
        """
        data_K = self.int3d_BtB * factor_K
        self.stiffness_matrix = csr_matrix((data_K.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        if self.model.drop_domain:
            self.stiffness_matrix = self.stiffness_matrix[self.acoustic_dofs, :][:, self.acoustic_dofs]

        self.stiffness_matrix_r = self.stiffness_matrix[:, self.prescribed_dof_indices]

        if self.prescribed_dof_indices:
            self.stiffness_matrix = self.stiffness_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def assemble_global_damping_matrix_3d_elements(self, factor_Cvsic: np.ndarray, factor_fvsic: np.ndarray):
        """
        This method assembles the global damping matrix to account
        the bulk damping effects.
        https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_thry/thy_acou2.html#thyeqacous-75
        """

        data_C = self.int3d_BtB * factor_Cvsic
        self.visc_damping_matrix = csr_matrix((data_C.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        data_f = self.int3d_BtB * factor_fvsic
        self.visc_load_matrix = csr_matrix((data_f.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        if self.model.drop_domain:
            self.visc_damping_matrix = self.visc_damping_matrix[self.acoustic_dofs, :][:, self.acoustic_dofs]
            self.visc_load_matrix = self.visc_load_matrix[self.acoustic_dofs, :][:, self.acoustic_dofs]

        self.visc_damping_matrix_r = self.visc_damping_matrix[:, self.prescribed_dof_indices]
        self.visc_load_matrix_r = self.visc_load_matrix[:, self.prescribed_dof_indices]

        if self.prescribed_dof_indices:
            self.visc_damping_matrix = self.visc_damping_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]
            self.visc_load_matrix = self.visc_load_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def assemble_global_damping_matrix_2d_elements(self, index: int = 0):
        """
        This method computes the global damping matrix asseble.

        Parameters
        ----------
        index: int, optional.
            It corresponds to the frequency step index.
        """

        self.damping_matrix = csr_matrix(self.gm_shape)

        if self.impedances_assembler.integration_data_Zsi is not None:
            rows_Zout = self.impedances_assembler.rows_Zsi
            cols_Zout = self.impedances_assembler.cols_Zsi
            data_Zout = self.impedances_assembler.data_Zsi[index].flatten()
            self.damping_matrix += csr_matrix((data_Zout, (rows_Zout, cols_Zout)), shape=self.gm_shape)

        if self.impedances_assembler.integration_data_Zat is not None:
            rows_Zout = self.impedances_assembler.rows_Zat
            cols_Zout = self.impedances_assembler.cols_Zat
            data_Zout = self.impedances_assembler.data_Zat[index].flatten()
            self.damping_matrix += csr_matrix((data_Zout, (rows_Zout, cols_Zout)), shape=self.gm_shape)

        if self.impedances_assembler.integration_data_ipw is not None:
            rows_Zout = self.impedances_assembler.rows_Zipw
            cols_Zout = self.impedances_assembler.cols_Zipw
            data_Zout = self.impedances_assembler.data_Zipw[index].flatten()
            self.damping_matrix += csr_matrix((data_Zout, (rows_Zout, cols_Zout)), shape=self.gm_shape)

        if self.impedances_assembler.integration_data_Zas is not None:
            rows_Zout = self.impedances_assembler.rows_Zas
            cols_Zout = self.impedances_assembler.cols_Zas
            data_Zout = self.impedances_assembler.data_Zas[index].flatten()
            self.damping_matrix += csr_matrix((data_Zout, (rows_Zout, cols_Zout)), shape=self.gm_shape)

        if self.impedances_assembler.integration_data_Zpp is not None:
            rows_A = self.impedances_assembler.rows_Zpp_A
            rows_B = self.impedances_assembler.rows_Zpp_B
            cols_A = self.impedances_assembler.cols_Zpp_A
            cols_B = self.impedances_assembler.cols_Zpp_B
            Zin_A = self.impedances_assembler.data_Zpp_A[index].flatten()
            Zin_B = self.impedances_assembler.data_Zpp_B[index].flatten()

            values_Zin = np.concatenate((Zin_A, -Zin_A, -Zin_B, Zin_B))
            rows_Zin = np.concatenate((rows_A, rows_A, rows_B, rows_B))
            cols_Zin = np.concatenate((cols_A, cols_B, cols_A, cols_B))

            self.damping_matrix += csr_matrix((values_Zin, (rows_Zin, cols_Zin)), shape=self.gm_shape)

        if self.impedances_assembler.integration_data_Zti is not None:
            rows_A = self.impedances_assembler.rows_Zti_A
            rows_B = self.impedances_assembler.rows_Zti_B
            cols_A = self.impedances_assembler.cols_Zti_A
            cols_B = self.impedances_assembler.cols_Zti_B
            Zin_A = self.impedances_assembler.data_Zti_A[index].flatten()
            Zin_B = self.impedances_assembler.data_Zti_B[index].flatten()

            values_Zin = np.concatenate((Zin_A, -Zin_A, -Zin_B, Zin_B))
            rows_Zin = np.concatenate((rows_A, rows_A, rows_B, rows_B))
            cols_Zin = np.concatenate((cols_A, cols_B, cols_A, cols_B))

            self.damping_matrix += csr_matrix((values_Zin, (rows_Zin, cols_Zin)), shape=self.gm_shape)

        if self.model.drop_domain:
            self.damping_matrix = self.damping_matrix[self.acoustic_dofs, :][:, self.acoustic_dofs]

        self.damping_matrix_r = self.damping_matrix[:, self.prescribed_dof_indices]

        if self.prescribed_dof_indices:
            self.damping_matrix = self.damping_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def assemble_global_matrices(self, reorder: bool = True, stacked_matrices: bool = True, print_log: bool = False):
        """
        This method assembles the global matrices of the acoustic model.
        """

        if not self.model.model_domains:
            self.model.update_domains_mappings()

        logging.info("Processing data to assemble global matrices... [10/100]")
        self.define_acoustic_elements()
        self.update_number_of_frequencies()

        logging.info("Processing data to assemble global matrices... [20/100]")
        t0 = time()
        if stacked_matrices:
            self.compute_data_to_assemble_global_matrices(reorder=reorder)
        else:
            self.compute_data_to_assemble_global_matrices_using_loop(reorder=reorder, print_log=print_log)
        dt = time() - t0
        if print_log:
            print(f"Elapsed time to gather data to assemble global matrices: {dt : .6f} [s]")

        if self.model.stop_processing:
            return

        logging.info("Processing data to assemble damping matrix... [40/100]")
        t0 = time()
        self.impedances_assembler.compute_data_to_assemble_damping_matrix()
        dt = time() - t0
        if print_log:
            print(f"Elapsed time to gather data to assemble damping matrices: {dt : .6f} [s]")

        logging.info("Computing the global matrices factors... [45/100]")
        t0 = time()
        factor_K, factor_M, factor_Cvisc, factor_fvisc = self.compute_global_matrices_factors()
        dt = time() - t0
        if print_log:
            print(f"Elapsed time to compute global matrices factor: {dt : .6f} [s]")

        logging.info("Assembling global stiffness matrix... [50/100]")
        t0 = time()
        self.assemble_global_stiffness_matrix(factor_K)
        dt = time() - t0
        if print_log:
            print(f"Elapsed time to assemble the global stiffness matrix: {dt : .6f} [s]")

        logging.info("Assembling global mass matrix... [60/100]")
        t0 = time()
        self.assemble_global_mass_matrix(factor_M)
        dt = time() - t0
        if print_log:
            print(f"Elapsed time to assemble the global mass matrix: {dt : .6f} [s]")

        logging.info("Assembling global mass matrix... [70/100]")
        t0 = time()
        self.assemble_global_damping_matrix_3d_elements(factor_Cvisc, factor_fvisc)
        self.assemble_global_damping_matrix_2d_elements()
        dt = time() - t0
        if print_log:
            print(f"Elapsed time to assemble the global damping matrix: {dt : .6f} [s]\n")


    def assemble_global_matrices_and_excitations(self, reorder: bool = True, stacked_matrices: bool = True, print_log: bool = False):
        """
        This method assembles the global matrices and excitations of the acoustic model.
        """
        self.assemble_global_matrices(reorder = reorder, stacked_matrices = stacked_matrices, print_log = print_log)        
        self.mass_flow_vector =self.excitations_assembler.assemble_model_excitations()


    def build_harmonic_system(self, freq: float, i: int):

        # mass and stiffness matrices
        M = self.mass_matrix
        K = self.stiffness_matrix

        # create the frequency vector
        omega = 2 * np.pi * freq

        # update the damping matrix [C]
        self.assemble_global_damping_matrix_2d_elements(index=i)
        
        # sum damping matrices
        C = self.damping_matrix + self.visc_damping_matrix

        if self.frequency_dependent:
            # reassemble the global mass and stiffness matrices
            factor_K, factor_M, _, _ = self.compute_global_matrices_factors(index=i)
            self.assemble_global_mass_matrix(factor_M)
            self.assemble_global_stiffness_matrix(factor_K)

            M = self.mass_matrix
            K = self.stiffness_matrix

            # reassemble the mass source matrices
            self.excitations_assembler.assemble_mass_source_matrices_from_surfaces(index=i)
            self.excitations_assembler.assemble_mass_source_matrices_from_volumes(index=i)

        # update the prescribed dof-related load vector for each frequency step
        f_eq = self.excitations_assembler.get_prescribed_pressure_model_excitation(index=i)

        # mass source-related load vector
        f_ms = self.excitations_assembler.compute_mass_source_load_vector(omega, index=i)

        # viscous damping-related load vector
        f_visc = self.visc_load_matrix @ self.mass_flow_vector[:, i]

        # mass flow-related load vector
        f_mf = 1j * omega * self.mass_flow_vector[:, i]

        # define the linear system equation terms [A]{x} = {f}
        A = K - (omega ** 2) * M + 1j * omega * C
        f = f_ms + f_visc - f_mf - f_eq

        is_complex = np.any(np.iscomplex(A.data)) or np.any(np.iscomplex(f))
        if not is_complex:
            A.data = np.real(A.data)
            f = np.real(f)

        return A, f


    def build_eigenproblem_system(self):
        K = self.stiffness_matrix
        M = self.mass_matrix

        C_imp = self.damping_matrix
        
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

        prescribed_values, array_prescribed_values = self.get_prescribed_dof_values()

        rows = len(solution) + len(self.prescribed_dof_indices)
        cols = solution.shape[1]

        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[self.unprescribed_dof_indices, :] = solution

        if len(self.prescribed_dof_indices):
            if modal_analysis:
                full_solution[self.prescribed_dof_indices, :] = np.zeros((len(prescribed_values), cols))
            else:
                full_solution[self.prescribed_dof_indices, :] = array_prescribed_values[:, 0:cols]

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

        _, array_prescribed_values = self.get_prescribed_dof_values()

        rows = len(solution) + len(self.prescribed_dof_indices)

        full_solution = np.zeros(rows, dtype=complex)
        full_solution[self.unprescribed_dof_indices] = solution

        if len(self.prescribed_dof_indices):
            full_solution[self.prescribed_dof_indices] = array_prescribed_values[:, freq_index]

        return full_solution