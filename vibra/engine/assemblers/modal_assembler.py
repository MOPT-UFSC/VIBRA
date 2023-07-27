from time import time

import numpy as np
from scipy.sparse import coo_matrix

import logging
from vibra.utils.progress_status import ProgressStatus


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

        logging.info("Finding correct element formulation" + ProgressStatus(10, 100))
        element = self.new_element()
        ind_rows, ind_cols = element.generate_ind_rows_cols()

        dofs = element.DOFS_PER_ELEMENT
        nel = len(element.connectivity)
        total_dofs = element.DOF_PER_NODE * len(element.nodal_coordinates)

        self.data_K = np.zeros((nel, dofs, dofs), dtype=float)
        self.data_M = np.zeros((nel, dofs, dofs), dtype=float)

        logging.info(f"Assembling elements" + ProgressStatus(15, 100))
        for el in range(nel):
            Ke, Me = element.elementary_matrices(el)
            self.data_K[el, :, :] = Ke
            self.data_M[el, :, :] = Me

        self.data_K = self.data_K.flatten()
        self.data_M = self.data_M.flatten()

        logging.info("Creating sparse matrices from data" + ProgressStatus(90, 100))
        self.stiffness_matrix = coo_matrix(
            (self.data_K, (ind_rows, ind_cols)), shape=(total_dofs, total_dofs)
        )
        self.mass_matrix = coo_matrix(
            (self.data_M, (ind_rows, ind_cols)), shape=(total_dofs, total_dofs)
        )

    def new_element(self):
        '''
        Returns the correct element according to the
        model mesh configuration.
        '''
        raise NotImplementedError("new_element function not implemented")
