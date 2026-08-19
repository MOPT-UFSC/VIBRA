
import logging
from collections import defaultdict
from time import time

import numpy as np
from scipy.sparse import csr_matrix

from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.engine.model import Model
from vibra.engine.properties.material import Material


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
        self.prescribed_dof_indexes = np.array([])
        self.unprescribed_dof_indexes = np.array([])

        self.surface_data_for_shell_elements = dict()
        self.material_from_volume = dict()


    def define_structural_elements(self):
        self.model.set_structural_elements()
        self.element_2d = self.model.structural_element_2d
        self.element_3d = self.model.structural_element_3d


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


    def get_property_data_for_selected_property(self, selected_property: str):
        """
        """
        output_data = defaultdict(int)

        for (property, surface_id), data in self.properties.surface_properties.items():
            if property != selected_property:
                continue

            nodes = self.model.mesh.get_nodes_from_surface(surface_id)
            if nodes is None:
                continue

            property_data_from_nodes = self.model.get_structural_property_data_from_nodes(nodes, data, "surfaces")
            for gdof, p_data in property_data_from_nodes.items():
                output_data[gdof] += p_data

        for (property, line_id), data in self.properties.line_properties.items():
            if property != selected_property:
                continue

            nodes = self.model.mesh.get_nodes_from_line(line_id)
            if nodes is None:
                continue

            property_data_from_nodes = self.model.get_structural_property_data_from_nodes(nodes, data, "lines")
            for gdof, p_data in property_data_from_nodes.items():
                output_data[gdof] += p_data

        for (property, point_id), data in self.properties.point_properties.items():
            if property != selected_property:
                continue

            node_id = self.model.mesh.nodes_from_points.get(point_id)
            if node_id is None:
                continue

            _node_id = np.array([node_id], dtype=int)
            property_data_from_nodes = self.model.get_structural_property_data_from_nodes(_node_id, data, "points")
            for gdof, p_data in property_data_from_nodes.items():
                output_data[gdof] += p_data

        for (property, node_id), data in self.properties.nodal_properties.items():
            if property != selected_property:
                continue

            nodes = np.array([node_id], dtype=int)
            property_data_from_nodes = self.model.get_structural_property_data_from_nodes(nodes, data, "nodes")
            for gdof, p_data in property_data_from_nodes.items():
                output_data[gdof] += p_data

        return output_data


    def process_property_arrays(self, data: dict):
        """
        This method returns all the values of the structural degrees of freedom with prescribed structural displacement or rotation boundary conditions.

        Returns
        ----------
        array
            Values of the structural degrees of freedom with prescribed displacement or rotation boundary conditions.

        See also
        --------
        get_prescribed_indexes : Indexes of the structural degrees of freedom with prescribed displacement or rotation boundary conditions.

        get_unprescribed_indexes : Indexes of the structural free degrees of freedom.
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

        self.prescribed_dof_indexes = list(output_prescribed_dof_data.keys())
        self.unprescribed_dof_indexes = self.get_unprescribed_indexes()


    def get_unprescribed_indexes(self):
        """ 
        Returns the unprescribed dof indexes.
        """
        all_indexes = np.arange(self.total_dof, dtype=int)
        return np.delete(all_indexes, self.prescribed_dof_indexes)


    def get_matrices_dropping_indexes(self):
        return self.unprescribed_dof_indexes, self.prescribed_dof_indexes


    def get_prescribed_dof_values(self):
        return self.prescribed_dof_values, self.array_prescribed_values
    

    def get_displacement_dof(self):
        """
        This method returns the displacement dof from
        3d solid elements if there is any volume or
        the 2d face elements, otherwise.
        """
        if self.model.mesh.solids_connectivity.size:
            displacement_dof = np.arange(self.total_dof, dtype=int)

        else:
            nodes_from_2d_elements = np.array([*set(self.model.mesh.faces_connectivity[:, 4:].flatten())], dtype=int)

            dof = self.element_2d.DOF_PER_NODE
            local_dof_2d = np.arange(self.element_2d.DOF_PER_NODE, dtype=int)            
            displacement_ldof_2d = local_dof_2d[0 : int(self.element_2d.DOF_PER_NODE / 2)]

            displacement_dof_from_2d_elements = dof * nodes_from_2d_elements.reshape(-1, 1) + displacement_ldof_2d
            displacement_dof = displacement_dof_from_2d_elements.flatten()

        return displacement_dof


    def get_structural_excitations_by_nodal_attribution(self):

        input_nodal_loads_data = self.get_property_data_for_selected_property("nodal_loads")
        output_nodal_loads_data = self.reorder_property_data_based_on_gdof(input_nodal_loads_data)
        nodal_loads, _ = self.process_property_arrays(output_nodal_loads_data)

        # self.nodal_loads_indexes = list(output_nodal_loads_data.keys())
        output = np.zeros((self.total_dof, self.number_frequencies), dtype=complex)

        if nodal_loads:
            indexes = list(nodal_loads.keys())
            excitation = list(nodal_loads.values())
            output[indexes, :] = np.array(excitation)

        if self.prescribed_dof_indexes:
            return output[self.unprescribed_dof_indexes, :]

        return output


    def process_loads_arrays(self, values: list[np.ndarray | None]):
        """
        For a given list of values, this method returns an output list of two-dimensional 
        arrays whose columns have the same size as the frequencies vector.

        Parameters
        ----------
        values: list
            The input values list to be converted.

        Returns
        -------
        array_of_values: np.ndarray
            The output two-bidimensional array vector whose columns
            have the same size as the frequencies vector.
        """

        if self.frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)

        try:

            values_list = []
            aux_ones = np.ones(number_frequencies, dtype=complex)
            aux_zeros = np.zeros(number_frequencies, dtype=complex)

            for value in values:

                if value is None:
                    values_list.append(aux_zeros)

                elif isinstance(value, complex):
                    values_list.append(aux_ones * value)

                elif isinstance(value, np.ndarray):
                    values_list.append(value[:number_frequencies])

        except Exception as _error_log:
            print(str(_error_log))
            # TODO: check matrix dimensions for compatibility
            return aux_ones
        
        array_of_values = np.array(values_list, dtype=complex)

        # filter values based on frequency mask
        if array_of_values.shape[1] - self.frequencies.size:
            return array_of_values[self.model.solution_steps_mask, :]

        return array_of_values


    # def get_value_in_array_form(
    #         self, 
    #         value: float | np.ndarray, 
    #         flatten: bool = False, 
    #         filter_frequencies: bool=True,
    #         ) -> np.ndarray:
    #     """
    #     This method returns, for a given input value, an output vector with 
    #     the same length as the frequencies vector.

    #     Parameters
    #     ----------
    #     value: float or np.ndarray
    #         The input value to be converted in array with
    #         the same length as the frequencies vector.
        
    #     flatten: bool, optional
    #         Controls whether the output vector will be flattened or not.

    #     Returns
    #     -------
    #     output_vector: np.ndarray
    #         The output vector with the same length as the frequencies
    #         vector.
    #     """

    #     aux_ones = np.ones((1, self.number_frequencies), dtype=complex)

    #     if isinstance(value, complex | float):
    #         output_vector = value * aux_ones

    #     elif isinstance(value, np.ndarray):
    #         if value.shape[0] == 1:
    #             output_vector = value * aux_ones

    #         elif len(value.shape) == 1:
    #             output_vector = value.reshape(1, -1)

    #         else:
    #             output_vector = value

    #     if filter_frequencies:
    #         if (output_vector.shape[1] - self.number_frequencies) and self.model.solution_steps_mask:
    #             # filter values based on the solution steps mask
    #             output_vector = output_vector[:, self.model.solution_steps_mask]

    #     return output_vector.flatten() if flatten else output_vector


    def get_excitation_data_for_element_integration(self, property_label: str) -> dict:
        """ 
        This method processes the excitation property data for element face
        integration.

        Parameters
        ----------
        property_label: str
            The property label on which the surface data will be processed.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        aux_data = {}
        aux_connect = {}
        integration_data = {}

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop != property_label:
                continue

            data: dict

            if property_label in ["normal_pressure_load", "nodal_loads", "distributed_load"]:
                element_type = data.get("element_type")
                if element_type == "2d_element":
                    continue

            if data.get("nodal_distribution", False):
                continue

            complex_values = data.get("values")

            # normalize data type to array
            complex_values_array = self.process_loads_arrays(complex_values)

            surf_elements = list(self.model.mesh.elements_from_surface.get(surface_id))
            surf_connect = self.model.mesh.get_connectivity_from_surface(surface_id)

            if property_label == "nodal_loads":
                surface_area = self.element_2d.integrate_area(surf_connect)
                complex_values_array /= surface_area

            # print(surface_id, surface_area)
            # print(complex_values_array / surface_area)
            # print(complex_values_array.shape)

            for i, el in enumerate(surf_elements):
                aux_connect[el] = surf_connect[i]
                aux_data[el] = complex_values_array

        if aux_connect:

            integration_data = {
                "element_ids" : np.array(list(aux_connect.keys()), dtype=int),
                "connectivities" : np.array(list(aux_connect.values()), dtype=int),
                "surface_data" : aux_data,
                # "surface_data" : np.array(list(aux_data.values()), dtype=complex),
                }

        return integration_data


    def get_structural_excitations_by_element_integration_2d(self):
        """ 
        This method processes the acoustic model excitations and
        returns the output data in the form of mass flow rate.
        """

        total_dof = self.element_2d.dof_per_node * len(self.element_2d.nodal_coordinates)
        load_vectors = np.zeros((total_dof, self.number_frequencies), dtype=complex)

        prop_labels = [
            "nodal_loads",
            "normal_pressure_load",
            "distributed_loads",
        ]

        for prop_label in prop_labels:

            integration_data = self.get_excitation_data_for_element_integration(prop_label)
            if not integration_data:
                continue

            match prop_label:
                case "normal_pressure_load":
                    load_vectors = self.integrate_normal_pressure_load(integration_data, load_vectors)

                case "distributed_loads" | "nodal_loads":
                    load_vectors = self.integrate_distributed_load(integration_data, load_vectors)

        if self.prescribed_dof_indexes:
            return load_vectors[self.unprescribed_dof_indexes, :]

        return load_vectors


    def integrate_normal_pressure_load(self, integration_data: dict, load_vectors: np.ndarray):

        element_ids = integration_data.get("element_ids")
        connectivities = integration_data.get("connectivities")
        surface_data: dict = integration_data.get("surface_data")

        surface_elements_connectivities = self.model.mesh.faces_connectivity[element_ids, :]
        elements_normals = self.model.mesh.get_element_face_normal_batched(surface_elements_connectivities)

        self.element_2d.reorder_connect(connectivities)
        for i, complex_values in enumerate(surface_data.values()):
            indices = self.element_2d.element_indexes(i)
            e_normal = elements_normals[i, :].reshape(-1, 1)
            load_vectors[indices, :] += self.element_2d.integrate_normal_pressure_load(i, e_normal, complex_values)

        return load_vectors


    def integrate_distributed_load(self, integration_data: dict, load_vectors: np.ndarray):

        # element_ids = integration_data.get("element_ids")
        connectivities = integration_data.get("connectivities")
        surface_data: dict = integration_data.get("surface_data")

        self.element_2d.reorder_connect(connectivities)
        for i, complex_values in enumerate(surface_data.values()):
            indices = self.element_2d.element_indexes(i)
            load_vectors[indices, :] += self.element_2d.integrate_distributed_load(i, complex_values)

        return load_vectors


    def process_distributed_loads(self):

        output = np.zeros((self.total_dof, self.number_frequencies), dtype=complex)

        for (property, surface_id), data in self.properties.surface_properties.items():
            if property not in ["distributed_loads", "normal_pressure_loads"]:
                continue

            if data.get("element_type") != "element_2d":
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
                    if data.get("element_type") == "2d_element":
                        g_dof, F_elem = self.element_2d.process_forces_for_normal_pressure_load(connect, normal_pressure)
                    else:
                        print("passei B")
                        g_dof, F_elem = self.element_2d.normal_pressure_load(connect, normal_pressure)

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

        if self.prescribed_dof_indexes:
            return output[self.unprescribed_dof_indexes, :]

        return output


    def process_material_from_volumes(self):
        """
        This method maps the materials against each volume.
        """
        self.material_from_volume.clear()

        for vol_id in self.model.mesh.elements_from_volume.keys():
            material = self.properties._get_property("material", volume=vol_id)
            if isinstance(material, Material):
                self.material_from_volume[vol_id] = material


    def process_surface_data_for_shell_elements(self):
        """
        This method maps the surface data against each surface.
        """
        self.surface_data_for_shell_elements.clear()

        for surf_id in self.model.mesh.elements_from_surface.keys():
            
            material = self.properties._get_property("material", surface=surf_id)
            if material is None:
                continue
            
            surface_data = self.properties._get_property("surface_thickness", surface=surf_id)
            if surface_data is None:
                continue

            if isinstance(surface_data, dict) and isinstance(material, Material):
                self.surface_data_for_shell_elements[surf_id] = {
                    "material" : material,
                    "surface_data" : surface_data
                }


    def compute_data_to_process_global_matrices_for_shell_elements(self, reorder: bool = True):
        """
        Calculates global matrices.
        """

        self.ind_rows, self.ind_cols = self.element_2d.generate_ind_rows_cols(reorder=reorder)

        self.dof = self.element_2d.DOF_PER_ELEMENT
        self.number_2d_elements = len(self.element_2d.connectivity)
        self.total_dof = self.element_2d.DOF_PER_NODE * len(self.element_2d.nodal_coordinates)

        self.displacement_dof = self.get_displacement_dof()
    
        # global_matrices shape
        self.gm_shape = (self.total_dof, self.total_dof)

        self.data_K = np.zeros((self.number_2d_elements, self.dof, self.dof), dtype=complex)
        self.data_M = np.zeros((self.number_2d_elements, self.dof, self.dof), dtype=complex)

        # initialize variable
        last_progress = 0

        # loop for 2d elements
        for element_id, surf_id, _, _, *connect_nodes in self.model.mesh.faces_connectivity:

            if self.model.stop_processing:
                return True

            progress = int(100 * (element_id / self.number_2d_elements))
            if progress != last_progress:
                logging.info(f"Processing the elementary matrices data for face elements... [{int(progress)}/100]")

            last_progress = progress

            # material from surface
            material = self.surface_data_for_shell_elements[surf_id]["material"]
            
            # material from volume
            surface_data = self.surface_data_for_shell_elements[surf_id]["surface_data"]

            Ke, Me = self.element_2d.elementary_matrices(element_id, material, surface_data.get("surface_thickness"))

            self.data_K[element_id, :, :] = Ke
            self.data_M[element_id, :, :] = Me


    def compute_data_to_process_global_matrices_for_solid_elements(self, reorder: bool = True):
        """
        Calculates global matrices.
        """

        self.active_2d_element_dof = list()

        self.ind_rows, self.ind_cols = self.element_3d.generate_ind_rows_cols(reorder=reorder)

        self.dof = self.element_3d.DOF_PER_ELEMENT
        self.number_3d_elements = len(self.element_3d.connectivity)
        self.total_dof = self.element_3d.DOF_PER_NODE * len(self.element_3d.nodal_coordinates)

        self.displacement_dof = self.get_displacement_dof()

        # global_matrices shape
        self.gm_shape = (self.total_dof, self.total_dof)

        self.data_K = np.zeros((self.number_3d_elements, self.dof, self.dof), dtype=complex)
        self.data_M = np.zeros((self.number_3d_elements, self.dof, self.dof), dtype=complex)

        # initialize variable
        last_progress = 0

        # loop for 3d elements
        for element_id, vol_id, *_ in self.model.mesh.solids_connectivity:
            
            if self.model.stop_processing:
                return True

            progress = int(100 * (element_id / self.number_3d_elements))
            if progress != last_progress:
                logging.info(f"Processing the elementary matrices data for solid elements... [{int(progress)}/100]")

            last_progress = progress

            # material from volume
            material = self.material_from_volume.get(vol_id)

            Ke, Me = self.element_3d.elementary_matrices(element_id, material)
            self.data_K[element_id, :, :] = Ke
            self.data_M[element_id, :, :] = Me


    def compute_data_to_process_global_matrices(self, reorder: bool = True):
        """
        """
        if self.model.mesh.solids_connectivity.size:
            self.process_material_from_volumes()
            self.compute_data_to_process_global_matrices_for_solid_elements(reorder = reorder)

        else:
            self.process_surface_data_for_shell_elements()
            self.compute_data_to_process_global_matrices_for_shell_elements(reorder = reorder)

        self.process_prescribed_dof_data()


    def assemble_global_stiffness_matrix(self):
        """
        This method assembles the global stiffness matrix.
        """
        _stiffness_matrix_full = csr_matrix((self.data_K.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_dof_indexes, :][:, self.unprescribed_dof_indexes]
        self.stiffness_matrix_r = _stiffness_matrix_full[:, self.prescribed_dof_indexes]


    def assemble_global_mass_matrix(self):
        """
        This method assembles the global mass matrix.
        """
        _mass_matrix_full = csr_matrix((self.data_M.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        self.mass_matrix = _mass_matrix_full[self.unprescribed_dof_indexes, :][:, self.unprescribed_dof_indexes]
        self.mass_matrix_r = _mass_matrix_full[:, self.prescribed_dof_indexes]


    def assemble_global_matrices(self, reorder: bool=True, **kwargs):
        """
        This method assembles the global matrices of the structural model.
        """

        logging.info("Gathering data to assemble global matrices... [10/100]")
        self.define_structural_elements()
        self.update_number_of_frequencies()
        self.model.process_surface_thickness()

        logging.info("Gathering data to assemble global matrices... [20/100]")
        t0 = time()
        if self.compute_data_to_process_global_matrices(reorder=reorder):
            return
        dt = time() - t0
        print(f"Elapsed time to process data to assemble global matrices: {dt : .6f} [s]")

        if self.model.stop_processing:
            return

        logging.info("Assembling global stiffness matrix... [50/100]")
        t0 = time()
        self.assemble_global_stiffness_matrix()
        dt = time() - t0
        print(f"Elapsed time to assemble the global stiffness matrix: {dt : .6f} [s]")

        logging.info("Assembling global mass matrix... [60/100]")
        t0 = time()
        self.assemble_global_mass_matrix()
        dt = time() - t0
        print(f"Elapsed time to assemble the global mass matrix: {dt : .6f} [s]")

    
    def assemble_model_excitations(self):
        """
        This method assembles the excitations of the structural model.
        """
        A = self.get_structural_excitations_by_nodal_attribution()
        B = self.get_structural_excitations_by_element_integration_2d()
        C = self.process_distributed_loads()

        self.structural_loads = A + B + C


    def assemble_global_matrices_and_excitations(self, reorder: bool=True, **kwargs):
        """
        This method assembles the global matrices and excitations of the structural model.
        """
        self.assemble_global_matrices(reorder = reorder)
        self.assemble_model_excitations()


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

        if len(self.prescribed_dof_indexes):
            if modal_analysis:
                full_solution[self.prescribed_dof_indexes, :] = np.zeros((len(self.prescribed_dof_indexes), cols))
            else:
                full_solution[self.prescribed_dof_indexes, :] = self.array_prescribed_values[:, 0:cols]

        full_solution[self.unprescribed_dof_indexes, :] = solution

        return full_solution
    

    def reinsert_the_prescribed_dof_into_solution_freq(self, solution: np.ndarray, freq_index: int):
        rows = self.total_dof
        full_solution = np.zeros(rows, dtype=complex)

        if len(self.prescribed_dof_indexes):
            full_solution[self.prescribed_dof_indexes] = self.array_prescribed_values[:, freq_index]

        full_solution[self.unprescribed_dof_indexes] = solution

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

        alpha, beta, eta = self.model.global_damping
        frequencies = analysis_setup.get_frequencies()

        omega = 2 * np.pi * frequencies[index]
        values = self.array_prescribed_values[:, index]

        self.Kr = self.stiffness_matrix_r
        self.Mr = self.mass_matrix_r

        Kr_add = self.Kr @ values
        Mr_add = self.Mr @ values

        f_eq = (1 + 1j*(eta + omega * beta)) * Kr_add + (-(omega**2) + 1j*(omega * alpha)) * Mr_add

        unprescribed_indexes = self.unprescribed_dof_indexes

        return f_eq[unprescribed_indexes]


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

        unprescribed_indexes = self.unprescribed_dof_indexes

        Kr = (self.stiffness_matrix_r.toarray())[unprescribed_indexes, :]
        Mr = (self.mass_matrix_r.toarray())[unprescribed_indexes, :]

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


    def build_harmonic_system(self, freq: float, index: int):
        omega = 2 * np.pi * freq

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        alpha, beta, eta = self.model.global_damping

        M = self.mass_matrix
        K = self.stiffness_matrix

        f = self.get_combined_nodal_loads_vector(index=index)

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