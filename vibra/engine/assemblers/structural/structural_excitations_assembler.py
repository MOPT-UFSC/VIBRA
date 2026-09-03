
import logging
from collections import defaultdict
from dataclasses import dataclass
from time import time
from typing import TYPE_CHECKING

import numpy as np

from vibra.engine.analysis_info import HarmonicAnalysisSetup

if TYPE_CHECKING:
    from vibra.engine.assemblers.structural.structural_assembler import StructuralAssembler


@dataclass
class StructuralExcitationData:
    element_ids: np.ndarray
    connectivities: np.ndarray
    pdata_values: np.ndarray | dict


class StructuralExcitationsAssembler:
    def __init__(self, assembler : "StructuralAssembler"):

        self.assembler = assembler

        self.reset()


    def reset(self):
        self.structural_load = None


    @property
    def model(self):
        return self.assembler.model


    @property
    def mesh(self):
        return self.assembler.model.mesh


    @property
    def properties(self):
        return self.assembler.model.properties


    @property
    def element_1d(self):
        return self.assembler.element_1d


    @property
    def element_2d(self):
        return self.assembler.element_2d


    @property
    def number_3d_elements(self):
        return self.model.number_3d_structural_elements


    @property
    def structural_dofs(self):
        return self.model.structural_dofs_indices


    @property
    def structural_ndofs(self):
        return len(self.model.structural_dofs_indices)


    @property
    def total_dofs(self):
        return self.model.total_dof


    @property
    def gm_shape(self):
        return (self.model.total_dof, self.model.total_dof)


    @property
    def number_frequencies(self):
        return self.assembler.number_frequencies


    @property
    def prescribed_dof_indices(self):
        return self.assembler.prescribed_dof_indices


    @property
    def unprescribed_dof_indices(self):
        return self.assembler.unprescribed_dof_indices


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

        if np.sum(self.assembler.array_prescribed_values) == 0:
            return 0.

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        alpha, beta, eta = self.model.global_damping
        frequencies = analysis_setup.get_frequencies()

        omega = 2 * np.pi * frequencies[index]
        values = self.assembler.array_prescribed_values[:, index]

        self.Kr = self.assembler.stiffness_matrix_r
        self.Mr = self.assembler.mass_matrix_r

        Kr_add = self.Kr @ values
        Mr_add = self.Mr @ values

        f_eq = (1 + 1j*(eta + omega * beta)) * Kr_add + (-(omega**2) + 1j*(omega * alpha)) * Mr_add

        return f_eq[self.unprescribed_dof_indices]


    def get_prescribed_dof_model_excitation_reference(self, freq_dependent: bool = False):
        """
        This method adds the effects of prescribed acoustic pressure into mass flow global vector.

        Returns
        ----------
        array
            F_eq. Each column corresponds to a frequency of analysis.
        """

        if np.sum(self.assembler.array_prescribed_values) == 0:
            return 0.

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        alpha, beta, eta = self.model.global_damping
        frequencies = self.model.frequencies

        unprescribed_indices = self.unprescribed_dof_indices

        Kr = (self.assembler.stiffness_matrix_r.toarray())[unprescribed_indices, :]
        Mr = (self.assembler.mass_matrix_r.toarray())[unprescribed_indices, :]

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
            Kr_add = np.sum((Kr * self.assembler.array_prescribed_values[:, i]), axis=1)
            Mr_add = np.sum((Mr * self.assembler.array_prescribed_values[:, i]), axis=1)
            #
            omega = 2 * np.pi * freq
            f_Kadd = Kr_add
            f_Madd = -(omega**2) * Mr_add
            f_Cadd = 1j * ((eta + omega * beta) * Kr_add + (omega * alpha) * Mr_add)
            f_eq[:, i] = f_Madd + f_Cadd + f_Kadd

        logging.info("Processing prescribed dof model excitation... [100/100]")

        return f_eq

    
    def get_combined_nodal_loads_vector(self, index: int):
        
        f_eq = self.get_prescribed_dof_model_excitation(index=index)
        f = self.structural_load[:, index] - f_eq

        return f


    def process_structural_excitations_by_nodal_attribution(self):

        input_nodal_loads_data = self.assembler.get_property_data_for_selected_property("nodal_loads")
        output_nodal_loads_data = self.assembler.reorder_property_data_based_on_gdof(input_nodal_loads_data)
        nodal_loads = self.assembler.process_property_arrays(output_nodal_loads_data)

        if nodal_loads:
            indices = list(nodal_loads.keys())
            self.structural_load[indices, :] += np.array(list(nodal_loads.values()), dtype=complex)


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
            # TODO: check matrix dimensions for compatibility
            return aux_ones
        
        array_of_values = np.array(values_list, dtype=complex)

        # filter values based on frequency mask
        if array_of_values.shape[1] - self.number_frequencies:
            return array_of_values[self.model.solution_steps_mask, :]

        return array_of_values


    def get_excitation_data_for_1d_element_integration(self, property_label: str) -> StructuralExcitationData | None:
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

        pdata_values = {}
        connectivities = {}
        integration_data = {}

        for key, data in self.properties.line_properties.items():

            property, line_id = key
            if property != property_label:
                continue

            if property in ["normal_pressure_load", "nodal_loads", "distributed_load"]:
                element_type = data.get("element_type")
                if element_type == "2d_element":
                    continue

            data: dict
            element_integration = data.get("element_integration", True)
            if property == "nodal_loads" and not element_integration:
                continue

            complex_values = data.get("values")

            # normalize data type to array
            complex_values_array = self.process_loads_arrays(complex_values)

            elements = list(self.mesh.elements_from_line.get(line_id))
            connect = self.mesh.get_connectivity_from_line(line_id)

            if property_label == "nodal_loads":
                line_length = self.element_1d.integrate_length(connect)
                complex_values_array /= line_length

            for i, el in enumerate(elements):
                connectivities[el] = connect[i]
                pdata_values[el] = complex_values_array

        if connectivities:

            integration_data = {
                "element_ids" : np.array(list(connectivities.keys()), dtype=int),
                "connectivities" : np.array(list(connectivities.values()), dtype=int),
                "pdata_values" : np.array(list(pdata_values.values()), dtype=complex),
                }

            return StructuralExcitationData(**integration_data)


    def get_excitation_data_for_2d_element_integration(self, property_label: str) -> StructuralExcitationData | None:
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

        pdata_values = {}
        connectivities = {}
        integration_data = {}

        for key, data in self.properties.surface_properties.items():

            property, surface_id = key
            if property != property_label:
                continue

            if property in ["normal_pressure_load", "nodal_loads", "distributed_load"]:
                element_type = data.get("element_type")
                if element_type == "2d_element":
                    continue

            data: dict
            element_integration = data.get("element_integration", True)
            if property == "nodal_loads" and not element_integration:
                continue

            complex_values = data.get("values")

            # normalize data type to array
            complex_values_array = self.process_loads_arrays(complex_values)

            elements = list(self.mesh.elements_from_surface.get(surface_id))
            connect = self.mesh.get_connectivity_from_surface(surface_id)

            if property_label == "nodal_loads":
                surface_area = self.element_2d.integrate_area(connect)
                complex_values_array /= surface_area

            for i, el in enumerate(elements):
                connectivities[el] = connect[i]
                pdata_values[el] = complex_values_array

        if connectivities:

            integration_data = {
                "element_ids" : np.array(list(connectivities.keys()), dtype=int),
                "connectivities" : np.array(list(connectivities.values()), dtype=int),
                "pdata_values" : np.array(list(pdata_values.values()), dtype=complex),
                }

            return StructuralExcitationData(**integration_data)


    def process_structural_excitations_by_1d_element_integration(self):
        """ 
        This method processes the acoustic model excitations and
        returns the output data in the form of mass flow rate.
        """

        prop_labels = [
            "nodal_loads",
            "normal_pressure_load",
            "distributed_loads",
        ]

        for prop_label in prop_labels:

            integration_data = self.get_excitation_data_for_1d_element_integration(prop_label)
            if integration_data is None:
                continue

            match prop_label:
                case "distributed_loads" | "nodal_loads":
                    self.process_distributed_load_1d(integration_data)


    def process_structural_excitations_by_2d_element_integration(self):
        """ 
        This method processes the acoustic model excitations and
        returns the output data in the form of mass flow rate.
        """

        prop_labels = [
            "nodal_loads",
            "normal_pressure_load",
            "distributed_loads",
        ]

        for prop_label in prop_labels:

            integration_data = self.get_excitation_data_for_2d_element_integration(prop_label)
            if not integration_data:
                continue

            match prop_label:
                case "normal_pressure_load":
                    self.process_normal_pressure_load(integration_data)

                case "distributed_loads" | "nodal_loads":
                    self.process_distributed_load_2d(integration_data)


    def process_normal_pressure_load(self, integration_data: StructuralExcitationData):

        connectivities = integration_data.connectivities
        pdata_values = integration_data.pdata_values

        self.element_2d.reorder_connect(connectivities)
        for i, complex_values in enumerate(pdata_values):
            indices = self.element_2d.get_rows_and_cols_indices_1D(i)
            self.structural_load[indices, :] += self.element_2d.integrate_normal_pressure_load(i, complex_values)


    def process_distributed_load_1d(self, integration_data: StructuralExcitationData):

        connectivities = integration_data.connectivities
        pdata_values = integration_data.pdata_values

        self.element_1d.reorder_connect(connectivities)
        for i, complex_values in enumerate(pdata_values):
            indices = self.element_1d.get_rows_and_cols_indices_1D(i)
            self.structural_load[indices, :] += self.element_1d.integrate_distributed_load(i, complex_values)


    def process_distributed_load_2d(self, integration_data: StructuralExcitationData):

        connectivities = integration_data.connectivities
        pdata_values = integration_data.pdata_values

        self.element_2d.reorder_connect(connectivities)
        for i, complex_values in enumerate(pdata_values):
            indices = self.element_2d.get_rows_and_cols_indices_1D(i)
            self.structural_load[indices, :] += self.element_2d.integrate_distributed_load(i, complex_values)


    def process_structural_loading_from_acoustic_solution(self):

        structural_domains = self.model.model_domains.get("structural", [])
        surface_ids = list(self.model.fluid_structure_interfaces.keys())

        mask = np.isin(self.mesh.faces_connectivity[:, 1], surface_ids)
        interface_connectivities = self.mesh.faces_connectivity[mask, :]

        # reorder the connectivities
        self.element_2d.reorder_connect(interface_connectivities[:, 4:].copy())

        # TODO: remove after validation is concluded
        self.mesh.element_normals_data.clear()

        # correct the connectivities order
        for i, elem2d_id in enumerate(interface_connectivities[:, 0]):

            elem3d_ids = self.mesh.face_to_solid_element.get(elem2d_id, [])

            if len(elem3d_ids) != 2:
                print(f"The element 2D {elem2d_id} touches the solid elements: {[int(elem_id) for elem_id in elem3d_ids]}")
                continue

            # cache_connect = self.element_2d.connectivities[i, :].copy()

            for elem3d_id in self.mesh.face_to_solid_element.get(elem2d_id, []):
                vol_id = self.mesh.solids_connectivity[elem3d_id, 1]
                face_coords = self.mesh.nodal_coordinates[self.element_2d.connectivities[i, :], 1:]
                solid_coords = self.mesh.nodal_coordinates[self.mesh.solids_connectivity[elem3d_id, 4:], 1:]
                is_inverted = self.mesh.is_element_normal_vector_inverted(elem2d_id, face_coords, solid_coords)
                if vol_id in structural_domains and is_inverted:
                    self.element_2d.invert_element_connectivity(i)
                    # print(f"O elemento {i} foi invertido: {cache_connect} >> {self.element_2d.connectivities[i, :]}")
                    break

        from vibra import app
        app().main_window.results_widget.visualization_filter.element_normal_symbols = True
        app().main_window.update_symbols()

        # acoustic solution data
        nodal_solution = self.model.acoustic_solution.nodal_solution

        # integrate the structural loads caused by the acoustic pressure field on fluid-structure domain interfaces
        for i, connect in enumerate(self.element_2d.connectivities):
            _nodes = self.model.fluid_node_mapping[connect]
            element_pressures = nodal_solution[_nodes, :]
            indices = self.element_2d.get_rows_and_cols_indices_1D(i)
            self.structural_load[indices, :] += self.element_2d.integrate_normal_pressure_load(i, element_pressures, acoustic_excitation=True)


    def process_distributed_loads_for_shell_elements(self):

        for (property, surface_id), data in self.properties.surface_properties.items():
            if property not in ["distributed_loads", "normal_pressure_loads"]:
                continue

            if data.get("element_type") != "element_2d":
                continue

            connectivities_from_surface = self.mesh.get_connectivity_from_surface(surface_id)
            if property == "distributed_loads":
                surface_load = self.process_loads_arrays(data["values"])
                if surface_load is None:
                    continue

                for connect in connectivities_from_surface:
                    g_dof, F_elem = self.element_2d.process_forces_for_distributed_load_over_area(connect, surface_load)
                    self.structural_load[g_dof, :] += F_elem

            elif property == "normal_pressure_load":
                normal_pressure = self.process_loads_arrays(data["values"])
                if normal_pressure is None:
                    continue

                for connect in connectivities_from_surface:
                    if data.get("element_type") == "2d_element":
                        g_dof, F_elem = self.element_2d.process_forces_for_normal_pressure_load(connect, normal_pressure)

                    self.structural_load[g_dof, :] += F_elem

        for (property, line_id), data in self.properties.line_properties.items():
            if property != "distributed_loads":
                continue

            if data.get("element_type") != "element_2d":
                continue
        
            line_load = self.process_loads_arrays(data["values"])
            if line_load is None:
                continue

            nodes = self.mesh.get_nodes_from_line(line_id)
            if nodes is None:
                continue

            for surface_id in self.mesh.surfaces_from_line[line_id]:
                connectivities_from_surface = self.mesh.get_connectivity_from_surface(surface_id)
                rows = np.sum(np.isin(connectivities_from_surface, nodes), axis=1) == 2

                for connect_2d in connectivities_from_surface[rows, :]:
                    active_nodes = [1 if node_id in nodes else 0 for node_id in connect_2d]
                    g_dof, F_elem = self.element_2d.process_forces_for_distributed_load_over_line(connect_2d, active_nodes, line_load)
                    self.structural_load[g_dof, :] += F_elem


    def assemble_model_excitations(self):
        """
        This method assembles the excitations of the structural model.
        """

        # initialize the structural load vector
        self.structural_load = np.zeros((self.total_dofs, self.number_frequencies), dtype=complex)

        self.process_structural_excitations_by_nodal_attribution()
        self.process_structural_excitations_by_1d_element_integration()
        self.process_structural_excitations_by_2d_element_integration()

        if self.model.analysis_id.is_harmonic_coupled():
            self.process_structural_loading_from_acoustic_solution()

        # loads of shell structure
        self.process_distributed_loads_for_shell_elements()

        # partitioning the load vector
        if self.model.drop_domain:
            self.structural_load = self.structural_load[self.structural_dofs, :]

        if self.prescribed_dof_indices:
            self.structural_load = self.structural_load[self.unprescribed_dof_indices, :]

        return self.structural_load