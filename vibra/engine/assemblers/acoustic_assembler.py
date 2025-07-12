from vibra.engine.model import Model

# 3D elements
from vibra.engine.elements.acoustic_hex8_element import ACT_HEXAHEDRON_8C
from vibra.engine.elements.acoustic_hex20_element import ACT_HEXAHEDRON_20C
from vibra.engine.elements.acoustic_tet4_element import ACT_TETRAHEDRON_4C
from vibra.engine.elements.acoustic_tet10_element import ACT_TETRAHEDRON_10C

# 2D elements
from vibra.engine.elements.acoustic_face3_element import ACT_FACE_3
from vibra.engine.elements.acoustic_face4_element import ACT_FACE_4
from vibra.engine.properties.fluid import Fluid
#
from vibra.engine.mesher.element_type import (
    TETRAHEDRON_4,
    TETRAHEDRON_10,
    HEXAHEDRON_8,
    HEXAHEDRON_20,
)

import logging
import numpy as np

from collections import defaultdict

from scipy.sparse import csr_matrix
from sys import getsizeof
from time import time


class AcousticAssembler:
    def __init__(self, model : Model):

        self.model = model
        self.properties = model.properties

        self.reset()


    def reset(self):
        self.frequency_dependent = False
        self.stiffness_matrix = None
        self.mass_matrix = None
        self.damping_matrix = None
        self.mass_flow_vectors = None
        self.frequencies = None
        self.number_frequencies = 1
        self.prescribed_values = list()
        self.prescribed_indexes = list()
        self.unprescribed_indexes = list()


    def get_element(self):
        element_type = self.model.mesh.element_type

        if element_type == TETRAHEDRON_4:
            return ACT_TETRAHEDRON_4C(self.model), ACT_FACE_3(self.model)
        elif element_type == TETRAHEDRON_10:
            return ACT_TETRAHEDRON_10C(self.model), None
        elif element_type == HEXAHEDRON_8:
            return ACT_HEXAHEDRON_8C(self.model), ACT_FACE_4(self.model)
        elif element_type == HEXAHEDRON_20:
            return ACT_HEXAHEDRON_20C(self.model), None
        else:
            raise NotImplementedError(f'Element type "{element_type}" is not supported yet.')


    def set_element_formulation(self, element):
        self.element = element


    def update_number_of_frequencies(self):
        self.frequencies = self.model.frequencies
        if self.frequencies is None:
            self.number_frequencies = 1
        else:
            self.number_frequencies = len(self.frequencies)


    def is_assembled(self):
        return (self.stiffness_matrix is not None) and (self.mass_matrix is not None)


    def get_prescribed_dofs_values(self):
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

        global_prescribed = list()
        list_prescribed_dofs = list()

        aux_ones = np.ones(self.number_frequencies, dtype=complex)

        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "acoustic_pressure":

                if "values" in data.keys():
                    complex_values = data["values"]
                else:
                    real_values = np.array(data["real_values"])
                    imag_values = np.array(data["imag_values"])
                    complex_values = real_values + 1j * imag_values
                
                nodes = self.model.mesh.nodes_from_surfaces[surface_id]

                for _ in nodes:
                    for _complex_values in complex_values:
                        global_prescribed.append(_complex_values)

        # TODO: implement same structure for lines

        try:

            for value in global_prescribed:
                if isinstance(value, complex):
                    list_prescribed_dofs.append(aux_ones * value)
                elif isinstance(value, np.ndarray):
                    if len(value) == 1:
                       list_prescribed_dofs.append(aux_ones * value)
                    else: 
                        list_prescribed_dofs.append(value[0:self.number_frequencies])

            array_prescribed_values = np.array(list_prescribed_dofs)

        except Exception as _error_log:
            print(str(_error_log))

        return global_prescribed, array_prescribed_values


    def get_prescribed_indexes(self):
        """
        Returns the prescribed dof indexes.
        """
        _prescribed_indexes = list()
        for key, _ in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "acoustic_pressure":
                nodes = self.model.mesh.nodes_from_surfaces[surface_id]
                for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
                    _prescribed_indexes.append(index)

        return _prescribed_indexes


    def get_unprescribed_indexes(self):
        """ 
        Returns the unprescribed dof indexes.
        """
        element_3D, _ = self.get_element()
        total_dofs = element_3D.DOFS_PER_NODE * len(element_3D.nodal_coordinates)
        all_indexes = np.arange(total_dofs, dtype=int)
        prescribed_indexes = self.get_prescribed_indexes()
        return np.delete(all_indexes, prescribed_indexes)


    def process_indexes(self):
        self.prescribed_indexes = self.get_prescribed_indexes()
        self.unprescribed_indexes = self.get_unprescribed_indexes()


    def get_matrices_dropping_indexes(self):
        return self.unprescribed_indexes, self.prescribed_indexes


    def get_surface_data_for_element_integration_by_property(self, property_label: str) -> dict:
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

        aux_data = dict()
        aux_connect = dict()
        integration_data = dict()

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop != property_label:
                continue

            rho_eff_pm, C_eff_pm = self.model.get_porous_material_model_effective_properties(surface_id)
            rho_eff_tv, C_eff_tv = self.model.get_viscous_thermal_model_effective_properties(surface_id)

            if isinstance(rho_eff_pm, np.ndarray):
                density = rho_eff_pm
                speed_of_sound = C_eff_pm

            elif isinstance(rho_eff_tv, np.ndarray):
                density = rho_eff_tv
                speed_of_sound = C_eff_tv

            else:
                fluid = self.model.properties._get_property("fluid", surface=surface_id)
                density = fluid.fluid_density
                speed_of_sound = fluid.speed_of_sound

            data: dict
            if "anechoic_termination" in data.keys():
                _complex_values = density * speed_of_sound

            elif property_label ==  "absorption_surface":
                alpha = np.array(data.get("values")[0], dtype=float)
                Z_0 = density * speed_of_sound
                Z_s = Z_0 * ((1 + (1-alpha)**(1/2)) / (1 - (1-alpha)**(1/2)))
                _complex_values = Z_s

            else:
                if "values" in data.keys():
                    _complex_values = data.get("values")[0]

            complex_values = self.get_value_in_array_form(_complex_values, flatten=True)

            surface_elements = list(self.model.mesh.elements_from_surface[surface_id])
            surf_connect = self.model.mesh.connectivity_from_surfaces[surface_id]    

            for i, el in enumerate(surface_elements):
                aux_connect[el] = surf_connect[i]
                aux_data[el] = complex_values

        if aux_connect:
            integration_data = {
                                "connectivities" : np.array(list(aux_connect.values()), dtype=int),
                                "surface_data" : np.array(list(aux_data.values()), dtype=complex),
                                }

        return integration_data


    def get_plane_wave_surface_data_for_element_integration(self) -> dict:
        """ 
        This method processes the plane wave data for element face
        integration.

        Returns
        -------
        integration_data: dict
            A dictionary containing the connectivities and the data of each
            processed 2d elements.
        """

        aux_connect = dict()
        integration_data = dict()

        k_wave = dict()
        e_normals = dict()
        pressures = dict()
        plane_wave_impedances = dict()

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop != "incident_plane_wave":
                continue

            rho_eff_pm, C_eff_pm = self.model.get_porous_material_model_effective_properties(surface_id)
            rho_eff_tv, C_eff_tv = self.model.get_viscous_thermal_model_effective_properties(surface_id)

            wave_vector = np.array(data.get("wave_vector"), dtype=float)
            norm_wave_vector = np.linalg.norm(wave_vector)
            if norm_wave_vector > 1:
                wave_vector /= norm_wave_vector

            if isinstance(rho_eff_pm, np.ndarray):
                density = rho_eff_pm
                speed_of_sound = C_eff_pm

            elif isinstance(rho_eff_tv, np.ndarray):
                density = rho_eff_tv
                speed_of_sound = C_eff_tv

            else:
                fluid = self.model.properties._get_property("fluid", surface=surface_id)
                density = fluid.fluid_density
                speed_of_sound = fluid.speed_of_sound

            surface_elements = list(self.model.mesh.elements_from_surface[surface_id])
            surf_connect = self.model.mesh.connectivity_from_surfaces[surface_id]

            data: dict
            values = data.get("values")
            p_inc = self.get_value_in_array_form(values[0], flatten=True)
            Z = self.get_value_in_array_form(density * speed_of_sound, flatten=True)

            for i, el in enumerate(surface_elements):
                aux_connect[el] = surf_connect[i]
                plane_wave_impedances[el] = Z
                e_normals[el] = self.model.mesh.get_element_face_normal(surf_connect[i])
                k_wave[el] = wave_vector
                pressures[el] = p_inc

        if aux_connect:
            connectivities = np.array(list(aux_connect.values()), dtype=int)
            integration_data = {
                                "connectivities" : connectivities,
                                "plane_wave_impedances" : plane_wave_impedances,
                                "e_normals" : e_normals,
                                "k_wave" : k_wave,
                                "pressures" : pressures,
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

        factor_Qms1 = dict()
        factor_Qms2 = dict()
        aux_connect = dict()
        integration_data = dict()

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

            surface_elements = list(self.model.mesh.elements_from_surface[surface_id])
            surf_connect = self.model.mesh.connectivity_from_surfaces[surface_id]   

            for i, el in enumerate(surface_elements):
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


    def get_value_in_array_form(self, value: float | np.ndarray, flatten: bool = False) -> np.ndarray:
        """
        This method returns, for a given input value, an output vector with 
        the same length as the frequencies vector.

        Parameters
        ----------
        value: float or np.ndarray
            The input value to be converted in array with
            the same lenght as the frequencies vector.
        
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
        
        if flatten:
            return output_vector.flatten()

        return output_vector


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

        surface_data_A = dict()
        surface_data_B = dict()
        connectivity_surface_A = dict()
        connectivity_surface_B = dict()
        integration_data = dict()

        aux_ones = np.ones(self.number_frequencies, dtype=complex)

        for (property_label, surface_ids), p_data in self.properties.surface_properties.items():

            if property_label != "transfer_impedance":
                continue
        
            p_data: dict
            values = p_data.get("values")
            if values is None:
                continue

            _complex_values = values[0]

            if isinstance(_complex_values, complex | float):
                Z_tr = _complex_values * aux_ones

            elif isinstance(_complex_values, np.ndarray):

                if _complex_values.shape[0] == 1:
                    Z_tr = _complex_values * aux_ones

                else:
                    Z_tr = _complex_values

            else:
                continue

            if p_data.get("coupling_type") == "inside_surfaces":

                decouple_data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_ids)
                if not isinstance(decouple_data, dict):
                    continue

                new_surface_id = decouple_data.get("new_surface_id")
                if new_surface_id is None:
                    continue

                surface_elements_A = list(self.model.mesh.elements_from_surface[surface_ids])
                surface_elements_B = list(self.model.mesh.elements_from_surface[new_surface_id])

            else:

                surface_elements_A = list()
                for surface_id_A in p_data.get("surfaces_A"):
                    surface_elements_A.extend(list(self.model.mesh.elements_from_surface[surface_id_A]))

                surface_elements_B = list()
                for surface_id_B in p_data.get("surfaces_B"):
                    surface_elements_B.extend(list(self.model.mesh.elements_from_surface[surface_id_B]))

            for i, el in enumerate(surface_elements_A):
                nodes_from_element = self.model.mesh.faces_connectivity[el, 4:]
                connectivity_surface_A[el] = nodes_from_element

                surface_data_A[el] = Z_tr

            for i, el in enumerate(surface_elements_B):
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

        surface_data_A = dict()
        surface_data_B = dict()
        connectivity_surface_A = dict()
        connectivity_surface_B = dict()

        integration_data = dict()

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

                if pp_data.get("coupling_type") == "inside_surfaces":

                    decouple_data = self.properties._get_property("degrees_of_freedom_decoupling", surface=surface_ids)
                    if not isinstance(decouple_data, dict):
                        continue

                    new_surface_id = decouple_data.get("new_surface_id")
                    if new_surface_id is None:
                        continue

                    surface_elements_A = list(self.model.mesh.elements_from_surface[surface_ids])
                    surface_elements_B = list(self.model.mesh.elements_from_surface[new_surface_id])

                else:

                    surface_elements_A = list()
                    for surface_id_A in pp_data.get("surfaces_A"):
                        surface_elements_A.extend(list(self.model.mesh.elements_from_surface[surface_id_A]))

                    surface_elements_B = list()
                    for surface_id_B in pp_data.get("surfaces_B"):
                        surface_elements_B.extend(list(self.model.mesh.elements_from_surface[surface_id_B]))

                for i, el in enumerate(surface_elements_A):

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

                for i, el in enumerate(surface_elements_B):

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
                                "connectivities_A" : np.array(list(connectivity_surface_A.values()), dtype=int),
                                "connectivities_B" : np.array(list(connectivity_surface_B.values()), dtype=int),
                                "surface_data_A" : np.array(list(surface_data_A.values()), dtype=complex),
                                "surface_data_B" : np.array(list(surface_data_B.values()), dtype=complex),
                                "non_linear" : non_linear,
                                }

        return integration_data


    def process_nodal_mass_source_data(self):
        """ 
        This method processes the nodal mass source vector data.
        """
        self.mass_source_vector_points = np.array([])
        self.mass_source_vector_surfaces = np.array([])
        self.mass_source_vector_volumes = np.array([])

        model_properties = {
                            "point_properties" : self.properties.point_properties,
                            "nodal_properties" : self.properties.nodal_properties,
                            }

        for prop_label, model_property in model_properties.items():
            for (property, *args), data in model_property.items():

                if property != "mass_source":
                    continue

                if not self.mass_source_vector_points.any():
                    self.mass_source_vector_points = np.zeros((self.total_dofs, self.number_frequencies), dtype=complex)

                if "values" in data.keys():
                    _complex_values = data.get("values")[0]

                volume_id = data.get("volume_id")
                fluid = self.model.properties._get_property("fluid", volume=volume_id)
                density = fluid.fluid_density

                if prop_label == "nodal_properties":
                    node_id = args[0]
                else:
                    point_id = args[0]
                    node_id = self.model.mesh.nodes_from_points.get(point_id)

                self.mass_source_vector_points[node_id, :] += self.get_value_in_array_form(_complex_values, flatten=True) / density

        if self.mass_source_vector_points.any():
            self.mass_source_vector_points = self.mass_source_vector_points[self.unprescribed_indexes, :]


        for (property, *args), data in self.properties.surface_properties.items():

            if property != "mass_source":
                continue

            if not self.mass_source_vector_surfaces.any():
                self.mass_source_vector_surfaces = np.zeros((self.total_dofs, self.number_frequencies), dtype=complex)

            if "values" in data.keys():
                _complex_values = data.get("values")[0]

            node_ids = self.model.mesh.nodes_from_surfaces.get(args[0])
            aux_ones = np.ones((node_ids.size, 1))

            self.mass_source_vector_surfaces[node_ids, :] += aux_ones @ self.get_value_in_array_form(_complex_values)

        if self.mass_source_vector_surfaces.any():
            self.mass_source_vector_surfaces = self.mass_source_vector_surfaces[self.unprescribed_indexes, :]


        for (property, *args), data in self.properties.volume_properties.items():

            if property != "mass_source":
                continue

            if not self.mass_source_vector_volumes.any():
                self.mass_source_vector_volumes = np.zeros((self.total_dofs, self.number_frequencies), dtype=complex)

            if "values" in data.keys():
                _complex_values = data.get("values")[0]

            node_ids = self.model.mesh.nodes_from_volumes.get(args[0])
            aux_ones = np.ones((node_ids.size, 1))

            self.mass_source_vector_volumes[node_ids, :] += aux_ones @ self.get_value_in_array_form(_complex_values)

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

        if not self.mass_source_vector_surfaces.any():
            return

        self.data_Qmsf = dict()
        self.ind_rows_Qmsf = np.array([], dtype=int)
        self.ind_cols_Qmsf = np.array([], dtype=int) 

        _, element_2D = self.get_element()
        dofs = element_2D.DOFS_PER_ELEMENT
        self.total_dofs_2d = element_2D.DOFS_PER_NODE * len(element_2D.nodal_coordinates)

        self.integration_data_Qms = self.get_mass_source_data_for_2d_element_integration()
        if not self.integration_data_Qms:
            return
        
        logging.info(f"Processing the mass source data to assemble matrices... [1/2]")
        connectivities = self.integration_data_Qms.get("connectivities")

        nel = connectivities.shape[0]
        for j in range(self.number_frequencies):
            self.data_Qmsf[j] = np.zeros((nel, dofs, dofs), dtype=complex)

        logging.info(f"Processing the mass source data to assemble matrices... [2/2]")
        self.ind_rows_Qmsf, self.ind_cols_Qmsf = element_2D.generate_ind_rows_cols(connectivities)
        self.int2d_NtN, self.int2d_BtB = element_2D.stacked_matrices_NtN_and_BtB()


    def process_fluid_properties_from_volumes(self):
        """
        This method maps the fluid properties against each volume
        to calculate the global matrices factors.
        """
        nf = self.number_frequencies
        aux_nf = np.ones(nf, dtype=float)

        self.frequency_dependent = False
        self.fluid_properties_from_volume = dict()

        for vol_id in self.model.mesh.elements_from_volume.keys():

            pm_data = self.properties._get_property("porous_material_model", volume=vol_id)
            vt_data = self.properties._get_property("viscous_thermal_model", volume=vol_id)
            fluid = self.properties._get_property("fluid", volume=vol_id)

            if isinstance(pm_data, dict):
                pm_data = self.model.porous_material_properties.get(vol_id)
                rho_f = pm_data["rho_eff"]
                C_f = pm_data["C_eff"]
                self.frequency_dependent = True

            elif isinstance(vt_data, dict):
                vt_data = self.model.viscous_thermal_model_properties.get(vol_id)
                rho_f = vt_data["rho_eff"]
                C_f = vt_data["C_eff"]
                self.frequency_dependent = True

            elif isinstance(fluid, Fluid):
                proportional_damping = self.properties._get_property("proportional_damping", volume=vol_id)
                rho = self.properties.get_fluid_density(fluid, proportional_damping)
                C = self.properties.get_speed_of_sound(fluid, proportional_damping)
                rho_f = rho * aux_nf
                C_f = C * aux_nf

            else:
                continue

            self.fluid_properties_from_volume[vol_id] = {
                                                         "rho_f" : rho_f,
                                                         "C_f" : C_f,
                                                         "rho_0" : fluid.fluid_density,
                                                         "C_0" : fluid.speed_of_sound, 
                                                         "mu_0" : fluid.dynamic_viscosity
                                                         }


    def gather_data_to_assemble_global_matrices(self, reorder: bool = True):
        """ 
        This method processes the data required to assemble the global matrices
        based on the stacked elementary matrices.

        Parameters
        ----------
        reorder: bool, optional
            Control when the connectivity matrix will be reordered.
        """

        element_3D, _ = self.get_element()
        self.ind_rows, self.ind_cols = element_3D.generate_ind_rows_cols(reorder=reorder)

        self.dofs = element_3D.DOFS_PER_ELEMENT
        self.number_3d_elements = len(element_3D.connectivity)
        self.total_dofs = element_3D.DOFS_PER_NODE * len(element_3D.nodal_coordinates)

        # global_matrices shape
        self.gm_shape = (self.total_dofs, self.total_dofs)

        self.int3d_BtB, self.int3d_NtN = element_3D.stacked_elementary_matrices_NtN_BtB()
        self.data_Cvisc = np.zeros((self.number_3d_elements, self.dofs, self.dofs), dtype=complex)

        self.process_fluid_properties_from_volumes()
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

            if not self.frequency_dependent and index == 0:
                int3d_BtB = self.int3d_BtB[elements_from_volume, :, :]
                self.data_Cvisc[elements_from_volume, :, :] = ((4 * mu_0) / (3 * ((rho_0 * C_0)**2))) * int3d_BtB

        return factor_K.reshape(-1, 1, 1), factor_M.reshape(-1, 1, 1)


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

        factor_Qms1 = self.integration_data_Qms.get("factor_Qms1")
        factor_Qms2 = self.integration_data_Qms.get("factor_Qms2")

        data_Qms1 = factor_Qms1[:, index].reshape(-1, 1, 1) * self.int2d_NtN
        Q_ms1 = csr_matrix((data_Qms1.flatten(), (self.ind_rows_Qmsf, self.ind_cols_Qmsf)), shape=self.gm_shape)

        data_Qms2 = factor_Qms2[:, index].reshape(-1, 1, 1) * self.int2d_BtB
        Q_ms2 = csr_matrix((data_Qms2.flatten(), (self.ind_rows_Qmsf, self.ind_cols_Qmsf)), shape=self.gm_shape)

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

        if self.mass_source_vector_surfaces.any():
            mass_source_s = self.mass_source_vector_surfaces[:, index]
            Q_ms += (1j * omega * self.Qms1_2d + self.Qms2_2d) @ mass_source_s

        if self.mass_source_vector_volumes.any():
            mass_source_v = self.mass_source_vector_volumes[:, index]
            Q_ms += (1j * omega * self.Qms1_3d + self.Qms2_3d) @ mass_source_v

        return Q_ms


    def gather_data_to_assemble_global_matrices_reference(self, reorder: bool = True):
        """ 
        This method processes the data required to assemble the global matrices
        sweeping all solid elements.

        Parameters
        ----------
        reorder: bool, optional
            Control when the connectivity matrix will be reordered.
        """

        element_3D, _ = self.get_element()
        self.ind_rows, self.ind_cols = element_3D.generate_ind_rows_cols(reorder=reorder)

        self.dofs = element_3D.DOFS_PER_ELEMENT
        self.number_3d_elements = len(element_3D.connectivity)
        self.total_dofs = element_3D.DOFS_PER_NODE * len(element_3D.nodal_coordinates)

        self.int3d_BtB = np.zeros((self.number_3d_elements, self.dofs, self.dofs), dtype=complex)
        self.int3d_NtN = np.zeros((self.number_3d_elements, self.dofs, self.dofs), dtype=complex)
        self.data_Cvisc = np.zeros((self.number_3d_elements, self.dofs, self.dofs), dtype=complex)

        pm_model_active = self.model.porous_material_properties
        vt_model_active = self.model.viscous_thermal_model_properties

        last_progress = 0

        if pm_model_active or vt_model_active:

            nf = self.number_frequencies
            aux_ones = np.ones(nf, dtype=complex)

            self.den_M = np.zeros((self.number_3d_elements, nf), dtype=complex)
            self.den_K = np.zeros((self.number_3d_elements, nf), dtype=complex)

            for el in range(self.number_3d_elements):

                progress = 100 * np.round(el/self.number_3d_elements, 2)
                if progress != last_progress:
                    logging.info(f"Processing the elementary matrices data... [{int(progress)}/100]")

                last_progress = progress

                Ke, Me = element_3D.elementary_matrices(el)
                self.int3d_BtB[el, :, :] = Ke
                self.int3d_NtN[el, :, :] = Me

                volume_id = self.model.get_volume(element=el)

                if volume_id in self.model.porous_material_properties.keys():

                    rho_eff = self.model.porous_material_properties[volume_id]["rho_eff"]
                    C_eff = self.model.porous_material_properties[volume_id]["C_eff"]

                    self.den_K[el, :] = 1 / (rho_eff)
                    self.den_M[el, :] = 1 / (rho_eff * C_eff**2)

                elif volume_id in self.model.viscous_thermal_model_properties.keys():

                    rho_eff = self.model.viscous_thermal_model_properties[volume_id]["rho_eff"]
                    C_eff = self.model.viscous_thermal_model_properties[volume_id]["C_eff"]

                    self.den_K[el, :] = 1 / (rho_eff)
                    self.den_M[el, :] = 1 / (rho_eff * C_eff**2)

                else:

                    fluid = self.model.properties._get_property("fluid", volume=volume_id)
                    proportional_damping = self.properties._get_property("proportional_damping", volume=volume_id)

                    rho_0 = self.properties.get_fluid_density(fluid, proportional_damping)
                    C_0 = self.properties.get_speed_of_sound(fluid, proportional_damping)
                    mu_0 = fluid.dynamic_viscosity

                    self.den_K[el, :] = aux_ones / (rho_0)
                    self.den_M[el, :] = aux_ones / (rho_0 * C_0**2)

                    # self.data_Cvisc[el, :, :] = ((4 * mu_0) / (3 * rho_0 * C_0**2)) * Ke

        else:

            nf = 1
            aux_ones = np.ones(nf, dtype=float)
            self.den_M = np.zeros((self.number_3d_elements, nf), dtype=complex)
            self.den_K = np.zeros((self.number_3d_elements, nf), dtype=complex)

            for el in range(self.number_3d_elements):

                progress = 100 * np.round(el/self.number_3d_elements, 2)
                if progress != last_progress:
                    logging.info(f"Processing the elementary matrices data... [{int(progress)}/100]")

                last_progress = progress

                volume_id = self.model.get_volume(element=el)
                fluid = self.model.properties._get_property("fluid", volume=volume_id)
                proportional_damping = self.properties._get_property("proportional_damping", volume=volume_id)

                rho_0 = self.properties.get_fluid_density(fluid, proportional_damping)
                C_0 = self.properties.get_speed_of_sound(fluid, proportional_damping)
                mu_0 = fluid.dynamic_viscosity

                self.den_K[el, :] = aux_ones / (rho_0)
                self.den_M[el, :] = aux_ones / (rho_0 * C_0**2)

                Ke, Me = element_3D.elementary_matrices(el)
                self.int3d_BtB[el, :, :] = Ke
                self.int3d_NtN[el, :, :] = Me

                self.data_Cvisc[el, :, :] = ((4 * mu_0) / (3 * ((rho_0 * C_0)**2))) * Ke

        self.process_indexes()


    def process_specific_impedance_data_to_assemble_damping_matrix(self):
        """ 
        This method processes the specific impedance data to assemble
        the global damping matrix.
        """

        self.data_Zsi = dict()
        self.ind_rows_Zsi = np.array([], dtype=int)
        self.ind_cols_Zsi = np.array([], dtype=int)

        _, element_2D = self.get_element()
        dofs = element_2D.DOFS_PER_ELEMENT
        self.total_dofs_2d = element_2D.DOFS_PER_NODE * len(element_2D.nodal_coordinates)

        self.integration_data_Zsi = self.get_surface_data_for_element_integration_by_property("specific_impedance")
        if not self.integration_data_Zsi:
            return

        logging.info(f"Processing the impedance data to assemble damping matrix... [1/10]")
        connectivities = self.integration_data_Zsi.get("connectivities")       
        Z_si = self.integration_data_Zsi.get("surface_data")

        nel = connectivities.shape[0]
        for j in range(self.number_frequencies):
            self.data_Zsi[j] = np.zeros((nel, dofs, dofs), dtype=complex)

        logging.info(f"Processing the impedance data to assemble damping matrix... [2/10]")
        self.ind_rows_Zsi, self.ind_cols_Zsi = element_2D.generate_ind_rows_cols(connectivities)
        int2d_NtN = element_2D.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zsi[j] = int2d_NtN / Z_si[:, j].reshape(-1, 1, 1)

        # TODO: remove after confirming that everything is working properly
        # for i, complex_values in enumerate(surface_data.values()):
        #     normalized_matrix_Z = element_2D.damping_matrix_Ce(i)
        #     for j in range(self.number_frequencies):
        #         self.data_Zsi[j][i, :, :] = normalized_matrix_Z / complex_values[0, j]


    def process_incident_plane_wave_data_to_assemble_damping_matrix(self):
        """ 
        This method processes the incident plane wave data to assemble
        the global damping matrix.
        """

        self.data_Zpw = dict()
        self.ind_rows_Zpw = np.array([], dtype=int)
        self.ind_cols_Zpw = np.array([], dtype=int)

        self.integration_data_pw = self.get_plane_wave_surface_data_for_element_integration()
        if not self.integration_data_pw:
            return

        logging.info(f"Processing the impedance data to assemble damping matrix... [1/10]")
        _k_wave = self.integration_data_pw.get("k_wave")
        _e_normals = self.integration_data_pw.get("e_normals")
        _pressures = self.integration_data_pw.get("pressures")
        connectivities = self.integration_data_pw.get("connectivities")
        _pw_impedances = self.integration_data_pw.get("plane_wave_impedances")

        _, element_2D = self.get_element()
        dofs = element_2D.DOFS_PER_ELEMENT
        self.total_dofs_2d = element_2D.DOFS_PER_NODE * len(element_2D.nodal_coordinates)

        nel = connectivities.shape[0]
        for j in range(self.number_frequencies):
            self.data_Zpw[j] = np.zeros((nel, dofs, dofs), dtype=complex)

        logging.info(f"Processing the impedance data to assemble damping matrix... [2/10]")
        self.ind_rows_Zpw, self.ind_cols_Zpw = element_2D.generate_ind_rows_cols(connectivities)
        int2d_NtN = element_2D.stacked_matrices_NtN()
        # eface_normals = element_2D.get_stacked_element_face_normals()

        e_normals = np.array(list(_e_normals.values())).reshape(-1, 1, 3)
        k_wave = np.array(list(_k_wave.values())).reshape(-1, 3, 1)
        pressures = np.array(list(_pressures.values()))
        pw_impedances = np.array(list(_pw_impedances.values()))

        n_k = e_normals @ k_wave

        for j in range(self.number_frequencies):
            P_inc = pressures[:, j].reshape(-1, 1, 1)
            Z_pw = pw_impedances[:, j].reshape(-1, 1, 1)

            # the negative signal is being used to revert the signal from the elementary matrix
            self.data_Zpw[j] = - int2d_NtN * (P_inc / Z_pw) * n_k


    def process_surface_impedance_data_to_assemble_damping_matrix(self):
        """ 
        This method processes the surface impedance data resulting from
        absorption surface to assemble the global damping matrix.
        """

        self.data_Zas = dict()
        self.ind_rows_Zas = np.array([])
        self.ind_cols_Zas = np.array([])

        _, element_2D = self.get_element()
        dofs = element_2D.DOFS_PER_ELEMENT
        self.total_dofs_2d = element_2D.DOFS_PER_NODE * len(element_2D.nodal_coordinates)

        self.integration_data_Zas = self.get_surface_data_for_element_integration_by_property("absorption_surface")
        if not self.integration_data_Zas:
            return
        
        logging.info(f"Processing the impedance data to assemble damping matrix... [3/10]")
        connectivities = self.integration_data_Zas.get("connectivities")       
        Z_as = self.integration_data_Zas.get("surface_data")

        nel = connectivities.shape[0]
        for j in range(self.number_frequencies):
            self.data_Zas[j] = np.zeros((nel, dofs, dofs), dtype=complex)

        logging.info(f"Processing the impedance data to assemble damping matrix... [4/10]")
        self.ind_rows_Zas, self.ind_cols_Zas = element_2D.generate_ind_rows_cols(connectivities)
        int2d_NtN = element_2D.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zas[j] = int2d_NtN / Z_as[:, j].reshape(-1, 1, 1)


    def process_transfer_impedance_data_to_assemble_damping_matrix(self):
        """
        This method processes the internal transfer impedance data 
        to assemble the global damping matrix.
        """

        self.data_Zti_A = dict()
        self.ind_rows_Zti_A = np.array([])
        self.ind_cols_Zti_A = np.array([])

        self.data_Zti_B = dict()
        self.ind_rows_Zti_B = np.array([])
        self.ind_cols_Zti_B = np.array([])

        _, element_2D = self.get_element()
        dofs = element_2D.DOFS_PER_ELEMENT
        self.total_dofs_2d = element_2D.DOFS_PER_NODE * len(element_2D.nodal_coordinates)

        self.integration_data_Zti = self.get_transfer_impedance_data_for_element_integration()
        if not self.integration_data_Zti:
            return

        logging.info(f"Processing the impedance data to assemble damping matrix... [5/10]")
        connectivities_A = self.integration_data_Zti.get("connectivities_A")
        connectivities_B = self.integration_data_Zti.get("connectivities_B")
        Zti_A = self.integration_data_Zti.get("surface_data_A")
        Zti_B = self.integration_data_Zti.get("surface_data_B")

        nel_A = connectivities_A.shape[0]
        nel_B = connectivities_B.shape[0]

        for j in range(self.number_frequencies):
            self.data_Zti_A[j] = np.zeros((nel_A, dofs, dofs), dtype=complex)
            self.data_Zti_B[j] = np.zeros((nel_B, dofs, dofs), dtype=complex)

        logging.info(f"Processing the impedance data to assemble damping matrix... [6/10]")
        self.ind_rows_Zti_A, self.ind_cols_Zti_A = element_2D.generate_ind_rows_cols(connectivities_A)
        int2d_NtN_A = element_2D.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zti_A[j] = int2d_NtN_A / Zti_A[j].reshape(-1, 1, 1)

        logging.info(f"Processing the impedance data to assemble damping matrix... [7/10]")
        self.ind_rows_Zti_B, self.ind_cols_Zti_B = element_2D.generate_ind_rows_cols(connectivities_B)
        int2d_NtN_B = element_2D.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zti_B[j] = int2d_NtN_B / Zti_B[j].reshape(-1, 1, 1)


    def process_perforated_plate_impedance_data_to_assemble_damping_matrix(self, solution: np.ndarray | None = None):
        """
        This method processes the perforated plate impedance data 
        to assemble the global damping matrix.

        Parameters
        ----------
        solution: np.ndarray, optional
        """

        self.data_Zpp_A = dict()
        self.ind_rows_Zpp_A = np.array([])
        self.ind_cols_Zpp_A = np.array([])

        self.data_Zpp_B = dict()
        self.ind_rows_Zpp_B = np.array([])
        self.ind_cols_Zpp_B = np.array([])

        _, element_2D = self.get_element()
        dofs = element_2D.DOFS_PER_ELEMENT
        self.total_dofs_2d = element_2D.DOFS_PER_NODE * len(element_2D.nodal_coordinates)

        self.integration_data_Zpp = self.get_perforated_plate_data_for_element_integration(solution)
        if not self.integration_data_Zpp:
            return
        
        logging.info(f"Processing the impedance data to assemble damping matrix... [8/10]")

        Zpp_A = self.integration_data_Zpp.get("surface_data_A")
        Zpp_B = self.integration_data_Zpp.get("surface_data_B")
        non_linear = self.integration_data_Zpp.get("non_linear")
        connectivities_A = self.integration_data_Zpp.get("connectivities_A")
        connectivities_B = self.integration_data_Zpp.get("connectivities_B")

        nel_A = connectivities_A.shape[0]
        nel_B = connectivities_B.shape[0]

        for j in range(self.number_frequencies):
            self.data_Zpp_A[j] = np.zeros((nel_A, dofs, dofs), dtype=complex)
            self.data_Zpp_B[j] = np.zeros((nel_B, dofs, dofs), dtype=complex)

        logging.info(f"Processing the impedance data to assemble damping matrix... [9/10]")
        self.ind_rows_Zpp_A, self.ind_cols_Zpp_A = element_2D.generate_ind_rows_cols(connectivities_A)
        int2d_NtN_A = element_2D.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zpp_A[j] = int2d_NtN_A / Zpp_A[:, j].reshape(-1, 1, 1)

        logging.info(f"Processing the impedance data to assemble damping matrix... [10/10]")
        self.ind_rows_Zpp_B, self.ind_cols_Zpp_B = element_2D.generate_ind_rows_cols(connectivities_B)
        int2d_NtN_B = element_2D.stacked_matrices_NtN()

        for j in range(self.number_frequencies):
            self.data_Zpp_B[j] = int2d_NtN_B / Zpp_B[:, j].reshape(-1, 1, 1)


    def gather_data_to_assemble_damping_matrix(self):
        self.process_specific_impedance_data_to_assemble_damping_matrix()
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


    def assemble_global_damping_matrix_3d_elements(self):
        """
        This method assembles the global damping matrix to account
        the bulk damping effects.
        """
        _visc_damping_matrix_full = csr_matrix((self.data_Cvisc.flatten(), (self.ind_rows, self.ind_cols)), shape=self.gm_shape)

        self.visc_damping_matrix = _visc_damping_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.visc_damping_matrix_r = _visc_damping_matrix_full[:, self.prescribed_indexes]


    def assemble_global_damping_matrix_2d_elements(self, index: int = 0):
        """
        This method computes the global damping matrix asseble.

        Parameters
        ----------
        index: int, optional.
            It corresponds to the frequency step index.
        """

        N_dofs = self.total_dofs_2d
        rows_Zout = np.array([], dtype=int)
        cols_Zout = np.array([], dtype=int)
        data_Zout = np.array([], dtype=complex)

        if self.integration_data_Zsi:
            rows_Zout = self.ind_rows_Zsi
            cols_Zout = self.ind_cols_Zsi
            data_Zout = self.data_Zsi[index].flatten()

        if self.integration_data_pw:
            rows_Zout = np.append(rows_Zout, self.ind_rows_Zpw) 
            cols_Zout = np.append(cols_Zout, self.ind_cols_Zpw)
            data_Zout = np.append(data_Zout, self.data_Zpw[index].flatten())

        if self.integration_data_Zas:
            rows_Zout = np.append(rows_Zout, self.ind_rows_Zas) 
            cols_Zout = np.append(cols_Zout, self.ind_cols_Zas)
            data_Zout = np.append(data_Zout, self.data_Zas[index].flatten())

        if data_Zout.size:
            _matrix_full_A = csr_matrix((data_Zout, (rows_Zout, cols_Zout)), shape=(N_dofs, N_dofs))

        else:
            _matrix_full_A = csr_matrix((N_dofs, N_dofs))

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
            _matrix_full_B = csr_matrix((values_Zin, (rows_Zin, cols_Zin)), shape=(N_dofs, N_dofs))

        else:
            _matrix_full_B = csr_matrix((N_dofs, N_dofs))

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

        self.model.set_acoustic_element(self.get_element())

        for (property, surface_id), data in self.properties.surface_properties.items():
            if property == "mass_flow_rate":

                _complex_values = data["values"][0]
                if isinstance(_complex_values, complex):
                    complex_values = _complex_values * aux_ones
                elif isinstance(_complex_values, np.ndarray):
                    if _complex_values.shape[0] == 1:
                        complex_values = _complex_values * aux_ones
                    elif len(_complex_values.shape) == 1:
                        complex_values = _complex_values.reshape(1,-1)
                    else:
                        complex_values = _complex_values

                if data["nodal_attribution"]:

                    nodes = self.model.mesh.nodes_from_surfaces[surface_id]
                    N = len(nodes)

                    for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
                        if data["averaged"]:
                            acoustic_excitation[index] += complex_values / N
                        else:
                            acoustic_excitation[index] += complex_values

            elif property in ["surface_velocity", "reciprocating_compressor_excitation"]:

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

                    nodes = self.model.mesh.nodes_from_surfaces[surface_id]
                    N = len(nodes)

                    self.model.mesh._process_face_elements_connected_to_nodes(surface_id)
                    area = self.model.mesh.surface_area_from_element_integration[surface_id]

                    for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
                        if data["averaged"]:
                            acoustic_excitation[index] += (complex_values * area) / N
                        else:
                            acoustic_excitation[index] += complex_values * area

        element_3D, _ = self.get_element()
        total_dofs = element_3D.DOFS_PER_NODE * len(element_3D.nodal_coordinates)
        output = np.zeros((total_dofs, self.number_frequencies), dtype=complex)

        if acoustic_excitation:
            indexes = list(acoustic_excitation.keys())
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

        _, element_2D = self.get_element()
        total_dofs = element_2D.DOFS_PER_NODE * len(element_2D.nodal_coordinates)
        output = np.zeros((total_dofs, self.number_frequencies), dtype=complex)

        integration_data_mf = self.get_surface_data_for_element_integration_by_property("mass_flow_rate")
        if integration_data_mf:

            connectivities_mf = integration_data_mf.get("connectivities")
            surface_data_mf = integration_data_mf.get("surface_data")

            element_2D.reorder_connect(connectivities_mf)
            for i, complex_values in enumerate(surface_data_mf):
                indices = element_2D.connect_face[i, :]
                int2d_N = element_2D.load_vector(i)

                output[indices, :] += int2d_N @ complex_values.reshape(1, -1)
       
        for excitation_label in ["surface_velocity", "reciprocating_compressor_excitation"]:

            integration_data_sv = self.get_surface_data_for_element_integration_by_property(excitation_label)
            if integration_data_sv:

                connectivities_sv = integration_data_sv.get("connectivities")
                surface_data_sv = integration_data_sv.get("surface_data")

                element_2D.reorder_connect(connectivities_sv)
                for i, complex_values in enumerate(surface_data_sv):
                    indices = element_2D.connect_face[i, :]
                    int2d_N = element_2D.load_vector(i)

                    output[indices, :] += int2d_N @ complex_values.reshape(1, -1)

        if self.integration_data_pw:

            k_wave = self.integration_data_pw.get("k_wave")
            e_normals = self.integration_data_pw.get("e_normals")
            pressures = self.integration_data_pw.get("pressures")
            connectivities_pw = self.integration_data_pw.get("connectivities")
            pw_impedances = self.integration_data_pw.get("plane_wave_impedances")

            element_2D.reorder_connect(connectivities_pw)

            for i, (el_index, Z) in enumerate(pw_impedances.items()):

                int2d_N = element_2D.load_vector(i)

                # element face connectivity
                e_connect = connectivities_pw[i, :]

                # element face normal
                n = e_normals[el_index]

                # incident wave vector
                k = k_wave[el_index]

                # incident pressure amplitude
                p_inc = pressures[el_index]

                # surface impedance
                Z = pw_impedances[el_index]

                # auxilar vector
                aux = (p_inc / Z) * (n @ k )

                # the negative signal is being used to revert the signal from the elementary load vector ???
                output[e_connect, :] +=  2 * int2d_N @ aux.reshape(1, -1)

        if self.prescribed_indexes:
            return output[self.unprescribed_indexes, :]

        return output


    def process_assemble(self):

        self.update_number_of_frequencies()

        logging.info("Gathering data to assemble global matrices... [10/100]")
        t0 = time()
        self.gather_data_to_assemble_global_matrices()
        dt = time() - t0
        print(f"Elapsed time to gather data to assemble global matrices: {round(dt, 4)} [s]")

        logging.info("Gathering data to assemble damping matrix... [40/100]")
        t0 = time()
        self.gather_data_to_assemble_damping_matrix()
        dt = time() - t0
        print(f"Elapsed time to gather data to assemble damping matrices: {round(dt, 4)} [s]")

        logging.info("Computing the global matrices factors... [45/100]")
        t0 = time()
        factor_K, factor_M = self.compute_global_matrices_factors()
        dt = time() - t0
        print(f"Elapsed time to compute global matrices factor: {round(dt, 4)} [s]")

        logging.info("Assembling global stiffness matrix... [50/100]")
        t0 = time()
        self.assemble_global_stiffness_matrix(factor_K)
        dt = time() - t0
        print(f"Elapsed time to assemble the global stiffness matrix: {round(dt, 4)} [s]")

        logging.info("Assembling global mass matrix... [60/100]")
        t0 = time()
        self.assemble_global_mass_matrix(factor_M)
        dt = time() - t0
        print(f"Elapsed time to assemble the global mass matrix: {round(dt, 4)} [s]")

        logging.info("Assembling global mass matrix... [70/100]")
        t0 = time()
        self.assemble_global_damping_matrix_3d_elements()
        self.assemble_global_damping_matrix_2d_elements()
        dt = time() - t0
        print(f"Elapsed time to assemble the global damping matrix: {round(dt, 4)} [s]\n")

        logging.info("Processing element related loads... [75/100]")
        B = self.get_acoustic_excitations_by_element_integration()

        logging.info("Processing nodal related loads... [85/100]")
        A = self.get_acoustic_excitations_by_nodal_attribution()

        logging.info("Processing nodal related loads... [90/100]")
        self.process_mass_source_data_to_assemble_matrices()
        self.assemble_mass_source_matrices_from_surfaces()
        self.assemble_mass_source_matrices_from_volumes()

        logging.info("Finishing the model building... [98/100]")
        self.mass_flow_vectors = A + B