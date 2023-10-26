import numpy as np

from vibra.engine.elements.solid_elements import Element3D


def shapeH8(ssx, ttx, rrx):
    """Shape Functions and Derivatives."""
    denominator = 8
    # shape functions
    phi = np.zeros(8, dtype=float)
    #
    phi[0] = (1.0 - ssx) * (1.0 - ttx) * (1.0 - rrx)
    phi[1] = (1.0 + ssx) * (1.0 - ttx) * (1.0 - rrx)
    phi[2] = (1.0 + ssx) * (1.0 + ttx) * (1.0 - rrx)
    phi[3] = (1.0 - ssx) * (1.0 + ttx) * (1.0 - rrx)
    phi[4] = (1.0 - ssx) * (1.0 - ttx) * (1.0 + rrx)
    phi[5] = (1.0 + ssx) * (1.0 - ttx) * (1.0 + rrx)
    phi[6] = (1.0 + ssx) * (1.0 + ttx) * (1.0 + rrx)
    phi[7] = (1.0 - ssx) * (1.0 + ttx) * (1.0 + rrx)
    phi = phi / denominator

    # derivatives
    dphi = np.zeros((3, 8), dtype=float)
    #
    dphi[0, 0] = (-1.0) * (1.0 - ttx) * (1.0 - rrx)
    dphi[0, 1] = (1.0) * (1.0 - ttx) * (1.0 - rrx)
    dphi[0, 2] = (1.0) * (1.0 + ttx) * (1.0 - rrx)
    dphi[0, 3] = (-1.0) * (1.0 + ttx) * (1.0 - rrx)
    dphi[0, 4] = (-1.0) * (1.0 - ttx) * (1.0 + rrx)
    dphi[0, 5] = (1.0) * (1.0 - ttx) * (1.0 + rrx)
    dphi[0, 6] = (1.0) * (1.0 + ttx) * (1.0 + rrx)
    dphi[0, 7] = (-1.0) * (1.0 + ttx) * (1.0 + rrx)

    dphi[1, 0] = (1.0 - ssx) * (-1.0) * (1.0 - rrx)
    dphi[1, 1] = (1.0 + ssx) * (-1.0) * (1.0 - rrx)
    dphi[1, 2] = (1.0 + ssx) * (1.0) * (1.0 - rrx)
    dphi[1, 3] = (1.0 - ssx) * (1.0) * (1.0 - rrx)
    dphi[1, 4] = (1.0 - ssx) * (-1.0) * (1.0 + rrx)
    dphi[1, 5] = (1.0 + ssx) * (-1.0) * (1.0 + rrx)
    dphi[1, 6] = (1.0 + ssx) * (1.0) * (1.0 + rrx)
    dphi[1, 7] = (1.0 - ssx) * (1.0) * (1.0 + rrx)

    dphi[2, 0] = (1.0 - ssx) * (1.0 - ttx) * (-1.0)
    dphi[2, 1] = (1.0 + ssx) * (1.0 - ttx) * (-1.0)
    dphi[2, 2] = (1.0 + ssx) * (1.0 + ttx) * (-1.0)
    dphi[2, 3] = (1.0 - ssx) * (1.0 + ttx) * (-1.0)
    dphi[2, 4] = (1.0 - ssx) * (1.0 - ttx) * (1.0)
    dphi[2, 5] = (1.0 + ssx) * (1.0 - ttx) * (1.0)
    dphi[2, 6] = (1.0 + ssx) * (1.0 + ttx) * (1.0)
    dphi[2, 7] = (1.0 - ssx) * (1.0 + ttx) * (1.0)

    dphi = dphi / denominator

    return phi, dphi


