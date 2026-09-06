import logging
import sys
from collections import defaultdict
from dataclasses import dataclass
from time import time

import numpy as np
from scipy.sparse import csr_matrix
from tqdm import tqdm

from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.engine.assemblers.structural.structural_excitations_assembler import StructuralExcitationsAssembler
from vibra.engine.model import Model
from vibra.engine.properties.material import Material


@dataclass
class DistributedMassData:
    element_ids: np.ndarray
    connectivities: np.ndarray
    pdata_values: np.ndarray | dict


class StructuralAssembler:
    def __init__(self, model : Model):

        self.model = model
        self.properties = model.properties

        self.reset()

        self.excitations_assembler = StructuralExcitationsAssembler(self)


    def reset(self):
        self.frequencies = None
        self.mass_matrix = None
        self.stiffness_matrix = None

        self.prescribed_dof_values = {}
        self.array_prescribed_values = np.array([])

        self.displacement_dof = np.array([])
        self.prescribed_dof_indices = None
        self.unprescribed_dof_indices = None

        self.surface_data_for_shell_elements = {}
        self.material_from_volume = {}

        self.mass_matrix = None
        self.mass_matrix_r = None
        self.stiffness_matrix = None
        self.stiffness_matrix_r = None
        self.structural_load = None


    @property
    def number_3d_elements(self):
        return self.model.domains_processor.number_3d_structural_elements


    @property
    def structural_dofs_indices(self):
        return self.model.domains_processor.structural_dofs_indices


    def define_structural_elements(self):
        self.model.set_structural_elements()
        self.element_1d = self.model.structural_element_1d
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


    def get_property_data_for_selected_property(self, selected_property: str) -> dict[int, np.ndarray]:
        """
        This method returns, for a given property, the integrated 
        property-related data in array format.
        """
        output_data = defaultdict(int)

        for (property, surface_id), data in self.properties.surface_properties.items():
            if property != selected_property:
                continue

            if not isinstance(data, dict):
                continue

            element_integration = data.get("element_integration", True)
            if property == "nodal_loads" and element_integration:
                continue

            nodes = self.model.mesh.get_nodes_from_surface(surface_id)
            if nodes is None:
                continue

            _nodes = self.model.get_mapped_nodes(nodes, "structural")

            property_data_from_nodes = self.model.get_structural_property_data_from_nodes(_nodes, data, "surfaces")
            for gdof, p_data in property_data_from_nodes.items():
                output_data[gdof] += p_data

        for (property, line_id), data in self.properties.line_properties.items():
            if property != selected_property:
                continue

            element_integration = data.get("element_integration", True)
            if property == "nodal_loads" and element_integration:
                continue

            nodes = self.model.mesh.get_nodes_from_line(line_id)
            if nodes is None:
                continue

            _nodes = self.model.get_mapped_nodes(nodes, "structural")

            property_data_from_nodes = self.model.get_structural_property_data_from_nodes(_nodes, data, "lines")
            for gdof, p_data in property_data_from_nodes.items():
                output_data[gdof] += p_data

        for (property, point_id), data in self.properties.point_properties.items():
            if property != selected_property:
                continue

            node_id = self.model.mesh.nodes_from_points.get(point_id)
            if node_id is None:
                continue

            _nodes = self.model.get_mapped_nodes(node_id, "structural")
            # _nodes = np.array([node_id], dtype=int)
            property_data_from_nodes = self.model.get_structural_property_data_from_nodes(_nodes, data, "points")
            for gdof, p_data in property_data_from_nodes.items():
                output_data[gdof] += p_data

        for (property, node_id), data in self.properties.nodal_properties.items():
            if property != selected_property:
                continue

            _nodes = self.model.get_mapped_nodes(node_id, "structural")
            # _nodes = np.array([node_id], dtype=int)
            property_data_from_nodes = self.model.get_structural_property_data_from_nodes(_nodes, data, "nodes")
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
        get_prescribed_indices : Indexes of the structural degrees of freedom with prescribed displacement or rotation boundary conditions.

        get_unprescribed_indices : Indexes of the structural free degrees of freedom.
        """

        try:

            property_data = {}
            for gdof in data:
                value = data[gdof]

                aux_ones = np.ones(self.number_frequencies, dtype=complex)
                if isinstance(value, complex):
                    property_data[gdof] = aux_ones * value

                elif isinstance(value, np.ndarray):
                    property_data[gdof] = value[: self.number_frequencies]

        except Exception as _error_log:
            print(str(_error_log))

        return property_data


    def reorder_property_data_based_on_gdof(self, input_property_data: dict):

        output_property_data = {}
        ordered_gdof = np.sort(list(input_property_data.keys()))
        for gdof in ordered_gdof:
            output_property_data[gdof] = input_property_data[gdof]

        return output_property_data


    def process_prescribed_dof_data(self):

        input_prescribed_dof_data = self.get_property_data_for_selected_property("prescribed_dof")
        output_prescribed_dof_data = self.reorder_property_data_based_on_gdof(input_prescribed_dof_data)
        self.prescribed_dof_values = self.process_property_arrays(output_prescribed_dof_data)

        self.prescribed_dof_indices = list(self.prescribed_dof_values.keys())
        self.array_prescribed_values = np.array(list(self.prescribed_dof_values.values()), dtype=complex)


    def process_unprescribed_indices(self):
        """ 
        Returns the unprescribed dof indices.
        """
        all_indices = np.arange(self.model.domains_processor.total_str_dofs, dtype=int)
        self.unprescribed_dof_indices = np.delete(all_indices, self.prescribed_dof_indices)


    def process_dofs_indices(self):
        self.process_prescribed_dof_data()
        self.process_unprescribed_indices()


    def get_displacement_dof(self):
        """
        This method returns the displacement dof from
        3d solid elements if there is any volume or
        the 2d face elements, otherwise.
        """
        if self.model.mesh.solids_connectivity.size:
            return self.structural_dofs_indices

        else:
            nodes_from_2d_elements = np.array([*set(self.model.mesh.faces_connectivity[:, 4:].flatten())], dtype=int)

            dof = self.element_2d.dof_per_node
            local_dof_2d = np.arange(self.element_2d.dof_per_node, dtype=int)            
            displacement_ldof_2d = local_dof_2d[0 : int(self.element_2d.dof_per_node / 2)]

            displacement_dof_from_2d_elements = dof * nodes_from_2d_elements.reshape(-1, 1) + displacement_ldof_2d
            displacement_dof = displacement_dof_from_2d_elements.flatten()

        return displacement_dof


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

        try:

            values_list = []
            aux_ones = np.ones(self.number_frequencies, dtype=complex)
            aux_zeros = np.zeros(self.number_frequencies, dtype=complex)

            for value in values:

                if value is None:
                    values_list.append(aux_zeros)

                elif isinstance(value, complex):
                    values_list.append(aux_ones * value)

                elif isinstance(value, np.ndarray):
                    values_list.append(value[: self.number_frequencies])

        except Exception as _error_log:
            print(str(_error_log))
            return aux_ones
        
        array_of_values = np.array(values_list, dtype=complex)

        # filter values based on frequency mask
        if array_of_values.shape[1] - self.number_frequencies:
            return array_of_values[self.model.solution_steps_mask, :]

        return array_of_values


    def process_material_from_volumes(self):
        """
        This method maps the materials against each volume.
        """
        self.material_from_volume.clear()

        for vol_id in self.model.mesh.elements_from_volume:
            material = self.properties._get_property("material", volume=vol_id)
            if isinstance(material, Material):
                self.material_from_volume[vol_id] = material


    def get_distributed_mass_data_for_2d_element_integration(self) -> DistributedMassData | None:
        """ 
        This method processes the excitation property data for element face
        integration.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        pdata_values = {}
        connectivities = {}
        integration_data = {}

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop != "distributed_mass":
                continue

            data: dict
            mass = np.real(data.get("values"))

            surf_elements = list(self.model.mesh.elements_from_surface.get(surface_id))
            surf_connect = self.model.mesh.get_connectivity_from_surface(surface_id)
            surface_area = self.element_2d.integrate_area(surf_connect)

            # calculate the surface density
            mass_density = mass / surface_area

            # print()
            # print(f"Area: {surface_area} m²")
            # print(f"mass_density: {mass_density} kg/m²")
            # print()

            # mass_density = 1249.600004
            # mass_density = 2060.641904

            for i, el in enumerate(surf_elements):
                connectivities[el] = surf_connect[i]
                pdata_values[el] = mass_density

        if connectivities:

            integration_data = {
                "element_ids" : np.array(list(connectivities.keys()), dtype=int),
                "connectivities" : np.array(list(connectivities.values()), dtype=int),
                "pdata_values" : np.array(list(pdata_values.values()), dtype=float),
                }

            return DistributedMassData(**integration_data)


    def get_distributed_mass_data_for_1d_element_integration(self) -> DistributedMassData | None:
        """ 
        This method processes the excitation property data for element face
        integration.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        pdata_values = {}
        connectivities = {}
        integration_data = {}

        for key, data in self.properties.line_properties.items():

            prop, line_id = key
            if prop != "distributed_mass":
                continue

            data: dict
            mass = np.real(data.get("values"))

            line_elements = list(self.model.mesh.elements_from_line.get(line_id))
            line_connect = self.model.mesh.get_connectivity_from_line(line_id)
            line_length = self.element_1d.integrate_length(line_connect)

            # calculate the line density
            line_density = mass / line_length

            for i, el in enumerate(line_elements):
                connectivities[el] = line_connect[i]
                pdata_values[el] = line_density

        if connectivities:

            integration_data = {
                "element_ids" : np.array(list(connectivities.keys()), dtype=int),
                "connectivities" : np.array(list(connectivities.values()), dtype=int),
                "pdata_values" : np.array(list(pdata_values.values()), dtype=float),
                }

            return DistributedMassData(**integration_data)


    def process_surface_data_for_shell_elements(self):
        """
        This method maps the surface data against each surface.
        """
        self.surface_data_for_shell_elements.clear()

        for surf_id in self.model.mesh.elements_from_surface:
            
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


    def compute_data_to_process_global_matrices_for_shell_elements(self, reorder: bool = True, print_log: bool = False):
        """
        Calculates global matrices.
        """

        self.ind_rows, self.ind_cols = self.element_2d.generate_ind_rows_cols(reorder=reorder)

        self.dof = self.element_2d.dof_per_element
        self.number_2d_elements = len(self.element_2d.connectivity)

        self.total_dof = self.element_2d.dof_per_node * len(self.element_2d.nodal_coordinates)

        self.displacement_dof = self.get_displacement_dof()
    
        self.data_K = np.zeros((self.number_2d_elements, self.dof, self.dof), dtype=complex)
        self.data_M = np.zeros((self.number_2d_elements, self.dof, self.dof), dtype=complex)

        # initialize variable
        last_progress = 0

        # loop for 2d elements
        with tqdm(
            self.model.mesh.faces_connectivity,
            desc="Processing the elementary matrices data for face elements",
            unit="element",
            file=sys.stdout,
            disable=not print_log,
        ) as progress_bar:
            for element_id, surf_id, _, _, *connect_nodes in progress_bar:
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


    def compute_data_to_process_global_matrices_for_solid_elements(self, reorder: bool = True, print_log: bool = False):
        """
        Calculates global matrices.
        """

        self.active_2d_element_dof = []
        self.dof = self.element_3d.dof_per_element

        self.ind_rows, self.ind_cols, _ = self.element_3d.generate_ind_rows_cols(reorder=reorder)

        self.displacement_dof = self.get_displacement_dof()

        self.data_K = np.zeros((self.number_3d_elements, self.dof, self.dof), dtype=complex)
        self.data_M = np.zeros((self.number_3d_elements, self.dof, self.dof), dtype=complex)

        # initialize variable
        last_progress = 0

        # with tqdm(
        #     self.model.mesh.solids_connectivity,
        #     desc="Processing the elementary matrices data for solid elements",
        #     unit="element",
        #     file=sys.stdout,
        #     disable=not print_log,
        # ) as progress_bar:

        # loop for 3d elements
        for index, element_id in enumerate(self.model.domains_processor.elements_of_domain.get("structural", [])):

            if self.model.stop_processing:
                return True

            progress = int((100 * (index / self.number_3d_elements) // 5) * 5)
            if progress != last_progress:
                logging.info(f"Processing the elementary matrices data for solid elements... [{int(progress)}/100]")

            last_progress = progress

            # get the volume of the 3D element
            vol_id = self.model.mesh.solids_connectivity[element_id, 1]

            # material from volume
            material = self.material_from_volume.get(vol_id)
            if material is None:
                print(f"-> Element without material: {element_id}")
                continue

            Ke, Me = self.element_3d.elementary_matrices(element_id, material)
            self.data_K[index, :, :] = Ke
            self.data_M[index, :, :] = Me


    def compute_data_to_process_global_matrices(self, reorder: bool = True, print_log: bool = False):
        """
        This method preprocesses all the required data to assemble the global matrices.
        """
        if self.model.mesh.solids_connectivity.size:
            self.process_material_from_volumes()
            self.compute_data_to_process_global_matrices_for_solid_elements(reorder=reorder, print_log=print_log)

        else:
            self.process_surface_data_for_shell_elements()
            self.compute_data_to_process_global_matrices_for_shell_elements(reorder=reorder, print_log=print_log)

        self.process_dofs_indices()


    def assemble_distributed_mass_matrix_for_lines(self):

        integration_data_1d = self.get_distributed_mass_data_for_1d_element_integration()
        if integration_data_1d is None:
            return

        connectivities = integration_data_1d.connectivities
        pdata_values = integration_data_1d.pdata_values

        n_el = len(connectivities)
        e_dofs = self.element_1d.dof_per_element
        data_Mdist = np.zeros((n_el, e_dofs, e_dofs), dtype=float)

        ind_rows, ind_cols = self.element_1d.get_rows_and_cols_indices_2D(connectivities)

        for i, surface_density in enumerate(pdata_values):
            data_Mdist[i, :, :] = self.element_1d.integrate_distributed_mass(i, surface_density)

        self.mass_matrix += csr_matrix((data_Mdist.flatten(), (ind_rows, ind_cols)), shape=self.model.gm_shape)


    def assemble_distributed_mass_matrix_for_surfaces(self):

        integration_data_2d = self.get_distributed_mass_data_for_2d_element_integration()
        if integration_data_2d is None:
            return

        connectivities = integration_data_2d.connectivities
        pdata_values = integration_data_2d.pdata_values

        n_el = len(connectivities)
        e_dofs = self.element_2d.dof_per_element
        data_Mdist = np.zeros((n_el, e_dofs, e_dofs), dtype=float)

        ind_rows, ind_cols = self.element_2d.get_rows_and_cols_indices_2D(connectivities)

        for i, surface_density in enumerate(pdata_values):
            data_Mdist[i, :, :] = self.element_2d.integrate_distributed_mass(i, surface_density)

        self.mass_matrix += csr_matrix((data_Mdist.flatten(), (ind_rows, ind_cols)), shape=self.model.gm_shape)


    def assemble_global_mass_matrix(self):
        """
        This method assembles the global mass matrix.
        """
        self.mass_matrix = csr_matrix((self.data_M.flatten(), (self.ind_rows, self.ind_cols)), shape=self.model.gm_shape)

        self.assemble_distributed_mass_matrix_for_lines()
        self.assemble_distributed_mass_matrix_for_surfaces()

        if self.model.drop_domain:
            self.mass_matrix = self.mass_matrix[self.structural_dofs_indices, :][:, self.structural_dofs_indices]

        self.mass_matrix_r = self.mass_matrix[:, self.prescribed_dof_indices]

        if self.prescribed_dof_indices:
            self.mass_matrix = self.mass_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def assemble_global_stiffness_matrix(self, print_log: bool=False):
        """
        This method assembles the global stiffness matrix.
        """
        self.stiffness_matrix = csr_matrix((self.data_K.flatten(), (self.ind_rows, self.ind_cols)), shape=self.model.gm_shape)

        if self.model.drop_domain:
            self.stiffness_matrix = self.stiffness_matrix[self.structural_dofs_indices, :][:, self.structural_dofs_indices]

        self.stiffness_matrix_r = self.stiffness_matrix[:, self.prescribed_dof_indices]

        if self.prescribed_dof_indices:
            self.stiffness_matrix = self.stiffness_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def assemble_global_matrices(self, reorder: bool = True, print_log: bool = False):
        """
        This method assembles the global matrices of the structural model.
        """

        if not self.model.volumes_of_domain:
            self.model.domains_processor.update_domains_mappings()

        logging.info("Gathering data to assemble global matrices... [10/100]")
        self.define_structural_elements()
        self.update_number_of_frequencies()
        self.model.process_surface_thickness()

        logging.info("Gathering data to assemble global matrices... [20/100]")
        t0 = time()
        if self.compute_data_to_process_global_matrices(reorder=reorder, print_log=print_log):
            return
        dt = time() - t0
        if print_log:
            print(f"Elapsed time to process data to assemble global matrices: {dt : .6f} [s]")

        if self.model.stop_processing:
            return

        logging.info("Assembling the global stiffness matrix... [50/100]")
        t0 = time()
        self.assemble_global_stiffness_matrix()
        dt = time() - t0
        if print_log:
            print(f"Elapsed time to assemble the global stiffness matrix: {dt : .6f} [s]")

        logging.info("Assembling the global mass matrix... [60/100]")
        t0 = time()
        self.assemble_global_mass_matrix()
        dt = time() - t0
        if print_log:
            print(f"Elapsed time to assemble the global mass matrix: {dt : .6f} [s]")


    def assemble_global_matrices_and_excitations(self, reorder: bool = True, print_log: bool = False):
        """
        This method assembles the global matrices and excitations of the structural model.
        """
        self.assemble_global_matrices(reorder=reorder, print_log=print_log)
        self.structural_load = self.excitations_assembler.assemble_model_excitations()


    def build_harmonic_system(self, freq: float, index: int):
        omega = 2 * np.pi * freq

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        alpha, beta, eta = self.model.global_damping

        M = self.mass_matrix
        K = self.stiffness_matrix

        f = self.excitations_assembler.get_combined_nodal_loads_vector(index=index)

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


    def reinsert_the_prescribed_dof(self, solution, modal_analysis: bool = False):
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

        rows = len(solution) + len(self.prescribed_dof_indices)
        cols = solution.shape[1]

        full_solution = np.zeros((rows, cols), dtype=complex)

        if len(self.prescribed_dof_indices):
            if modal_analysis:
                full_solution[self.prescribed_dof_indices, :] = np.zeros((len(self.prescribed_dof_indices), cols))
            else:
                full_solution[self.prescribed_dof_indices, :] = self.array_prescribed_values[:, :cols]

        full_solution[self.unprescribed_dof_indices, :] = solution

        return full_solution
    

    def reinsert_the_prescribed_dof_into_solution_freq(self, solution: np.ndarray, freq_index: int):

        rows = len(solution) + len(self.prescribed_dof_indices)

        full_solution = np.zeros(rows, dtype=complex)
        full_solution[self.unprescribed_dof_indices] = solution

        if len(self.prescribed_dof_indices):
            full_solution[self.prescribed_dof_indices] = self.array_prescribed_values[:, freq_index]

        return full_solution