from vibra.engine.model import Model

# 3D elements
from vibra.engine.elements.acoustic_hex8_element import ACT_HEXAHEDRON_8C
from vibra.engine.elements.acoustic_hex20_element import ACT_HEXAHEDRON_20C
from vibra.engine.elements.acoustic_tet4_element import ACT_TETRAHEDRON_4C
from vibra.engine.elements.acoustic_tet10_element import ACT_TETRAHEDRON_10C

# 2D elements
from vibra.engine.elements.acoustic_face3_element import ACT_FACE_3
from vibra.engine.elements.acoustic_face4_element import ACT_FACE_4
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
        self.ind_rows_Z = np.array([])
        self.ind_cols_Z = np.array([])
        self.model = model
        self.properties = model.properties

        self.reset()

    def reset(self):
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
        ----------
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

    def get_surface_data_for_element_integration_by_property(self, property_label: str):
        """ """
        connect = None
        surface_data = dict()
        aux_connect = dict()
        all_indexes = list()

        aux_ones = np.ones((1, self.number_frequencies), dtype=complex)

        for key, data in self.properties.surface_properties.items():

            prop, surface_id = key
            if prop == property_label:
                if not data["nodal_attribution"]:

                    pm_active, rho_eff_pm, C_eff_pm = self.model.is_porous_material_model_active(surface_id)
                    tv_active, rho_eff_tv, C_eff_tv = self.model.is_viscous_thermal_model_active(surface_id)

                    if pm_active:
                        density = rho_eff_pm
                        speed_of_sound = C_eff_pm

                    elif tv_active:
                        density = rho_eff_tv
                        speed_of_sound = C_eff_tv

                    else:
                        fluid = self.model.properties._get_property("fluid", surface=surface_id)
                        density = fluid.fluid_density
                        speed_of_sound = fluid.speed_of_sound

                    if "anechoic_termination" in data.keys():
                        _complex_values = density * speed_of_sound

                    else:
                        if "values" in data.keys():
                            _complex_values = data["values"][0]

                    if isinstance(_complex_values, complex | float):
                        complex_values = _complex_values * aux_ones

                    elif isinstance(_complex_values, np.ndarray):

                        if _complex_values.shape[0] == 1:
                            complex_values = _complex_values * aux_ones

                        elif len(_complex_values.shape) == 1:
                            complex_values = _complex_values.reshape(1,-1)

                        else:
                            complex_values = _complex_values

                    surface_elements = list(self.model.mesh.elements_from_surface[surface_id])
                    all_indexes.extend(surface_elements)

                    surf_connect = self.model.mesh.connectivity_from_surfaces[surface_id]

                    source_factor = 1
                    if property_label == "surface_velocity":
                        for _key in self.properties.surface_properties.keys():
                            if _key[0] == "specific_impedance" and _key[1] == surface_id:
                                source_factor = 1
                                break

                    for i, el in enumerate(surface_elements):
                        aux_connect[el] = surf_connect[i]
                        surface_data[el] = [complex_values, source_factor]

        if aux_connect:
            connect = np.array(list(aux_connect.values()), dtype=int)

            # if property_label == "specific_impedance":
            #     # element_indexes = np.array(all_indexes)
            #     # filename = f"connect_data_{property_label}.dat"
            #     # np.savetxt(filename, np.insert(connect, 0, element_indexes, axis=1), fmt="%i")
            #     app().main_window.action_mesh_workspace_callback()
            #     mesh_widget = app().main_window.mesh_widget
            #     mesh_widget.select_multiple_faces(all_indexes)

        return connect, surface_data
    
    def get_perforated_plate_data_for_element_integration(self, solution: np.ndarray | None = None):
                    
        connect = None
        surface_data = dict()
        aux_connect = dict()
        all_indexes = list()
        # aux_ones = np.ones((1, self.number_frequencies), dtype=complex)

        for key in self.properties.surface_properties.keys():

            property_label, surface_id = key
            if property_label == "perforated_plate_model":

                pp_data = self.model.perforated_plate_impedance_data[surface_id]
                a = pp_data.get("a", 0)
                b = pp_data.get("b", 0)
                Z_0 = pp_data.get("Z_0", 0)

                surface_elements = list(self.model.mesh.elements_from_surface[surface_id])
                all_indexes.extend(surface_elements)
                surf_connect = self.model.mesh.connectivity_from_surfaces[surface_id]

                for i, el in enumerate(surface_elements):

                    aux_connect[el] = surf_connect[i]
                    if solution is None:
                        U_rms = 0
                    else:
                        p = solution[surf_connect[i], :]
                        p2_avg = np.average((1/2)*np.real(p*np.conj(p)), axis=0)
                        p_rms = np.sqrt(p2_avg)
                        U_rms = p_rms / Z_0

                    Z_tr = Z_0 * (a + b*U_rms)
                    surface_data[el] = Z_tr

        if aux_connect:
            connect = np.array(list(aux_connect.values()), dtype=int)

            # if property_label == "perforated_plate_model":
            #     from vibra import app
            # #     # element_indexes = np.array(all_indexes)
            # #     # filename = f"connect_data_{property_label}.dat"
            # #     # np.savetxt(filename, np.insert(connect, 0, element_indexes, axis=1), fmt="%i")
            #     app().main_window.action_mesh_workspace_callback()
            #     app().main_window.set_mesh_selection(faces=all_indexes)

        return connect, surface_data

    def get_data_to_process_global_matrices(self, reorder=True):
        """ This method processes the data required to assemble the global matrices. """

        element_3D, _ = self.get_element()
        self.ind_rows, self.ind_cols = element_3D.generate_ind_rows_cols(reorder=reorder)

        dofs = element_3D.DOFS_PER_ELEMENT
        nel = len(element_3D.connectivity)
        self.total_dofs = element_3D.DOFS_PER_NODE * len(element_3D.nodal_coordinates)

        self.data_K = np.zeros((nel, dofs, dofs), dtype=complex)
        self.data_M = np.zeros((nel, dofs, dofs), dtype=complex)
        self.data_Cvisc = np.zeros((nel, dofs, dofs), dtype=complex)
        self.data_Qvisc = np.zeros((nel, dofs, dofs), dtype=complex)

        pm_model_active = self.model.porous_material_properties
        vt_model_active = self.model.viscous_thermal_model_properties

        last_progress = 0

        if pm_model_active or vt_model_active:

            nf = self.number_frequencies
            aux_ones = np.ones(nf, dtype=complex)

            self.den_M = np.zeros((nel, nf), dtype=complex)
            self.den_K = np.zeros((nel, nf), dtype=complex)

            for el in range(nel):

                progress = 100 * np.round(el/nel, 2)
                if progress != last_progress:
                    logging.info(f"Processing the elementary matrices data... [{int(progress)}/100]")

                last_progress = progress

                Ke, Me = element_3D.elementary_matrices(el)
                self.data_K[el, :, :] = Ke
                self.data_M[el, :, :] = Me

                if el in self.model.porous_material_properties.keys():

                    rho_eff = self.model.porous_material_properties[el]["rho_eff"]
                    C_eff = self.model.porous_material_properties[el]["C_eff"]

                    self.den_K[el, :] = 1 / (rho_eff)
                    self.den_M[el, :] = 1 / (rho_eff * C_eff**2)

                elif el in self.model.viscous_thermal_model_properties.keys():

                    rho_eff = self.model.viscous_thermal_model_properties[el]["rho_eff"]
                    C_eff = self.model.viscous_thermal_model_properties[el]["C_eff"]

                    self.den_K[el, :] = 1 / (rho_eff)
                    self.den_M[el, :] = 1 / (rho_eff * C_eff**2)

                else:

                    volume_id = self.model.get_volume(element=el)
                    fluid = self.model.properties._get_property("fluid", volume=volume_id)
                    proportional_damping = self.properties._get_property("proportional_damping", volume=volume_id)

                    rho_0 = self.properties.get_fluid_density(fluid, proportional_damping)
                    C_0 = self.properties.get_speed_of_sound(fluid, proportional_damping)
                    mu_0 = fluid.dynamic_viscosity

                    self.den_K[el, :] = aux_ones / (rho_0)
                    self.den_M[el, :] = aux_ones / (rho_0 * C_0**2)

                    # self.data_Cvisc[el, :, :] = ((4 * mu_0) / (3 * rho_0 * C_0**2)) * Ke
                    # self.data_Qvisc[el, :, :] = 0 * ((4 * mu_0) / (3 * rho_0)) * Ke

        else:

            nf = 1
            aux_ones = np.ones(nf, dtype=float)
            self.den_M = np.zeros((nel, nf), dtype=complex)
            self.den_K = np.zeros((nel, nf), dtype=complex)

            for el in range(nel):

                progress = 100 * np.round(el/nel, 2)
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
                self.data_K[el, :, :] = Ke
                self.data_M[el, :, :] = Me

                self.data_Cvisc[el, :, :] = ((4 * mu_0) / (3 * ((rho_0 * C_0)**2))) * Ke
                self.data_Qvisc[el, :, :] = ((4 * mu_0) / (3 * rho_0**2)) * Ke

        self.process_indexes()
        self.process_perforated_plate_impedance_data_to_assemble_damping_matrix()
        self.get_specific_impendace_data_to_process_damping_matrix()

    def get_specific_impendace_data_to_process_damping_matrix(self):
        """
        """

        self.data_Cimp = dict()
        self.ind_rows_Z = np.array([])
        self.ind_cols_Z = np.array([])

        _, element_2D = self.get_element()
        dofs = element_2D.DOFS_PER_ELEMENT
        self.total_dofs_2d = element_2D.DOFS_PER_NODE * len(element_2D.nodal_coordinates)

        self.si_connect, surface_data = self.get_surface_data_for_element_integration_by_property("specific_impedance")

        if self.si_connect is not None:

            nel = self.si_connect.shape[0]
            for j in range(self.number_frequencies):
                self.data_Cimp[j] = np.zeros((nel, dofs, dofs), dtype=complex)

            self.ind_rows_Z, self.ind_cols_Z = element_2D.generate_ind_rows_cols(self.si_connect)
            for i, [complex_values, _] in enumerate(surface_data.values()):
                normalized_matrix_Z = element_2D.matrices_Z(i)
                for j in range(self.number_frequencies):
                    self.data_Cimp[j][i, :, :] = normalized_matrix_Z / complex_values[0, j]

    def process_perforated_plate_impedance_data_to_assemble_damping_matrix(self, solution: np.ndarray | None = None):
        """
        """

        self.data_Zpp = dict()
        self.ind_rows_Zpp = np.array([])
        self.ind_cols_Zpp = np.array([])

        _, element_2D = self.get_element()
        dofs = element_2D.DOFS_PER_ELEMENT
        self.total_dofs_2d = element_2D.DOFS_PER_NODE * len(element_2D.nodal_coordinates)

        self.pp_connect, surface_data = self.get_perforated_plate_data_for_element_integration(solution)
        if self.pp_connect is not None:

            nel = self.pp_connect.shape[0]
            for j in range(self.number_frequencies):
                self.data_Zpp[j] = np.zeros((nel, dofs, dofs), dtype=complex)

            self.ind_rows_Zpp, self.ind_cols_Zpp = element_2D.generate_ind_rows_cols(self.pp_connect)
            for i, Z_tr in enumerate(surface_data.values()):
                normalized_matrix_Z = element_2D.matrices_Z(i)
                for j in range(self.number_frequencies):
                    self.data_Zpp[j][i, :, :] = normalized_matrix_Z / Z_tr[j]

    def assemble_global_stiffness_matrix(self, index=0):
        """
        """
        data_K = self.data_K * self.den_K[:, index].reshape(-1, 1, 1)
        _stiffness_matrix_full = csr_matrix((data_K.flatten(), (self.ind_rows, self.ind_cols)), shape=(self.total_dofs, self.total_dofs))
        self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.stiffness_matrix_r = _stiffness_matrix_full[:, self.prescribed_indexes]

    def assemble_global_mass_matrix(self, index=0):
        """
        """
        data_M = self.data_M * self.den_M[:, index].reshape(-1, 1, 1)
        _mass_matrix_full = csr_matrix((data_M.flatten(), (self.ind_rows, self.ind_cols)), shape=(self.total_dofs, self.total_dofs))
        self.mass_matrix = _mass_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.mass_matrix_r = _mass_matrix_full[:, self.prescribed_indexes]

    def assemble_global_damping_matrix_3d_elements(self):
        """
        """
        # assemble the viscous damping matrix
        _visc_damping_matrix_full = csr_matrix((self.data_Cvisc.flatten(), (self.ind_rows, self.ind_cols)), shape=(self.total_dofs, self.total_dofs))
        self.visc_damping_matrix = _visc_damping_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.visc_damping_matrix_r = _visc_damping_matrix_full[:, self.prescribed_indexes]

        # assemble the Qviscous damping matrix
        _Qvisc_damping_matrix_full = csr_matrix((self.data_Qvisc.flatten(), (self.ind_rows, self.ind_cols)), shape=(self.total_dofs, self.total_dofs))
        self.Qvisc_damping_matrix = _Qvisc_damping_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.Qvisc_damping_matrix_r = _Qvisc_damping_matrix_full[:, self.prescribed_indexes]

    def assemble_global_damping_matrix_2d_elements(self, index=0):
        """
        """
        N_dofs = self.total_dofs_2d

        if self.si_connect is None:
            _matrix_full_A = csr_matrix((N_dofs, N_dofs))
        else:
            _matrix_full_A = csr_matrix((self.data_Cimp[index].flatten(), (self.ind_rows_Z, self.ind_cols_Z)), shape=(N_dofs, N_dofs))

        if self.pp_connect is None:
            _matrix_full_B = csr_matrix((N_dofs, N_dofs))
        else:
            _matrix_full_B = csr_matrix((self.data_Zpp[index].flatten(), (self.ind_rows_Zpp, self.ind_cols_Zpp)), shape=(N_dofs, N_dofs))

        _matrix_full = _matrix_full_A + _matrix_full_B

        self.damping_matrix = _matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.damping_matrix_r = _matrix_full[:, self.prescribed_indexes]

    def get_acoustic_excitations_by_nodal_attribution(self):
        """ This method processes the acoustic model excitations and
            returns the output data in the form of mass flow rate.
        """

        # aux_ones = np.ones((1, self.number_frequencies), dtype=complex)
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

        """ This method processes the acoustic model excitations and
            returns the output data in the form of mass flow rate.
        """

        _, element_2D = self.get_element()
        total_dofs = element_2D.DOFS_PER_NODE * len(element_2D.nodal_coordinates)
        output = np.zeros((total_dofs, self.number_frequencies), dtype=complex)

        connect_mf, data_mf = self.get_surface_data_for_element_integration_by_property("mass_flow_rate")
        if connect_mf is not None:
            element_2D.reorder_connect(connect_mf)
            for i, [complex_values, _] in enumerate(data_mf.values()):

                indices = element_2D.connect_face[i, :]
                normalized_excitation_matrix = element_2D.excitation_F(i)

                output[indices, :] += normalized_excitation_matrix @ complex_values

        # connect_vv, data_vv = self.get_surface_data_for_element_integration_by_property("volume_velocity")
        # if connect_vv is not None:
        #     element_2D.reorder_connect(connect_vv)
        #     for i, [complex_values, _] in enumerate(data_vv.values()):

        #         if complex_values.shape[0] == 1:
        #             complex_values = complex_values * aux_ones

        #         elif len(complex_values.shape) == 1:
        #             complex_values = complex_values.reshape(1,-1)
              
        #         indices = element_2D.connect_face[i, :]
        #         normalized_excitation_matrix = element_2D.excitation_F(i)

        #         output[indices, :] += normalized_excitation_matrix @ complex_values
        
        for excitation_label in ["surface_velocity", "reciprocating_compressor_excitation"]:

            connect_sv, data_sv = self.get_surface_data_for_element_integration_by_property(excitation_label)

            if connect_sv is not None:
                element_2D.reorder_connect(connect_sv)
                for i, [complex_values, source_factor] in enumerate(data_sv.values()):

                    indices = element_2D.connect_face[i, :]
                    normalized_excitation_matrix = source_factor * element_2D.excitation_F(i)

                    output[indices, :] += normalized_excitation_matrix @ complex_values

        if self.prescribed_indexes:
            return output[self.unprescribed_indexes, :]
        else:
            return output

    def show_required_memory(self):

        sizes = dict(
                     size_K = getsizeof(self.data_K),
                     size_M = getsizeof(self.data_M),
                     size_Cvisc = getsizeof(self.data_Cvisc),
                     size_Qvisc = getsizeof(self.data_Qvisc),
                     size_Cimp = getsizeof(self.data_Cimp),
                     size_ind_rows = getsizeof(self.ind_rows),
                     size_ind_cols = getsizeof(self.ind_cols),
                     size_ind_rows_Z = getsizeof(self.ind_rows_Z),
                     size_ind_cols_Z = getsizeof(self.ind_cols_Z)
                     )

        total_size = 0.
        for name, size in sizes.items():
            size_MB = size / 1e6
            print(f"{name} = {round(size_MB, 4)}[MB]")
            total_size += size_MB

        print(f"Total memory required: {round(total_size, 4)}[MB]\n")

    def process_assemble(self):

        self.update_number_of_frequencies()

        logging.info("Gathering data to assemble global matrices... [10/100]")
        t0 = time()
        self.get_data_to_process_global_matrices()
        dt = time() - t0
        print(f"Elapsed time to process data to assemble global matrices: {round(dt, 4)} [s]")
        
        logging.info( "Assembling global stiffness matrix... [50/100]")
        t0 = time()
        self.assemble_global_stiffness_matrix()
        dt = time() - t0
        print(f"Elapsed time to assemble the global stiffness matrix: {round(dt, 4)} [s]")
        
        logging.info( "Assembling global mass matrix... [60/100]")
        t0 = time()
        self.assemble_global_mass_matrix()
        dt = time() - t0
        print(f"Elapsed time to assemble the global mass matrix: {round(dt, 4)} [s]")
        
        logging.info( "Assembling global mass matrix... [70/100]")
        t0 = time()
        # self.assemble_global_damping_matrix()
        self.assemble_global_damping_matrix_3d_elements()
        self.assemble_global_damping_matrix_2d_elements()
        dt = time() - t0
        print(f"Elapsed time to assemble the global damping matrix: {round(dt, 4)} [s]\n")

        # self.show_required_memory()

        logging.info( "Processing element related loads... [80/100]")
        B = self.get_acoustic_excitations_by_element_integration()
        
        logging.info( "Processing nodal related loads... [90/100]")
        A = self.get_acoustic_excitations_by_nodal_attribution()
        
        logging.info( "Finishing the model building... [90/100]")
        self.mass_flow_vectors = A + B
