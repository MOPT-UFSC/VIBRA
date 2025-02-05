
# fmt: off

from vibra.engine.model import Model

from vibra.engine.elements.structural_hex8_element import STRUCT_HEXAHEDRON_8
from vibra.engine.elements.structural_hex20_element import STRUCT_HEXAHEDRON_20
from vibra.engine.elements.structural_tet4_element import STRUCT_TETRAHEDRON_4S
from vibra.engine.elements.structural_tet10_element import STRUCT_TETRAHEDRON_10S
from vibra.engine.elements.structural_tria3_element import STRUCT_TRIANGULAR_3

from vibra.engine.mesher.element_type import *
from vibra.utils.progress_status import ProgressStatus

from collections import defaultdict
from time import time

import logging
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

        self.prescribed_values = np.array([])
        self.prescribed_indexes = np.array([])
        self.unprescribed_indexes = np.array([])

    def get_element(self):

        element_type = self.model.mesh.element_type

        if element_type == TETRAHEDRON_4:
            return STRUCT_TETRAHEDRON_4S(self.model), STRUCT_TRIANGULAR_3(self.model)

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

        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "prescribed_dofs":
                values = data["values"]
                nodes = self.model.mesh.nodes_from_surfaces[surface_id]
                for _ in nodes:
                    global_prescribed.extend(values)

        for key, data in self.properties.line_properties.items():
            property, line_id = key
            if property == "prescribed_dofs":
                values = data["values"]
                nodes = self.model.mesh.nodes_from_lines[line_id]
                for _ in nodes:
                    global_prescribed.extend(values)

        for key, data in self.properties.point_properties.items():
            property, point_id = key
            if property == "prescribed_dofs":
                values = data["values"]
                nodes = self.model.mesh.nodes_from_points[point_id]
                for _ in nodes:
                    global_prescribed.extend(values)

        for key, data in self.properties.nodal_properties.items():
            property, _ = key
            if property == "prescribed_dofs":
                values = data["values"]
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

        for (property, surface_id), data in self.properties.surface_properties.items():
            if property == "prescribed_dofs":
                element_type = data["element_type"]
                nodes = self.model.mesh.nodes_from_surfaces[surface_id]
                for index in self.model.get_structural_global_dofs_from_nodes(nodes, element_type):
                    _prescribed_indexes.append(index)

        for (property, line_id), data in self.properties.line_properties.items():
            if property == "prescribed_dofs":
                element_type = data["element_type"]
                nodes = self.model.mesh.nodes_from_lines[line_id]
                for index in self.model.get_structural_global_dofs_from_nodes(nodes, element_type):
                    _prescribed_indexes.append(index)

        for (property, point_id), data in self.properties.point_properties.items():
            if property == "prescribed_dofs":
                element_type = data["element_type"]
                nodes = self.model.mesh.nodes_from_points[point_id]
                for index in self.model.get_structural_global_dofs_from_nodes(nodes, element_type):
                    _prescribed_indexes.append(index)

        for (property, node_id), data in self.properties.nodal_properties.items():
            if property == "prescribed_dofs":
                element_type = data["element_type"]
                for index in self.model.get_structural_global_dofs_from_nodes(np.array([node_id]), element_type):
                    _prescribed_indexes.append(index)

        return _prescribed_indexes

    def get_unprescribed_indexes(self):
        prescribed_indexes = np.array([*set(self.prescribed_indexes)], dtype=int)
        return np.delete(self.all_dofs, prescribed_indexes)

    def get_matrices_dropping_indexes(self):
        return self.unprescribed_indexes, self.prescribed_indexes

    def get_all_degrees_of_freedom(self, element_2D, element_3D, active_2d_dofs):

        nodes_from_2d_elements = np.array([*set(self.model.mesh.faces_connectivity[:, 4:].flatten())], dtype=int)
        nodes_from_3d_elements = np.array([*set(self.model.mesh.solids_connectivity[:, 4:].flatten())], dtype=int)

        local_dofs_2d = np.arange(element_2D.DOFS_PER_NODE)
        local_dofs_3d = np.arange(element_3D.DOFS_PER_NODE)
        rotation_local_dofs_2d = local_dofs_2d[int(element_2D.DOFS_PER_NODE / 2):]

        dofs_from_2d_elements = element_2D.DOFS_PER_NODE * nodes_from_2d_elements.reshape(-1, 1) + local_dofs_2d
        dofs_from_3d_elements = element_3D.DOFS_PER_NODE * nodes_from_3d_elements.reshape(-1, 1) + local_dofs_3d
        rotation_dofs_from_2d_elements = element_2D.DOFS_PER_NODE * nodes_from_2d_elements.reshape(-1, 1) + rotation_local_dofs_2d

        self.dofs_from_2d_elements = dofs_from_2d_elements.flatten()
        self.dofs_from_3d_elements = dofs_from_3d_elements.flatten()
        self.rotation_dofs_from_2d_elements = rotation_dofs_from_2d_elements.flatten()

        print(f"dofs_from_2d_elements: {len(self.dofs_from_2d_elements)}")
        print(f"dofs_from_3d_elements: {len(self.dofs_from_3d_elements)}")
        print(f"rotation_dofs_from_2d_elements: {len(self.rotation_dofs_from_2d_elements)}")

        internal_dofs_from_3d_elements = np.array([])

        if len(active_2d_dofs):

            if len(nodes_from_3d_elements):
                shift = int((np.max(dofs_from_2d_elements) + 1) / 2)
                internal_nodes = np.delete(nodes_from_3d_elements, nodes_from_2d_elements)
                internal_dofs_from_3d_elements = element_3D.DOFS_PER_NODE * internal_nodes.reshape(-1, 1) + local_dofs_3d + shift
                internal_dofs_from_3d_elements = internal_dofs_from_3d_elements.flatten()

            total_dofs_apd = np.append(self.dofs_from_2d_elements, internal_dofs_from_3d_elements)
            all_dofs = np.array([*set(total_dofs_apd)], dtype=int)
            self.displacement_dofs = np.delete(all_dofs, self.rotation_dofs_from_2d_elements)
            print(f"total_dofs_apd: {len(total_dofs_apd)}")
            print(f"all_dofs: {len(all_dofs)}")
            print(f"displacement_dofs: {len(self.displacement_dofs)}")
            print(f"internal_dofs_from_3d_elements: {len(internal_dofs_from_3d_elements)}")
            return all_dofs

        else:

            print(">> passei aqui")

            self.displacement_dofs = self.dofs_from_3d_elements.copy()
            return self.dofs_from_3d_elements

    def process_face_elements_with_thickness(self, element_2D, element_3D):

        active_nodes_list = list()
        for key in self.model.properties.surface_properties.keys():
            property, surface_id = key
            if property == "surface_thickness":
                active_nodes_list.extend(self.model.mesh.nodes_from_surfaces[surface_id])

        active_dofs = np.array([])
        if active_nodes_list:
            shell_local_dofs = np.arange(element_2D.DOFS_PER_NODE)
            active_nodes = np.array([*set(active_nodes_list)], dtype=int)
            active_dofs = element_2D.DOFS_PER_NODE * active_nodes.reshape(-1, 1) + shell_local_dofs 
            active_dofs = np.sort(active_dofs.flatten())

        self.all_dofs = self.get_all_degrees_of_freedom(element_2D, element_3D, active_dofs)
        # print(f"nodes from surfaces: {nodes_from_surfaces}")

        return active_dofs, len(self.all_dofs)

    def get_data_to_process_global_matrices(self):
        """
        Calculates global matrices.
        """

        self.data_K = np.array([], dtype=float)
        self.data_M = np.array([], dtype=float)

        self.ind_cols = np.array([], dtype=int)
        self.ind_rows = np.array([], dtype=int)

        element_3D, element_2D = self.get_element()
        self.active_2d_element_dofs, self.n_dofs = self.process_face_elements_with_thickness(element_2D, element_3D)
        # total_dofs = element_2D.DOFS_PER_NODE * len(element_3D.nodal_coordinates)

        rows_se, cols_se = element_3D.generate_ind_rows_cols()
        self.ind_rows = np.append(self.ind_rows, rows_se)
        self.ind_cols = np.append(self.ind_cols, cols_se)

        dofs = element_3D.DOFS_PER_ELEMENT
        nel = len(element_3D.connectivity)
        # total_dofs = element_3D.DOFS_PER_NODE * len(element_3D.nodal_coordinates)

        data_K_se = np.zeros((nel, dofs, dofs), dtype=float)
        data_M_se = np.zeros((nel, dofs, dofs), dtype=float)

        # loop for solid elements
        for el_index, vol_id, *_ in self.model.mesh.solids_connectivity:

            material = self.model.properties._get_property("material", volume=vol_id)
            if material is None:
                continue

            Ke, Me = element_3D.elementary_matrices(el_index, material)
            data_K_se[el_index, :, :] = Ke
            data_M_se[el_index, :, :] = Me

        self.data_K = np.append(self.data_K, data_K_se.flatten())
        self.data_M = np.append(self.data_M, data_M_se.flatten())

        if len(self.active_2d_element_dofs):

            rows_fe, cols_fe = element_2D.generate_ind_rows_cols()

            dofs = element_2D.DOFS_PER_ELEMENT
            nel = len(element_2D.connectivity)

            self.ind_rows = np.append(self.ind_rows, rows_fe)
            self.ind_cols = np.append(self.ind_cols, cols_fe)
            # np.savetxt("indexes.dat", np.array([ind_rows, ind_cols], dtype=int).T, fmt="%i")

            data_K_fe = np.zeros((nel, dofs, dofs), dtype=float)
            data_M_fe = np.zeros((nel, dofs, dofs), dtype=float)

            # loop for face elements
            for el_index, surf_id, *_ in self.model.mesh.faces_connectivity:

                material = self.model.properties._get_property("material", surface=surf_id)
                if material is None:
                    continue

                surface_data = self.model.properties._get_property("surface_thickness", surface=surf_id)
                if surface_data is None:
                    continue

                t = surface_data["surface_thickness"]
 
                # s_data = self.model.mesh.face_element_thickness.get(el_index, None)
                # if s_data is None:
                #     continue

                # t = s_data.get("surface_thickness", None)
                # if t is None:
                #     continue

                Ke, Me = element_2D.elementary_matrices(el_index, material, t)

                data_K_fe[el_index, :, :] = Ke
                data_M_fe[el_index, :, :] = Me

            self.data_K = np.append(self.data_K, data_K_fe.flatten())
            self.data_M = np.append(self.data_M, data_M_fe.flatten())

    def assemble_global_matrices(self):

        _stiffness_matrix_full = csr_matrix((self.data_K, (self.ind_rows, self.ind_cols)), shape=(self.n_dofs, self.n_dofs))
        _mass_matrix_full = csr_matrix((self.data_M, (self.ind_rows, self.ind_cols)), shape=(self.n_dofs, self.n_dofs))

        self.process_indexes()

        if len(self.active_2d_element_dofs):
            self.unprescribed_shell_dofs = np.intersect1d(self.unprescribed_indexes, self.active_2d_element_dofs)
            self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_shell_dofs, :][:, self.unprescribed_shell_dofs]
            self.mass_matrix = _mass_matrix_full[self.unprescribed_shell_dofs, :][:, self.unprescribed_shell_dofs]

        else:

            # self.unprescribed_indexes = self.dofs_from_3d_elements
            self.mass_matrix = _mass_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
            self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
            
            if self.prescribed_indexes:
                self.mass_matrix = _mass_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
                self.stiffness_matrix = _stiffness_matrix_full[self.unprescribed_indexes, :][:, self.unprescribed_indexes]

            else:
                self.mass_matrix = _mass_matrix_full
                self.stiffness_matrix = _stiffness_matrix_full

    def process_assemble(self):

        self.update_number_of_frequencies()
        self.model.process_surface_thickness()

        logging.info( "Gathering data to assemble global matrices..." + ProgressStatus(10, 100))
        t0 = time()
        self.get_data_to_process_global_matrices()
        dt = time() - t0
        print(f"Elapsed time to process data to assemble global matrices: {round(dt, 4)} [s]")

        logging.info( "Assembling global matrices..." + ProgressStatus(50, 100))
        t0 = time()
        self.assemble_global_matrices()
        dt = time() - t0
        print(f"Elapsed time to assemble the global stiffness matrix: {round(dt, 4)} [s]")

        # A = self.get_structural_excitations_by_nodal_attribution()
        # B = self.get_structural_excitations_by_element_integration()
        # self.flow_mass_vectors = A + B
        #
        # indA = np.arange(0, len(A), 1)
        # indB = np.arange(0, len(B), 1)
        # np.savetxt("excitation_nodal.dat", np.array([indA, A[:,-1]]).T, delimiter=",")
        # np.savetxt("excitation_element.dat", np.array([indB, B[:,-1]]).T, delimiter=",")

# fmt: on