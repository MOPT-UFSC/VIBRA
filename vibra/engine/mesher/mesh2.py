import gmsh
import sys
import os
import numpy as np
from collections import OrderedDict


class Mesher:

    def __init__(self) -> None:
        self.reset_variables()

        
    def reset_variables(self):
        self.node_coords = OrderedDict()
        self.nodal_coordinates = None
        self.segments = list()
        self.face_data = {}
        self.solid_data = {}
        self.faces_connectivity_array = None
        self.solids_connectivity_array = None
        self.faces_connectivity = {}
        self.solids_connectivity = {}
        self.export_data = False
        self.element_size = 2000
        self.number_of_threads = 4
        self.element_keys = [5, 1, 0, 0, 0, 0, 1]
        self.path = ""
        self.basename = ""


    def set_element_size(self, element_size):
        self.element_size = element_size


    def set_number_of_threads_in_mesh_processing(self, number_of_threads):
        self.number_of_threads = number_of_threads

    def set_export_data_state(self, _bool):
        self.export_data = _bool


    def clear(self):
        self.node_coords.clear()


    def add_node_coords(self, i, x, y, z):
        self.node_coords[i] = [x, y, z]

    
    def get_element_keys(self, element_type):
        """
        """
        element_info = {"tetrahedron-4"  : [ 5, 1, 0, 0, 0, 0, 1],
                        "tetrahedron-10" : [ 5, 1, 0, 0, 0, 0, 2],
                        "hexahedron-8"   : [11, 1, 1, 3, 2, 0, 1],
                        "hexahedron-20"  : [11, 1, 1, 3, 2, 1, 2]}
        
        if element_type in element_info.keys():
            self.element_keys = element_info[element_type]
        else:
            print(f"The entered element label '{element_type}' is not valid. The tetrahedron-4 element setup will be adopted as default.")
            self.element_keys = [5, 1, 0, 0, 0, 0, 1]
    

    def initialize_GMSH_and_load_CAD_file(self, path):
        """
        """        
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", self.number_of_threads)
        gmsh.merge(path)
        #
        self.path = path
        self.basename = os.path.basename(path)


    def configure_mesh(self, element_label):
        """
        """
        if self.element_size > 0:
            gmsh.option.setNumber("Mesh.MeshSizeMin", self.element_size)
            gmsh.option.setNumber("Mesh.MeshSizeMax", self.element_size)
        else:
            gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.5)
        
        gmsh.option.setNumber("Geometry.Tolerance", 1e-6)

        self.get_element_keys(element_label)

        if "script" not in self.basename:
            gmsh.option.setNumber("Mesh.Algorithm", self.element_keys[0])
            gmsh.option.setNumber("Mesh.Algorithm3D", self.element_keys[1])
            gmsh.option.setNumber("Mesh.RecombineAll", self.element_keys[2])
            gmsh.option.setNumber("Mesh.RecombinationAlgorithm", self.element_keys[3])
            gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", self.element_keys[4])

        # gmsh.option.setNumber("Mesh.RecombineAll", 1)
        gmsh.option.setNumber('Mesh.SecondOrderIncomplete', self.element_keys[5])
        
        if self.element_keys[6] in [1, 2, 3]:
            gmsh.option.setNumber("Mesh.ElementOrder", self.element_keys[6])
        else:
            return
    

    def process_mesh(self, GMSH_GUI=False):
        """
        """
        self.connectivity_dim2 = {}
        self.connectivity_dim3 = {}
        gmsh.model.mesh.generate(dim=3)
        indexes, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
        
        for i, (x, y, z) in zip(indexes, split_sequence(coords, 3)):
            self.add_node_coords(i, x / 1000, y / 1000, z / 1000)

        self.get_nodal_coordinates()
        
        for dim, tag in gmsh.model.getEntities():

            _elements_data = {}
            
            element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(dim, tag)

            # number_elements = len(element_indexes[0])
            # mask = np.argsort(element_indexes[0])

            if not element_indexes:
                continue

            for i, element_type in enumerate(element_types):

                _, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(element_type)

                array_element_nodes = np.array(element_nodes[i]).reshape(-1, nodes_per_element)    

                _elements_data[element_type] = {    "indexes"             : element_indexes[i],
                                                    "array_element_nodes" : array_element_nodes,
                                                    "element_to_nodes"    : dict(zip(element_indexes[i], array_element_nodes))    } 

            if dim == 2: #Surfaces
                self.connectivity_dim2[tag] = _elements_data
                
            elif dim == 3: #Solids
                self.connectivity_dim3[tag] = _elements_data

        if GMSH_GUI:
            if '-nopopup' not in sys.argv:
                gmsh.fltk.run()

        gmsh.finalize()
    

    def get_nodal_coordinates(self):
        """
        """
        indexes = np.array(list(self.node_coords.keys()))
        coords = np.array(list(self.node_coords.values()), dtype=float)
        mask = np.argsort(indexes)
        nodal_coordinates = np.zeros((len(indexes), 4))
        nodal_coordinates[:,0] = indexes[mask]
        nodal_coordinates[:,1:] = coords[mask]
        self.nodal_coordinates = nodal_coordinates
        if self.export_data:
            try:
                header = "Node index || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
                np.savetxt("output_data\\nodal_coordinates.dat", nodal_coordinates, delimiter=";", header=header, fmt=["%i", "%.16f", "%.16f", "%.16f"])
            except Exception as error_log:
                print(str(error_log))
        return indexes, coords
    

    def process_connectivities(self):
        """
        """

        self.process_faces_connectivity(self.connectivity_dim2)
        self.process_solids_connectivity(self.connectivity_dim3)

        # os dados de connectividade dos elementos de superfície estão dispostos em colunas na forma: 
        # Index || Element index ||Face ID || Element type ID || Node IDS
        # array: self.faces_connectivity_array
        # dictionary: self.faces_connectivity (as chaves são os índices dos elementos e os valores são a conectividade)

        # os dados de connectividade dos elementos sólidos estão dispostos em colunas na forma: 
        # Index || Element index || Solid ID || Element type ID || Node IDS
        # array: self.solids_connectivity_array
        # dictionary: self.solids_connectivity (as chaves são os índices dos elementos e os valores são a conectividade)

        self.connectivity_matrix = self.solids_connectivity_array#[:, [0, 4, 5, 6, 7]] #tet4
        #connect = self.mesh.solids_connectivity_array[:, [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]] #tet10
        self.number_of_nodes = len(self.nodal_coordinates)
        self.number_of_elements = len(self.connectivity_matrix)


    def process_faces_connectivity(self, data):
        """
        """
        self.face_data = data
        self.faces_connectivity_array, self.faces_connectivity = get_connectivity_data(data)
        if self.export_data:
            try:
                header = "Index || Element ID || Face ID || Element type ID || Connected Node IDs"
                export_data(self.faces_connectivity_array, "output_data\\faces_connectivity.dat", header)
            except Exception as error_log:
                print(str(error_log))


    def process_solids_connectivity(self, data):
        """
        """
        self.solid_data = data
        self.solids_connectivity_array, self.solids_connectivity = get_connectivity_data(data)
        if self.export_data:
            try:
                header = "Index || Solid ID || Element type ID || Element ID || Connected Node IDs"
                export_data(self.solids_connectivity_array, "output_data\\solids_connectivity.dat", header)
            except Exception as error_log:
                print(str(error_log))
    
    
