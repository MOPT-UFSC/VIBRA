import numpy as np
from scipy.sparse import csr_matrix, coo_matrix
from time import time
import matplotlib.pyplot as plt
from vibra.engine.elements.acoustic_tet4_element import ACT_TETRAHEDRON_4C


class ModalAssembler:
    def __init__(self, model=None):
        self.model = model
        # self.assemble_global_matrices()

    def set_model(self, model):
        self.model = model

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
