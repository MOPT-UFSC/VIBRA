from time import time

import numpy as np
from scipy.sparse import coo_matrix

from vibra.engine.elements.acoustic_tet4_element import ACT_TETRAHEDRON_4C

#TODO: implementar todos os elementos acústicos, para validação preciso ter todos operacionais!!!
# o tipo de elemento pode ser acessado em self.project.model.mesh_setup["element_type"]

# from vibra.engine.elements.acoustic_tet10_element import ACT_TETRAHEDRON_10C
# from vibra.engine.elements.acoustic_hex8_element import ACT_HEXAHEDRON_8C
# from vibra.engine.elements.acoustic_hex20_element import ACT_HEXAHEDRON_20C

class ModalAssembler:
    def __init__(self, model):
        #
        self.model = model
        self.stiffness_matrix = None
        self.mass_matrix = None

    def set_element_formulation(self, element):
        self.element = element

    def is_assembled(self):
        return (self.stiffness_matrix is not None) and (self.mass_matrix is not None)

    def assemble_global_matrices(self):
        """
        Calculates global matrices.
        """
        element = ACT_TETRAHEDRON_4C(self.model)
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

        self.stiffness_matrix = coo_matrix(
            (self.data_K, (ind_rows, ind_cols)), shape=(total_dofs, total_dofs)
        )
        self.mass_matrix = coo_matrix(
            (self.data_M, (ind_rows, ind_cols)), shape=(total_dofs, total_dofs)
        )
