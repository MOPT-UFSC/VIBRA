from collections import defaultdict
from time import time

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix

from vibra.engine.elements.structural_hex8_element import STRUCT_HEXAHEDRON_8
from vibra.engine.elements.structural_hex20_element import STRUCT_HEXAHEDRON_20
# from vibra.engine.assemblers.modal_assembler import ModalAssembler
from vibra.engine.elements.structural_tet4_element import STRUCT_TETRAHEDRON_4S
from vibra.engine.elements.structural_tet10_element import (
    STRUCT_TETRAHEDRON_10S,
)
from vibra.engine.mesher.element_type import *


class StructuralAssembler:
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
            return STRUCT_TETRAHEDRON_4S(self.model)
        elif element_type == TETRAHEDRON_10:
            return STRUCT_TETRAHEDRON_10S(self.model)
        elif element_type == HEXAHEDRON_8:
            return STRUCT_HEXAHEDRON_8(self.model)
        elif element_type == HEXAHEDRON_20:
            return STRUCT_HEXAHEDRON_20(self.model)
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

    def process_indexes(self):
        self.prescribed_indexes = self.get_prescribed_indexes()
        self.unprescribed_indexes = self.get_unprescribed_indexes()

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

        for key, data in self.properties.line_properties.items():
            property, line_id = key
            if property == "prescribed_dofs":
                values = data["values"]
                nodes = self.model.mesh.nodes_from_lines[line_id]
                for _ in nodes:
                    global_prescribed.extend(values)

        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "prescribed_dofs":
                values = data["values"]
                nodes = self.model.mesh.nodes_from_surfaces[surface_id]
                for _ in nodes:
                    global_prescribed.extend(values)

        try:
            aux_ones = np.ones(number_frequencies, dtype=complex)
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

        for (property, line_id) in self.properties.line_properties.keys():
            if property == "prescribed_dofs":
                nodes = self.model.mesh.nodes_from_lines[line_id]
                for index in self.model.get_structural_global_dofs_from_nodes(nodes):
                    _prescribed_indexes.append(index)

        for (property, surface_id) in self.properties.surface_properties.keys():
            if property == "prescribed_dofs":    
                nodes = self.model.mesh.nodes_from_surfaces[surface_id]
                for index in self.model.get_structural_global_dofs_from_nodes(nodes):
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

        self.data_K = np.zeros((nel, dofs, dofs), dtype=float)
        self.data_M = np.zeros((nel, dofs, dofs), dtype=float)

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
            self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_indexes, :][
                :, self.unprescribed_indexes
            ]
            self.mass_matrix = _mass_matrix_full[self.unprescribed_indexes, :][
                :, self.unprescribed_indexes
            ]
        else:
            self.stiffness_matrix = _stiffness_matrix_full
            self.mass_matrix = _mass_matrix_full
