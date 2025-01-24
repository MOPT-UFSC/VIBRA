
# fmt: off

from vibra.engine.model import Model

from vibra.engine.elements.structural_hex8_element import STRUCT_HEXAHEDRON_8
from vibra.engine.elements.structural_hex20_element import STRUCT_HEXAHEDRON_20
from vibra.engine.elements.structural_tet4_element import STRUCT_TETRAHEDRON_4S
from vibra.engine.elements.structural_tet10_element import STRUCT_TETRAHEDRON_10S
from vibra.engine.elements.structural_face3_element import STRUCT_FACE_3

from vibra.engine.mesher.element_type import *

from collections import defaultdict
from time import time

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix

class StructuralAssembler:
    def __init__(self, model : Model):
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
            return STRUCT_TETRAHEDRON_4S(self.model), STRUCT_FACE_3(self.model)
        elif element_type == TETRAHEDRON_10:
            return STRUCT_TETRAHEDRON_10S(self.model), None
        elif element_type == HEXAHEDRON_8:
            return STRUCT_HEXAHEDRON_8(self.model), None
        elif element_type == HEXAHEDRON_20:
            return STRUCT_HEXAHEDRON_20(self.model), None
        else:
            raise NotImplementedError(f"Element type is not supported yet.")

    def set_element_formulation(self, element):
        self.element = element

    def update_number_of_frequencies(self):
        self.frequencies = self.model.frequencies
        if self.frequencies is None:
            self.number_frequencies = 1
        else:
            self.number_frequencies = len(self.frequencies)

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

        global_prescribed = list()
        list_prescribed_dofs = list()
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

        _prescribed_indexes = list()
        for property, line_id in self.properties.line_properties.keys():
            if property == "prescribed_dofs":
                nodes = self.model.mesh.nodes_from_lines[line_id]
                for index in self.model.get_structural_global_dofs_from_nodes(nodes):
                    _prescribed_indexes.append(index)

        for property, surface_id in self.properties.surface_properties.keys():
            if property == "prescribed_dofs":
                nodes = self.model.mesh.nodes_from_surfaces[surface_id]
                for index in self.model.get_structural_global_dofs_from_nodes(nodes):
                    _prescribed_indexes.append(index)

        if len(_prescribed_indexes) == 0:
            return _prescribed_indexes
        else:
            return _prescribed_indexes

    def get_unprescribed_indexes(self):

        element_3D, _ = self.get_element()
        total_dofs = element_3D.DOF_PER_NODE * len(element_3D.nodal_coordinates)
        all_indexes = np.arange(total_dofs, dtype=int)
        # prescribed_indexes = self.get_prescribed_indexes()

        return np.delete(all_indexes, self.prescribed_indexes)

    def get_matrices_dropping_indexes(self):
        return self.unprescribed_indexes, self.prescribed_indexes
    
    def process_displacement_and_rotation_dofs(self, n_dofs: int, rotation_dofs: np.ndarray):
        self.dofs = np.arange(n_dofs)
        self.rotation_dofs = np.sort(rotation_dofs.flatten())
        if len(self.rotation_dofs):
            self.displacement_dofs = np.delete(self.dofs, self.rotation_dofs)
        else:
            self.displacement_dofs = self.dofs.copy()
        # np.savetxt("displacement_dofs.dat", self.displacement_dofs.reshape(-1, 1), delimiter=",", fmt="%i")
        # np.savetxt("rotation_dofs.dat", self.rotation_dofs.reshape(-1, 1), delimiter=",", fmt="%i")

    def process_nodes_from_face_elements_with_thickness(self, element_2D, element_3D):

        nodes_from_surfaces = list()
        for surface_nodes in self.model.mesh.nodes_from_surfaces.values():
            nodes_from_surfaces.extend(surface_nodes)

        nodes_from_surfaces = np.array([*set(nodes_from_surfaces)], dtype=int)
        # print(f"nodes from surfaces: {nodes_from_surfaces}")

        active_nodes_list = list()
        for key in self.model.properties.surface_properties.keys():
            property, surface_id = key
            if property == "surface_thickness":
                active_nodes_list.extend(self.model.mesh.nodes_from_surfaces[surface_id])

        shell_local_dofs = np.arange(element_2D.DOF_PER_NODE)
        rotation_local_dofs = shell_local_dofs[int(element_2D.DOF_PER_NODE / 2):]

        number_of_surface_nodes = 0
        active_dofs = np.array([])
        rotation_dofs = np.array([])

        if active_nodes_list:
            active_nodes = np.array([*set(active_nodes_list)], dtype=int)
            active_dofs = element_2D.DOF_PER_NODE * active_nodes.reshape(-1, 1) + shell_local_dofs 
            active_dofs = np.sort(active_dofs.flatten())

            # active_rotation_dofs = element_2D.DOF_PER_NODE * active_nodes.reshape(-1, 1) + rotations_dofs
            rotation_dofs = element_2D.DOF_PER_NODE * nodes_from_surfaces.reshape(-1, 1) + rotation_local_dofs
            # rotation_dofs = np.sort(rotation_dofs.flatten())
            number_of_surface_nodes = len(nodes_from_surfaces)

        number_of_nodes = len(element_3D.nodal_coordinates)
        n_dofs = number_of_nodes * element_3D.DOF_PER_NODE + number_of_surface_nodes * int(element_2D.DOF_PER_NODE / 2)

        self.process_displacement_and_rotation_dofs(n_dofs, rotation_dofs)
        # print(len(active_nodes), number_of_surface_nodes, number_of_nodes, n_dofs)

        return active_dofs, n_dofs

    def assemble_mass_and_stiffness_global_matrices(self):
        """
        Calculates global matrices.
        """

        self.data_K = np.array([], dtype=float)
        self.data_M = np.array([], dtype=float)

        ind_cols = np.array([], dtype=int)
        ind_rows = np.array([], dtype=int)

        element_3D, element_2D = self.get_element()
        self.shell_dofs, self.n_dofs = self.process_nodes_from_face_elements_with_thickness(element_2D, element_3D)
        # total_dofs = element_2D.DOF_PER_NODE * len(element_3D.nodal_coordinates)

        # rows_se, cols_se = element_3D.generate_ind_rows_cols()
        # ind_rows = np.append(ind_rows, rows_se)
        # ind_cols = np.append(ind_cols, cols_se)

        # dofs = element_3D.DOFS_PER_ELEMENT
        # nel = len(element_3D.connectivity)
        # # total_dofs = element_3D.DOF_PER_NODE * len(element_3D.nodal_coordinates)

        # data_K_se = np.zeros((nel, dofs, dofs), dtype=float)
        # data_M_se = np.zeros((nel, dofs, dofs), dtype=float)

        # # loop for solid elements
        # for el_index in range(nel):
        #     Ke, Me = element_3D.elementary_matrices(el_index)
        #     data_K_se[el_index, :, :] = Ke
        #     data_M_se[el_index, :, :] = Me

        # self.data_K = np.append(self.data_K, data_K_se.flatten())
        # self.data_M = np.append(self.data_M, data_M_se.flatten())

        if len(self.shell_dofs):

            rows_fe, cols_fe = element_2D.generate_ind_rows_cols()

            dofs = element_2D.DOFS_PER_ELEMENT
            nel = len(element_2D.connectivity)

            ind_rows = np.append(ind_rows, rows_fe)
            ind_cols = np.append(ind_cols, cols_fe)
            # np.savetxt("indexes.dat", np.array([ind_rows, ind_cols], dtype=int).T, fmt="%i")

            data_K_fe = np.zeros((nel, dofs, dofs), dtype=float)
            data_M_fe = np.zeros((nel, dofs, dofs), dtype=float)

            # loop for solid elements
            for el_index in range(nel):

                s_data = self.model.mesh.face_element_thickness.get(el_index, None)
                if s_data is None:
                    continue

                t = s_data.get("surface_thickness", None)
                if t is None:
                    continue

                Ke, Me = element_2D.elementary_matrices(el_index, t)

                data_K_fe[el_index, :, :] = Ke
                data_M_fe[el_index, :, :] = Me

            self.data_K = np.append(self.data_K, data_K_fe.flatten())
            self.data_M = np.append(self.data_M, data_M_fe.flatten())

        _stiffness_matrix_full = csr_matrix((self.data_K, (ind_rows, ind_cols)), shape=(self.n_dofs, self.n_dofs))
        _mass_matrix_full = csr_matrix((self.data_M, (ind_rows, ind_cols)), shape=(self.n_dofs, self.n_dofs))

        if len(self.shell_dofs):
            _stiffness_matrix_full = _stiffness_matrix_full[self.shell_dofs, :][:, self.shell_dofs]
            _mass_matrix_full = _mass_matrix_full[self.shell_dofs, :][:, self.shell_dofs]

        self.process_indexes()

        if self.prescribed_indexes:
            self.mass_matrix = _mass_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
            self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]

        else:
            self.mass_matrix = _mass_matrix_full
            self.stiffness_matrix = _stiffness_matrix_full
            # np.savetxt("stiffness_matrix_global_test.dat", _stiffness_matrix_full.toarray(), delimiter=",")
            # np.savetxt("mass_matrix_global_test.dat", _mass_matrix_full.toarray(), delimiter=",")
            # print(np.linalg.det(_stiffness_matrix_full.toarray()), np.linalg.det(_mass_matrix_full.toarray()))

    def process_assemble(self):

        self.update_number_of_frequencies()
        self.model.process_surface_thickness()

        self.assemble_mass_and_stiffness_global_matrices()
        # A = self.get_structural_excitations_by_nodal_attribution()
        # B = self.get_structural_excitations_by_element_integration()
        # self.flow_mass_vectors = A + B
        #
        # indA = np.arange(0, len(A), 1)
        # indB = np.arange(0, len(B), 1)
        # np.savetxt("excitation_nodal.dat", np.array([indA, A[:,-1]]).T, delimiter=",")
        # np.savetxt("excitation_element.dat", np.array([indB, B[:,-1]]).T, delimiter=",")

# fmt: on