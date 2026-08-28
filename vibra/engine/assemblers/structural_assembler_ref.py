
from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.engine.model import Model

import logging
import numpy as np

from collections import defaultdict
from scipy.sparse import csr_matrix
from time import time


class StructuralAssembler:
    def __init__(self, model : Model):

        self.model = model
        self.properties = model.properties

        self.reset()

    def reset(self):
        self.frequencies = None
        self.mass_matrix = None
        self.stiffness_matrix = None

        self.prescribed_dof_values = dict()
        self.array_prescribed_values = np.array([])

        self.displacement_dof = np.array([])
        self.prescribed_dof_indices = np.array([])
        self.unprescribed_dof_indices = np.array([])

    def define_structural_elements(self):
        self.model.set_structural_elements()
        self.element_2d = self.model.structural_element_2d
        self.element_3d = self.model.structural_element_3d

    def update_number_of_frequencies(self):
        self.frequencies = self.model.frequencies
        if self.frequencies is None:
            self.number_frequencies = 1
        else:
            self.number_frequencies = len(self.frequencies)

    def is_assembled(self):
        return (self.stiffness_matrix is not None) and (self.mass_matrix is not None)

    def get_property_data_for_selected_property(self, selected_property: str):
        """
        """
        prescribed_data = defaultdict(int)
        for (property, surface_id), data in self.properties.surface_properties.items():
            if property == selected_property:
                nodes = self.model.mesh.get_nodes_from_surface(surface_id)
                if nodes is None:
                    continue

                property_data_from_nodes = self.model.get_structural_property_data_from_nodes(nodes, data, "surfaces")
                for gdof, p_data in property_data_from_nodes.items():
                    prescribed_data[gdof] += p_data

        for (property, line_id), data in self.properties.line_properties.items():
            if property == selected_property:
                nodes = self.model.mesh.get_nodes_from_line(line_id)
                if nodes is None:
                    continue

                property_data_from_nodes = self.model.get_structural_property_data_from_nodes(nodes, data, "lines")
                for gdof, p_data in property_data_from_nodes.items():
                    prescribed_data[gdof] += p_data

        for (property, point_id), data in self.properties.point_properties.items():
            if property != selected_property:
                continue

            node_id = self.model.mesh.nodes_from_points.get(point_id)
            if node_id is None:
                continue

            _node_id = np.array([node_id], dtype=int)
            property_data_from_nodes = self.model.get_structural_property_data_from_nodes(_node_id, data, "points")
            for gdof, p_data in property_data_from_nodes.items():
                prescribed_data[gdof] += p_data

        for (property, node_id), data in self.properties.nodal_properties.items():
            if property == selected_property:
                nodes = np.array([node_id], dtype=int)
                property_data_from_nodes = self.model.get_structural_property_data_from_nodes(nodes, data, "nodes")
                for gdof, p_data in property_data_from_nodes.items():
                    prescribed_data[gdof] += p_data

        return prescribed_data

    def process_property_arrays(self, data: dict):
        """
        This method returns all the values of the structural degrees of freedom with prescribed structural displacement or rotation boundary conditions.

        Returns
        ----------
        array
            Values of the structural degrees of freedom with prescribed displacement or rotation boundary conditions.

        See also
        --------
        get_prescribed_indices : Indexes of the structural degrees of freedom with prescribed displacement or rotation boundary conditions.

        get_unprescribed_indices : Indexes of the structural free degrees of freedom.
        """

        if self.frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)

        try:

            property_data = dict()
            for gdof in data.keys():
                value = data[gdof]

                aux_ones = np.ones(number_frequencies, dtype=complex)
                if isinstance(value, complex):
                    property_data[gdof] = aux_ones * value

                elif isinstance(value, np.ndarray):
                    property_data[gdof] = value[0:number_frequencies]

        except Exception as _error_log:
            print(str(_error_log))

        return property_data, np.array(list(property_data.values()))

    def process_loads_arrays(self, structural_loads: list):
        """
        This method returns...
        """

        if self.frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)

        try:

            loads_list = list()
            aux_ones = np.ones(number_frequencies, dtype=complex)
            aux_zeros = np.zeros(number_frequencies, dtype=complex)

            for value in structural_loads:

                if value is None:
                    loads_list.append(aux_zeros)

                elif isinstance(value, complex):
                    loads_list.append(aux_ones * value)

                elif isinstance(value, np.ndarray):
                    loads_list.append(value[0:number_frequencies])

        except Exception as _error_log:
            print(str(_error_log))
            # TODO: check matrix dimensions for compatibility
            return aux_ones

        return np.array(loads_list, dtype=complex)

    def get_unprescribed_indices(self):
        prescribed_indices = np.array([*set(self.prescribed_dof_indices)], dtype=int)
        return np.delete(self.all_dof, prescribed_indices)

    def reorder_property_data_based_on_gdof(self, input_property_data: dict):

        output_property_data = dict()
        ordered_gdof = np.sort(list(input_property_data.keys()))
        for gdof in ordered_gdof:
            output_property_data[gdof] = input_property_data[gdof]

        return output_property_data

    def process_prescribed_dof_data(self):

        input_prescribed_dof_data = self.get_property_data_for_selected_property("prescribed_dof")
        output_prescribed_dof_data = self.reorder_property_data_based_on_gdof(input_prescribed_dof_data)
        self.prescribed_dof_values, self.array_prescribed_values = self.process_property_arrays(output_prescribed_dof_data)

        self.prescribed_dof_indices = list(output_prescribed_dof_data.keys())
        self.unprescribed_dof_indices = self.get_unprescribed_indices()

    def process_structural_nodal_loads(self):

        input_nodal_loads_data = self.get_property_data_for_selected_property("nodal_loads")
        output_nodal_loads_data = self.reorder_property_data_based_on_gdof(input_nodal_loads_data)
        nodal_loads, _ = self.process_property_arrays(output_nodal_loads_data)

        # self.nodal_loads_indices = list(output_nodal_loads_data.keys())
        output = np.zeros((len(self.all_dof), self.number_frequencies), dtype=complex)

        if nodal_loads:
            indices = list(nodal_loads.keys())
            excitation = list(nodal_loads.values())
            output[indices, :] = np.array(excitation)

        if self.prescribed_dof_indices:
            if len(self.active_2d_element_dof):
                return output[self.unprescribed_shell_dof, :]
            else:
                return output[self.unprescribed_dof_indices, :]
        else:
            return output

    def process_distributed_loads(self):

        output = np.zeros((len(self.all_dof), self.number_frequencies), dtype=complex)

        for (property, surface_id), data in self.properties.surface_properties.items():
            if property not in ["distributed_loads", "normal_pressure_loads"]:
                continue

            connectivities_from_surface = self.model.mesh.get_connectivity_from_surface(surface_id)
            if property == "distributed_loads":
                surface_load = self.process_loads_arrays(data["values"])
                if surface_load is None:
                    continue

                for connect in connectivities_from_surface:
                    g_dof, F_elem = self.element_2d.process_forces_for_distributed_load_over_area(connect, surface_load)
                    output[g_dof, :] += F_elem

            elif property == "normal_pressure_load":
                normal_pressure = self.process_loads_arrays(data["values"])
                if normal_pressure is None:
                    continue

                for connect in connectivities_from_surface:
                    g_dof, F_elem = self.element_2d.process_forces_for_normal_pressure_load(connect, normal_pressure)
                    output[g_dof, :] += F_elem

        for (property, line_id), data in self.properties.line_properties.items():
            if property == "distributed_loads":
                line_load = self.process_loads_arrays(data["values"])
                if line_load is None:
                    continue

                nodes = self.model.mesh.get_nodes_from_line(line_id)
                if nodes is None:
                    continue

                for surface_id in self.model.mesh.surfaces_from_line[line_id]:
                    connectivities_from_surface = self.model.mesh.get_connectivity_from_surface(surface_id)
                    rows = np.sum(np.isin(connectivities_from_surface, nodes), axis=1) == 2

                    for connect_2d in connectivities_from_surface[rows, :]:
                        active_nodes = [1 if node_id in nodes else 0 for node_id in connect_2d]
                        g_dof, F_elem = self.element_2d.process_forces_for_distributed_load_over_line(connect_2d, active_nodes, line_load)
                        output[g_dof, :] += F_elem

        if self.prescribed_dof_indices:
            if len(self.active_2d_element_dof):
                return output[self.unprescribed_shell_dof, :]
            else:
                return output[self.unprescribed_dof_indices, :]
        else:
            return output

    # def get_matrices_dropping_indices(self):
    #     return self.unprescribed_dof_indices, self.prescribed_dof_indices

    def get_prescribed_dof_values(self):
        return self.prescribed_dof_values, self.array_prescribed_values

    def get_all_degrees_of_freedom(self, element_2D, element_3D, active_2d_dof):

        nodes_from_2d_elements = np.array([*set(self.model.mesh.faces_connectivity[:, 4:].flatten())], dtype=int)
        nodes_from_3d_elements = np.array([*set(self.model.mesh.solids_connectivity[:, 4:].flatten())], dtype=int)

        local_dof_2d = np.arange(element_2D.DOF_PER_NODE)
        local_dof_3d = np.arange(element_3D.DOF_PER_NODE)
        rotation_local_dof_2d = local_dof_2d[int(element_2D.DOF_PER_NODE / 2):]

        dof_from_2d_elements = element_2D.DOF_PER_NODE * nodes_from_2d_elements.reshape(-1, 1) + local_dof_2d
        dof_from_3d_elements = element_3D.DOF_PER_NODE * nodes_from_3d_elements.reshape(-1, 1) + local_dof_3d
        rotation_dof_from_2d_elements = element_2D.DOF_PER_NODE * nodes_from_2d_elements.reshape(-1, 1) + rotation_local_dof_2d

        self.dof_from_2d_elements = dof_from_2d_elements.flatten()
        self.dof_from_3d_elements = dof_from_3d_elements.flatten()
        self.rotation_dof_from_2d_elements = rotation_dof_from_2d_elements.flatten()

        shift_index = 0
        internal_dof_from_3d_elements = np.array([], dtype=int)

        if len(active_2d_dof):

            if len(nodes_from_3d_elements):
                shift_index = int((np.max(dof_from_2d_elements) + 1) / 2)
                internal_nodes = np.delete(nodes_from_3d_elements, nodes_from_2d_elements)
                internal_dof_from_3d_elements = element_3D.DOF_PER_NODE * internal_nodes.reshape(-1, 1) + local_dof_3d + shift_index
                internal_dof_from_3d_elements = internal_dof_from_3d_elements.flatten()

            total_dof_apd = np.append(self.dof_from_2d_elements, internal_dof_from_3d_elements)
            all_dof = np.array([*set(total_dof_apd)], dtype=int)
            self.displacement_dof = np.delete(all_dof, self.rotation_dof_from_2d_elements)

            return all_dof, shift_index

        else:

            self.displacement_dof = self.dof_from_3d_elements.copy()
            return self.dof_from_3d_elements, shift_index

    def process_face_elements_with_thickness(self, element_2D, element_3D):

        active_nodes_list = list()
        for key in self.model.properties.surface_properties.keys():
            property, surface_id = key
            if property == "surface_thickness":
                nodes = self.model.mesh.get_nodes_from_surface(surface_id)
                if nodes is None:
                    continue

                active_nodes_list.extend(nodes)

        active_dof = np.array([])
        if active_nodes_list:
            shell_local_dof = np.arange(element_2D.DOF_PER_NODE)
            active_nodes = np.unique(active_nodes_list).astype(int)
            active_dof = element_2D.DOF_PER_NODE * active_nodes.reshape(-1, 1) + shell_local_dof 
            active_dof = np.sort(active_dof.flatten())

        self.all_dof, shift_index = self.get_all_degrees_of_freedom(element_2D, element_3D, active_dof)

        return active_dof, len(self.all_dof), shift_index

    def compute_data_to_process_global_matrices(self, reorder: bool = True):
        """
        Calculates global matrices.
        """

        self.data_K = np.array([], dtype=float)
        self.data_M = np.array([], dtype=float)

        self.ind_cols = np.array([], dtype=int)
        self.ind_rows = np.array([], dtype=int)

        self.active_2d_element_dof, self.total_dof, shift_index = self.process_face_elements_with_thickness(self.element_2d, self.element_3d)

        if self.model.mesh.solids_connectivity.size:
            self.element_3d.reorder_connect()

            dof = self.element_3d.DOF_PER_ELEMENT
            nel = len(self.element_3d.connectivity)

            ind_rows = np.zeros((nel, dof, dof), dtype=int)
            ind_cols = np.zeros((nel, dof, dof), dtype=int)
            data_K_se = np.zeros((nel, dof, dof), dtype=complex)
            data_M_se = np.zeros((nel, dof, dof), dtype=complex)

            last_progress = 0

            # loop for 3d elements
            for el_index, vol_id, *_ in self.model.mesh.solids_connectivity:
                progress = 100 * np.round(el_index/nel, 2)
                if progress != last_progress:
                    logging.info(f"Processing the elementary matrices data for solid elements... [{int(progress)}/100]")

                last_progress = progress

                material = self.model.properties._get_property("material", volume=vol_id)
                if material is None:
                    continue

                rows, cols = self.element_3d.get_rows_and_cols_indices(el_index, shift_index)
                ind_rows[el_index, :, :] = rows
                ind_cols[el_index, :, :] = cols

                Ke, Me = self.element_3d.elementary_matrices(el_index, material)
                data_K_se[el_index, :, :] = Ke
                data_M_se[el_index, :, :] = Me

            self.data_K = np.append(self.data_K, data_K_se.flatten())
            self.data_M = np.append(self.data_M, data_M_se.flatten())

            self.ind_rows = np.append(self.ind_rows, ind_rows.flatten())
            self.ind_cols = np.append(self.ind_cols, ind_cols.flatten())

            # np.savetxt("indices_exported.dat", np.array([ind_rows.flatten(), ind_cols.flatten()], dtype=int).T, delimiter=",", fmt="%i")

        aux_nodes = list()

        if len(self.active_2d_element_dof):

            rows_fe, cols_fe = self.element_2d.generate_ind_rows_cols()

            dof = self.element_2d.dfo_per_element
            nel = len(self.element_2d.connectivity)

            self.ind_rows = np.append(self.ind_rows, rows_fe)
            self.ind_cols = np.append(self.ind_cols, cols_fe)
            # np.savetxt("indices.dat", np.array([ind_rows, ind_cols], dtype=int).T, fmt="%i")

            data_K_fe = np.zeros((nel, dof, dof), dtype=complex)
            data_M_fe = np.zeros((nel, dof, dof), dtype=complex)

            last_progress = 0

            # loop for 2d elements
            for el_index, surf_id, _, _, *connect_nodes in self.model.mesh.faces_connectivity:
                progress = 100 * np.round(el_index/nel, 2)
                if progress != last_progress:
                    logging.info(f"Processing the elementary matrices data for face elements... [{int(progress)}/100]")

                last_progress = progress

                material = self.model.properties._get_property("material", surface=surf_id)
                if material is None:
                    continue

                surface_data = self.model.properties._get_property("surface_thickness", surface=surf_id)
                if surface_data is None:
                    continue

                t = surface_data["surface_thickness"]
 
                Ke, Me = self.element_2d.elementary_matrices(el_index, material, t)

                if np.sum(Ke) == 0.:

                    for node_id in connect_nodes:
                        if node_id not in aux_nodes:
                            aux_nodes.append(node_id)

                data_K_fe[el_index, :, :] = Ke
                data_M_fe[el_index, :, :] = Me

            self.data_K = np.append(self.data_K, data_K_fe.flatten())
            self.data_M = np.append(self.data_M, data_M_fe.flatten())

            if aux_nodes:
                from vibra import app
                app().main_window.selection.set_mesh_selection(nodes=aux_nodes)

    def assemble_global_matrices(self):

        _stiffness_matrix_full = csr_matrix((self.data_K, (self.ind_rows, self.ind_cols)), shape=(self.total_dof, self.total_dof))
        _mass_matrix_full = csr_matrix((self.data_M, (self.ind_rows, self.ind_cols)), shape=(self.total_dof, self.total_dof))

        self.process_prescribed_dof_data()

        if len(self.active_2d_element_dof):
            self.unprescribed_shell_dof = np.intersect1d(self.unprescribed_dof_indices, self.active_2d_element_dof)
            self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_shell_dof, :][:, self.unprescribed_shell_dof]
            self.mass_matrix = _mass_matrix_full[self.unprescribed_shell_dof, :][:, self.unprescribed_shell_dof]

        else:

            self.mass_matrix = _mass_matrix_full[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]
            self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]
            
            if self.prescribed_dof_indices:
                self.mass_matrix = _mass_matrix_full[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]
                self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]

            else:
                self.mass_matrix = _mass_matrix_full
                self.stiffness_matrix = _stiffness_matrix_full

        self.mass_matrix_r = _mass_matrix_full[:, self.prescribed_dof_indices]
        self.stiffness_matrix_r = _stiffness_matrix_full[:, self.prescribed_dof_indices]

    def process_assemble(self, reorder: bool=True, stacked_matrices: bool=True, **kwargs):

        logging.info("Gathering data to assemble global matrices... [10/100]")
        self.define_structural_elements()
        self.update_number_of_frequencies()
        self.model.process_surface_thickness()

        logging.info("Gathering data to assemble global matrices... [20/100]")
        t0 = time()
        if self.compute_data_to_process_global_matrices(reorder=reorder):
            return
        dt = time() - t0
        print(f"Elapsed time to process data to assemble global matrices: {round(dt, 4)} [s]")

        logging.info("Assembling global matrices... [50/100]")
        t0 = time()
        self.assemble_global_matrices()
        dt = time() - t0
        print(f"Elapsed time to assemble the global stiffness matrix: {round(dt, 4)} [s]")

        A = self.process_structural_nodal_loads()
        B = self.process_distributed_loads()

        self.structural_loads = A + B

    def reinsert_the_prescribed_dof(self, solution, modal_analysis=False):
        """
        This method reinsert the value of the prescribed degree of freedom in the solution.

        Parameters
        ----------
        solution : array
            Solution data from the direct method, modal superposition or modal shapes from modal analysis.

        modal_analysis : boll, optional
            True if the modal analysis was evaluated.

        Returns
        ----------
        array
            Solution of all the degrees of freedom.
        """

        rows = self.total_dof
        cols = solution.shape[1]
        full_solution = np.zeros((rows, cols), dtype=complex)

        if len(self.prescribed_dof_indices):
            if modal_analysis:
                full_solution[self.prescribed_dof_indices, :] = np.zeros((len(self.prescribed_dof_indices), cols))
            else:
                full_solution[self.prescribed_dof_indices, :] = self.array_prescribed_values[:, 0:cols]

        if len(self.active_2d_element_dof):
            full_solution[self.unprescribed_shell_dof, :] = solution

        else:
            full_solution[self.unprescribed_dof_indices, :] = solution

        return full_solution
    
    def reinsert_the_prescribed_dof_into_solution_freq(self, solution: np.ndarray, freq_index: int):
        rows = self.total_dof
        full_solution = np.zeros(rows, dtype=complex)

        if len(self.prescribed_dof_indices):
            full_solution[self.prescribed_dof_indices] = self.array_prescribed_values[:, freq_index]

        if len(self.active_2d_element_dof):
            full_solution[self.unprescribed_shell_dof] = solution

        else:
            full_solution[self.unprescribed_dof_indices] = solution

        return full_solution

    def get_prescribed_dof_model_excitation(self, index: int = 0):
        """
        This method adds the effects of prescribed acoustic pressure into mass flow global vector.

        Parameter
        ---------
        index: int, optional
        It corresponds to the frequency index.

        Returns
        -------
        f_eq: np.ndarray
        The array of equivalent prescribed dof model excitation from
        i-th frequency index.
        """

        if np.sum(self.array_prescribed_values) == 0:
            return 0.

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        alpha, beta, eta = self.model.analysis_setup.global_damping

        frequencies = self.model.frequencies
        omega = 2 * np.pi * frequencies[index]

        values = self.array_prescribed_values[:, index]

        self.Kr = self.stiffness_matrix_r
        self.Mr = self.mass_matrix_r

        Kr_add = self.Kr @ values
        Mr_add = self.Mr @ values

        f_eq = (1 + 1j*(eta + omega * beta)) * Kr_add + (-(omega**2) + 1j*(omega * alpha)) * Mr_add

        if len(self.active_2d_element_dof):
            unprescribed_indices = self.unprescribed_shell_dof
        else:
            unprescribed_indices = self.unprescribed_dof_indices

        return f_eq[unprescribed_indices]

    def get_prescribed_dof_model_excitation_reference(self, freq_dependent: bool = False):
        """
        This method adds the effects of prescribed acoustic pressure into mass flow global vector.

        Returns
        ----------
        array
            F_eq. Each column corresponds to a frequency of analysis.
        """

        if np.sum(self.array_prescribed_values) == 0:
            return 0.

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        alpha, beta, eta = self.model.global_damping
        frequencies = self.model.frequencies

        if len(self.active_2d_element_dof):
            unprescribed_indices = self.unprescribed_shell_dof
        else:
            unprescribed_indices = self.unprescribed_dof_indices

        Kr = (self.stiffness_matrix_r.toarray())[unprescribed_indices, :]
        Mr = (self.mass_matrix_r.toarray())[unprescribed_indices, :]

        logging.info(f"Processing prescribed dof model excitation... [10/{len(frequencies)}]")

        rows = Kr.shape[0]
        if freq_dependent:
            cols = 1
            f_eq = np.zeros(rows, dtype=complex)

        else:
            cols = len(frequencies)
            f_eq = np.zeros((rows, cols), dtype=complex)

        for i, freq in enumerate(frequencies):
            #
            logging.info(f"Processing prescribed dof model excitation... [{i + 10}/{len(frequencies) + 10}]")
            #
            Kr_add = np.sum((Kr * self.array_prescribed_values[:, i]), axis=1)
            Mr_add = np.sum((Mr * self.array_prescribed_values[:, i]), axis=1)
            #
            omega = 2 * np.pi * freq
            f_Kadd = Kr_add
            f_Madd = -(omega**2) * Mr_add
            f_Cadd = 1j * ((eta + omega * beta) * Kr_add + (omega * alpha) * Mr_add)
            f_eq[:, i] = f_Madd + f_Cadd + f_Kadd

        logging.info("Processing prescribed dof model excitation... [100/100]")

        return f_eq

    
    def get_combined_nodal_loads_vector(self, index: int):

        structural_loads = self.structural_loads
        
        f_eq = self.get_prescribed_dof_model_excitation(index=index)
        f = structural_loads[:, index] - f_eq

        return f

    def build_harmonic_system(self, freq, i):
        omega = 2 * np.pi * freq

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        alpha, beta, eta = self.model.global_damping

        M = self.mass_matrix
        K = self.stiffness_matrix

        f = self.get_combined_nodal_loads_vector(index=i)

        A = (-(omega**2) + 1j*(omega * alpha)) * M + (1 + 1j*(eta + omega * beta)) * K

        is_complex = np.any(np.iscomplex(A.data)) or np.any(np.iscomplex(f))
        if not is_complex:
            A.data = np.real(A.data)
            f = np.real(f)

        return A, f

    def build_eigenproblem_system(self):
        K = self.stiffness_matrix
        M = self.mass_matrix
        
        is_complex = np.any(np.iscomplex(K.data)) or np.any(np.iscomplex(M.data))
        if not is_complex:
            K.data = np.real(K.data)
            M.data = np.real(M.data)

        return K, M, True