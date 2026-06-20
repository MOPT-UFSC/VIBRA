
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee as rcm

# fmt: off

class Reordering:

    def __init__(self, mesh):
        self.mesh = mesh
        self.nodal_coordinates = self.mesh.nodal_coordinates
        self.solids_connectivity = self.mesh.solids_connectivity
        self.initialize()

    def initialize(self):

        self.nodes_by_element_type = {  1  :  2,     # Line2 
                                        2  :  3,     # Tria3
                                        3  :  4,     # Quad4
                                        4  :  4,     # Tet4
                                        5  :  8,     # Hex8
                                        8  :  3,     # Line3
                                        9  :  6,     # Tria6
                                        11  : 10,    # Tet10
                                        17  : 20  }  # Hex20

        self.mask_tet4 = np.array([ [1, 1, 1, 1],
                                    [1, 1, 1, 1],
                                    [1, 1, 1, 1],
                                    [1, 1, 1, 1] ], dtype=float).flatten()
                
        self.mask_tet10 = np.array([[1, 0, 0, 0, 1, 0, 1, 1, 0, 0],
                                    [0, 1, 0, 0, 1, 1, 0, 0, 0, 1],
                                    [0, 0, 1, 0, 0, 1, 1, 0, 1, 0],
                                    [0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
                                    [1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
                                    [0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
                                    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                                    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                                    [0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
                                    [0, 1, 0, 1, 0, 0, 0, 0, 0, 1] ], dtype=float).flatten()

        self.mask_hex8 = np.array([ [1, 1, 0, 1, 1, 0, 0, 0],
                                    [1, 1, 1, 0, 0, 1, 0, 0],
                                    [0, 1, 1, 1, 0, 0, 1, 0],
                                    [1, 0, 1, 1, 0, 0, 0, 1],
                                    [1, 0, 0, 0, 1, 1, 0, 1],
                                    [0, 1, 0, 0, 1, 1, 1, 0],
                                    [0, 0, 1, 0, 0, 1, 1, 1],
                                    [0, 0, 0, 1, 1, 0, 1, 1] ], dtype=float).flatten()

        self.mask_hex20 = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
                                    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]], dtype=float).flatten()

    def get_global_graph(self):
        """
        """
        Nt = np.sum(self.solids_connectivity[:, 3]**2)
        rows = np.zeros(Nt, dtype=int)
        cols = np.zeros(Nt, dtype=int)
        graph_data = np.zeros(Nt, dtype=float)
        #
        start = 0
        end = 0
        for i, values in enumerate(self.solids_connectivity):
            n_nodes = self.nodes_by_element_type[values[2]]
            mat = self.get_elementary_graph_info(values[2])
            indexes = values[4 : 4 + n_nodes]
            end += len(mat)
            aux = np.tile(indexes, (len(indexes), 1))
            rows[start:end] = aux.T.flatten()
            cols[start:end] = aux.flatten()
            graph_data[start:end] = mat
            start = end
        #    
        N_gl = self.nodal_coordinates.shape[0]
        full_graph = csr_matrix((graph_data, (rows, cols)), shape=[N_gl, N_gl])
        #
        return full_graph

    def _process_reordering(self):
        """
        """
        self.map_nodes_indexes = dict()
        graph = self.get_global_graph()
        # self.plot_graph(graph)
        perm_rcm = rcm(graph, symmetric_mode=True)
        indexes = (self.nodal_coordinates[:, 0]).astype(int)
        self.perm = self.sp_permute_vector(indexes.reshape(-1, 1), perm_rcm).flatten()
        self.map_nodes_indexes = dict(zip(indexes, self.perm))

        # for node_id_gmsh in indexes:
        #     self.map_nodes_indexes[node_id_gmsh] = self.perm[node_id_gmsh]

        # # saving data
        # gmsh_id = self.nodal_coordinates[:, 0]
        # data = np.array([gmsh_id, perm_rcm], dtype=int).T
        # data2 = np.array([gmsh_id, self.perm], dtype=int).T
        # np.savetxt("dicionario_permutador_reord.dat", data, delimiter=",", fmt="%i")
        # np.savetxt("dicionario_permutador_reord_new.dat", data2, delimiter=",", fmt="%i")

    def get_new_nodal_coordinates(self):
        """
        """
        indexes = np.argsort(self.perm)
        self.nodal_coordinates[:, 1:] = self.nodal_coordinates[indexes, 1:]
        return self.nodal_coordinates

    def get_new_connectivity(self, connectivity_array):
        """
        """
        _connectivity = connectivity_array.copy()
        for el, values in enumerate(connectivity_array):
            n_nodes = self.nodes_by_element_type[values[2]]
            _connectivity[el, 4 : 4 + n_nodes] = self.get_new_indexes_nodes_for_vector(values[4 : 4 + n_nodes])
        return _connectivity

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

    def updates_nodes_from(self, input_data):
        """ This method returns ...
        """
        aux_dict = dict()
        if not isinstance(input_data, dict):
            return aux_dict
        for key, data in input_data.items():
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
        """ This method returns the elemetary mask matrix.
            
            Parameters:
            ----------
            etype_tag: int value corresponding to gmsh elm_type.
            
            Returns:
            ---------
            mask_matrix: np.ndarray elementary mask matrix

        """
        if etype_tag == 4: # tetrahedron-4
            return self.mask_tet4
        elif etype_tag == 11: # tetrahedron-10
            return self.mask_tet10
        elif etype_tag == 5: # hexahedron-8
            return self.mask_hex8
        elif etype_tag == 17: # hexahedron-20
            return self.mask_hex20
        else:
            print(f"Not implemented element: {etype_tag}")
            return None

    def plot_graph(self, graph):
        import matplotlib.pyplot as plt
        plt.ion()
        plt.cla()
        plt.spy(graph, color=(0.25,0.25,0.25))
        plt.show()

    def sp_permute_matrix(self, A, perm_r, perm_c):
        """ permute rows and columns of A """
        M, N = A.shape
        # row permumation matrix
        Pr = coo_matrix((np.ones(M), (np.arange(M), perm_r))).tocsr()
        # column permutation matrix
        Pc = coo_matrix((np.ones(N), (perm_c, np.arange(N)))).tocsr()
        return Pc.T * A * Pr.T

    def sp_permute_vector(self, A, perm_r):
        """ permute rows and columns of A """
        M, N = A.shape
        # row permumation matrix
        Pr = coo_matrix((np.ones(M), (np.arange(M), perm_r))).tocsr()
        return Pr.T * A

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

# fmt: on