def get_detJAC_and_invJAC_3D(JAC):
    """ """

    detJAC = (
        JAC[:, 0, 0] * JAC[:, 1, 1] * JAC[:, 2, 2]
        + JAC[:, 0, 1] * JAC[:, 1, 2] * JAC[:, 2, 0]
        + JAC[:, 0, 2] * JAC[:, 1, 0] * JAC[:, 2, 1]
    ) - (
        JAC[:, 2, 0] * JAC[:, 1, 1] * JAC[:, 0, 2]
        + JAC[:, 2, 1] * JAC[:, 1, 2] * JAC[:, 0, 0]
        + JAC[:, 2, 2] * JAC[:, 1, 0] * JAC[:, 0, 1]
    )
    detJAC = detJAC.reshape(-1, 1, 1)
    # adj(JAC)
    AUJJ = np.zeros((detJAC.shape[0], 3, 3), dtype=float)
    AUJJ[:, 0, 0] =  ((JAC[:, 1, 1] * JAC[:, 2, 2]) - (JAC[:, 2, 1] * JAC[:, 1, 2]))
    AUJJ[:, 1, 0] = -((JAC[:, 1, 0] * JAC[:, 2, 2]) - (JAC[:, 1, 2] * JAC[:, 2, 0]))
    AUJJ[:, 2, 0] =  ((JAC[:, 1, 0] * JAC[:, 2, 1]) - (JAC[:, 1, 1] * JAC[:, 2, 0]))
    AUJJ[:, 0, 1] = -((JAC[:, 0, 1] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 1]))
    AUJJ[:, 1, 1] =  ((JAC[:, 0, 0] * JAC[:, 2, 2]) - (JAC[:, 0, 2] * JAC[:, 2, 0]))
    AUJJ[:, 2, 1] = -((JAC[:, 0, 0] * JAC[:, 2, 1]) - (JAC[:, 0, 1] * JAC[:, 2, 0]))
    AUJJ[:, 0, 2] =  ((JAC[:, 0, 1] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 1]))
    AUJJ[:, 1, 2] = -((JAC[:, 0, 0] * JAC[:, 1, 2]) - (JAC[:, 0, 2] * JAC[:, 1, 0]))
    AUJJ[:, 2, 2] =  ((JAC[:, 0, 0] * JAC[:, 1, 1]) - (JAC[:, 0, 1] * JAC[:, 1, 0]))

    return detJAC, (1 / detJAC) * AUJJ


