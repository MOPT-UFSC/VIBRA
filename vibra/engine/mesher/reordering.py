
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee as rcm


class Reordering:

    def __init__(self, mesh):
        self.mesh = mesh
        self.nodal_coordinates = self.mesh.nodal_coordinates
        self.solids_connectivity = self.mesh.solids_connectivity
        self.faces_connectivity = self.mesh.faces_connectivity
        self.lines_connectivity = self.mesh.lines_connectivity

    def get_global_graph(self):
        graph_data = []
        rows, cols = [], []
        for i, values in enumerate(self.solids_connectivity):
            etype_tag = values[2]
            mat, n_nodes = self.get_elementary_graph_info(etype_tag)
            indexes = values[4 : 4 + n_nodes]
            aux = np.tile(indexes, (len(indexes), 1))
            rows += list(aux.T.flatten())
            cols += list(aux.flatten())
            graph_data += list(mat.flatten())

        N_gl = self.nodal_coordinates.shape[0]
        full_graph = csr_matrix((graph_data, (rows, cols)), shape=[N_gl, N_gl])
        return full_graph

    def _process_reordering(self):
        graph = self.get_global_graph()
        self.map_nodes_indexes = dict()
        self.nodal_coordinates_data = dict()
        self.perm = rcm(graph, symmetric_mode=True)# + 1 # inicia no índice 1
        for vector in self.nodal_coordinates:
            node_id_gmsh = int(vector[0])
            self.map_nodes_indexes[self.perm[node_id_gmsh]] = node_id_gmsh
            self.nodal_coordinates_data[self.perm[node_id_gmsh]] = vector[1:]

    def get_new_nodal_coordinates(self):
        """
        """
        _nodal_coordinates = np.zeros_like(self.nodal_coordinates, dtype=float)
        _nodal_coordinates[:, 0 ] = np.array(list(self.nodal_coordinates_data.keys()))
        _nodal_coordinates[:, 1:] = np.array(list(self.nodal_coordinates_data.values()))
        indexes = np.argsort(_nodal_coordinates[:, 0])
        _nodal_coordinates = _nodal_coordinates[indexes, :]
        return _nodal_coordinates

    def get_new_connectivity(self, connectivity_array):
        """
        """
        _solids_connectivity = np.zeros_like(connectivity_array, dtype=int)
        _solids_connectivity[:, 0] = np.arange(len(_solids_connectivity), dtype=int)
        _solids_connectivity[:, 1] = _solids_connectivity[:,1]
        _solids_connectivity[:, 2] = _solids_connectivity[:,2]
        _solids_connectivity[:, 3] = _solids_connectivity[:,3]
        for el, values in enumerate(connectivity_array):
            _solids_connectivity[el, 4:] = self.get_new_indexes_nodes_for_vector(values[4:])
        return _solids_connectivity

    def get_new_indexes_nodes_for_vector(self, indexes):
        """ This method returns ...
        """
        vect_nodes = np.zeros_like(indexes, dtype=int)
        for i, index in enumerate(indexes):
            vect_nodes[i] = self.map_nodes_indexes[index]
        return vect_nodes

    def get_new_indexes_nodes_for_matrix(self, mat_indexes):
        """ This method returns ...
        """
        mat_nodes = np.zeros_like(mat_indexes, dtype=int)
        for i, vector in enumerate(mat_indexes):
            mat_nodes[i, :] = self.get_new_indexes_nodes_for_vector(vector)
        return mat_nodes

    def updates_nodes_from(self, data):
        """ This method returns ...
        """
        aux_dict = dict()
        if not isinstance(data, dict):
            return aux_dict
        for key, data in data.items():
            if isinstance(data, dict):
                temp = dict()
                if "element_indexes" in data.keys():
                    temp["element_indexes"] = data["element_indexes"]  
                if "connectivity" in data.keys():
                    temp["connectivity"] = self.get_new_indexes_nodes_for_matrix(data["connectivity"])
                aux_dict[key] = temp
            else:
                aux_dict[key] = self.get_new_indexes_nodes_for_vector(data)
        return aux_dict


    def get_elementary_graph_info(self, etype_tag):
        """ This method returns the elemetary mask matrix 
            and the number of nodes per element.
            
            Parameters:
            ----------
            etype_tag: int value corresponding to gmsh elm_type.
            
            Returns:
            ---------
            mask_matrix: np.ndarray elementary mask matrix
            nodes_per_element: int value equals to the number of nodes per element.
        """
        if etype_tag == 4: # tetrahedron-4
            return self.mask_matrix_tet4_act(), 4
        elif etype_tag == 11: # tetrahedron-10
            return self.mask_matrix_tet10_act(), 10
        elif etype_tag == 5: # hexahedron-8
            return self.mask_matrix_hex8_act(), 8
        elif etype_tag == 17: # hexahedron-20
            return self.mask_matrix_hex20_act(), 20
        else:
            print(f"Not implemented element: {etype_tag}")
            return None

    def mask_matrix_tet4_act(self):
        mat = np.array([[1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1]], dtype=float)
        return mat

    def mask_matrix_tet10_act(self):
        mat = np.array([[1, 0, 0, 0, 1, 0, 1, 1, 0, 0],
                        [0, 1, 0, 0, 1, 1, 0, 0, 0, 1],
                        [0, 0, 1, 0, 0, 1, 1, 0, 1, 0],
                        [0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
                        [1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
                        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                        [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                        [0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
                        [0, 1, 0, 1, 0, 0, 0, 0, 0, 1]], dtype=float)
        return mat

    def mask_matrix_hex8_act(self):
        mat = np.array([[1, 1, 0, 1, 1, 0, 0, 0],
                        [1, 1, 1, 0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 0, 0, 1, 0],
                        [1, 0, 1, 1, 0, 0, 0, 1],
                        [1, 0, 0, 0, 1, 1, 0, 1],
                        [0, 1, 0, 0, 1, 1, 1, 0],
                        [0, 0, 1, 0, 0, 1, 1, 1],
                        [0, 0, 0, 1, 1, 0, 1, 1]], dtype=float)
        return mat
        
    def mask_matrix_hex20_act(self):
        mat = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
                        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],                        
                        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]], dtype=float)
        return mat
        