def get_connectivity_data(input_data):
    """
    """
    if isinstance(input_data, dict):

        max_cols = 0
        N_list = []
        for data_0 in input_data.values():
            for data_1 in data_0.values():
                if "indexes" in data_1.keys():
                    N_list.append(len(data_1["indexes"]))
                    array_nodes = data_1["array_element_nodes"]
                    if max_cols < array_nodes.shape[1]:
                        max_cols = array_nodes.shape[1]
        N = np.sum(N_list)
        output_data = np.zeros((N, max_cols+4), dtype=int)

        start, end, ind = 0, 0, 0
        for entity_tag, e_data in input_data.items():
            for etype_tag, data in e_data.items():
            
                end += N_list[ind]
                indexes = data["indexes"]
                nodes = data["array_element_nodes"]
                rows = len(indexes)
                cols = nodes.shape[1]
                
                output_data[start:end, 1       ] = np.ones(rows)*entity_tag
                output_data[start:end, 2       ] = np.ones(rows)*etype_tag
                output_data[start:end, 3       ] = indexes     
                output_data[start:end, 4:4+cols] = nodes
                start = end
                ind += 1

        output_data[:, 0] = np.arange(1, N+1, 1)
        connect_data = dict(zip(output_data[:, 1], list(output_data[:, 4:])))

        return output_data, connect_data
    return False, False


def export_data(connect_data, filename, header):
    """
    """
    # connect_data, _ = get_connectivity_data(input_data)
    if isinstance(connect_data, np.ndarray):
        np.savetxt(filename, connect_data, delimiter=";", header=header, fmt="%i")


def split_sequence(sequence, size):
    """
    """
    for start in range(0, len(sequence), size):
        end = start + size
        yield sequence[start:end]


if __name__ == "__main__":
    
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Paralelepipedo.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Tetraedro.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Cubo_1m3.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Cilindro.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\script_files\\script_hex_elements.txt"

    path = "/home/andre/Documentos/VibraEngine/examples/geometry_files/Tetraedro.STEP"

    if not os.path.exists(path):
        raise FileNotFoundError
        
    mesher = Mesher()
    mesher.set_element_size(1000)
    mesher.initialize_GMSH_and_load_CAD_file(path)
    mesher.configure_mesh("tetrahedron-4")
    mesher.process_mesh(GMSH_GUI=True)
    mesher.set_export_data_state(True)
    mesher.get_nodal_coordinates()
    mesher.process_connectivities()