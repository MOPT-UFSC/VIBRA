import logging
import sys
from collections import defaultdict
from dataclasses import dataclass
from time import perf_counter

import numpy as np
from scipy.sparse import csr_matrix
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
    pdata_values: np.ndarray | dict


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
        self.distributed_stiffness_matrix = None
        self.distributed_stiffness_matrix_r = None

        self.structural_load = None
        self.sparse_matrix_data: dict[str, SparseMatrixData] = {}


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


    def process_frequency_based_arrays(self, values: list[np.ndarray | None]):
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
            n_freq = self.number_frequencies

            aux_ones = np.ones(n_freq, dtype=complex)
            aux_zeros = np.zeros(n_freq, dtype=complex)

            for value in values:

                if value is None:
                    values_list.append(aux_zeros)

                elif isinstance(value, complex):
                    values_list.append(aux_ones * value)

                elif isinstance(value, np.ndarray):
                    values_list.append(value[: n_freq])

        except Exception as _error_log:
            print(str(_error_log))
            # TODO: check matrix dimensions for compatibility
            return aux_ones

        array_of_values = np.array(values_list, dtype=complex)

        # filter values based on frequency mask
        if array_of_values.shape[1] - n_freq:
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

        for key, data in self.properties.line_properties.items():

            prop, line_id = key
            if prop != property_label:
                continue

            data: dict
            k_value = np.array(data.get("values"), dtype=complex)

            line_elements = list(self.model.mesh.elements_from_line.get(line_id))
            line_connect = self.model.mesh.get_connectivity_from_line(line_id)
            line_length = self.element_1d.integrate_length(line_connect)

            # calculate the foundation stiffness density
            k_density = self.process_frequency_based_arrays(k_value / line_length)

            for i, el in enumerate(line_elements):
                connectivities[el] = line_connect[i]
                pdata_values[el] = k_density

        if connectivities:

            integration_data = {
                "element_ids" : np.array(list(connectivities.keys()), dtype=int),
                "connectivities" : np.array(list(connectivities.values()), dtype=int),
                "pdata_values" : np.array(list(pdata_values.values()), dtype=complex),
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

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop != property_label:
                continue

            data: dict
            k_value = np.array(data.get("values"), dtype=complex)

            surf_elements = list(self.model.mesh.elements_from_surface.get(surface_id))
            surf_connect = self.model.mesh.get_connectivity_from_surface(surface_id)
            surface_area = self.element_2d.integrate_area(surf_connect)

            # calculate the foundation stiffness density
            k_density = self.process_frequency_based_arrays(k_value / surface_area)

            # print()
            # print(f"Area: {surface_area} m²")
            # print(f"mass_density: {mass_density} kg/m²")
            # print()

            # mass_density = 1249.600004
            # mass_density = 2060.641904

            for i, el in enumerate(surf_elements):
                connectivities[el] = surf_connect[i]
                pdata_values[el] = k_density

        if connectivities:

            integration_data = {
                "element_ids" : np.array(list(connectivities.keys()), dtype=int),
                "connectivities" : np.array(list(connectivities.values()), dtype=int),
                "pdata_values" : np.array(list(pdata_values.values()), dtype=complex),
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


    def compute_data_to_process_global_matrices_for_solid_elements(self, reorder: bool = True, print_log: bool = False):
        """
        This method computes data to process the global matrices for solid elements.
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
        self.mass_matrix = csr_matrix((self.data_M.flatten(), (self.ind_rows, self.ind_cols)), shape=self.model.gm_shape)

        if self.model.drop_domain:
            self.mass_matrix = self.mass_matrix[self.structural_dofs_indices, :][:, self.structural_dofs_indices]

        self.mass_matrix_r = self.mass_matrix[:, self.prescribed_dof_indices]

        if self.prescribed_dof_indices:
            self.mass_matrix = self.mass_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def assemble_global_stiffness_matrix(self, index: int = 0):
        """
        This method assembles the global stiffness matrix.
        """
        self.stiffness_matrix = csr_matrix((self.data_K.flatten(), (self.ind_rows, self.ind_cols)), shape=self.model.gm_shape)

        if self.model.drop_domain:
            self.stiffness_matrix = self.stiffness_matrix[self.structural_dofs_indices, :][:, self.structural_dofs_indices]

        self.stiffness_matrix_r = self.stiffness_matrix[:, self.prescribed_dof_indices]

        if self.prescribed_dof_indices:
            self.stiffness_matrix = self.stiffness_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


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

            if _property == "distributed_damping":
                all_integration_data[f"{_property}_2d"]

        for key, integration_data in all_integration_data.items():
            if not isinstance(integration_data, DistributedPropertyData):
                continue

            element = self.element_1d if "_1d" in key else self.element_2d
            is_vectorial = "_mass" not in key

            self.sparse_matrix_data[key] = self.get_global_matrix_data_to_assemble_sparse_matrix(integration_data, element, is_vectorial)


    def get_global_matrix_data_to_assemble_sparse_matrix(
        self,
        integration_data: DistributedPropertyData,
        element: Structural1DElement | Structural2DElement,
        is_vectorial: bool,
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

        n_el = len(connectivities)
        n_freq = self.number_frequencies
        e_dofs = element.dof_per_element

        # intialize the 4D data array
        data = np.zeros((n_freq, n_el, e_dofs, e_dofs), dtype=complex)

        # process the rows and columns indices to assemble sparse matrices
        rows, cols = element.get_rows_and_cols_indices_2D(connectivities)

        for i, value in enumerate(pdata_values):
            if is_vectorial:
                x_density = get_3d_diagonal_matrix(value.T)
            else:
                x_density = np.eye(element.dof_per_node) * value.reshape(-1, 1, 1)

            data[:, i, :, :] = element.integrate_distributed_property(i, x_density)

        sp_data = SparseMatrixData(data, rows, cols)

        return sp_data


    def assemble_distributed_mass_global_matrix(self, index: int = 0):
        """
        This method assembles the distributed stiffness global matrix by 
        accounting for the contributions of 1D and 2D elements.

        Parameter
        ---------
        index: int, optional
            The frequency step index.

        """
        self.distributed_mass_matrix = 0.
        self.distributed_mass_matrix_r = 0.

        if "distributed_mass_1d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_mass_1d")
            self.distributed_mass_matrix += csr_matrix(
                (sp_data.data[index, :, :, :].flatten(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            )

        if "distributed_mass_2d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_mass_2d")
            self.distributed_mass_matrix += csr_matrix(
                (sp_data.data[index, :, :, :].flatten(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            )

        if not isinstance(self.distributed_mass_matrix, csr_matrix):
            return
 
        if self.model.drop_domain:
            self.distributed_mass_matrix = self.distributed_mass_matrix[self.structural_dofs_indices, :][:, self.structural_dofs_indices]

        self.distributed_mass_matrix_r = self.distributed_mass_matrix[:, self.prescribed_dof_indices]

        if self.prescribed_dof_indices:
            self.distributed_mass_matrix = self.distributed_mass_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def assemble_distributed_stiffness_global_matrix(self, index: int = 0):
        """
        This method assembles the distributed stiffness global matrix by 
        accounting for the contributions of 1D and 2D elements.

        Parameter
        ---------
        index: int, optional
            The frequency step index.

        """
        self.distributed_stiffness_matrix = 0.
        self.distributed_stiffness_matrix_r = 0.

        if "distributed_stiffness_1d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_stiffness_1d")
            self.distributed_stiffness_matrix += csr_matrix(
                (sp_data.data[index, :, :, :].flatten(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            )

        if "distributed_stiffness_2d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_stiffness_2d")
            self.distributed_stiffness_matrix += csr_matrix(
                (sp_data.data[index, :, :, :].flatten(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            )

        if not isinstance(self.distributed_stiffness_matrix, csr_matrix):
            return

        if self.model.drop_domain:
            self.distributed_stiffness_matrix = self.distributed_stiffness_matrix[self.structural_dofs_indices, :][:, self.structural_dofs_indices]

        self.distributed_stiffness_matrix_r = self.distributed_stiffness_matrix[:, self.prescribed_dof_indices]

        if self.prescribed_dof_indices:
            self.distributed_stiffness_matrix = self.distributed_stiffness_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def assemble_distributed_damping_global_matrix(self, index: int = 0):
        """
        This method assembles the distributed damping global matrix by 
        accounting for the contributions of 1D and 2D elements.

        Parameter
        ---------
        index: int, optional
            The frequency step index.

        """
        self.distributed_damping_matrix = 0.
        self.distributed_damping_matrix_r = 0.

        if "distributed_damping_1d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_damping_1d")
            self.distributed_damping_matrix += csr_matrix(
                (sp_data.data[index, :, :, :].flatten(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            )

        if "distributed_damping_2d" in self.sparse_matrix_data:
            sp_data = self.sparse_matrix_data.get("distributed_damping_2d")
            self.distributed_damping_matrix += csr_matrix(
                (sp_data.data[index, :, :, :].flatten(), (sp_data.rows, sp_data.cols)), shape=self.model.gm_shape
            )

        if not isinstance(self.distributed_damping_matrix, csr_matrix):
            return
 
        if self.model.drop_domain:
            self.distributed_damping_matrix = self.distributed_damping_matrix[self.structural_dofs_indices, :][:, self.structural_dofs_indices]

        self.distributed_damping_matrix_r = self.distributed_damping_matrix[:, self.prescribed_dof_indices]

        if self.prescribed_dof_indices:
            self.distributed_damping_matrix = self.distributed_damping_matrix[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


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
        t0 = perf_counter()
        if self.compute_data_to_process_global_matrices(reorder=reorder, print_log=print_log):
            return
        dt = perf_counter() - t0
        if print_log:
            print(f"Elapsed time to process data to assemble global matrices: {dt : .6f} [s]")

        if self.model.stop_processing:
            return

        logging.info("Assembling the global stiffness matrix... [50/100]")
        t0 = perf_counter()
        self.assemble_global_stiffness_matrix()
        self.assemble_distributed_stiffness_global_matrix()
        self.assemble_distributed_damping_global_matrix()
        dt = perf_counter() - t0
        if print_log:
            print(f"Elapsed time to assemble the global stiffness matrix: {dt : .6f} [s]")

        logging.info("Assembling the global mass matrix... [60/100]")
        t0 = perf_counter()
        self.assemble_global_mass_matrix()
        self.assemble_distributed_mass_global_matrix()
        dt = perf_counter() - t0
        if print_log:
            print(f"Elapsed time to assemble the global mass matrix: {dt : .6f} [s]")


    def assemble_global_matrices_and_excitations(self, reorder: bool = True, print_log: bool = False):
        """
        This method assembles the global matrices and excitations of the structural model.
        """
        self.assemble_global_matrices(reorder=reorder, print_log=print_log)
        self.structural_load = self.excitations_assembler.assemble_model_excitations()


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

        return self.excitations_assembler.get_combined_nodal_loads_vector(index=index)


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

        omega = 2 * np.pi * freq

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        alpha, beta, eta = self.model.global_damping

        if index > 0:
            # reassemble the global distributed matrices
            self.assemble_distributed_stiffness_global_matrix(index=index)
            self.assemble_distributed_damping_global_matrix(index=index)

        M = self.mass_matrix + self.distributed_mass_matrix
        K = self.stiffness_matrix + self.distributed_stiffness_matrix
        C_dist = self.distributed_damping_matrix

        # compute the dynamic stiffness matrix Kd
        Kd = (-(omega**2) + 1j * (omega * alpha)) * M + (1 + 1j * (eta + omega * beta)) * K + (1j * omega) * C_dist

        return Kd


    def build_eigenproblem_system(self):

        K = self.stiffness_matrix + self.distributed_stiffness_matrix
        M = self.mass_matrix + self.distributed_mass_matrix

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