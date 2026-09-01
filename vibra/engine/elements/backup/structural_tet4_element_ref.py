import numpy as np

from vibra.engine.elements.elements_3d.solid_elements import Element3D
from vibra.engine.properties.material import Material

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.engine.model import Model

# fmt: off

def shapeT4C(ssx, ttx, rrx):
    """This function returns the shape functions and its derivatives."""
    # shape functions
    phi = np.array([1 - ssx - ttx - rrx, ttx, rrx, ssx], dtype=float)
    # derivatives
    dphi = np.array([[-1, 0, 0, 1], [-1, 1, 0, 0], [-1, 0, 1, 0]], dtype=float)

    return phi, dphi


class StructuralTetrahedron4S(Element3D):
    #
    nodes_per_element = 4
    dof_per_node = 3
    dof_per_element = nodes_per_element * dof_per_node

    def __init__(self, model: "Model"):
        #
        self.model = model
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()

    def initialize_variables(self):
        """ """
        self.connectivity = None
        self.element_label = "structural_tetrahedron_4"
        
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.solids_connectivity = self.model.mesh.solids_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.solids_connectivity)

    def define_integration_points(self):
        """ """
        # integration points
        # nint = 1
        # con = 1/4
        # pint = np.array([[ con, con, con]])
        # wps = 1
        # integration points
        self.nint = 4
        con1 = (5 - np.sqrt(5)) / 20
        con2 = (5 + 3 * np.sqrt(5)) / 20
        self.wps = 1 / 4
        self.pint = np.array([  [con1, con1, con1], 
                                [con1, con1, con2], 
                                [con1, con2, con1], 
                                [con2, con1, con1]  ])

    def process_shape_functions_and_derivatives(self):
        """This method processes the shape functions and their
        derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        rrx = self.pint[:, 2]
        # shape functions
        self.phi = np.array([1 - ssx - ttx - rrx, ttx, rrx, ssx], dtype=float)
        # derivatives
        self.dphi = np.array([[-1, 0, 0, 1], 
                              [-1, 1, 0, 0], 
                              [-1, 0, 1, 0]], dtype=float)

    def elementary_matrices(self, el_index: int, material: Material):
        """Stiffness and mass matrices.
        This is not a p-u mixed fomulation. Do not compare with SOLID285.
        """

        const_mat, rho = self.get_constitutive_model(material, model_type="linear-isotropic")

        ie = self.connectivity[el_index, 1:]
        JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = self.get_detJAC_and_invJAC(JAC)
        dphi_t = invJAC @ self.dphi

        B = np.zeros((6, self.dof_per_element), dtype=float)
        B[0, 0::3] = dphi_t[0, :]
        B[1, 1::3] = dphi_t[1, :]
        B[2, 2::3] = dphi_t[2, :]
        B[3, 0::3] = dphi_t[1, :]
        B[3, 1::3] = dphi_t[0, :]
        B[4, 0::3] = dphi_t[2, :]
        B[4, 2::3] = dphi_t[0, :]
        B[5, 1::3] = dphi_t[2, :]
        B[5, 2::3] = dphi_t[1, :]

        N = np.zeros((self.nint, 3, self.dof_per_element), dtype=float)
        N[:, 0, 0::3] = self.phi
        N[:, 1, 1::3] = self.phi
        N[:, 2, 2::3] = self.phi

        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            Ke += (1 / 6) * B.T @ const_mat @ B * (detJAC * self.wps)
            Me += (1 / 6) * rho * N[i, :, :].T @ N[i, :, :] * (detJAC * self.wps)

        return Ke, Me

    def reorder_connect(self, reorder: bool = True):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        if self.solids_connectivity.shape[1] == self.nodes_per_element + 4:
            self.connectivity = self.solids_connectivity[:, [0, 6, 4, 5, 7]]

    def get_rows_and_cols_indices(self, el_index: int, shift_index: int):

        edof = self.dof_per_element
        node_ids = self.connectivity[el_index, 1:]
        local_dof = np.arange(self.dof_per_node, dtype=int)

        _dof = np.zeros(len(node_ids), dtype=int)
        _shifts = np.zeros(len(node_ids), dtype=int)

        for i, node_id in enumerate(node_ids):

            shift = shift_index
            dof_node = self.dof_per_node
            surface_ids = self.model.mesh.get_surfaces_from_node(node_id)

            for surface_id in surface_ids:
                shell_data = self.model.properties._get_property("surface_thickness", surface=surface_id)
                if isinstance(shell_data, dict):
                    dof_node = 2 * self.dof_per_node
                    shift = 0
                    break

            _dof[i] = dof_node
            _shifts[i] = shift

        _indices = (_dof * node_ids + _shifts).reshape(-1, 1) + local_dof
        aux = np.tile(_indices.flatten(), (edof, 1))
        ind_rows = aux.T
        ind_cols = aux

        return ind_rows, ind_cols

    def generate_ind_rows_cols(self, reorder: bool = True):
        """This method processess the dof indices (rows and columns) for assembly"""

        if reorder:
            self.reorder_connect()
        else:
            self.connectivity = self.solids_connectivity[:, [0, 4, 5, 6, 7]]

        dof = self.dof_per_node
        edof = self.dof_per_element

        # ind_dof = np.array([  dof * self.connectivity[:, 1] + 0,
        #                        dof * self.connectivity[:, 1] + 1,
        #                        dof * self.connectivity[:, 1] + 2,
        #                        dof * self.connectivity[:, 2] + 0,
        #                        dof * self.connectivity[:, 2] + 1,
        #                        dof * self.connectivity[:, 2] + 2,
        #                        dof * self.connectivity[:, 3] + 0,
        #                        dof * self.connectivity[:, 3] + 1,
        #                        dof * self.connectivity[:, 3] + 2,
        #                        dof * self.connectivity[:, 4] + 0,
        #                        dof * self.connectivity[:, 4] + 1,
        #                        dof * self.connectivity[:, 4] + 2  ], dtype=int).T

        local_dof = np.arange(dof, dtype=int)

        ind_dof = np.array([dof * self.connectivity[:, 1].reshape(-1, 1) + local_dof,
                            dof * self.connectivity[:, 2].reshape(-1, 1) + local_dof,
                            dof * self.connectivity[:, 3].reshape(-1, 1) + local_dof,
                            dof * self.connectivity[:, 4].reshape(-1, 1) + local_dof], dtype=int)

        self.ind_rows = ((np.tile(ind_dof.flatten(), (edof, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dof, edof)).flatten()

        return self.ind_rows, self.ind_cols

# fmt: on