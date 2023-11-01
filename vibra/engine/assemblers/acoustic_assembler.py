import logging
from collections import defaultdict
from time import time

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
# 3D elements
from vibra.engine.elements.acoustic_hex8_element import ACT_HEXAHEDRON_8C
from vibra.engine.elements.acoustic_hex20_element import ACT_HEXAHEDRON_20C
from vibra.engine.elements.acoustic_tet4_element import ACT_TETRAHEDRON_4C
from vibra.engine.elements.acoustic_tet10_element import ACT_TETRAHEDRON_10C
# 2D elements
from vibra.engine.elements.acoustic_face3_element import ACT_FACE_3
from vibra.engine.elements.acoustic_face4_element import ACT_FACE_4
#
from vibra.engine.mesher.element_type import *
from vibra.utils.progress_status import ProgressStatus



class AcousticAssembler:
    def __init__(self, model):
        self.model = model
        self.properties = model.properties
        self.reset()

    def reset(self):
        self.stiffness_matrix = None
        self.mass_matrix = None
        self.damping_matrix = None
        self.mass_flow_vectors = None
        self.frequencies = None
        self.prescribed_values = []
        self.prescribed_indexes = []
        self.unprescribed_indexes = []

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
            raise NotImplementedError(f"Element type is not supported yet.")

    def set_element_formulation(self, element):
        self.element = element

    def set_analysis_data(self, data):
        self.analysis_data = data
        if "frequencies" in data.keys():
            self.frequencies = data["frequencies"]

    def set_frequencies(self, frequencies):
        self.frequencies = frequencies

    def is_assembled(self):
        return (self.stiffness_matrix is not None) and (self.mass_matrix is not None)

    def get_prescribed_values(self):
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

        global_prescribed = []
        list_prescribed_dofs = []
        if self.frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)

        aux_ones = np.ones(number_frequencies, dtype=complex)

        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "acoustic_pressure":
                real_values = np.array(data["real_values"])
                imag_values = np.array(data["imag_values"])
                complex_values = real_values + 1j * imag_values
                nodes = self.model.mesh.nodes_from_surfaces[surface_id]
                for _ in nodes:
                    global_prescribed.extend(complex_values)

        # TODO: implement same structure for lines

        try:

            for value in global_prescribed:
                if isinstance(value, complex):
                    list_prescribed_dofs.append(aux_ones * value)
                elif isinstance(value, np.ndarray):
                    list_prescribed_dofs.append(value[0:number_frequencies])
            array_prescribed_values = np.array(list_prescribed_dofs)

        except Exception as _error_log:
            print(str(_error_log))

        return global_prescribed, array_prescribed_values

    def get_prescribed_indexes(self):
        _prescribed_indexes = []
        for key, _ in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "acoustic_pressure":
                nodes = self.model.mesh.nodes_from_surfaces[surface_id]
                for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
                    _prescribed_indexes.append(index)

        if len(_prescribed_indexes) == 0:
            return _prescribed_indexes
        else:
            return _prescribed_indexes

    def get_unprescribed_indexes(self):
        element_3D, _ = self.get_element()
        total_dofs = element_3D.DOF_PER_NODE * len(element_3D.nodal_coordinates)
        all_indexes = np.arange(total_dofs, dtype=int)
        prescribed_indexes = self.get_prescribed_indexes()
        return np.delete(all_indexes, prescribed_indexes)

    def process_indexes(self):
        self.prescribed_indexes = self.get_prescribed_indexes()
        self.unprescribed_indexes = self.get_unprescribed_indexes()

    def get_matrices_dropping_indexes(self):
        return self.unprescribed_indexes, self.prescribed_indexes

    def get_surface_data_for_element_integration_by_property(self, label):
        """ """
        connect = None
        output_data = dict()
        aux_connect = dict()
        # index = 0

        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == label:
                if not data["nodal_attribution"]:
                    # TODO: get the surface fluid property
                    fluid = self.model.properties.get_fluid()
                    rho = fluid.fluid_density
                    if surface_id in self.model.surfaces_areas.keys():
                        area = self.model.surfaces_areas[surface_id]
                    else:
                        area = None
                    real_values = np.array(data["real_values"], dtype=float)
                    imag_values = np.array(data["imag_values"], dtype=float)
                    complex_values = real_values + 1j*imag_values 
                    info = self.model.mesh.connectivity_from_surfaces[surface_id] 

                    for i, el in enumerate(info["element_indexes"]):
                        aux_connect[el] = info["connectivity"][i]
                        output_data[el] = [el, complex_values, rho, area]
                        
        if len(aux_connect) > 0:
            connect = np.array(list(aux_connect.values()), dtype=int)

        return connect, output_data

    def assemble_mass_and_stiffness_global_matrices(self, reorder=True):
        """
        Calculates global matrices.
        """

        element_3D, _ = self.get_element()
        ind_rows, ind_cols = element_3D.generate_ind_rows_cols(reorder=reorder)

        dofs = element_3D.DOFS_PER_ELEMENT
        nel = len(element_3D.connectivity)
        total_dofs = element_3D.DOF_PER_NODE * len(element_3D.nodal_coordinates)

        self.data_K = np.zeros((nel, dofs, dofs), dtype=complex)
        self.data_M = np.zeros((nel, dofs, dofs), dtype=complex)
        self.data_Cvisc = np.zeros((nel, dofs, dofs), dtype=complex)

        for el in range(nel):
            Ke, Me = element_3D.elementary_matrices(el)
            rho_0, c_0, mu_0 = element_3D.get_fluid_properties(el)
            self.data_K[el, :, :] = Ke
            self.data_M[el, :, :] = Me
            self.data_Cvisc[el, :, :] = ((4*mu_0)/(3*rho_0*c_0**2))*Ke

        self.data_K = self.data_K.flatten()
        self.data_M = self.data_M.flatten()
        self.data_Cvisc = self.data_Cvisc.flatten()

        _stiffness_matrix_full = csr_matrix((self.data_K, (ind_rows, ind_cols)), shape=(total_dofs, total_dofs))
        _mass_matrix_full = csr_matrix((self.data_M, (ind_rows, ind_cols)), shape=(total_dofs, total_dofs))
        _visc_damping_matrix_full = csr_matrix((self.data_Cvisc, (ind_rows, ind_cols)), shape=(total_dofs, total_dofs))

        self.process_indexes()
        self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.mass_matrix = _mass_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        self.visc_damping_matrix = _visc_damping_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        
        self.stiffness_matrix_r = _stiffness_matrix_full[:, self.prescribed_indexes]
        self.mass_matrix_r = _mass_matrix_full[:, self.prescribed_indexes]   
        self.visc_damping_matrix_r = _visc_damping_matrix_full[:, self.prescribed_indexes]

    def assemble_global_damping_matrix(self):

        if self.frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)
        
        aux_ones = np.ones(number_frequencies, dtype=complex)
        _, element_2D = self.get_element()
        dofs_Z = element_2D.DOFS_PER_ELEMENT
        total_dofs = element_2D.DOF_PER_NODE * len(element_2D.nodal_coordinates)
        self.data_Z = dict()

        connect_Z, data = self.get_surface_data_for_element_integration_by_property("specific_impedance")
        if connect_Z is None:
            _damping_matrix_full = [csr_matrix((total_dofs, total_dofs)) for _ in range(number_frequencies)]
        else:

            nel_Z = connect_Z.shape[0]
            for j in range(number_frequencies):
                self.data_Z[j] = np.zeros((nel_Z, dofs_Z, dofs_Z), dtype=complex)

            ind_rows_Z, ind_cols_Z = element_2D.generate_ind_rows_cols(connect_Z)
            for i, [el, complex_values, rho, _] in enumerate(data.values()):
                normalized_matrix_Z = element_2D.matrices_Z(i)
                # normalized_matrix_Z_base = element_2D.matrices_Z_base(i)
                # print(el, normalized_matrix_Z-normalized_matrix_Z_base)
                if complex_values.shape[0] == 1:
                    complex_values = complex_values * aux_ones
                for j in range(number_frequencies):
                    self.data_Z[j][i, :, :] = normalized_matrix_Z * (rho / complex_values[j])

            _damping_matrix_full = [csr_matrix((self.data_Z[j].flatten(), (ind_rows_Z, ind_cols_Z)), shape=(total_dofs, total_dofs)) for j in range(number_frequencies)]
            
        self.damping_matrix = [matrix[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for matrix in _damping_matrix_full]
        self.damping_matrix_r = [matrix[:, self.prescribed_indexes] for matrix in _damping_matrix_full]

    def get_acoustic_excitations_by_nodal_attribution(self):
        """ This method processes the acoustic model excitations and
            returns the output data in the form of mass flow rate.
        """

        if self.frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)

        aux_ones = np.ones(number_frequencies, dtype=complex)
        acoustic_excitation = defaultdict(float)

        for (property, _id), data in self.properties.surface_properties.items():
            if property == "mass_flow_rate":
                real_values = np.array(data["real_values"])
                imag_values = np.array(data["imag_values"])
                complex_values = real_values + 1j * imag_values
                if complex_values.shape[0] == 1:
                    complex_values = complex_values * aux_ones

                if data["nodal_attribution"]:
                    nodes = self.model.mesh.nodes_from_surfaces[_id]
                    N = len(nodes)
                    for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
                        if data["averaged"]:
                            acoustic_excitation[index] += complex_values / N
                        else:
                            acoustic_excitation[index] += complex_values

            elif property == "volume_velocity":
                real_values = np.array(data["real_values"])
                imag_values = np.array(data["imag_values"])
                complex_values = real_values + 1j * imag_values
                if complex_values.shape[0] == 1:
                    complex_values = complex_values * aux_ones

                if data["nodal_attribution"]:
                    nodes = self.model.mesh.nodes_from_surfaces[_id]
                    N = len(nodes)
                    # TODO: get the surface fluid property
                    fluid = self.model.properties.get_fluid()
                    rho = fluid.fluid_density
                    for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
                        if data["averaged"]:
                            acoustic_excitation[index] += (complex_values * rho) / N
                        else:
                            acoustic_excitation[index] += complex_values * rho

            elif property == "surface_velocity":
                real_values = np.array(data["real_values"])
                imag_values = np.array(data["imag_values"])
                complex_values = real_values + 1j * imag_values
                if complex_values.shape[0] == 1:
                    complex_values = complex_values * aux_ones

                if data["nodal_attribution"]:
                    nodes = self.model.mesh.nodes_from_surfaces[_id]
                    N = len(nodes)
                    # TODO: get the surface fluid property
                    fluid = self.model.properties.get_fluid()
                    rho = fluid.fluid_density
                    area = self.model.surfaces_areas[_id]
                    for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
                        if data["averaged"]:
                            acoustic_excitation[index] += (rho * area * complex_values) / N
                        else:
                            acoustic_excitation[index] += rho * area * complex_values
        
        element_3D, _ = self.get_element()
        total_dofs = element_3D.DOF_PER_NODE * len(element_3D.nodal_coordinates)
        output = np.zeros((total_dofs, number_frequencies), dtype=complex)
        #
        if len(acoustic_excitation) > 0:
            indexes = list(acoustic_excitation.keys())
            excitation = list(acoustic_excitation.values())
            output[indexes, :] = np.array(excitation)
        
        if len(self.prescribed_indexes) > 0:
            return output[self.unprescribed_indexes, :]
        else:
            return output
        
    def get_acoustic_excitations_by_element_integration(self):

        """ This method processes the acoustic model excitations and
            returns the output data in the form of mass flow rate.
        """

        if self.frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)

        _, element_2D = self.get_element()
        total_dofs = element_2D.DOF_PER_NODE * len(element_2D.nodal_coordinates)
        output = np.zeros((total_dofs, number_frequencies), dtype=complex)
        aux_ones = np.ones((1, number_frequencies), dtype=complex)

        connect_mf, data_mf = self.get_surface_data_for_element_integration_by_property("mass_flow_rate")
        if connect_mf is not None:
            element_2D.reorder_connect(connect_mf)
            for i, [el, complex_values, _, _] in enumerate(data_mf.values()):
                indices = element_2D.connect_face[i, :]
                normalized_excitation_matrix = element_2D.excitation_F(i)
                if complex_values.shape[0] == 1:
                    complex_values = complex_values * aux_ones
                elif len(complex_values.shape) == 1:
                    complex_values = complex_values.reshape(1,-1)
                output[indices, :] += normalized_excitation_matrix @ complex_values
        
        connect_vv, data_vv = self.get_surface_data_for_element_integration_by_property("volume_velocity")
        if connect_vv is not None:
            element_2D.reorder_connect(connect_vv)
            for i, [el, complex_values, rho, _] in enumerate(data_vv.values()):
                indices = element_2D.connect_face[i, :]
                normalized_excitation_matrix = element_2D.excitation_F(i)
                if complex_values.shape[0] == 1:
                    complex_values = complex_values * aux_ones
                elif len(complex_values.shape) == 1:
                    complex_values = complex_values.reshape(1,-1)
                output[indices, :] += (normalized_excitation_matrix @ complex_values) * rho
        
        connect_sv, data_sv = self.get_surface_data_for_element_integration_by_property("surface_velocity")
        if connect_sv is not None:
            element_2D.reorder_connect(connect_sv)
            for i, [el, complex_values, rho, _] in enumerate(data_sv.values()):
                indices = element_2D.connect_face[i, :]
                normalized_excitation_matrix = element_2D.excitation_F(i)
                # normalized_excitation_matrix_base = element_2D.excitation_F_base(i)
                # print(normalized_excitation_matrix)
                # print(normalized_excitation_matrix_base)
                # print(el, normalized_excitation_matrix - normalized_excitation_matrix_base)
                if complex_values.shape[0] == 1:
                    complex_values = complex_values * aux_ones
                elif len(complex_values.shape) == 1:
                    complex_values = complex_values.reshape(1,-1)
                output[indices, :] += (normalized_excitation_matrix @ complex_values) * rho
            
        if len(self.prescribed_indexes) > 0:
            return output[self.unprescribed_indexes, :]
        else:
            return output

    def process_assemble(self):
        logging.info( "Assembling global matrices..." + ProgressStatus(10, 100))
        self.assemble_mass_and_stiffness_global_matrices()
        
        logging.info( "Assembling global matrices..." + ProgressStatus(70, 100))
        self.assemble_global_damping_matrix()
        
        logging.info( "Assembling global matrices..." + ProgressStatus(80, 100))
        B = self.get_acoustic_excitations_by_element_integration()
        
        logging.info( "Processing element related loads..." + ProgressStatus(90, 100))
        A = self.get_acoustic_excitations_by_nodal_attribution()
        
        logging.info( "Processing nodal loads..." + ProgressStatus(100, 100))
        self.mass_flow_vectors = A + B