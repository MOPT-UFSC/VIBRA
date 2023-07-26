from time import time

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix

#TODO: implementar todos os elementos acústicos, para validação preciso ter todos operacionais!!!
# o tipo de elemento pode ser acessado em self.project.model.mesh_setup["element_type"]


class ModalAssembler:
    def __init__(self, model):
        self.model = model
        self.reset()

    def reset(self):
        self.stiffness_matrix = None
        self.mass_matrix = None
        self.frequencies = None
        self.prescribed_values = []
        self.prescribed_indexes = []
        self.unprescribed_indexes = []

    def set_element_formulation(self, element):
        self.element = element

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

        for _id, values in self.model.surfaces_with_prescribed_dofs.items():
            nodes = self.model.mesh.nodes_from_surfaces[_id]
            for _ in nodes:
                global_prescribed.extend(values)

        for _id, values in self.model.lines_with_prescribed_dofs.items():
            nodes = self.model.mesh.nodes_from_lines[_id]
            for _ in nodes:
                global_prescribed.extend(values)

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

        for _id in self.model.lines_with_prescribed_dofs:
            nodes = self.model.mesh.nodes_from_surfaces[_id]
            for index in self.model.get_structural_global_dofs_from_nodes(nodes):
                _prescribed_indexes.append(index)

        for _id in self.model.surfaces_with_prescribed_dofs:
            nodes = self.model.mesh.nodes_from_surfaces[_id]
            for index in self.model.get_structural_global_dofs_from_nodes(nodes):
                _prescribed_indexes.append(index)
        
        if len(_prescribed_indexes) == 0:
            return _prescribed_indexes
        else:
            return _prescribed_indexes

    def get_unprescribed_indexes(self):

        element = self.new_element()
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

        element = self.new_element()
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
            self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
            self.mass_matrix = _mass_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        else:
            self.stiffness_matrix = _stiffness_matrix_full
            self.mass_matrix = _mass_matrix_full


    def new_element(self):
        '''
        Returns the correct element according to the
        model mesh configuration.
        '''
        raise NotImplementedError("new_element function not implemented")