# The GMSH Nodes ordering information are available at  https://gmsh.info/doc/texinfo/gmsh.html#Node-ordering

"""

1 -> 2-node line.

2 -> 3-node triangle.

3 -> 4-node quadrangle.

4 -> 4-node tetrahedron.

5 -> 8-node hexahedron.

6 -> 6-node prism.

7 -> 5-node pyramid.

8 -> 3-node second order line (2 nodes associated with the vertices and 1 with the edge).

9 -> 6-node second order triangle (3 nodes associated with the vertices and 3 with the edges).

10 -> 9-node second order quadrangle (4 nodes associated with the vertices, 4 with the edges and 1 with the face).

11 -> 10-node second order tetrahedron (4 nodes associated with the vertices and 6 with the edges).

12 -> 27-node second order hexahedron (8 nodes associated with the vertices, 12 with the edges, 6 with the faces and 1 with the volume).

13 -> 18-node second order prism (6 nodes associated with the vertices, 9 with the edges and 3 with the quadrangular faces).

14 -> 14-node second order pyramid (5 nodes associated with the vertices, 8 with the edges and 1 with the quadrangular face).

15 -> 1-node point.

16 -> 8-node second order quadrangle (4 nodes associated with the vertices and 4 with the edges).

17 -> 20-node second order hexahedron (8 nodes associated with the vertices and 12 with the edges).

18 -> 15-node second order prism (6 nodes associated with the vertices and 9 with the edges).

19 -> 13-node second order pyramid (5 nodes associated with the vertices and 8 with the edges).

20 -> 9-node third order incomplete triangle (3 nodes associated with the vertices, 6 with the edges)

21 -> 10-node third order triangle (3 nodes associated with the vertices, 6 with the edges, 1 with the face)

22 -> 12-node fourth order incomplete triangle (3 nodes associated with the vertices, 9 with the edges)

23 -> 15-node fourth order triangle (3 nodes associated with the vertices, 9 with the edges, 3 with the face)

24 -> 15-node fifth order incomplete triangle (3 nodes associated with the vertices, 12 with the edges)

25 -> 21-node fifth order complete triangle (3 nodes associated with the vertices, 12 with the edges, 6 with the face)

26 -> 4-node third order edge (2 nodes associated with the vertices, 2 internal to the edge)

27 -> 5-node fourth order edge (2 nodes associated with the vertices, 3 internal to the edge)

28 -> 6-node fifth order edge (2 nodes associated with the vertices, 4 internal to the edge)

29 -> 20-node third order tetrahedron (4 nodes associated with the vertices, 12 with the edges, 4 with the faces)

30 -> 35-node fourth order tetrahedron (4 nodes associated with the vertices, 18 with the edges, 12 with the faces, 1 in the volume)

31 -> 56-node fifth order tetrahedron (4 nodes associated with the vertices, 24 with the edges, 24 with the faces, 4 in the volume)

92 -> 64-node third order hexahedron (8 nodes associated with the vertices, 24 with the edges, 24 with the faces, 8 in the volume)

93 -> 125-node fourth order hexahedron (8 nodes associated with the vertices, 36 with the edges, 54 with the faces, 27 in the volume)

"""

    # # TODO: TOP REDUCT CODE - remove before validation
    # def get_global_graph(self):
    #     if self.dim == 2:
    #         dict_elements = self.elements_2d
    #     elif self.dim == 3:
    #         dict_elements = self.elements_3d
    #     rows = []
    #     cols = []
    #     graph_data = []
    #     total = len(self.nodes)

    #     for element in dict_elements.values():
    #         indexes = element.nodes_indexes-1
    #         mat = element.graph_matrix
    #         # mat = np.ones((len(indexes), len(indexes)))
    #         aux = np.tile(indexes, (len(indexes),1))
    #         rows += list(aux.T.flatten())
    #         cols += list(aux.flatten())
    #         graph_data += list(mat.flatten())

    #     full_graph = csr_matrix((graph_data, (rows, cols)), shape=[total, total])
    #     return full_graph