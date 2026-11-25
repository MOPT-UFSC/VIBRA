import gc
import logging
import sys
from collections import defaultdict
from dataclasses import dataclass
from time import perf_counter

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from tqdm import tqdm

from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.engine.assemblers.structural.structural_excitations_assembler import StructuralExcitationsAssembler
from vibra.engine.elements.elements_1d.structural.structural_1d_element import Structural1DElement
from vibra.engine.elements.elements_2d.structural.structural_2d_element import Structural2DElement
from vibra.engine.model import Model
from vibra.engine.properties.material import Material


@dataclass
class DistributedPropertyData:
    element_ids: np.ndarray
    connectivities: np.ndarray
    pdata_values: list[complex | np.ndarray]
    is_normal: np.ndarray


@dataclass
class SparseMatrixData:
    data: np.ndarray
    rows: np.ndarray
    cols: np.ndarray


class StructuralAssembler:
    def __init__(self, model : Model):

        self.model = model
        self.properties = model.properties

        self.reset()

        self.excitations_assembler = StructuralExcitationsAssembler(self)


    def reset(self):

        self.frequency_dependent = False
        self.frequencies = None

        self.prescribed_dof_values = {}
        self.prescribed_values = np.array([])

        self.displacement_dof = np.array([])
        self.prescribed_dof_indices = None
        self.unprescribed_dof_indices = None

        self.dampings_from_volume = {}
        self.material_from_volume = {}
        self.surface_data_for_shell_elements = {}

        # global matrices and excitation vector
        self.reset_global_matrices_attributes()
        self.reset_reduced_matrices_attributes()


    def reset_global_matrices_attributes(self):
        self.data_K = None
        self.data_M = None
        self.cols = None
        self.rows = None
        self.mass_matrix = None
        self.stiffness_matrix = None
        self.structural_local_dampings = None
        self.f_eq = None

        self.sparse_matrix_data: dict[str, SparseMatrixData] = {}


    def reset_reduced_matrices_attributes(self):
        self.mass_matrix_r = None
        self.stiffness_matrix_r = None
        self.damping_matrix_r = None


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
            # _nodes = np.array([node_id], dtype=np.int32)
            property_data_from_nodes = self.model.get_structural_property_data_from_nodes(_nodes, data, "points")
            for gdof, p_data in property_data_from_nodes.items():
                output_data[gdof] += p_data

        for (property, node_id), data in self.properties.nodal_properties.items():
            if property != selected_property:
                continue

            _nodes = self.model.get_mapped_nodes(node_id, "structural")
            # _nodes = np.array([node_id], dtype=np.int32)
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

                aux_ones = np.ones(self.number_frequencies, dtype=np.complex128)
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
        self.prescribed_values = np.array(list(self.prescribed_dof_values.values()), dtype=np.complex128)


    def process_unprescribed_indices(self):
        """ 
        Returns the unprescribed dof indices.
        """
        all_indices = np.arange(self.model.domains_processor.total_str_dofs, dtype=np.int32)
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
            nodes_from_2d_elements = np.array([*set(self.model.mesh.faces_connectivity[:, 4:].ravel())], dtype=np.int32)

            dof = self.element_2d.dof_per_node
            local_dof_2d = np.arange(self.element_2d.dof_per_node, dtype=np.int32)            
            displacement_ldof_2d = local_dof_2d[0 : int(self.element_2d.dof_per_node / 2)]

            displacement_dof_from_2d_elements = dof * nodes_from_2d_elements.reshape(-1, 1) + displacement_ldof_2d
            displacement_dof = displacement_dof_from_2d_elements.ravel()

        return displacement_dof


    def process_frequency_based_arrays(self, values: list[complex | float | np.ndarray | None], denominator: float = 1.0):
        """
        For a given list of values, this method returns an output list of two-dimensional
        arrays whose columns have the same size as the frequencies vector.

        Parameters
        ----------
        values: list
            The input values list to be converted.

        denominator: float, optional
            The denominator value used to compute the property density.

        Returns
        -------
        array_of_values: np.ndarray
            The output two-bidimensional array vector whose columns
            have the same size as the frequencies vector.
        """

        try:

            values_list = []
            n_freq = self.number_frequencies

            aux_ones = np.ones(n_freq, dtype=np.complex128)
            aux_zeros = np.zeros(n_freq, dtype=np.complex128)

            for value in values:

                if value is None:
                    values_list.append(aux_zeros)

                elif isinstance(value, complex | float):
                    values_list.append(aux_ones * value)

                elif isinstance(value, np.ndarray):
                    values_list.append(value[: n_freq])

        except Exception as _error_log:
            print(str(_error_log))
            # TODO: check matrix dimensions for compatibility
            return aux_ones

        array_of_values = np.array(values_list, dtype=np.complex128) / denominator

        # filter values based on frequency mask
        if array_of_values.shape[1] - n_freq:
            return array_of_values[self.model.solution_steps_mask, :]

        return array_of_values


    def process_material_from_volumes(self):
        """
        This method maps the materials against each volume.
        """
        self.material_from_volume.clear()
        self.dampings_from_volume.clear()

        for vol_id in self.model.mesh.elements_from_volume:
            material = self.properties._get_property("material", volume=vol_id)
            if isinstance(material, Material):
                self.material_from_volume[vol_id] = material

            dampings = self.properties._get_property("structural_local_dampings", volume=vol_id)
            if dampings is None:
                continue

            self.dampings_from_volume[vol_id] = dampings


    def get_distributed_data_for_1d_element_integration(self, property_label: str) -> DistributedPropertyData | None:
        """ 
        This method processes the foundation stiffness data for element integration.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        pdata_values = {}
        connectivities = {}
        integration_data = {}
        is_normal = {}

        for key, data in self.properties.line_properties.items():

            prop, line_id = key
            if prop != property_label:
                continue

            data: dict
            values = data.get("values")
            normal = data.get("normal", False)
            direct_input = data.get("direct_input", True)

            line_elements = list(self.model.mesh.elements_from_line.get(line_id))
            line_connect = self.model.mesh.get_connectivity_from_line(line_id)

            if direct_input:
                line_length = self.element_1d.integrate_length(line_connect)
                k_densities = self.process_frequency_based_arrays(values, denominator=line_length)
            else:
                k_densities = self.process_frequency_based_arrays(values)

            for i, el in enumerate(line_elements):
                connectivities[el] = line_connect[i]
                pdata_values[el] = k_densities
                is_normal[el] = normal

        if connectivities:

            integration_data = {
                "element_ids" : np.array(list(connectivities.keys()), dtype=np.int32),
                "connectivities" : np.array(list(connectivities.values()), dtype=np.int32),
                "pdata_values" : list(pdata_values.values()),
                "is_normal" : np.array(list(is_normal.values()), dtype=bool),
                }

            return DistributedPropertyData(**integration_data)


    def get_distributed_data_for_2d_element_integration(self, property_label: str) -> DistributedPropertyData | None:
        """ 
        This method processes the foundation stiffness data for element integration.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        pdata_values = {}
        connectivities = {}
        integration_data = {}
        is_normal = {}

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop != property_label:
                continue

            data: dict
            values = data.get("values")
            normal = data.get("normal", False)
            direct_input = data.get("direct_input", True)

            surf_elements = list(self.model.mesh.elements_from_surface.get(surface_id))
            surf_connect = self.model.mesh.get_connectivity_from_surface(surface_id)

            if direct_input:
                surface_area = self.element_2d.integrate_area(surf_connect)
                k_densities = self.process_frequency_based_arrays(values, denominator=surface_area)
            else:
                k_densities = self.process_frequency_based_arrays(values)

            # # # NOTE: uncomment the following lines if interested in validating the distributed mass property
            # if property_label == "distributed_mass":
            #     k_densities = self.process_frequency_based_arrays([435.4350843])

            # print()
            # print(f"Area: {surface_area} m²")
            # print(f"property_density: {k_densities} {data.get("units")}")
            # print()

            for i, el in enumerate(surf_elements):
                connectivities[el] = surf_connect[i]
                pdata_values[el] = k_densities
                is_normal[el] = normal

        if connectivities:

            integration_data = {
                "element_ids" : np.array(list(connectivities.keys()), dtype=np.int32),
                "connectivities" : np.array(list(connectivities.values()), dtype=np.int32),
                "pdata_values" : list(pdata_values.values()),
                "is_normal" : np.array(list(is_normal.values()), dtype=bool),
                }

            return DistributedPropertyData(**integration_data)


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

        self.rows, self.cols = self.element_2d.generate_ind_rows_cols(reorder=reorder)

        self.dof = self.element_2d.dof_per_element
        self.number_2d_elements = len(self.element_2d.connectivity)

        self.total_dof = self.element_2d.dof_per_node * len(self.element_2d.nodal_coordinates)

        self.displacement_dof = self.get_displacement_dof()
    
        self.data_K = np.zeros((self.number_2d_elements, self.dof, self.dof), dtype=np.complex128)
        self.data_M = np.zeros((self.number_2d_elements, self.dof, self.dof), dtype=np.complex128)

        # initialize variable
        last_progress = 0

        # loop for 2d elements
        with tqdm(
            self.model.mesh.faces_connectivity,
            desc="Processing the elementary matrices data for face elements",
            unit="element",
            file=sys.stderr,
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

        if self.model.reduced_memory_mode:
            self.write_global_matrices_arrays()


    def compute_data_to_process_global_matrices_for_solid_elements(self, reorder: bool = True, print_log: bool = False):
        """
        This method computes data to process the global matrices for solid elements.
        """

        self.active_2d_element_dof = []
        self.dof = self.element_3d.dof_per_element

        self.rows, self.cols, _ = self.element_3d.generate_ind_rows_cols(reorder=reorder)

        self.displacement_dof = self.get_displacement_dof()

        self.data_K = np.zeros((self.number_3d_elements, self.dof, self.dof), dtype=float)
        self.data_M = np.zeros((self.number_3d_elements, self.dof, self.dof), dtype=float)

        if self.dampings_from_volume:
            self.structural_local_dampings = np.zeros((self.number_3d_elements, 3), dtype=float)

        for index, element_id in enumerate(self.model.domains_processor.elements_of_domain.get("structural", [])):
            vol_id = self.model.mesh.solids_connectivity[element_id, 1]

        # initialize variable
        last_progress = 0

        # with tqdm(
        #     self.model.mesh.solids_connectivity,
        #     desc="Processing the elementary matrices data for solid elements",
        #     unit="element",
        #     file=sys.stderr,
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

            # dampings from volume
            structural_local_dampings = self.dampings_from_volume.get(vol_id)
            if structural_local_dampings is None:
                continue

            self.structural_local_dampings[index, :] = structural_local_dampings

        if self.model.reduced_memory_mode:
            self.write_global_matrices_arrays()


    def compute_data_to_process_global_matrices(self, reorder: bool = True, print_log: bool = False):
        """
        This method preprocesses all the required data to assemble the global matrices.
        """
        if self.model.mesh.solids_connectivity.size:
            self.process_material_from_volumes()
            self.compute_data_to_process_global_matrices_for_solid_elements(reorder=reorder, print_log=print_log)
            self.process_data_to_assemble_distributed_global_matrices()

        else:
            self.process_surface_data_for_shell_elements()
            self.compute_data_to_process_global_matrices_for_shell_elements(reorder=reorder, print_log=print_log)

        self.process_dofs_indices()


    def assemble_global_mass_matrix(self, index: int = 0):
        """
        This method assembles the global mass matrix.
        """
        M = coo_matrix((self.data_M.ravel(), (self.rows, self.cols)), shape=self.model.gm_shape).tocsr()

        if self.model.drop_domain:
            idx = self.structural_dofs_indices
            M = M[idx, :][:, idx]

        if not self.model.reduced_memory_mode:
            self.mass_matrix = M

        return M


    def assemble_global_stiffness_matrix(self, index: int = 0):
        """
        This method assembles the global stiffness matrix.
        """
        K = coo_matrix((self.data_K.ravel(), (self.rows, self.cols)), shape=self.model.gm_shape).tocsr()

        if self.model.drop_domain:
            idx = self.structural_dofs_indices
            K = K[idx, :][:, idx]

        if not self.model.reduced_memory_mode:
            self.stiffness_matrix = K

        return K


    def assemble_global_mass_and_stiffness_matrices(self, index: int = 0):
        """
        This method assembles the global mass matrix.
        """

        if  any(item is None for item in [self.rows, self.cols, self.data_M, self.data_K]):
            self.load_global_matrices_data()

        logging.info("Processing global mass matrix... [35/100]")
        M = coo_matrix((self.data_M.ravel(), (self.rows, self.cols)), shape=self.model.gm_shape).tocsr()

        logging.info("Processing global stiffness matrix... [75/100]")
        K = coo_matrix((self.data_K.ravel(), (self.rows, self.cols)), shape=self.model.gm_shape).tocsr()

        if self.model.drop_domain:
            idx = self.structural_dofs_indices
            M = M[idx, :][:, idx]
            K = K[idx, :][:, idx]

        if not self.model.reduced_memory_mode:
            self.mass_matrix = M
            self.stiffness_matrix = K

        return M, K


    def assemble_global_damping_matrix(self, freq: float, index: int, M: csr_matrix, K: csr_matrix):

        if not freq:
            raise ValueError(f"Unsupported frequency value: {freq} [Hz]")

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        # assemble the global damping distributed matrix
        C_dist = self.assemble_distributed_damping_global_matrix(index=index)

        omega = 2 * np.pi * freq

        # compute the damping matrix contribution for structural global dampings
        if any(self.model.global_damping):
            alpha, beta, eta = self.model.global_damping
            C = alpha * M + (beta + eta / omega) * K + C_dist
        else:
            C = csr_matrix(self.model.gm_shape, dtype=np.float64)

        # process the contribution for structural local dampings
        if not self.dampings_from_volume:
            return C

        # proportional damping constants
        alpha = self.structural_local_dampings[:, 0].reshape(-1, 1, 1)
        beta = self.structural_local_dampings[:, 1].reshape(-1, 1, 1)

        # hysteretic structural damping constant
        eta = self.structural_local_dampings[:, 2].reshape(-1, 1, 1)

        # compute the global damping matrix
        data = alpha * self.data_M + (beta + eta / omega) * self.data_K 
        C_mat = coo_matrix((data.ravel(), (self.rows, self.cols)), shape=self.model.gm_shape).tocsr()

        if self.model.drop_domain:
            idx = self.structural_dofs_indices
            C_mat = C_mat[idx, :][:, idx]

        return C + C_mat


    def process_data_to_assemble_distributed_global_matrices(self):
        """
        This method processes the sparse matrix data to assemble all distributed-related
        properties global matrices.
        """

        properties = [
            "distributed_mass",
            "distributed_stiffness",
            "distributed_damping",
        ]

        self.sparse_matrix_data: dict[str, SparseMatrixData] = {}
        all_integration_data: dict[str, DistributedPropertyData | None] = {}

        for _property in properties:
            all_integration_data[f"{_property}_1d"] = self.get_distributed_data_for_1d_element_integration(_property)
            all_integration_data[f"{_property}_2d"] = self.get_distributed_data_for_2d_element_integration(_property)

        for key, integration_data in all_integration_data.items():
            if not isinstance(integration_data, DistributedPropertyData):
                continue

            element = self.element_1d if "1d" in key else self.element_2d
            self.sparse_matrix_data[key] = self.get_global_matrix_data_to_assemble_sparse_matrix(integration_data, element)


    def get_global_matrix_data_to_assemble_sparse_matrix(
        self,
        integration_data: DistributedPropertyData,
        element: Structural1DElement | Structural2DElement,
    ):
        """
        For a distributed property, this method processes data from the global 
        matrix in order to assemble the sparse matrix.

        Parameters
        ----------
        integration_data: DistributedPropertyData
            A data class with the preprocessed integration data.

        element: Structural1DElement or Structural2DElement
            The structural element type.

        is_vectorial: bool, optional
            This argument determines whether the distributed property is vectorial or not. 

        Return
        ------
        sp_data: SparseMatrixData
            The sparse matrix data to assemble the global matrix.
        """

        def get_3d_diagonal_matrix(matrix_2d: np.ndarray):
            n_rows, n_cols = matrix_2d.shape
            indices = np.arange(n_cols)

            matrix_3d = np.zeros((n_rows, n_cols, n_cols), dtype=matrix_2d.dtype)
            matrix_3d[:, indices, indices] = matrix_2d

            return matrix_3d

        connectivities = integration_data.connectivities
        pdata_values = integration_data.pdata_values
        is_normal = integration_data.is_normal

        n_el = len(connectivities)
        n_freq = self.number_frequencies
        e_dofs = element.dof_per_element

        # intialize the 4D data array
        data = np.zeros((n_freq, n_el, e_dofs, e_dofs), dtype=np.complex128)

        # process the rows and columns indices to assemble sparse matrices
        rows, cols = element.get_rows_and_cols_indices_2D(connectivities)

        for i, _normal in enumerate(is_normal):
            value = pdata_values[i]
            if len(value) == 1:
                if _normal:
                    x_density = value.reshape(-1, 1, 1)
                else:
                    x_density = np.eye(element.dof_per_node) * value.reshape(-1, 1, 1)

            else:
                x_density = get_3d_diagonal_matrix(value.T)
            
            data[:, i, :, :] = element.integrate_distributed_property(i, x_density, is_normal=_normal)

        sp_data = SparseMatrixData(data, rows, cols)

        return sp_data


    def assemble_distributed_mass_global_matrix(self, index: int = 0):
        """
        This method assembles the distributed mass global matrix by 
        accounting for the contributions of 1D and 2D elements.

        Parameter
        ---------
        index: int, optional
            The frequency step index.

        """
        M_dist = 0.

        if "distributed_mass_1d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_mass_1d")
            M_dist += csr_matrix(
                (sp_data.data[index, :, :, :].ravel(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            )

        if "distributed_mass_2d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_mass_2d")
            M_dist += csr_matrix(
                (sp_data.data[index, :, :, :].ravel(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            )

        if not isinstance(M_dist, csr_matrix):
            return 0.
 
        if self.model.drop_domain:
            idx = self.structural_dofs_indices
            M_dist = M_dist[idx, :][:, idx]

        return M_dist


    def assemble_distributed_stiffness_global_matrix(self, index: int = 0):
        """
        This method assembles the distributed stiffness global matrix by 
        accounting for the contributions of 1D and 2D elements.

        Parameter
        ---------
        index: int, optional
            The frequency step index.

        """
        K_dist = 0.

        if "distributed_stiffness_1d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_stiffness_1d")
            K_dist += coo_matrix(
                (sp_data.data[index, :, :, :].ravel(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            ).tocsr()

        if "distributed_stiffness_2d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_stiffness_2d")
            K_dist += coo_matrix(
                (sp_data.data[index, :, :, :].ravel(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            ).tocsr()

        if not isinstance(K_dist, csr_matrix):
            return 0.

        if self.model.drop_domain:
            idx = self.structural_dofs_indices
            K_dist = K_dist[idx, :][:, idx]

        return K_dist


    def assemble_distributed_damping_global_matrix(self, index: int = 0):
        """
        This method assembles the distributed damping global matrix by 
        accounting for the contributions of 1D and 2D elements.

        Parameter
        ---------
        index: int, optional
            The frequency step index.

        """
        C_dist = 0.

        if "distributed_damping_1d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_damping_1d")
            C_dist += coo_matrix(
                (sp_data.data[index, :, :, :].ravel(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            ).tocsr()

        if "distributed_damping_2d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_damping_2d")
            C_dist += coo_matrix(
                (sp_data.data[index, :, :, :].ravel(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            ).tocsr()

        if not isinstance(C_dist, csr_matrix):
            return 0.
 
        if self.model.drop_domain:
            idx = self.structural_dofs_indices
            C_dist = C_dist[idx, :][:, idx]

        return C_dist


    def process_global_matrices_data(self, reorder: bool = True, print_log: bool = False):
        """
        This method assembles the global matrices of the structural model.
        """

        if not self.model.volumes_of_domain:
            self.model.domains_processor.update_domains_mappings()

        logging.info("Gathering data to assemble global matrices... [10/100]")
        self.define_structural_elements()
        self.update_number_of_frequencies()
        self.model.process_surface_thickness()

        logging.info("Gathering data to assemble global matrices... [25/100]")
        t0 = perf_counter()
        if self.compute_data_to_process_global_matrices(reorder=reorder, print_log=print_log):
            return
        dt = perf_counter() - t0
        if print_log:
            print(f"Elapsed time to process data to assemble global matrices: {dt : .6f} [s]")

        if self.model.stop_processing:
            return


    def process_global_matrices_data_and_excitations(self, reorder: bool = True, print_log: bool = False):
        """
        This method assembles the global matrices and excitations of the structural model.
        """
        self.process_global_matrices_data(reorder=reorder, print_log=print_log)
        self.excitations_assembler.assemble_model_excitations()


    def process_reduced_global_matrices(self, C: csr_matrix, M: csr_matrix, K: csr_matrix):
        """
        """
        # prescribed indexes
        idx = self.prescribed_dof_indices

        logging.info("Processing reduced global matrices... [90/100]")
        self.damping_matrix_r = C[:, idx]
        self.mass_matrix_r = M[:, idx]
        self.stiffness_matrix_r = K[:, idx]


    def compute_load_vector(self, index: int) -> np.ndarray:
        """
        Use this method to compute the structural load vector {f}.

        Parameters
        ----------       
        index: int
            The solution step index.

        Return
        ------
        load_vector: np.ndarray
            The structural load vector

        """

        logging.info("Computing the load vector... [95/100]")
        # self.f_eq = self.excitations_assembler.get_prescribed_dof_model_excitation(index=index)
        load_vector = self.excitations_assembler.structural_load[:, index] - self.f_eq

        if self.prescribed_dof_indices:
            return load_vector[self.unprescribed_dof_indices]

        return load_vector


    def compute_dynamic_stiffness_matrix(self, freq: float, index: int) -> csr_matrix:
        """
        Use this method to compute the global structural dynamic stiffness matrix.

        Parameters
        ----------
        freq: float
            The frequency value in Hz.

        index: int
            The solution step index.

        Return
        ------
        Kd: csr_matrix
            The global structural dynamic stiffness matrix.

        """

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        logging.info("Processing global mass and stiffness matrices... [25/100]")

        # reassemble the global distributed mass and stiffness matrices
        M_dist = self.assemble_distributed_mass_global_matrix(index=index)
        K_dist = self.assemble_distributed_stiffness_global_matrix(index=index)

        if index == 0 or self.model.reduced_memory_mode:
            M, K = self.assemble_global_mass_and_stiffness_matrices(index=index)

        else:
            M = self.mass_matrix
            K = self.stiffness_matrix

        logging.info("Processing global damping matrix... [80/100]")
        C = self.assemble_global_damping_matrix(freq, index, M, K)

        M += M_dist
        K += K_dist

        logging.info("Processing dynamic stiffness matrix... [85/100]")
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

        # process the global mass and stiffness matrices
        M, K = self.assemble_global_mass_and_stiffness_matrices()

        # reassemble the global distributed mass and stiffness matrices
        M_dist = self.assemble_distributed_mass_global_matrix()
        K_dist = self.assemble_distributed_stiffness_global_matrix()

        M += M_dist
        K += K_dist

        if self.prescribed_dof_indices:
            idx = self.unprescribed_dof_indices
            M = M[idx, :][:, idx]
            K = K[idx, :][:, idx]

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

        full_solution = np.zeros((rows, cols), dtype=np.complex128)
        print(len(self.unprescribed_dof_indices), len(self.prescribed_dof_indices))
        print(full_solution.shape, solution.shape)

        if len(self.prescribed_dof_indices):
            if modal_analysis:
                full_solution[self.prescribed_dof_indices, :] = np.zeros((len(self.prescribed_dof_indices), cols))
            else:
                full_solution[self.prescribed_dof_indices, :] = self.prescribed_values[:, :cols]

        full_solution[self.unprescribed_dof_indices, :] = solution

        return full_solution
    

    def reinsert_the_prescribed_dof_into_solution_freq(self, solution: np.ndarray, freq_index: int):

        rows = len(solution) + len(self.prescribed_dof_indices)

        full_solution = np.zeros(rows, dtype=np.complex128)
        full_solution[self.unprescribed_dof_indices] = solution

        if len(self.prescribed_dof_indices):
            full_solution[self.prescribed_dof_indices] = self.prescribed_values[:, freq_index]

        return full_solution


    def write_global_matrices_arrays(self):

        print()
        print("Allocated RAM for structural global matrices")
        print(f"data K -> {self.get_size_in_GB(self.data_K) : .4f} GB")
        print(f"data M -> {self.get_size_in_GB(self.data_M) : .4f} GB")
        print(f"rows I -> {self.get_size_in_GB(self.rows) : .4f} GB")
        print(f"cols J -> {self.get_size_in_GB(self.cols) : .4f} GB")

        logging.info("Writing the global matrices data... [25/100]")
        self.model.array_writer("structural_rows_indices.npy", self.rows)

        logging.info("Writing the global matrices data... [50/100]")
        self.model.array_writer("structural_cols_indices.npy", self.cols)

        logging.info("Writing the global matrices data... [75/100]")
        self.model.array_writer("structural_data_M.npy", self.data_M)

        logging.info("Writing the global matrices data... [98/100]")
        self.model.array_writer("structural_data_K.npy", self.data_K)


    def load_global_matrices_data(self):
        self.rows = self.model.array_reader("structural_rows_indices.npy")
        self.cols = self.model.array_reader("structural_cols_indices.npy")
        self.data_M = self.model.array_reader("structural_data_M.npy")
        self.data_K = self.model.array_reader("structural_data_K.npy")


    def get_size_in_GB(self, data: np.ndarray):
        return sys.getsizeof(data) / (1024**3)