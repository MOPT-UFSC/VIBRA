
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
from scipy.sparse import csr_matrix

from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.engine.properties.fluid import Fluid

if TYPE_CHECKING:
    from vibra.engine.assemblers.acoustic.acoustic_assembler import AcousticAssembler


@dataclass
class AcousticExcitationData:
    connectivities: np.ndarray
    surface_data: np.ndarray


@dataclass
class MassSourceData:
    connectivities: np.ndarray
    factor_Qms1: np.ndarray
    factor_Qms2: np.ndarray


class AcousticExcitationsAssembler:
    def __init__(self, assembler : "AcousticAssembler"):

        self.assembler = assembler

        self.reset()


    def reset(self):

        self.mass_flow_vector = None
        self.mass_source_vector_points = None
        self.mass_source_vector_lines = None
        self.mass_source_vector_surfaces = None
        self.mass_source_vector_volumes = None

        self.integration_data_Qms_1d: MassSourceData | None = None
        self.integration_data_Qms_2d: MassSourceData | None = None

        self.ind_rows_Qmsf_1d = np.array([], dtype=int)
        self.ind_cols_Qmsf_1d = np.array([], dtype=int)

        self.ind_rows_Qmsf_2d = np.array([], dtype=int)
        self.ind_cols_Qmsf_2d = np.array([], dtype=int)


    @property
    def model(self):
        return self.assembler.model


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


    @property
    def number_frequencies(self):
        return self.assembler.number_frequencies


    @property
    def prescribed_dof_indices(self):
        return self.assembler.prescribed_dof_indices


    @property
    def unprescribed_dof_indices(self):
        return self.assembler.unprescribed_dof_indices


    @property
    def fluid_properties_from_volume(self):
        return self.assembler.fluid_properties_from_volume


    def get_prescribed_pressure_model_excitation(self, index: int = 0):
        """
        This method computes the equivalent loads resulting from the degrees of freedom 
        prescription to compound the acoustic model excitation vector.

        Parameters
        ----------
        index: int, optional
            An integer values that represents the frequency index.

        Returns
        -------
        F_eq: np.ndarray
            The equivalent acoustic load vector of complex numbers in which
            each column corresponds to a frequency step of analysis.
        """
        _, prescribed_values = self.assembler.get_prescribed_dof_values()

        if prescribed_values.size == 0:
            return 0.

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        frequencies = analysis_setup.get_frequencies()
        omega = 2 * np.pi * frequencies[index]

        values = prescribed_values[:, index]

        self.Kr = self.assembler.stiffness_matrix_r
        self.Mr = self.assembler.mass_matrix_r
        self.Cr = self.assembler.damping_matrix_r
        self.Cr_visc = self.assembler.visc_damping_matrix_r

        Kr_add = self.Kr @ values
        Mr_add = self.Mr @ values
        Cr_add = (self.Cr + self.Cr_visc) @ values

        F_Kadd = Kr_add
        F_Madd = -(omega**2) * Mr_add 
        F_Cadd = 1j * omega * Cr_add
        F_eq = F_Kadd + F_Madd + F_Cadd

        return F_eq[self.unprescribed_dof_indices]


    def get_excitation_data_for_element_integration(self, property_label: str) -> AcousticExcitationData | None:
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
        connectivities = {}
        integration_data = {}

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop != property_label:
                continue

            data: dict
            if not data.get("element_integration", True):
                continue

            complex_values = data.get("values")[0]

            if property_label in ["compressor_excitation_spectrum", "compressor_excitation_waveform"]:
                excitation_type = data.get("excitation_type")

                if excitation_type in ["mass flow rate", "volumetric flow rate"]:

                    # compute the nozzle area
                    self.model.mesh.process_face_elements_connected_to_nodes(surface_id)
                    area = self.model.mesh.surface_area_from_element_integration.get(surface_id, 0)                    

                    if excitation_type == "mass flow rate":
                        # get the fluid density
                        density, _ = self.get_fluid_properties_from_surface(surface_id)

                        # convert the mass flow rate to surface velocity (oscilatting flow)
                        complex_values /= (density * area)

                    else:
                        # convert the volumetric flow rate to surface velocity (oscilatting flow)
                        complex_values /= area

            # normalize data type to array
            complex_values_array = self.assembler.get_value_in_array_form(complex_values, flatten=True)

            surf_elements = list(self.model.mesh.elements_from_surface.get(surface_id))
            surf_connect = self.model.mesh.get_connectivity_from_surface(surface_id)

            for i, el in enumerate(surf_elements):
                connectivities[el] = surf_connect[i]
                aux_data[el] = complex_values_array

        if connectivities:

            integration_data = {
                "connectivities" : np.array(list(connectivities.values()), dtype=int),
                "surface_data" : np.array(list(aux_data.values()), dtype=complex),
                }

            return AcousticExcitationData(**integration_data)


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


    def get_mass_source_data_for_1d_element_integration(self) -> MassSourceData | None:
        """ 
        This method processes the mass source data for element line
        integration.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 1d elements.
        """

        factor_Qms1 = {}
        factor_Qms2 = {}
        aux_connect = {}
        integration_data = {}

        for key, data in self.properties.line_properties.items():

            prop, line_id = key
            if prop != "mass_source":
                continue

            data: dict

            volume_id = data.get("volume_id")
            fluid_properties = self.fluid_properties_from_volume.get(volume_id)

            mu_0 = fluid_properties.get("mu_0")
            rho_f = fluid_properties.get("rho_f")
            _rho_f = self.assembler.get_value_in_array_form(rho_f, flatten=True)

            _factor_Qms1 = 1 / _rho_f
            _factor_Qms2 = (4 * mu_0) / (3 * _rho_f**2)

            line_elements = list(self.model.mesh.elements_from_line[line_id])
            line_connect = self.model.mesh.get_connectivity_from_line(line_id)

            for i, el in enumerate(line_elements):
                aux_connect[el] = line_connect[i]
                factor_Qms1[el] = _factor_Qms1
                factor_Qms2[el] = _factor_Qms2

        if aux_connect:

            integration_data = {
                "connectivities": np.array(list(aux_connect.values()), dtype=int),
                "factor_Qms1": np.array(list(factor_Qms1.values())),
                "factor_Qms2": np.array(list(factor_Qms2.values())),
            }

            return MassSourceData(**integration_data)


    def get_mass_source_data_for_2d_element_integration(self) -> MassSourceData | None:
        """ 
        This method processes the mass source data for element face
        integration.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        factor_Qms1 = {}
        factor_Qms2 = {}
        aux_connect = {}
        integration_data = {}

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop != "mass_source":
                continue

            data: dict

            volume_id = data.get("volume_id")
            fluid_properties = self.fluid_properties_from_volume.get(volume_id)

            mu_0 = fluid_properties.get("mu_0")
            rho_f = fluid_properties.get("rho_f")
            _rho_f = self.assembler.get_value_in_array_form(rho_f, flatten=True)

            _factor_Qms1 = 1 / _rho_f
            _factor_Qms2 = (4 * mu_0) / (3 * _rho_f**2)

            surf_elements = list(self.model.mesh.elements_from_surface.get(surface_id))
            surf_connect = self.model.mesh.get_connectivity_from_surface(surface_id) 

            for i, el in enumerate(surf_elements):
                aux_connect[el] = surf_connect[i]
                factor_Qms1[el] = _factor_Qms1
                factor_Qms2[el] = _factor_Qms2

        if aux_connect:

            integration_data = {
                "connectivities": np.array(list(aux_connect.values()), dtype=int),
                "factor_Qms1": np.array(list(factor_Qms1.values())),
                "factor_Qms2": np.array(list(factor_Qms2.values())),
            }

            return MassSourceData(**integration_data)


    def process_nodal_mass_source_data(self):
        """ 
        This method processes the nodal mass source vector data.
        """
        self.process_nodal_mass_source_data_for_nodes_and_points()
        self.process_nodal_mass_source_data_for_lines()
        self.process_nodal_mass_source_data_for_surfaces()
        self.process_nodal_mass_source_data_for_volumes()


    def process_nodal_mass_source_data_for_nodes_and_points(self):
        """ 
        This method processes the nodal mass source vector data assigned 
        to nodes and points.
        """

        model_properties = {
            "point_properties": self.properties.point_properties,
            "nodal_properties": self.properties.nodal_properties,
        }

        for prop_label, model_property in model_properties.items():
            for (property, *args), data in model_property.items():

                if property != "mass_source":
                    continue

                if not isinstance(data, dict):
                    continue

                if self.mass_source_vector_points is None:
                    self.mass_source_vector_points = np.zeros((self.total_dofs, self.number_frequencies), dtype=complex)

                volume_id = data.get("volume_id")
                if volume_id is None:
                    continue

                fluid = self.model.properties._get_property("fluid", volume=volume_id)
                if not isinstance(fluid, Fluid):
                    continue

                values = data.get("values")
                if values is None:
                    continue

                if prop_label == "nodal_properties":
                    node_id = args[0]
                else:
                    point_id = args[0]
                    node_id = self.model.mesh.nodes_from_points.get(point_id)

                # normalize data type to array
                complex_values_array = self.assembler.get_value_in_array_form(values[0], flatten=True)

                self.mass_source_vector_points[node_id, :] += complex_values_array / fluid.fluid_density

        if self.mass_source_vector_points is None:
            return

        if self.model.drop_domain:
            self.mass_source_vector_points = self.mass_source_vector_points[self.acoustic_dofs, :]

        if self.prescribed_dof_indices:
            self.mass_source_vector_points = self.mass_source_vector_points[self.unprescribed_dof_indices, :]


    def process_nodal_mass_source_data_for_lines(self):
        """ 
        This method processes the nodal mass source vector data assigned 
        to lines.
        """

        for (property, *args), data in self.properties.line_properties.items():

            if property != "mass_source":
                continue

            if not isinstance(data, dict):
                continue

            if self.mass_source_vector_lines is None:
                self.mass_source_vector_lines = np.zeros((self.total_dofs, self.number_frequencies), dtype=complex)

            values = data.get("values")
            if values is None:
                continue

            nodes = self.model.mesh.get_nodes_from_line(args[0])
            if nodes is None:
                continue

            aux_ones = np.ones((nodes.size, 1), dtype=float)

            # normalize data type to array
            complex_values_array = self.assembler.get_value_in_array_form(values[0])

            self.mass_source_vector_lines[nodes, :] += aux_ones @ complex_values_array

        if self.mass_source_vector_lines is None:
            return

        if self.model.drop_domain:
            self.mass_source_vector_lines = self.mass_source_vector_lines[self.acoustic_dofs, :]

        if self.prescribed_dof_indices:
            self.mass_source_vector_lines = self.mass_source_vector_lines[self.unprescribed_dof_indices, :]


    def process_nodal_mass_source_data_for_surfaces(self):
        """ 
        This method processes the nodal mass source vector data assigned 
        to surfaces.
        """

        for (property, *args), data in self.properties.surface_properties.items():

            if property != "mass_source":
                continue

            if not isinstance(data, dict):
                continue

            if self.mass_source_vector_surfaces is None:
                self.mass_source_vector_surfaces = np.zeros((self.total_dofs, self.number_frequencies), dtype=complex)

            values = data.get("values")
            if values is None:
                continue

            nodes = self.model.mesh.get_nodes_from_surface(args[0])
            if nodes is None:
                continue

            aux_ones = np.ones((nodes.size, 1), dtype=float)

            # normalize data type to array
            complex_values_array = self.assembler.get_value_in_array_form(values[0])

            self.mass_source_vector_surfaces[nodes, :] += aux_ones @ complex_values_array

        if self.mass_source_vector_surfaces is None:
            return

        if self.model.drop_domain:
            self.mass_source_vector_surfaces = self.mass_source_vector_surfaces[self.acoustic_dofs, :]

        if self.prescribed_dof_indices:
            self.mass_source_vector_surfaces = self.mass_source_vector_surfaces[self.unprescribed_dof_indices, :]


    def process_nodal_mass_source_data_for_volumes(self):
        """ 
        This method processes the nodal mass source vector data assigned 
        to volumes.
        """

        for (property, *args), data in self.properties.volume_properties.items():

            if property != "mass_source":
                continue

            if not isinstance(data, dict):
                continue

            if self.mass_source_vector_volumes is None:
                self.mass_source_vector_volumes = np.zeros((self.total_dofs, self.number_frequencies), dtype=complex)

            values = data.get("values")
            if values is None:
                continue

            nodes = self.model.mesh.get_nodes_from_volume(args[0])
            if nodes is None:
                continue

            aux_ones = np.ones((nodes.size, 1), dtype=float)

            # normalize data type to array
            complex_values_array = self.assembler.get_value_in_array_form(values[0])

            self.mass_source_vector_volumes[nodes, :] += aux_ones @ complex_values_array

        if self.mass_source_vector_points is None:
            return

        if self.model.drop_domain:
            self.mass_source_vector_volumes = self.mass_source_vector_volumes[self.acoustic_dofs, :]

        if self.prescribed_dof_indices:
            self.mass_source_vector_volumes = self.mass_source_vector_volumes[self.unprescribed_dof_indices, :]


    def process_mass_source_data_to_assemble_matrices(self):
        """
        This method assembles the mass source matrices Q_ms1 and Q_ms2.

        Parameters
        ----------
        index: int, optional
            The frequency index.
        """

        self.process_nodal_mass_source_data()

        if isinstance(self.mass_source_vector_lines, np.ndarray):
        
            self.integration_data_Qms_1d = self.get_mass_source_data_for_1d_element_integration()
            if self.integration_data_Qms_1d is not None:

                logging.info("Processing the mass source data to assemble matrices (1d elements)... [1/2]")
                connectivities = self.integration_data_Qms_1d.connectivities

                logging.info("Processing the mass source data to assemble matrices (1d elements)... [2/2]")
                self.ind_rows_Qmsf_1d, self.ind_cols_Qmsf_1d = self.element_1d.get_rows_and_cols_indices_2D(connectivities)
                self.int1d_NtN, self.int1d_BtB = self.element_1d.stacked_matrices_NtN_and_BtB()

        if isinstance(self.mass_source_vector_surfaces, np.ndarray):

            self.integration_data_Qms_2d = self.get_mass_source_data_for_2d_element_integration()
            if self.integration_data_Qms_2d is not None:

                logging.info("Processing the mass source data to assemble matrices (2d elements)... [1/2]")
                connectivities = self.integration_data_Qms_2d.connectivities

                logging.info("Processing the mass source data to assemble matrices (2d elements)... [2/2]")
                self.ind_rows_Qmsf_2d, self.ind_cols_Qmsf_2d = self.element_2d.get_rows_and_cols_indices_2D(connectivities)
                self.int2d_NtN, self.int2d_BtB = self.element_2d.stacked_matrices_NtN_and_BtB()


    def compute_mass_source_load_factors_for_volumes(self, index: int = 0):
        """
        This method evaluates the mass source factors that will multiply the 
        normalized global matrices.

        Parameters
        ----------
        index: int, optional
            The frequency index.

        Returns
        -------
        factor_Qms: np.ndarray
            An array containing the first and second mass-source vector factors.
        """

        factor_Qms1 = np.zeros(self.number_3d_elements, complex)
        factor_Qms2 = np.zeros(self.number_3d_elements, complex)

        for vol_id, elements_from_volume in self.model.mesh.elements_from_volume.items():
            fluid_data = self.fluid_properties_from_volume.get(vol_id)
            if not isinstance(fluid_data, dict):
                continue

            ms_data = self.properties._get_property("mass_source", volume=vol_id)
            if ms_data is None:
                continue 

            rho_f = fluid_data.get("rho_f")[index]
            # C_f = fluid_data.get("C_f")[index]
            mu_0 = fluid_data.get("mu_0")
            # rho_0 = fluid_data.get("rho_0")
            # C_0 = fluid_data.get("C_0")

            aux_ones = np.ones(elements_from_volume.size, dtype=float)

            factor_Qms1[elements_from_volume] = aux_ones / rho_f
            factor_Qms2[elements_from_volume] = aux_ones * ((4 * mu_0) / (3 * rho_f**2))

        return factor_Qms1.reshape(-1, 1, 1), factor_Qms2.reshape(-1, 1, 1)


    def assemble_mass_source_matrices_from_lines(self, index: int = 0):
        """
        This method assembles the mass source matrices Q_ms1 and Q_ms2
        due to line assignment.

        Parameters
        ----------
        index: int, optional
            The frequency index.
        """

        if self.integration_data_Qms_1d is None:
            return

        factor_Qms1 = self.integration_data_Qms_1d.factor_Qms1
        factor_Qms2 = self.integration_data_Qms_1d.factor_Qms2

        data_Qms1: np.ndarray = factor_Qms1[:, index].reshape(-1, 1, 1) * self.int1d_NtN
        self.Qms1_1d = csr_matrix((data_Qms1.flatten(), (self.ind_rows_Qmsf_1d, self.ind_cols_Qmsf_1d)), shape=self.gm_shape)

        data_Qms2: np.ndarray = factor_Qms2[:, index].reshape(-1, 1, 1) * self.int1d_BtB
        self.Qms2_1d = csr_matrix((data_Qms2.flatten(), (self.ind_rows_Qmsf_1d, self.ind_cols_Qmsf_1d)), shape=self.gm_shape)

        if self.model.drop_domain:
            self.Qms1_1d = self.Qms1_1d[self.acoustic_dofs, :][:, self.acoustic_dofs]
            self.Qms2_1d = self.Qms2_1d[self.acoustic_dofs, :][:, self.acoustic_dofs]

        if self.prescribed_dof_indices:
            self.Qms1_1d = self.Qms1_1d[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]
            self.Qms2_1d = self.Qms2_1d[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def assemble_mass_source_matrices_from_surfaces(self, index: int = 0):
        """
        This method assembles the mass source matrices Q_ms1 and Q_ms2
        due to surface assignment.

        Parameters
        ----------
        index: int, optional
            The frequency index.
        """

        if self.integration_data_Qms_2d is None:
            return

        factor_Qms1 = self.integration_data_Qms_2d.factor_Qms1
        factor_Qms2 = self.integration_data_Qms_2d.factor_Qms2

        data_Qms1: np.ndarray = factor_Qms1[:, index].reshape(-1, 1, 1) * self.int2d_NtN
        self.Qms1_2d = csr_matrix((data_Qms1.flatten(), (self.ind_rows_Qmsf_2d, self.ind_cols_Qmsf_2d)), shape=self.gm_shape)

        data_Qms2: np.ndarray = factor_Qms2[:, index].reshape(-1, 1, 1) * self.int2d_BtB
        self.Qms2_2d = csr_matrix((data_Qms2.flatten(), (self.ind_rows_Qmsf_2d, self.ind_cols_Qmsf_2d)), shape=self.gm_shape)

        if self.model.drop_domain:
            self.Qms1_2d = self.Qms1_2d[self.acoustic_dofs, :][:, self.acoustic_dofs]
            self.Qms2_2d = self.Qms2_2d[self.acoustic_dofs, :][:, self.acoustic_dofs]

        if self.prescribed_dof_indices:
            self.Qms1_2d = self.Qms1_2d[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]
            self.Qms2_2d = self.Qms2_2d[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def assemble_mass_source_matrices_from_volumes(self, index: int = 0):
        """
        This method assembles the mass source matrices Q_ms1 and Q_ms2
        due to volume assignment.

        Parameters
        ----------
        index: int, optional
            The frequency index.
        """

        if self.mass_source_vector_volumes is None:
            return

        factor_Qms1, factor_Qms2 = self.compute_mass_source_load_factors_for_volumes(index=index)

        data_Qms1: np.ndarray = factor_Qms1 * self.int3d_NtN
        self.Qms1_3d = csr_matrix((data_Qms1.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        data_Qms2: np.ndarray = factor_Qms2 * self.int3d_BtB
        self.Qms2_3d = csr_matrix((data_Qms2.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        if self.model.drop_domain:
            self.Qms1_3d = self.Qms1_3d[self.acoustic_dofs, :][:, self.acoustic_dofs]
            self.Qms2_3d = self.Qms2_3d[self.acoustic_dofs, :][:, self.acoustic_dofs]

        if self.prescribed_dof_indices:
            self.Qms1_3d = self.Qms1_3d[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]
            self.Qms2_3d = self.Qms2_3d[self.unprescribed_dof_indices, :][:, self.unprescribed_dof_indices]


    def compute_mass_source_load_vector(self, omega: float, index: int = 0):
        """
        Computes the mass source load vector for the i-th frequency index.

        Parameters
        ----------
        omega: float
            The frequency in radians.

        index: int, optional
            The frequency index.
        
        Returns
        -------

        Q_ms: np.ndarray
            The compound mass source vector. 
        """
        Q_ms = 0.
        if isinstance(self.mass_source_vector_points, np.ndarray):
            mass_source_p = self.mass_source_vector_points[:, index]
            Q_ms += 1j * omega * mass_source_p

        if isinstance(self.mass_source_vector_lines, np.ndarray):
            mass_source_l = self.mass_source_vector_lines[:, index]
            Q_ms += (1j * omega * self.Qms1_1d + self.Qms2_1d) @ mass_source_l

        if isinstance(self.mass_source_vector_surfaces, np.ndarray):
            mass_source_s = self.mass_source_vector_surfaces[:, index]
            Q_ms += (1j * omega * self.Qms1_2d + self.Qms2_2d) @ mass_source_s

        if isinstance(self.mass_source_vector_volumes, np.ndarray):
            mass_source_v = self.mass_source_vector_volumes[:, index]
            Q_ms += (1j * omega * self.Qms1_3d + self.Qms2_3d) @ mass_source_v

        return Q_ms


    def process_acoustic_excitations_by_nodal_attribution(self):
        """ 
        This method processes the acoustic model excitations and
        returns the output data in the form of mass flow rate.
        """

        if self.mass_flow_vector is None:
            self.mass_flow_vector = np.zeros((self.total_dofs, self.number_frequencies), dtype=complex)

        acoustic_excitation = defaultdict(float)
        aux_ones = np.ones((self.number_frequencies), dtype=complex)

        for (property, surface_id), data in self.properties.surface_properties.items():
            if property in ["surface_velocity", "reciprocating_compressor_excitation"]:

                if not isinstance(data, dict):
                    continue
        
                if data.get("element_integration", True):
                    continue

                _complex_values = data["values"][0]
                if isinstance(_complex_values, complex):
                    complex_values = _complex_values * aux_ones

                #TODO: check compressor excitation
                elif isinstance(_complex_values, np.ndarray):
                    if _complex_values.shape[0] == 1:
                        complex_values = _complex_values * aux_ones
                    elif len(_complex_values.shape) == 1:
                        complex_values = _complex_values.reshape(1,-1)
                    else:
                        complex_values = _complex_values

                nodes = self.model.mesh.get_nodes_from_surface(surface_id)
                if nodes is None:
                    continue

                _nodes = self.model.fluid_node_mapping[nodes]

                self.model.mesh.process_face_elements_connected_to_nodes(surface_id)
                area = self.model.mesh.surface_area_from_element_integration[surface_id]

                for global_dof in self.model.get_acoustic_global_dof_from_nodes(_nodes):
                    acoustic_excitation[global_dof] += complex_values * area

        if acoustic_excitation:
            indices = list(acoustic_excitation)
            excitation = list(acoustic_excitation.values())
            self.mass_flow_vector[indices, :] += np.array(excitation)


    def process_acoustic_excitations_by_element_integration(self):
        """ 
        This method processes the acoustic model excitations and
        returns the output data in the form of mass flow rate.
        """

        if self.mass_flow_vector is None:
            self.mass_flow_vector = np.zeros((self.total_dofs, self.number_frequencies), dtype=complex)

        prop_labels = [
            "surface_velocity",
            "compressor_excitation_spectrum",
            "compressor_excitation_waveform",
            "reciprocating_compressor_excitation",
        ]

        for prop_label in prop_labels:

            integration_data_sv = self.get_excitation_data_for_element_integration(prop_label)
            if integration_data_sv is None:
                continue

            connectivities_sv = integration_data_sv.connectivities
            surface_data_sv = integration_data_sv.surface_data

            # from vibra import app
            # surf_connect = self.model.mesh.get_connectivity_from_surface(4)
            # app().main_window.selection.set_mesh_selection(nodes=surf_connect.flatten())

            self.element_2d.reorder_connect(connectivities_sv)
            for i, complex_values in enumerate(surface_data_sv):
                indices = self.element_2d.get_rows_and_cols_indices_1D(i)
                int2d_N = self.element_2d.load_vector(i)
                self.mass_flow_vector[indices, :] += int2d_N @ complex_values.reshape(1, -1)

        integration_data_ipw = self.assembler.impedances_assembler.integration_data_ipw
        if integration_data_ipw is None:
            return
    
        p_inc: np.ndarray = integration_data_ipw.ipw_pressure
        s_vector: np.ndarray = integration_data_ipw.ipw_vector
        Z_ipw: np.ndarray = integration_data_ipw.ipw_impedance
        connectivities: np.ndarray = integration_data_ipw.connectivities
        element_normals: np.ndarray = integration_data_ipw.element_face_normals

        self.element_2d.reorder_connect(connectivities)

        for i, n_vector in enumerate(element_normals):

            int2d_N = self.element_2d.load_vector(i)

            # dof indices
            indices = self.element_2d.get_rows_and_cols_indices_1D(i)

            # auxilar vector
            aux: np.ndarray =  2 * np.dot(n_vector, s_vector) * p_inc / Z_ipw

            # assemble the acoustic load
            self.mass_flow_vector[indices, :] += int2d_N @ aux.reshape(1, -1)


    def assemble_model_excitations(self):
        """
        This method assembles the excitations of the acoustic model.
        """

        logging.info("Processing element related loads... [75/100]")
        self.process_acoustic_excitations_by_element_integration()

        logging.info("Processing nodal related loads... [85/100]")
        self.process_acoustic_excitations_by_nodal_attribution()

        logging.info("Processing source-terms related loads... [90/100]")
        self.process_mass_source_data_to_assemble_matrices()
        self.assemble_mass_source_matrices_from_lines()
        self.assemble_mass_source_matrices_from_surfaces()
        self.assemble_mass_source_matrices_from_volumes()

        logging.info("Partitioning the load vector... [95/100]")

        if self.model.drop_domain:
            self.mass_flow_vector = self.mass_flow_vector[self.acoustic_dofs, :]

        if self.prescribed_dof_indices:
            self.mass_flow_vector = self.mass_flow_vector[self.unprescribed_dof_indices, :]

        return self.mass_flow_vector
