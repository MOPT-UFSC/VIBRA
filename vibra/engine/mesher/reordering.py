
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee as rcm

class Reordering:
    def __init__(self, mesh):
        self.mesh = mesh
        self.nodal_cordinates = self.mesh.nodal_coordinates
        self.solids_connectivity = self.mesh.solids_connectivity
        self.faces_connectivity = self.mesh.faces_connectivity


    def get_global_graph(self):
        if self.dim == 2:
            dict_elements = self.elements_2d
        elif self.dim == 3:
            dict_elements = self.elements_3d
        rows = []
        cols = []
        graph_data = []
        total = len(self.nodes)

        for element in dict_elements.values():
            indexes = element.nodes_indexes-1
            mat = element.graph_matrix
            # mat = np.ones((len(indexes), len(indexes)))
            aux = np.tile(indexes, (len(indexes),1))
            rows += list(aux.T.flatten())
            cols += list(aux.flatten())
            graph_data += list(mat.flatten())

        full_graph = csr_matrix((graph_data, (rows, cols)), shape=[total, total])
        return full_graph

    def get_global_graph(self):
        graph_data = []
        rows, cols = [], []
        for i, values in self.solids_connectivity:
            etype_tag = values[i, 2]
            mat, n_nodes = self.get_elementary_graph_info(etype_tag)
            indexes = values[i, 4 : 4 + n_nodes]
            aux = np.tile(indexes, (len(indexes),1))
            rows += list(aux.T.flatten())
            cols += list(aux.flatten())
            graph_data += list(mat.flatten())

        N_gl = self.nodal_cordinates.shape[0]
        full_graph = csr_matrix((graph_data, (rows, cols)), shape=[N_gl, N_gl])
        return full_graph

    def _define_reordering(self):
        graph = self.get_global_graph()
        self.map_nodes_indexes = {}
        self.perm = rcm(graph, symmetric_mode=True) + 1 # inicia no índice 1
        for vector in self.nodal_cordinates:
            node_id_gmsh = int(vector[0])
            self.map_nodes_indexes[self.perm[node_id_gmsh - 1]] = node_id_gmsh
            self.nodes[self.perm[node_id_gmsh - 1]].index = node_id_gmsh

    def get_elementary_graph_info(self, etype_tag):
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
        mat = np.ones([[1, 1, 1, 1],
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

    def mask_matrix_hex8_act(self):
        mat = np.array([[1, 1, 0, 1, 1, 0, 0, 0],
                        [1, 1, 1, 0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 0, 0, 1, 0],
                        [1, 0, 1, 1, 0, 0, 0, 1],
                        [1, 0, 0, 0, 1, 1, 0, 1],
                        [0, 1, 0, 0, 1, 1, 1, 0],
                        [0, 0, 1, 0, 0, 1, 1, 1],
                        [0, 0, 0, 1, 1, 0, 1, 1]], dtype=float)
        
    def mask_matrix_hex20_act(self):
        mat = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],                        
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=float)
        
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