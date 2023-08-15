from time import time

import numpy as np
from collections import defaultdict
from scipy.sparse import coo_matrix, csr_matrix

# from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.elements.acoustic_tet4_element import ACT_TETRAHEDRON_4C
from vibra.engine.elements.acoustic_tet10_element import ACT_TETRAHEDRON_10C
from vibra.engine.elements.acoustic_hex8_element import ACT_HEXAHEDRON_8C
from vibra.engine.elements.acoustic_hex20_element import ACT_HEXAHEDRON_20C

from vibra.engine.mesher.element_type import *


class AcousticAssembler:
    def __init__(self, model):
        self.model = model
        self.properties = model.properties
        self.reset()

    def reset(self):
        self.stiffness_matrix = None
        self.mass_matrix = None
        self.frequencies = None
        self.prescribed_values = []
        self.prescribed_indexes = []
        self.unprescribed_indexes = []

    def get_element(self):
        
        element_type = self.model.mesh.element_type

        if element_type == TETRAHEDRON_4:
            return ACT_TETRAHEDRON_4C(self.model)
        elif element_type == TETRAHEDRON_10:
            return ACT_TETRAHEDRON_10C(self.model)
        elif element_type == HEXAHEDRON_8:
            return ACT_HEXAHEDRON_8C(self.model)
        elif element_type == HEXAHEDRON_20:
            return ACT_HEXAHEDRON_20C(self.model)
        else:
            raise NotImplementedError(f"Element type is not supported yet.")

    def set_element_formulation(self, element):
        self.element = element

    def set_frequencies(self, frequencies):
        self.frequencies = frequencies

    def is_assembled(self):
        return (self.stiffness_matrix is not None) and (self.mass_matrix is not None)

    def get_prescribed_values(self):
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
    
        global_prescribed = []
        list_prescribed_dofs = []
        if self.frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)

        for _id, values in self.properties.surfaces_with_acoustic_pressure.items():
            nodes = self.model.mesh.nodes_from_surfaces[_id]
            for _ in nodes:
                global_prescribed.extend(values)

        # for _id, values in self.properties.lines_with_acoustic_pressure.items():
        #     nodes = self.model.mesh.nodes_from_lines[_id]
        #     for _ in nodes:
        #         global_prescribed.extend(values)

        try:    
            
            aux_ones = np.ones(number_frequencies, dtype=complex)
            for value in global_prescribed:
                if isinstance(value, complex):
                    list_prescribed_dofs.append(aux_ones*value)
                elif isinstance(value, np.ndarray):
                    list_prescribed_dofs.append(value[0:number_frequencies])
            array_prescribed_values = np.array(list_prescribed_dofs)
        
        except Exception as _error_log:
            print(str(_error_log))

        return global_prescribed, array_prescribed_values

    def get_prescribed_indexes(self):

        _prescribed_indexes = []

        # for _id in self.properties.lines_with_acoustic_pressure:
        #     nodes = self.model.mesh.nodes_from_surfaces[_id]
        #     for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
        #         _prescribed_indexes.append(index)

        for _id in self.properties.surfaces_with_acoustic_pressure:
            nodes = self.model.mesh.nodes_from_surfaces[_id]

            for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
                _prescribed_indexes.append(index)
        
        if len(_prescribed_indexes) == 0:
            return _prescribed_indexes
        else:
            return _prescribed_indexes

    def get_unprescribed_indexes(self):

        element = self.get_element()
        total_dofs = element.DOF_PER_NODE * len(element.nodal_coordinates)
        all_indexes = np.arange(total_dofs, dtype=int)
        prescribed_indexes = self.get_prescribed_indexes()

        return np.delete(all_indexes, prescribed_indexes)

    def process_indexes(self):
        self.prescribed_indexes = self.get_prescribed_indexes()
        self.unprescribed_indexes = self.get_unprescribed_indexes()

    def get_matrices_dropping_indexes(self):
        return self.unprescribed_indexes, self.prescribed_indexes

    def assemble_global_matrices(self):
        """
        Calculates global matrices.
        """

        element = self.get_element()
        ind_rows, ind_cols = element.generate_ind_rows_cols()

        dofs = element.DOFS_PER_ELEMENT
        nel = len(element.connectivity)
        total_dofs = element.DOF_PER_NODE * len(element.nodal_coordinates)

        self.data_K = np.zeros((nel, dofs, dofs), dtype=complex)
        self.data_M = np.zeros((nel, dofs, dofs), dtype=complex)

        for el in range(nel):
            Ke, Me = element.elementary_matrices(el)
            self.data_K[el, :, :] = Ke
            self.data_M[el, :, :] = Me

        self.data_K = self.data_K.flatten()
        self.data_M = self.data_M.flatten()

        _stiffness_matrix_full = csr_matrix(
            (self.data_K, (ind_rows, ind_cols)), shape=(total_dofs, total_dofs)
        )
        _mass_matrix_full = csr_matrix(
            (self.data_M, (ind_rows, ind_cols)), shape=(total_dofs, total_dofs)
        )

        self.process_indexes()
        if len(self.prescribed_indexes) > 0:
            self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
            self.mass_matrix = _mass_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        else:
            self.stiffness_matrix = _stiffness_matrix_full
            self.mass_matrix = _mass_matrix_full

    def get_acoustic_excitations(self):

        acoustic_excitation = defaultdict(float)
        
        for _id, data in self.properties.surfaces_with_mass_flow_rate.items():
            values = data["values"]
            avg = data["averaged"]
            nodes = self.model.mesh.nodes_from_surfaces[_id]
            N = len(nodes)
            for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
                if bool(avg):
                    acoustic_excitation[index] += values/N
                else:
                    acoustic_excitation[index] += values

        for _id, data in self.properties.surfaces_with_volume_velocity.items():
            values = data["values"]
            avg = data["averaged"]
            nodes = self.model.mesh.nodes_from_surfaces[_id]
            #TODO: get the surface fluid property
            fluid = self.model.properties.get_fluid()
            rho = fluid.fluid_density
            N = len(nodes)
            for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
                if bool(avg):
                    acoustic_excitation[index] += (values*rho)/N
                else:
                    acoustic_excitation[index] += values*rho

        for _id, data in self.properties.surfaces_with_particle_velocity.items():
            values = data["values"]
            avg = data["averaged"]
            nodes = self.model.mesh.nodes_from_surfaces[_id]
            #TODO: get the surface fluid property
            fluid = self.model.properties.get_fluid()
            rho = fluid.fluid_density
            area = self.model.surfaces_areas[_id]
            N = len(nodes)
            for index in self.model.get_acoustic_global_dofs_from_nodes(nodes):
                if bool(avg):
                    acoustic_excitation[index] += (rho*area*values)/N
                else:
                    acoustic_excitation[index] += rho*area*values

        indexes = list(acoustic_excitation.keys())
        excitation = list(acoustic_excitation.values())
        
        element = self.get_element()
        total_dofs = element.DOF_PER_NODE * len(element.nodal_coordinates)
        output = np.zeros((total_dofs,1), dtype=complex)
        output[indexes, 0] = excitation

        return output[self.unprescribed_indexes, :]



# class AcousticAssembler(AcousticAssembler):
#     def new_element(self):
        
#         element_type = self.model.mesh.element_type

#         if element_type == TETRAHEDRON_4:
#             return ACT_TETRAHEDRON_4C(self.model)
#         elif element_type == TETRAHEDRON_10:
#             return ACT_TETRAHEDRON_10C(self.model)
#         elif element_type == HEXAHEDRON_8:
#             return ACT_HEXAHEDRON_8C(self.model)
#         elif element_type == HEXAHEDRON_20:
#             return ACT_HEXAHEDRON_20C(self.model)
#         else:
#             raise NotImplementedError(f"Element type is not supported yet.")