class ACT_HEXAHEDRON_8C(Element3D):
    #
    NODES_PER_ELEMENT = 8
    DOF_PER_NODE = 1
    DOFS_PER_ELEMENT = NODES_PER_ELEMENT * DOF_PER_NODE

    def __init__(self, model):
        self.model = model
        self.initialize_variables()
        self.define_integration_points()
        self.process_shape_functions_and_derivatives()

    def initialize_variables(self):
        """ """
        self.element_label = "acoustic_hexahedron_8"
        self.nodal_coordinates = self.model.mesh.nodal_coordinates
        self.connectivity = self.model.mesh.solids_connectivity
        #
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity)

    def define_integration_points(self):
        """ """
        self.nint = 8
        con = 1 / np.sqrt(3)
        self.wps = 1
        #
        self.pint = np.array( [ [-con, -con, -con],
                                [ con, -con, -con],
                                [ con,  con, -con],
                                [-con,  con, -con],
                                [-con, -con,  con],
                                [ con, -con,  con],
                                [ con,  con,  con],
                                [-con,  con,  con] ], dtype=float)

    def process_shape_functions_and_derivatives(self):
        """ This method processes the shape functions and their
            derivatives for all integration points.
        """
        ssx = self.pint[:, 0]
        ttx = self.pint[:, 1]
        rrx = self.pint[:, 2]
        #
        denominator = 8
        # shape functions
        phi = np.zeros((self.nint, self.NODES_PER_ELEMENT), dtype=float)
        #
        phi[:, 0] = (1.0 - ssx) * (1.0 - ttx) * (1.0 - rrx)
        phi[:, 1] = (1.0 + ssx) * (1.0 - ttx) * (1.0 - rrx)
        phi[:, 2] = (1.0 + ssx) * (1.0 + ttx) * (1.0 - rrx)
        phi[:, 3] = (1.0 - ssx) * (1.0 + ttx) * (1.0 - rrx)
        phi[:, 4] = (1.0 - ssx) * (1.0 - ttx) * (1.0 + rrx)
        phi[:, 5] = (1.0 + ssx) * (1.0 - ttx) * (1.0 + rrx)
        phi[:, 6] = (1.0 + ssx) * (1.0 + ttx) * (1.0 + rrx)
        phi[:, 7] = (1.0 - ssx) * (1.0 + ttx) * (1.0 + rrx)
        phi = phi / denominator

        # derivatives
        dphi = np.zeros((self.nint, 3, self.NODES_PER_ELEMENT), dtype=float)
        #
        dphi[:, 0, 0] = -(1.0 - ttx) * (1.0 - rrx)
        dphi[:, 0, 1] =  (1.0 - ttx) * (1.0 - rrx)
        dphi[:, 0, 2] =  (1.0 + ttx) * (1.0 - rrx)
        dphi[:, 0, 3] = -(1.0 + ttx) * (1.0 - rrx)
        dphi[:, 0, 4] = -(1.0 - ttx) * (1.0 + rrx)
        dphi[:, 0, 5] =  (1.0 - ttx) * (1.0 + rrx)
        dphi[:, 0, 6] =  (1.0 + ttx) * (1.0 + rrx)
        dphi[:, 0, 7] = -(1.0 + ttx) * (1.0 + rrx)

        dphi[:, 1, 0] = -(1.0 - ssx) * (1.0 - rrx)
        dphi[:, 1, 1] = -(1.0 + ssx) * (1.0 - rrx)
        dphi[:, 1, 2] =  (1.0 + ssx) * (1.0 - rrx)
        dphi[:, 1, 3] =  (1.0 - ssx) * (1.0 - rrx)
        dphi[:, 1, 4] = -(1.0 - ssx) * (1.0 + rrx)
        dphi[:, 1, 5] = -(1.0 + ssx) * (1.0 + rrx)
        dphi[:, 1, 6] =  (1.0 + ssx) * (1.0 + rrx)
        dphi[:, 1, 7] =  (1.0 - ssx) * (1.0 + rrx)

        dphi[:, 2, 0] = (1.0 - ssx) * (1.0 - ttx) * (-1.0)
        dphi[:, 2, 1] = (1.0 + ssx) * (1.0 - ttx) * (-1.0)
        dphi[:, 2, 2] = (1.0 + ssx) * (1.0 + ttx) * (-1.0)
        dphi[:, 2, 3] = (1.0 - ssx) * (1.0 + ttx) * (-1.0)
        dphi[:, 2, 4] = (1.0 - ssx) * (1.0 - ttx) * (1.0)
        dphi[:, 2, 5] = (1.0 + ssx) * (1.0 - ttx) * (1.0)
        dphi[:, 2, 6] = (1.0 + ssx) * (1.0 + ttx) * (1.0)
        dphi[:, 2, 7] = (1.0 - ssx) * (1.0 + ttx) * (1.0)

        dphi = dphi / denominator

        self.phi = phi
        self.dphi = dphi

    def elementary_matrices(self, el_index):
        """H8 stiffness and mass matrices."""

        # fluid = self.model.properties.get_fluid(element=el_index)
        # rho = fluid.fluid_density
        # c_0 = fluid.speed_of_sound

        c_0 = self.model.properties.get_speed_of_sound(element=el_index)
        ie = self.connectivity[el_index, 1:]
        #
        JAC = self.dphi @ self.nodal_coordinates[ie, 1:4]
        detJAC, invJAC = get_detJAC_and_invJAC_3D(JAC)
        dphi_t = invJAC @ self.dphi
        #
        B = np.zeros((self.nint, 3, self.DOFS_PER_ELEMENT), dtype=float)
        N = np.zeros((self.nint, 1, self.DOFS_PER_ELEMENT), dtype=float)
        #
        B[:, 0, :] = dphi_t[:, 0, :]
        B[:, 1, :] = dphi_t[:, 1, :]
        B[:, 2, :] = dphi_t[:, 2, :]
        #
        N[:, 0, :] = self.phi
        #
        # integration loop
        Ke, Me = 0, 0
        for i in range(self.nint):
            Ke += B[i, :, :].T @ B[i, :, :] * (detJAC[i, :, :] * self.wps)
            Me += (1 / c_0**2) * N[i, :, :].T @ N[i, :, :] * (detJAC[i, :, :] * self.wps)

        return Ke, Me

    def reorder_connect(self):
        """Reordering connectivity matrix to adequate the GMSH connectivity to the FE model"""
        self.connectivity = self.connectivity[:, [0, 4, 5, 6, 7, 8, 9, 10, 11]]

    def generate_ind_rows_cols(self):
        """This method processess the dofs indices (rows and columns) for assembly"""

        self.reorder_connect()
        dofs, edofs = self.DOF_PER_NODE, self.DOFS_PER_ELEMENT
        ind_dofs = dofs * self.connectivity[:, 1:]

        vect_indices = ind_dofs.flatten()
        self.ind_rows = ((np.tile(vect_indices, (edofs, 1))).T).flatten()
        self.ind_cols = (np.tile(ind_dofs, edofs)).flatten()

        return self.ind_rows, self.ind_cols
    
    def get_fluid_properties(self, el_index):
        """ This method returns the fluid properties """
        c_0 = self.model.properties.get_speed_of_sound(element = el_index)
        rho_0 = self.model.properties.get_fluid_density(element = el_index)
        fluid = self.model.properties.get_fluid(element = el_index)
        dinamic_viscosity = fluid.dynamic_viscosity
        return rho_0, c_0, dinamic_viscosity