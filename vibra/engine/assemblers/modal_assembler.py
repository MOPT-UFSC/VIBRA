import numpy as np
from scipy.sparse import csr_matrix, coo_matrix
from time import time
import matplotlib.pyplot as plt
from vibra.engine.elements.acoustic_tet4_element import ACT_TETRAHEDRON_4C


class ModalAssembler:

    def __init__(self, model):
        self.model = model
        self.element_formulation = ACT_TETRAHEDRON_4C(model)
        self.assemble_global_matrices()

        # element.reorder_connect()
        # self.element = element
        # self.initialize_variables()
        # self.ind_rows, self.ind_cols = element.generate_ind_rows_cols()
        # t0 = time()
        # self.assemble_global_matrices()
        # dt = time() - t0
        # print(f"Elpased time: {dt} [s]")


    # def initialize_variables(self):
    #     """
    #     """
    #     self.ind_rows = None
    #     self.ind_cols = None
    #     self.data_K = None
    #     self.data_M = None
    #     self.stiffness_matrix = None
    #     self.mass_matrix = None
    #     self.dof_per_node = self.element.dof_per_node
    #     self.dofs_per_element = self.element.dofs_per_element
    #     self.nodes_per_element = self.element.nodes_per_element
    #     self.number_of_nodes = self.element.number_of_nodes
    #     self.number_of_elements = self.element.number_of_elements
    #     self.connect = self.element.connect
    #     self.nodal_coordinates = self.element.nodal_coordinates


    def assemble_global_matrices(self):
        """
        Calculates global matrices.
        """

        dofs = self.element_formulation.DOFS_PER_ELEMENT
        nel = len(self.element_formulation.connectivity)
        total_dofs = self.element_formulation.DOF_PER_NODE * len(self.element_formulation.nodal_coordinates)

        self.data_K = np.zeros((nel, dofs, dofs), dtype=float)
        self.data_M = np.zeros((nel, dofs, dofs), dtype=float)
        
        for el in range(nel):
            Ke, Me = self.element.elementary_matrices(el)
            self.data_K[el, :, :] = Ke
            self.data_M[el, :, :] = Me
        
        self.data_K = self.data_K.flatten()
        self.data_M = self.data_M.flatten()
        
        self.stiffness_matrix = coo_matrix((self.data_K, (self.ind_rows, self.ind_cols)), shape=(total_dofs, total_dofs))
        self.mass_matrix = coo_matrix((self.data_M, (self.ind_rows, self.ind_cols)), shape=(total_dofs, total_dofs))        
