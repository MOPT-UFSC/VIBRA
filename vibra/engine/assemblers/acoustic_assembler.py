from tqdm import tqdm

import logging
from collections import defaultdict
from dataclasses import dataclass
from time import time

import numpy as np
from scipy.sparse import block_array, csr_matrix

from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.engine.model import Model
from vibra.engine.properties.fluid import Fluid


@dataclass
class IncidentPlaneWaveIntegrationData:
    ipw_vector: np.ndarray
    ipw_pressure: np.ndarray
    ipw_impedance: np.ndarray
    connectivities: np.ndarray
    element_face_normals: np.ndarray


class AcousticAssembler:
    def __init__(self, model : Model):

        self.model = model
        self.properties = model.properties

        self.reset()


    def reset(self):
        self.stiffness_matrix = None
        self.mass_matrix = None
        self.damping_matrix = None
        self.frequencies = None
        self.frequency_dependent = False

        self.number_frequencies = 1
        self.prescribed_values = []
        self.prescribed_indexes = []
        self.unprescribed_indexes = []
        self.fluid_properties_from_volume = {}

        self.element_1d = None
        self.element_2d = None
        self.element_3d = None


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
        get_prescribed_indexes : Indexes of the acoustic degrees of freedom with prescribed pressure boundary conditions.

        get_unprescribed_indexes : Indexes of the acoustic free degrees of freedom.
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


    def get_prescribed_indexes(self):
        """
        Returns the prescribed dof indexes.
        """
        _prescribed_indexes = []
        for key in self.properties.surface_properties:
            property, surface_id = key
            if property != "acoustic_pressure":
                continue

            nodes = self.model.mesh.get_nodes_from_surface(surface_id)
            if nodes is None:
                continue

            for index in self.model.get_acoustic_global_dof_from_nodes(nodes):
                _prescribed_indexes.append(index)

        return _prescribed_indexes


    def get_unprescribed_indexes(self):
        """ 
        Returns the unprescribed dof indexes.
        """
        total_dof = self.element_3d.DOF_PER_NODE * len(self.element_3d.nodal_coordinates)
        all_indexes = np.arange(total_dof, dtype=int)
        prescribed_indexes = self.get_prescribed_indexes()
        return np.delete(all_indexes, prescribed_indexes)


    def process_indexes(self):
        self.prescribed_indexes = self.get_prescribed_indexes()
        self.unprescribed_indexes = self.get_unprescribed_indexes()


    def get_matrices_dropping_indexes(self):
        return self.unprescribed_indexes, self.prescribed_indexes


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
        _, prescribed_values = self.get_prescribed_dof_values()

        if prescribed_values.size == 0:
            return 0.

        analysis_setup = self.model.analysis_setup
        assert isinstance(analysis_setup, HarmonicAnalysisSetup)

        frequencies = analysis_setup.get_frequencies()
        omega = 2 * np.pi * frequencies[index]

        values = prescribed_values[:, index]

        self.Kr = self.stiffness_matrix_r
        self.Mr = self.mass_matrix_r
        self.Cr = self.damping_matrix_r
        self.Cr_visc = self.visc_damping_matrix_r

        Kr_add = self.Kr @ values
        Mr_add = self.Mr @ values
        Cr_add = (self.Cr + self.Cr_visc) @ values

        F_Kadd = Kr_add
        F_Madd = -(omega**2) * Mr_add 
        F_Cadd = 1j * omega * Cr_add
        F_eq = F_Kadd + F_Madd + F_Cadd

        return F_eq[self.unprescribed_indexes]


    def get_impedance_data_for_element_integration(self, property_label: str) -> dict:
        """ 
        This method processes the surface property data for element face
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
            density, speed_of_sound = self.get_fluid_properties_from_surface(surface_id)

            if property_label ==  "anechoic_termination" or "anechoic_termination" in data:
                complex_values = density * speed_of_sound

            elif property_label ==  "absorption_surface":
                alpha = data.get("values")[0]

                Z_0 = density * speed_of_sound
                Z_s = Z_0 * ((1 + (1-alpha)**(1/2)) / (1 - (1-alpha)**(1/2)))
                complex_values = Z_s

            else:
                complex_values = data.get("values")[0]

            # normalize data type to array
            complex_values_array = self.get_value_in_array_form(complex_values, flatten=True)

            surf_elements = list(self.model.mesh.elements_from_surface.get(surface_id))
            surf_connect = self.model.mesh.get_connectivity_from_surface(surface_id)

            for i, el in enumerate(surf_elements):
                aux_connect[el] = surf_connect[i]
                aux_data[el] = complex_values_array

        if aux_connect:
            integration_data = {
                "connectivities" : np.array(list(aux_connect.values()), dtype=int),
                "surface_data" : np.array(list(aux_data.values()), dtype=complex),
                }

        return integration_data


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
            complex_values_array = self.get_value_in_array_form(complex_values, flatten=True)

            surf_elements = list(self.model.mesh.elements_from_surface.get(surface_id))
            surf_connect = self.model.mesh.get_connectivity_from_surface(surface_id)

            for i, el in enumerate(surf_elements):
                aux_connect[el] = surf_connect[i]
                aux_data[el] = complex_values_array

        if aux_connect:
            integration_data = {
                "connectivities" : np.array(list(aux_connect.values()), dtype=int),
                "surface_data" : np.array(list(aux_data.values()), dtype=complex),
                }

        return integration_data


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


    def get_incident_plane_wave_surface_data_for_element_integration(self) -> dict:
        """ 
        This method processes the plane wave data for element face
        integration.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        elements_connectivities = []
        elements_normals = []

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop != "incident_plane_wave":
                continue

            rho_eff_pm, C_eff_pm = self.model.get_porous_material_model_effective_properties(surface_id)
            rho_eff_tv, C_eff_tv = self.model.get_viscous_thermal_model_effective_properties(surface_id)

            ipw_vector = np.array(data.get("ipw_vector"), dtype=float)
            norm_ipw_vector = np.linalg.norm(ipw_vector)

            if norm_ipw_vector:
                ipw_vector /= norm_ipw_vector

            if isinstance(rho_eff_pm, np.ndarray):
                density = rho_eff_pm
                speed_of_sound = C_eff_pm

            elif isinstance(rho_eff_tv, np.ndarray):
                density = rho_eff_tv
                speed_of_sound = C_eff_tv

            else:
                fluid: Fluid = self.model.properties._get_property("fluid", surface=surface_id)
                if not isinstance(fluid, Fluid):
                    continue

                density = fluid.fluid_density
                speed_of_sound = fluid.speed_of_sound

            data: dict

            # normalize data type to array
            p_inc = self.get_value_in_array_form(data.get("values")[0], flatten=True)
            Z_ipw = self.get_value_in_array_form(density * speed_of_sound, flatten=True)

            rows = self.model.mesh.faces_connectivity[:, 1] == surface_id
            surface_elements_connectivities = self.model.mesh.faces_connectivity[rows, :]
            surface_elements_normals = self.model.mesh.get_element_face_normal_batched(surface_elements_connectivities)

            elements_connectivities.extend(surface_elements_connectivities[:, 4:])
            elements_normals.extend(surface_elements_normals)

        if not elements_connectivities:
            return None
    
        pw_data = {
            "ipw_vector": ipw_vector,
            "ipw_pressure": p_inc,
            "ipw_impedance": Z_ipw,
            "connectivities": np.array(elements_connectivities, dtype=int),
            "element_face_normals": np.array(elements_normals, dtype=float),
        }

        return IncidentPlaneWaveIntegrationData(**pw_data)


    def get_mass_source_data_for_1d_element_integration(self) -> dict:
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
            _rho_f = self.get_value_in_array_form(rho_f, flatten=True)

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
                                "connectivities" : np.array(list(aux_connect.values()), dtype=int),
                                "factor_Qms1" : np.array(list(factor_Qms1.values())),
                                "factor_Qms2" : np.array(list(factor_Qms2.values())),
                                }

        return integration_data


    def get_mass_source_data_for_2d_element_integration(self) -> dict:
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
            _rho_f = self.get_value_in_array_form(rho_f, flatten=True)

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
                                "connectivities" : np.array(list(aux_connect.values()), dtype=int),
                                "factor_Qms1" : np.array(list(factor_Qms1.values())),
                                "factor_Qms2" : np.array(list(factor_Qms2.values())),
                                }

        return integration_data


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


    def get_transfer_impedance_data_for_element_integration(self):
        """
        This method processes the transfer impedance data for element face
        integration.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        surface_data_A = {}
        surface_data_B = {}
        connectivity_surface_A = {}
        connectivity_surface_B = {}
        integration_data = {}

        # aux_ones = np.ones(self.number_frequencies, dtype=complex)

        for (property_label, surface_ids), p_data in self.properties.surface_properties.items():

            if property_label != "transfer_impedance":
                continue
        
            p_data: dict
            values = p_data.get("values")
            if values is None:
                continue

            _complex_values = values[0]
            if not isinstance(_complex_values, complex | float | np.ndarray):
                continue

            Z_tr = self.get_value_in_array_form(_complex_values, flatten=True)

            # if isinstance(_complex_values, complex | float):
            #     Z_tr = _complex_values * aux_ones

            # elif isinstance(_complex_values, np.ndarray):

            #     if _complex_values.shape[0] == 1:
            #         Z_tr = _complex_values * aux_ones

            #     else:
            #         Z_tr = _complex_values

            # else:
            #     continue

            decouple_data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_ids)
            if not isinstance(decouple_data, dict):
                continue

            new_surface_id = decouple_data.get("new_surface_id")
            if new_surface_id is None:
                continue

            surf_elements_A = list(self.model.mesh.elements_from_surface.get(surface_ids))
            surf_elements_B = list(self.model.mesh.elements_from_surface.get(new_surface_id))

            for i, el in enumerate(surf_elements_A):
                nodes_from_element = self.model.mesh.faces_connectivity[el, 4:]
                connectivity_surface_A[el] = nodes_from_element

                surface_data_A[el] = Z_tr

            for i, el in enumerate(surf_elements_B):
                nodes_from_element = self.model.mesh.faces_connectivity[el, 4:]
                connectivity_surface_B[el] = nodes_from_element

                surface_data_B[el] = Z_tr

        if connectivity_surface_A and connectivity_surface_B:
            integration_data = {
                                "connectivities_A" : np.array(list(connectivity_surface_A.values()), dtype=int),
                                "connectivities_B" : np.array(list(connectivity_surface_B.values()), dtype=int),
                                "surface_data_A" : np.array(list(surface_data_A.values()), dtype=complex),
                                "surface_data_B" : np.array(list(surface_data_B.values()), dtype=complex),
                                }

        return integration_data


    def get_perforated_plate_data_for_element_integration(self, solution: np.ndarray | None = None):
        """
        This method processes the perforated plate data for element face
        integration.

        Parameters
        ----------
        solution: np.ndarray, optional
            It corresponds to the acoustic pressure field that is adopted to
            update the impedance of the perforated plate whenever nonlinear 
            effects are enabled.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        surface_data_A = {}
        surface_data_B = {}
        connectivity_surface_A = {}
        connectivity_surface_B = {}

        integration_data = {}

        for (property_label, surface_ids), pp_data in self.properties.surface_properties.items():

            if property_label == "perforated_plate_model":
                pp_data: dict

                pp_model = self.model.perforated_plate_impedance_data[surface_ids]
                pp_model: dict

                z_orifice = pp_model.get("z_orifice", 0)
                z_end = pp_model.get("z_end", 0)
                z_nl_urms = pp_model.get("z_nl_urms", 0)
                z_ud = pp_model.get("z_ud", 0)
                Z_0 = pp_model.get("Z_0", 0)

                non_linear = z_nl_urms != 0
    
                decouple_data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_ids)
                if not isinstance(decouple_data, dict):
                    continue

                new_surface_id = decouple_data.get("new_surface_id")
                if new_surface_id is None:
                    continue

                surf_elements_A = list(self.model.mesh.elements_from_surface.get(surface_ids))
                surf_elements_B = list(self.model.mesh.elements_from_surface.get(new_surface_id))

                for i, el in enumerate(surf_elements_A):

                    U_rms = 0
                    nodes_from_element = self.model.mesh.faces_connectivity[el, 4:]
                    connectivity_surface_A[el] = nodes_from_element

                    # if solution is not None:
                    #     p = solution[nodes_from_element, :]
                    #     p2_avg = np.average((1/2)*np.real(p*np.conj(p)), axis=0)
                    #     p_rms = np.sqrt(p2_avg)
                    #     U_rms = p_rms / Z_0

                    Ztr_A = Z_0 * (z_orifice + z_end + z_nl_urms*U_rms + z_ud)
                    surface_data_A[el] = Ztr_A

                for i, el in enumerate(surf_elements_B):

                    U_rms = 0
                    nodes_from_element = self.model.mesh.faces_connectivity[el, 4:]
                    connectivity_surface_B[el] = nodes_from_element

                    # if solution is not None:
                    #     p = solution[nodes_from_element, :]
                    #     p2_avg = np.average((1/2)*np.real(p*np.conj(p)), axis=0)
                    #     p_rms = np.sqrt(p2_avg)
                    #     U_rms = p_rms / Z_0

                    Ztr_B = Z_0 * (z_orifice + z_end + z_nl_urms*U_rms + z_ud)
                    surface_data_B[el] = Ztr_B

        if connectivity_surface_A and connectivity_surface_B:
            integration_data = {
                "connectivities_A": np.array(list(connectivity_surface_A.values()), dtype=int),
                "connectivities_B": np.array(list(connectivity_surface_B.values()), dtype=int),
                "surface_data_A": np.array(list(surface_data_A.values()), dtype=complex),
                "surface_data_B": np.array(list(surface_data_B.values()), dtype=complex),
                "non_linear": non_linear,
            }

        return integration_data


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

        self.mass_source_vector_points = np.array([])

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

                if not self.mass_source_vector_points.any():
                    self.mass_source_vector_points = np.zeros((self.total_dof, self.number_frequencies), dtype=complex)

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
                complex_values_array = self.get_value_in_array_form(values[0], flatten=True)

                self.mass_source_vector_points[node_id, :] += complex_values_array / fluid.fluid_density

        if self.mass_source_vector_points.any():
            self.mass_source_vector_points = self.mass_source_vector_points[self.unprescribed_indexes, :]


    def process_nodal_mass_source_data_for_lines(self):
        """ 
        This method processes the nodal mass source vector data assigned 
        to lines.
        """

        self.mass_source_vector_lines = np.array([])

        for (property, *args), data in self.properties.line_properties.items():

            if property != "mass_source":
                continue

            if not isinstance(data, dict):
                continue

            if not self.mass_source_vector_lines.any():
                self.mass_source_vector_lines = np.zeros((self.total_dof, self.number_frequencies), dtype=complex)

            values = data.get("values")
            if values is None:
                continue

            nodes = self.model.mesh.get_nodes_from_line(args[0])
            if nodes is None:
                continue

            aux_ones = np.ones((nodes.size, 1), dtype=float)

            # normalize data type to array
            complex_values_array = self.get_value_in_array_form(values[0])

            self.mass_source_vector_lines[nodes, :] += aux_ones @ complex_values_array

        if self.mass_source_vector_lines.any():
            self.mass_source_vector_lines = self.mass_source_vector_lines[self.unprescribed_indexes, :]


    def process_nodal_mass_source_data_for_surfaces(self):
        """ 
        This method processes the nodal mass source vector data assigned 
        to surfaces.
        """

        self.mass_source_vector_surfaces = np.array([])

        for (property, *args), data in self.properties.surface_properties.items():

            if property != "mass_source":
                continue

            if not isinstance(data, dict):
                continue

            if not self.mass_source_vector_points.any():
                self.mass_source_vector_points = np.zeros((self.total_dof, self.number_frequencies), dtype=complex)

            values = data.get("values")
            if values is None:
                continue

            nodes = self.model.mesh.get_nodes_from_surface(args[0])
            if nodes is None:
                continue

            aux_ones = np.ones((nodes.size, 1), dtype=float)

            # normalize data type to array
            complex_values_array = self.get_value_in_array_form(values[0])

            self.mass_source_vector_surfaces[nodes, :] += aux_ones @ complex_values_array

        if self.mass_source_vector_surfaces.any():
            self.mass_source_vector_surfaces = self.mass_source_vector_surfaces[self.unprescribed_indexes, :]


    def process_nodal_mass_source_data_for_volumes(self):
        """ 
        This method processes the nodal mass source vector data assigned 
        to volumes.
        """

        self.mass_source_vector_volumes = np.array([])

        for (property, *args), data in self.properties.volume_properties.items():

            if property != "mass_source":
                continue

            if not isinstance(data, dict):
                continue

            if not self.mass_source_vector_volumes.any():
                self.mass_source_vector_volumes = np.zeros((self.total_dof, self.number_frequencies), dtype=complex)

            values = data.get("values")
            if values is None:
                continue

            nodes = self.model.mesh.get_nodes_from_volume(args[0])
            if nodes is None:
                continue

            aux_ones = np.ones((nodes.size, 1), dtype=float)

            # normalize data type to array
            complex_values_array = self.get_value_in_array_form(values[0])

            self.mass_source_vector_volumes[nodes, :] += aux_ones @ complex_values_array

        if self.mass_source_vector_volumes.any():
            self.mass_source_vector_volumes = self.mass_source_vector_volumes[self.unprescribed_indexes, :]


    def process_mass_source_data_to_assemble_matrices(self):
        """
        This method assembles the mass source matrices Q_ms1 and Q_ms2.

        Parameters
        ----------
        index: int, optional
            The frequency index.
        """

        self.process_nodal_mass_source_data()

        if self.mass_source_vector_lines.any():
        
            self.ind_rows_Qmsf_1d = np.array([], dtype=int)
            self.ind_cols_Qmsf_1d = np.array([], dtype=int)

            self.integration_data_Qms_1d = self.get_mass_source_data_for_1d_element_integration()

            if self.integration_data_Qms_1d:

                logging.info("Processing the mass source data to assemble matrices (1d elements)... [1/2]")
                connectivities = self.integration_data_Qms_1d.get("connectivities")

                logging.info("Processing the mass source data to assemble matrices (1d elements)... [2/2]")
                self.ind_rows_Qmsf_1d, self.ind_cols_Qmsf_1d = self.element_1d.generate_ind_rows_cols(connectivities)
                self.int1d_NtN, self.int1d_BtB = self.element_1d.stacked_matrices_NtN_and_BtB()

        if self.mass_source_vector_surfaces.any():

            self.ind_rows_Qmsf_2d = np.array([], dtype=int)
            self.ind_cols_Qmsf_2d = np.array([], dtype=int)

            self.integration_data_Qms_2d = self.get_mass_source_data_for_2d_element_integration()
            if self.integration_data_Qms_2d:

                logging.info("Processing the mass source data to assemble matrices (2d elements)... [1/2]")
                connectivities = self.integration_data_Qms_2d.get("connectivities")

                logging.info("Processing the mass source data to assemble matrices (2d elements)... [2/2]")
                self.ind_rows_Qmsf_2d, self.ind_cols_Qmsf_2d = self.element_2d.generate_ind_rows_cols(connectivities)
                self.int2d_NtN, self.int2d_BtB = self.element_2d.stacked_matrices_NtN_and_BtB()


    def compute_data_to_assemble_global_matrices(self, reorder: bool = True):
        """ 
        This method processes the data required to assemble the global matrices
        based on the stacked elementary matrices.

        Parameters
        ----------
        reorder: bool, optional
            Control when the connectivity matrix will be reordered.
        """

        self.ind_rows, self.ind_cols = self.element_3d.generate_ind_rows_cols(reorder=reorder)

        self.dof = self.element_3d.DOF_PER_ELEMENT
        self.number_3d_elements = len(self.element_3d.connectivity)
        self.total_dof = self.element_3d.DOF_PER_NODE * len(self.element_3d.nodal_coordinates)

        # global_matrices shape
        self.gm_shape = (self.total_dof, self.total_dof)

        logging.info("Processing the elementary matrices data... [25/100]")
        self.int3d_BtB, self.int3d_NtN = self.element_3d.stacked_elementary_matrices_NtN_BtB()

        if self.model.stop_processing:
            return True

        logging.info("Processing the elementary matrices data... [85/100]")
        self.fluid_properties_from_volume, self.frequency_dependent = self.model.map_fluid_properties_to_volumes()

        logging.info("Processing the elementary matrices data... [95/100]")
        self.process_indexes()


    def compute_data_to_assemble_global_matrices_using_loop(self, reorder: bool = True):
        """ 
        This method processes the data required to assemble the global matrices
        sweeping all solid elements.

        Parameters
        ----------
        reorder: bool, optional
            Control when the connectivity matrix will be reordered.
        """

        self.ind_rows, self.ind_cols = self.element_3d.generate_ind_rows_cols(reorder=reorder)

        self.dof = self.element_3d.DOF_PER_ELEMENT
        self.number_3d_elements = len(self.element_3d.connectivity)
        self.total_dof = self.element_3d.DOF_PER_NODE * len(self.element_3d.nodal_coordinates)

        # global_matrices shape
        self.gm_shape = (self.total_dof, self.total_dof)

        self.int3d_BtB = np.zeros((self.number_3d_elements, self.dof, self.dof), dtype=complex)
        self.int3d_NtN = np.zeros((self.number_3d_elements, self.dof, self.dof), dtype=complex)

        last_progress = 0
        with tqdm(range(self.number_3d_elements), desc="Processing the elementary matrices data", unit="element") as progress_bar:
            for element_id in progress_bar:
                if self.model.stop_processing:
                    return True

                progress = int(100 * (element_id / self.number_3d_elements))
                if progress != last_progress:
                    logging.info(f"Processing the elementary matrices data... [{progress}/100]")

                last_progress = progress

                Ke, Me = self.element_3d.elementary_matrices(element_id)
                self.int3d_BtB[element_id, :, :] = Ke
                self.int3d_NtN[element_id, :, :] = Me

        self.fluid_properties_from_volume, self.frequency_dependent = self.model.map_fluid_properties_to_volumes()
        self.process_indexes()

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

        if not self.mass_source_vector_lines.any():
            return

        factor_Qms1 = self.integration_data_Qms_1d.get("factor_Qms1")
        factor_Qms2 = self.integration_data_Qms_1d.get("factor_Qms2")

        data_Qms1 = factor_Qms1[:, index].reshape(-1, 1, 1) * self.int1d_NtN
        Q_ms1 = csr_matrix((data_Qms1.flatten(), (self.ind_rows_Qmsf_1d, self.ind_cols_Qmsf_1d)), shape=self.gm_shape)

        data_Qms2 = factor_Qms2[:, index].reshape(-1, 1, 1) * self.int1d_BtB
        Q_ms2 = csr_matrix((data_Qms2.flatten(), (self.ind_rows_Qmsf_1d, self.ind_cols_Qmsf_1d)), shape=self.gm_shape)

        self.Qms1_1d = Q_ms1[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.Qms2_1d = Q_ms2[self.unprescribed_indexes, :][:, self.unprescribed_indexes]


    def assemble_mass_source_matrices_from_surfaces(self, index: int = 0):
        """
        This method assembles the mass source matrices Q_ms1 and Q_ms2
        due to surface assignment.

        Parameters
        ----------
        index: int, optional
            The frequency index.
        """

        if not self.mass_source_vector_surfaces.any():
            return

        factor_Qms1 = self.integration_data_Qms_2d.get("factor_Qms1")
        factor_Qms2 = self.integration_data_Qms_2d.get("factor_Qms2")

        data_Qms1 = factor_Qms1[:, index].reshape(-1, 1, 1) * self.int2d_NtN
        Q_ms1 = csr_matrix((data_Qms1.flatten(), (self.ind_rows_Qmsf_2d, self.ind_cols_Qmsf_2d)), shape=self.gm_shape)

        data_Qms2 = factor_Qms2[:, index].reshape(-1, 1, 1) * self.int2d_BtB
        Q_ms2 = csr_matrix((data_Qms2.flatten(), (self.ind_rows_Qmsf_2d, self.ind_cols_Qmsf_2d)), shape=self.gm_shape)

        self.Qms1_2d = Q_ms1[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.Qms2_2d = Q_ms2[self.unprescribed_indexes, :][:, self.unprescribed_indexes]


    def assemble_mass_source_matrices_from_volumes(self, index: int = 0):
        """
        This method assembles the mass source matrices Q_ms1 and Q_ms2
        due to volume assignment.

        Parameters
        ----------
        index: int, optional
            The frequency index.
        """

        if not self.mass_source_vector_volumes.any():
            return

        factor_Qms1, factor_Qms2 = self.compute_mass_source_load_factors_for_volumes(index=index)

        data_Qms1 = factor_Qms1 * self.int3d_NtN
        Q_ms1 = csr_matrix((data_Qms1.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        data_Qms2 = factor_Qms2 * self.int3d_BtB
        Q_ms2 = csr_matrix((data_Qms2.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        self.Qms1_3d = Q_ms1[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.Qms2_3d = Q_ms2[self.unprescribed_indexes, :][:, self.unprescribed_indexes]


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
        if self.mass_source_vector_points.any():
            mass_source_p = self.mass_source_vector_points[:, index]
            Q_ms += 1j * omega * mass_source_p

        if self.mass_source_vector_lines.any():
            mass_source_l = self.mass_source_vector_lines[:, index]
            Q_ms += (1j * omega * self.Qms1_1d + self.Qms2_1d) @ mass_source_l

        if self.mass_source_vector_surfaces.any():
            mass_source_s = self.mass_source_vector_surfaces[:, index]
            Q_ms += (1j * omega * self.Qms1_2d + self.Qms2_2d) @ mass_source_s

        if self.mass_source_vector_volumes.any():
            mass_source_v = self.mass_source_vector_volumes[:, index]
            Q_ms += (1j * omega * self.Qms1_3d + self.Qms2_3d) @ mass_source_v

        return Q_ms


    def process_specific_impedance_data_to_assemble_damping_matrix(self):
        """ 
        This method processes the specific impedance data to assemble
        the global damping matrix.
        """

        self.data_Zsi = {}
        self.ind_rows_Zsi = np.array([], dtype=int)
        self.ind_cols_Zsi = np.array([], dtype=int)

        dof = self.element_2d.DOF_PER_ELEMENT
        self.total_dof_2d = self.element_2d.DOF_PER_NODE * len(self.element_2d.nodal_coordinates)

        self.integration_data_Zsi = self.get_impedance_data_for_element_integration("specific_impedance")
        if not self.integration_data_Zsi:
            return

        logging.info("Processing the impedance data to assemble damping matrix... [1/14]")
        connectivities = self.integration_data_Zsi.get("connectivities")       
        Z_si = self.integration_data_Zsi.get("surface_data")

        nel = connectivities.shape[0]
        for j in range(self.number_frequencies):
            self.data_Zsi[j] = np.zeros((nel, dof, dof), dtype=complex)

        logging.info("Processing the impedance data to assemble damping matrix... [2/14]")
        self.ind_rows_Zsi, self.ind_cols_Zsi = self.element_2d.generate_ind_rows_cols(connectivities)
        int2d_NtN = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zsi[j] = int2d_NtN / Z_si[:, j].reshape(-1, 1, 1)


    def process_anechoic_termination_data_to_assemble_damping_matrix(self):
        """ 
        This method processes the anechoic termination data to assemble
        the global damping matrix.
        """

        self.data_Zat = {}
        self.ind_rows_Zat = np.array([], dtype=int)
        self.ind_cols_Zat = np.array([], dtype=int)

        dof = self.element_2d.DOF_PER_ELEMENT
        self.total_dof_2d = self.element_2d.DOF_PER_NODE * len(self.element_2d.nodal_coordinates)

        self.integration_data_Zat = self.get_impedance_data_for_element_integration("anechoic_termination")
        if not self.integration_data_Zat:
            return

        logging.info("Processing the impedance data to assemble damping matrix... [3/14]")
        connectivities = self.integration_data_Zat.get("connectivities")       
        Z_at = self.integration_data_Zat.get("surface_data")

        nel = connectivities.shape[0]
        for j in range(self.number_frequencies):
            self.data_Zat[j] = np.zeros((nel, dof, dof), dtype=complex)

        logging.info("Processinng the impedance data to assemble damping matrix... [4/14]")
        self.ind_rows_Zat, self.ind_cols_Zat = self.element_2d.generate_ind_rows_cols(connectivities)
        int2d_NtN = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zat[j] = int2d_NtN / Z_at[:, j].reshape(-1, 1, 1)


    def process_incident_plane_wave_data_to_assemble_damping_matrix(self):
        """ 
        This method processes the incident plane wave data to assemble
        the global damping matrix.
        """

        self.data_Zipw = {}
        self.ind_rows_Zipw = np.array([], dtype=int)
        self.ind_cols_Zipw = np.array([], dtype=int)

        self.integration_data_ipw = self.get_incident_plane_wave_surface_data_for_element_integration()
        if not isinstance(self.integration_data_ipw, IncidentPlaneWaveIntegrationData):
            return

        logging.info("Processing the impedance data to assemble damping matrix... [5/14]")
        ipw_vector: np.ndarray = self.integration_data_ipw.ipw_vector
        Z_ipw: np.ndarray = self.integration_data_ipw.ipw_impedance
        connectivities: np.ndarray = self.integration_data_ipw.connectivities
        element_normals: np.ndarray = self.integration_data_ipw.element_face_normals

        dof = self.element_2d.DOF_PER_ELEMENT
        self.total_dof_2d = self.element_2d.DOF_PER_NODE * len(self.element_2d.nodal_coordinates)

        nel = connectivities.shape[0]
        for j in range(self.number_frequencies):
            self.data_Zipw[j] = np.zeros((nel, dof, dof), dtype=complex)

        logging.info("Processing the impedance data to assemble damping matrix... [6/14]")
        self.ind_rows_Zipw, self.ind_cols_Zipw = self.element_2d.generate_ind_rows_cols(connectivities)
        int2d_NtN = self.element_2d.stacked_matrices_NtN()

        s_vector = ipw_vector.reshape(3, 1)
        n_vectors = element_normals.reshape(-1, 1, 3)

        # the dot product between incident plane wave vector and the face element normal vector
        n_k = np.dot(n_vectors, s_vector)

        for j in range(self.number_frequencies):
            # the negative signal is being used to revert the signal from the elementary matrix
            self.data_Zipw[j] = -(n_k / Z_ipw[j]) * int2d_NtN


    def process_surface_impedance_data_to_assemble_damping_matrix(self):
        """ 
        This method processes the surface impedance data resulting from
        absorption surface to assemble the global damping matrix.
        """

        self.data_Zas = {}
        self.ind_rows_Zas = np.array([])
        self.ind_cols_Zas = np.array([])

        dof = self.element_2d.DOF_PER_ELEMENT
        self.total_dof_2d = self.element_2d.DOF_PER_NODE * len(self.element_2d.nodal_coordinates)

        self.integration_data_Zas = self.get_impedance_data_for_element_integration("absorption_surface")
        if not self.integration_data_Zas:
            return

        logging.info("Processing the impedance data to assemble damping matrix... [7/14]")
        connectivities = self.integration_data_Zas.get("connectivities")       
        Z_as = self.integration_data_Zas.get("surface_data")

        nel = connectivities.shape[0]
        for j in range(self.number_frequencies):
            self.data_Zas[j] = np.zeros((nel, dof, dof), dtype=complex)

        logging.info("Processing the impedance data to assemble damping matrix... [8/14]")
        self.ind_rows_Zas, self.ind_cols_Zas = self.element_2d.generate_ind_rows_cols(connectivities)
        int2d_NtN = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zas[j] = int2d_NtN / Z_as[:, j].reshape(-1, 1, 1)


    def process_transfer_impedance_data_to_assemble_damping_matrix(self):
        """
        This method processes the internal transfer impedance data 
        to assemble the global damping matrix.
        """

        self.data_Zti_A = {}
        self.ind_rows_Zti_A = np.array([])
        self.ind_cols_Zti_A = np.array([])

        self.data_Zti_B = {}
        self.ind_rows_Zti_B = np.array([])
        self.ind_cols_Zti_B = np.array([])

        dof = self.element_2d.DOF_PER_ELEMENT
        self.total_dof_2d = self.element_2d.DOF_PER_NODE * len(self.element_2d.nodal_coordinates)

        self.integration_data_Zti = self.get_transfer_impedance_data_for_element_integration()
        if not self.integration_data_Zti:
            return

        logging.info("Processing the impedance data to assemble damping matrix... [9/14]")
        connectivities_A = self.integration_data_Zti.get("connectivities_A")
        connectivities_B = self.integration_data_Zti.get("connectivities_B")
        Zti_A = self.integration_data_Zti.get("surface_data_A")
        Zti_B = self.integration_data_Zti.get("surface_data_B")

        nel_A = connectivities_A.shape[0]
        nel_B = connectivities_B.shape[0]

        for j in range(self.number_frequencies):
            self.data_Zti_A[j] = np.zeros((nel_A, dof, dof), dtype=complex)
            self.data_Zti_B[j] = np.zeros((nel_B, dof, dof), dtype=complex)

        logging.info("Processing the impedance data to assemble damping matrix... [10/14]")
        self.ind_rows_Zti_A, self.ind_cols_Zti_A = self.element_2d.generate_ind_rows_cols(connectivities_A)
        int2d_NtN_A = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zti_A[j] = int2d_NtN_A / Zti_A[:, j].reshape(-1, 1, 1)

        logging.info("Processing the impedance data to assemble damping matrix... [11/14]")
        self.ind_rows_Zti_B, self.ind_cols_Zti_B = self.element_2d.generate_ind_rows_cols(connectivities_B)
        int2d_NtN_B = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zti_B[j] = int2d_NtN_B / Zti_B[:, j].reshape(-1, 1, 1)


    def process_perforated_plate_impedance_data_to_assemble_damping_matrix(self, solution: np.ndarray | None = None):
        """
        This method processes the perforated plate impedance data 
        to assemble the global damping matrix.

        Parameters
        ----------
        solution: np.ndarray, optional
        """

        self.data_Zpp_A = {}
        self.ind_rows_Zpp_A = np.array([])
        self.ind_cols_Zpp_A = np.array([])

        self.data_Zpp_B = {}
        self.ind_rows_Zpp_B = np.array([])
        self.ind_cols_Zpp_B = np.array([])

        dof = self.element_2d.DOF_PER_ELEMENT
        self.total_dof_2d = self.element_2d.DOF_PER_NODE * len(self.element_2d.nodal_coordinates)

        self.integration_data_Zpp = self.get_perforated_plate_data_for_element_integration(solution)
        if not self.integration_data_Zpp:
            return

        logging.info("Processing the impedance data to assemble damping matrix... [12/14]")

        Zpp_A = self.integration_data_Zpp.get("surface_data_A")
        Zpp_B = self.integration_data_Zpp.get("surface_data_B")
        # non_linear = self.integration_data_Zpp.get("non_linear")
        connectivities_A = self.integration_data_Zpp.get("connectivities_A")
        connectivities_B = self.integration_data_Zpp.get("connectivities_B")

        nel_A = connectivities_A.shape[0]
        nel_B = connectivities_B.shape[0]

        for j in range(self.number_frequencies):
            self.data_Zpp_A[j] = np.zeros((nel_A, dof, dof), dtype=complex)
            self.data_Zpp_B[j] = np.zeros((nel_B, dof, dof), dtype=complex)

        logging.info("Processing the impedance data to assemble damping matrix... [13/14]")
        self.ind_rows_Zpp_A, self.ind_cols_Zpp_A = self.element_2d.generate_ind_rows_cols(connectivities_A)
        int2d_NtN_A = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zpp_A[j] = int2d_NtN_A / Zpp_A[:, j].reshape(-1, 1, 1)

        logging.info("Processing the impedance data to assemble damping matrix... [14/14]")
        self.ind_rows_Zpp_B, self.ind_cols_Zpp_B = self.element_2d.generate_ind_rows_cols(connectivities_B)
        int2d_NtN_B = self.element_2d.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zpp_B[j] = int2d_NtN_B / Zpp_B[:, j].reshape(-1, 1, 1)


    def compute_data_to_assemble_damping_matrix(self):
        self.process_specific_impedance_data_to_assemble_damping_matrix()
        self.process_anechoic_termination_data_to_assemble_damping_matrix()
        self.process_incident_plane_wave_data_to_assemble_damping_matrix()
        self.process_surface_impedance_data_to_assemble_damping_matrix()
        self.process_transfer_impedance_data_to_assemble_damping_matrix()
        self.process_perforated_plate_impedance_data_to_assemble_damping_matrix()


    def assemble_global_stiffness_matrix(self, factor_K: np.ndarray):
        """
        This method assembles the global stiffness matrix.

        Parameters
        ----------
        factor_K: np.ndarray
            An array containing all elementary stiffness factors in stacked form.
        """
        data_K = self.int3d_BtB * factor_K
        _stiffness_matrix_full = csr_matrix((data_K.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.stiffness_matrix_r = _stiffness_matrix_full[:, self.prescribed_indexes]


    def assemble_global_mass_matrix(self, factor_M: np.ndarray):
        """
        This method assembles the global mass matrix.

        Parameters
        ----------
        factor_M: np.ndarray
            An array containing all elementary mass factors in stacked form.
        """
        data_M = self.int3d_NtN * factor_M
        _mass_matrix_full = csr_matrix((data_M.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        self.mass_matrix = _mass_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.mass_matrix_r = _mass_matrix_full[:, self.prescribed_indexes]


    def assemble_global_damping_matrix_3d_elements(self, factor_Cvsic: np.ndarray, factor_fvsic: np.ndarray):
        """
        This method assembles the global damping matrix to account
        the bulk damping effects.
        https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_thry/thy_acou2.html#thyeqacous-75
        """

        data_C = self.int3d_BtB * factor_Cvsic
        _visc_damping_matrix_full = csr_matrix((data_C.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        self.visc_damping_matrix = _visc_damping_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.visc_damping_matrix_r = _visc_damping_matrix_full[:, self.prescribed_indexes]

        data_f = self.int3d_BtB * factor_fvsic
        _load_vector_viscous_full = csr_matrix((data_f.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        self.load_vector_viscous = _load_vector_viscous_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        # self.load_vector_viscous_r = _load_vector_viscous_full[:, self.prescribed_indexes]


    def assemble_global_damping_matrix_2d_elements(self, index: int = 0):
        """
        This method computes the global damping matrix asseble.

        Parameters
        ----------
        index: int, optional.
            It corresponds to the frequency step index.
        """

        N_dof = self.total_dof_2d
        rows_Zout = np.array([], dtype=int)
        cols_Zout = np.array([], dtype=int)
        data_Zout = np.array([], dtype=complex)

        if self.integration_data_Zsi:
            rows_Zout = self.ind_rows_Zsi
            cols_Zout = self.ind_cols_Zsi
            data_Zout = self.data_Zsi[index].flatten()

        if self.integration_data_Zat:
            rows_Zout = np.append(rows_Zout, self.ind_rows_Zat) 
            cols_Zout = np.append(cols_Zout, self.ind_cols_Zat)
            data_Zout = np.append(data_Zout, self.data_Zat[index].flatten())

        if isinstance(self.integration_data_ipw, IncidentPlaneWaveIntegrationData):
            rows_Zout = np.append(rows_Zout, self.ind_rows_Zipw) 
            cols_Zout = np.append(cols_Zout, self.ind_cols_Zipw)
            data_Zout = np.append(data_Zout, self.data_Zipw[index].flatten())

        if self.integration_data_Zas:
            rows_Zout = np.append(rows_Zout, self.ind_rows_Zas) 
            cols_Zout = np.append(cols_Zout, self.ind_cols_Zas)
            data_Zout = np.append(data_Zout, self.data_Zas[index].flatten())

        if data_Zout.size:
            _matrix_full_A = csr_matrix((data_Zout, (rows_Zout, cols_Zout)), shape=(N_dof, N_dof))

        else:
            _matrix_full_A = csr_matrix((N_dof, N_dof))

        rows_A = np.array([], dtype=int)
        rows_B = np.array([], dtype=int)
        cols_A = np.array([], dtype=int)
        cols_B = np.array([], dtype=int)
        Zin_A = np.array([], dtype=complex)
        Zin_B = np.array([], dtype=complex)

        if self.integration_data_Zpp:
            rows_A = self.ind_rows_Zpp_A
            rows_B = self.ind_rows_Zpp_B
            cols_A = self.ind_cols_Zpp_A
            cols_B = self.ind_cols_Zpp_B
            Zin_A = self.data_Zpp_A[index].flatten()
            Zin_B = self.data_Zpp_B[index].flatten()

        if self.integration_data_Zti:
            rows_A = np.concatenate((rows_A, self.ind_rows_Zti_A))
            rows_B = np.concatenate((rows_B, self.ind_rows_Zti_B))
            cols_A = np.concatenate((cols_A, self.ind_cols_Zti_A))
            cols_B = np.concatenate((cols_B, self.ind_cols_Zti_B))
            Zin_A = np.concatenate((Zin_A, self.data_Zti_A[index].flatten()))
            Zin_B = np.concatenate((Zin_B, self.data_Zti_B[index].flatten()))

        if rows_A.size:
            values_Zin = np.concatenate((Zin_A, -Zin_A, -Zin_B, Zin_B))
            rows_Zin = np.concatenate((rows_A, rows_A, rows_B, rows_B))
            cols_Zin = np.concatenate((cols_A, cols_B, cols_A, cols_B))
            _matrix_full_B = csr_matrix((values_Zin, (rows_Zin, cols_Zin)), shape=(N_dof, N_dof))

        else:
            _matrix_full_B = csr_matrix((N_dof, N_dof))

        _matrix_full = _matrix_full_A + _matrix_full_B

        self.damping_matrix = _matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.damping_matrix_r = _matrix_full[:, self.prescribed_indexes]


    def get_acoustic_excitations_by_nodal_attribution(self):
        """ 
        This method processes the acoustic model excitations and
        returns the output data in the form of mass flow rate.
        """

        aux_ones = np.ones((self.number_frequencies), dtype=complex)
        acoustic_excitation = defaultdict(float)

        for (property, surface_id), data in self.properties.surface_properties.items():
            if property in ["surface_velocity", "reciprocating_compressor_excitation"]:

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

                if data["nodal_attribution"]:
                    nodes = self.model.mesh.get_nodes_from_surface(surface_id)
                    if nodes is None:
                        continue

                    N = len(nodes)
                    self.model.mesh.process_face_elements_connected_to_nodes(surface_id)
                    area = self.model.mesh.surface_area_from_element_integration[surface_id]

                    for index in self.model.get_acoustic_global_dof_from_nodes(nodes):
                        if data["averaged"]:
                            acoustic_excitation[index] += (complex_values * area) / N
                        else:
                            acoustic_excitation[index] += complex_values * area

        total_dof = self.element_3d.DOF_PER_NODE * len(self.element_3d.nodal_coordinates)
        output = np.zeros((total_dof, self.number_frequencies), dtype=complex)

        if acoustic_excitation:
            indexes = list(acoustic_excitation)
            excitation = list(acoustic_excitation.values())
            output[indexes, :] = np.array(excitation)

        if self.prescribed_indexes:
            return output[self.unprescribed_indexes, :]
        else:
            return output


    def get_acoustic_excitations_by_element_integration(self):
        """ 
        This method processes the acoustic model excitations and
        returns the output data in the form of mass flow rate.
        """

        total_dof = self.element_2d.DOF_PER_NODE * len(self.element_2d.nodal_coordinates)
        output = np.zeros((total_dof, self.number_frequencies), dtype=complex)

        prop_labels = [
            "surface_velocity",
            "compressor_excitation_spectrum",
            "compressor_excitation_waveform",
            "reciprocating_compressor_excitation",
        ]

        for prop_label in prop_labels:
            integration_data_sv = self.get_excitation_data_for_element_integration(prop_label)

            if integration_data_sv:
                connectivities_sv = integration_data_sv.get("connectivities")
                surface_data_sv = integration_data_sv.get("surface_data")

                self.element_2d.reorder_connect(connectivities_sv)
                for i, complex_values in enumerate(surface_data_sv):
                    indices = self.element_2d.connectivities[i, :]
                    int2d_N = self.element_2d.load_vector(i)
                    output[indices, :] += int2d_N @ complex_values.reshape(1, -1)

        if isinstance(self.integration_data_ipw, IncidentPlaneWaveIntegrationData):
            p_inc: np.ndarray = self.integration_data_ipw.ipw_pressure
            s_vector: np.ndarray = self.integration_data_ipw.ipw_vector
            Z_ipw: np.ndarray = self.integration_data_ipw.ipw_impedance
            connectivities: np.ndarray = self.integration_data_ipw.connectivities
            element_normals: np.ndarray = self.integration_data_ipw.element_face_normals

            self.element_2d.reorder_connect(connectivities)

            for i, n_vector in enumerate(element_normals):

                int2d_N = self.element_2d.load_vector(i)

                # element face connectivity
                indices = self.element_2d.connectivities[i, :]

                # auxilar vector
                aux: np.ndarray =  2 * np.dot(n_vector, s_vector) * p_inc / Z_ipw

                # assemble the acoustic load
                output[indices, :] += int2d_N @ aux.reshape(1, -1)

        if self.prescribed_indexes:
            return output[self.unprescribed_indexes, :]

        return output


    def assemble_global_matrices(self, reorder: bool=True, stacked_matrices: bool=True):
        """
        This method assembles the global matrices of the acoustic model.
        """

        logging.info("Processing data to assemble global matrices... [10/100]")
        self.define_acoustic_elements()
        self.update_number_of_frequencies()

        logging.info("Processing data to assemble global matrices... [20/100]")
        t0 = time()
        if stacked_matrices:
            self.compute_data_to_assemble_global_matrices(reorder=reorder)
        else:
            self.compute_data_to_assemble_global_matrices_using_loop(reorder=reorder)
        dt = time() - t0
        print(f"Elapsed time to gather data to assemble global matrices: {dt : .6f} [s]")

        if self.model.stop_processing:
            return

        logging.info("Processing data to assemble damping matrix... [40/100]")
        t0 = time()
        self.compute_data_to_assemble_damping_matrix()
        dt = time() - t0
        print(f"Elapsed time to gather data to assemble damping matrices: {dt : .6f} [s]")

        logging.info("Computing the global matrices factors... [45/100]")
        t0 = time()
        factor_K, factor_M, factor_Cvisc, factor_fvisc = self.compute_global_matrices_factors()
        dt = time() - t0
        print(f"Elapsed time to compute global matrices factor: {dt : .6f} [s]")

        logging.info("Assembling global stiffness matrix... [50/100]")
        t0 = time()
        self.assemble_global_stiffness_matrix(factor_K)
        dt = time() - t0
        print(f"Elapsed time to assemble the global stiffness matrix: {dt : .6f} [s]")

        logging.info("Assembling global mass matrix... [60/100]")
        t0 = time()
        self.assemble_global_mass_matrix(factor_M)
        dt = time() - t0
        print(f"Elapsed time to assemble the global mass matrix: {dt : .6f} [s]")

        logging.info("Assembling global mass matrix... [70/100]")
        t0 = time()
        self.assemble_global_damping_matrix_3d_elements(factor_Cvisc, factor_fvisc)
        self.assemble_global_damping_matrix_2d_elements()
        dt = time() - t0
        print(f"Elapsed time to assemble the global damping matrix: {dt : .6f} [s]\n")


    def assemble_model_excitations(self):
        """
        This method assembles the excitations of the acoustic model.
        """

        logging.info("Processing element related loads... [75/100]")
        B = self.get_acoustic_excitations_by_element_integration()

        logging.info("Processing nodal related loads... [85/100]")
        A = self.get_acoustic_excitations_by_nodal_attribution()

        logging.info("Processing nodal related loads... [90/100]")
        self.process_mass_source_data_to_assemble_matrices()
        self.assemble_mass_source_matrices_from_lines()
        self.assemble_mass_source_matrices_from_surfaces()
        self.assemble_mass_source_matrices_from_volumes()

        logging.info("Finishing the model building... [98/100]")
        self.mass_flow_vectors = A + B


    def assemble_global_matrices_and_excitations(self, reorder: bool=True, stacked_matrices: bool=True, **kwargs):
        """
        This method assembles the global matrices and excitations of the acoustic model.
        """

        self.assemble_global_matrices(reorder = reorder, stacked_matrices = stacked_matrices)        
        self.assemble_model_excitations()


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
        unprescribed_indexes, prescribed_indexes = self.get_matrices_dropping_indexes()
        prescribed_values, array_prescribed_values = self.get_prescribed_dof_values()

        rows = solution.shape[0] + len(prescribed_indexes)
        cols = solution.shape[1]

        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[unprescribed_indexes, :] = solution

        if len(prescribed_indexes):
            if modal_analysis:
                full_solution[prescribed_indexes, :] = np.zeros((len(prescribed_values), cols))
            else:
                full_solution[prescribed_indexes, :] = array_prescribed_values[:, 0:cols]

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
        unprescribed_indexes, prescribed_indexes = self.get_matrices_dropping_indexes()
        _, array_prescribed_values = self.get_prescribed_dof_values()

        rows = solution.shape[0] + len(prescribed_indexes)

        full_solution = np.zeros(rows, dtype=complex)
        full_solution[unprescribed_indexes] = solution

        if len(prescribed_indexes):
            full_solution[prescribed_indexes] = array_prescribed_values[:, freq_index]

        return full_solution


    def build_harmonic_system(self, freq, i):

        # mass and stiffness matrices
        M = self.mass_matrix
        K = self.stiffness_matrix

        # create the frequency vector
        omega = 2 * np.pi * freq

        # update the damping matrix [C]
        self.assemble_global_damping_matrix_2d_elements(index=i)
        
        # damping matrices
        C_imp = self.damping_matrix
        C_visc = self.visc_damping_matrix
        C = C_imp + C_visc

        if self.frequency_dependent:
            # reassemble the global mass and stiffness matrices
            factor_K, factor_M, _, _ = self.compute_global_matrices_factors(index=i)
            self.assemble_global_mass_matrix(factor_M)
            self.assemble_global_stiffness_matrix(factor_K)

            M = self.mass_matrix
            K = self.stiffness_matrix

            # reassemble the mass source matrices
            self.assemble_mass_source_matrices_from_surfaces(index=i)
            self.assemble_mass_source_matrices_from_volumes(index=i)

        # update the prescribed dof-related load vector for each frequency step
        f_eq = self.get_prescribed_pressure_model_excitation(index=i)

        # mass source-related load vector
        f_ms = self.compute_mass_source_load_vector(omega, index=i)

        # viscous damping-related load vector 
        f_visc = self.load_vector_viscous @ self.mass_flow_vectors[:, i]

        # mass flow-related load vector
        f_mf = 1j * omega * self.mass_flow_vectors[:, i]

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