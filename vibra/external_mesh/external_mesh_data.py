import os
import numpy as np
from collections import defaultdict
from pathlib import Path

class ExternalMeshData():
    def __init__(self):
        self.reset()

    def reset(self):

        self.modo = None
        self.type = None
        self.named_selection = None
        self.skip_format_row = False

        self.nodal_coordinates = list()

        self.connectivity = defaultdict(list)
        self.nodes_from_named_selection = defaultdict(list)

        self.file_path = ""
        self.folder_name = "exported_mesh_files"

    def set_named_selections(self, named_selections):
        self.named_selections = named_selections

    def read_file(self, path):

        if isinstance(path, str):
            path = Path(path)

        self.file_path = path
        with open(self.file_path, 'r') as self.file:
            self.lines = self.file.readlines()

    def decode_mesh_data_from_file(self):

        for row, line in enumerate(self.lines[0: ]):

            if not line:
                continue

            if "NUMOFF,NODE," in line:
                line = line.replace(" ", "")
                number_nodes = int(line.split("NUMOFF,NODE,")[1])
                nodal_coordinates = np.zeros((number_nodes, 4), dtype=float)
                continue

            if "NUMOFF,ELEM," in line:
                line = line.replace(" ", "")
                number_elements = int(line.split("NUMOFF,ELEM,")[1])
                # nodal_coordinates = np.zeros((number_elements, 4), dtype=float)
                continue

            if "NBLOCK" in line or "nblock" in line:
                self.skip_format_row = True
                self.modo = "coordinates"
                continue

            elif "EBLOCK" in line or "eblock" in line:
                self.skip_format_row = True
                self.modo = "connectivity"
                continue
            
            elif "CMBLOCK" in line or "cmblock" in line:

                if self.modo is None:
                    if self.nodal_coordinates and self.connectivity:
                        for named_selection in self.named_selections:
                            if named_selection.upper() in line:
                                self.named_selection = named_selection
                                self.modo = "named_selection"
                                self.skip_format_row = True
                                break
                        continue

            if self.modo == "coordinates":
                
                if self.skip_format_row:
                    self.skip_format_row = False
                    start_col, spacing_cols = self.get_coordinates_format_info(line)
                    # print(f"coordinates: {start_col}, {spacing_cols}")
                    continue

                try:

                    size = len(line)
                    N_int = int((size-start_col)/(spacing_cols))

                    coordinates = list()
                    coordinates.append(int(line[:start_col]))
                    for j in range(N_int):
                        start = start_col + j*spacing_cols
                        end = start + spacing_cols
                        coordinates.append(float(line[start:end]))

                    if len(coordinates) == 4:
                        self.nodal_coordinates.append(coordinates)
                    
                    # nodal_coordinates[n_row, 0] = int(line[:int(start_col/3)])
                    # for j in range(N_int):
                    #     start = start_col + j*spacing_cols
                    #     end = start + spacing_cols
                    #     nodal_coordinates[n_row, j+1] = float(line[start:end])

                    # self.nodal_coordinates.append(nodal_coordinates[n_row, :])
                    # n_row += 1

                except:
                    self.modo = None
                    pass

            
            elif self.modo == "connectivity":
                
                if self.skip_format_row:
                    self.skip_format_row = False
                    number_of_cols, spacing_cols = self.get_connectivity_format_info(line)
                    # print(f"connectivity: {number_of_cols}, {spacing_cols}")
                    continue

                try:
                    
                    connect_data = [int(valor) for valor in line.split()]

                    if connect_data:

                        if len(connect_data) >= number_of_cols - 4:
                            body_id = connect_data[1]
                            element_id = connect_data[10]
                            _connect_data = self.filter_collapsed_nodes(connect_data[11:])
                            nodes_per_element = len(_connect_data)
                            # print(body_id, nodes_per_element)

                        else:
                            _connect_data = connect_data

                        if nodes_per_element == 4:
                            if len(connect_data) == number_of_cols:
                                _connect_data.insert(0, element_id)
                                _connect_data.insert(1, body_id)
                                _connect_data.insert(2, nodes_per_element)
                                # print(f"solid285 - tet4: {_connect_data}")
                                self.connectivity[body_id, "solid285_tet4"].append(_connect_data)
                        
                        elif nodes_per_element == 8:
                            if len(connect_data) == number_of_cols:
                                _connect_data.insert(0, element_id)
                                _connect_data.insert(1, body_id)
                                _connect_data.insert(2, nodes_per_element)
                                # print(f"solid185 - hex8: {_connect_data}")
                                self.connectivity[body_id, "solid185_hex8"].append(_connect_data)
                        
                        elif nodes_per_element == 10:
                            if len(connect_data) == number_of_cols:
                                cache_nodes = _connect_data
                            else:

                                if cache_nodes:
                                    for node_id in _connect_data:
                                        cache_nodes.append(node_id)

                                    cache_nodes.insert(0, element_id)
                                    cache_nodes.insert(1, body_id)
                                    cache_nodes.insert(2, nodes_per_element)
                                    # print(f"solid187 - tet10: {cache_nodes}")
                                    self.connectivity[body_id, "solid187_tet10"].append(cache_nodes)    
                                    cache_nodes = list()
                        
                        elif nodes_per_element == 20:
                            if len(connect_data) == number_of_cols:
                                cache_nodes = _connect_data
                            else:

                                if cache_nodes:
                                    for node_id in _connect_data:
                                        cache_nodes.append(node_id)

                                    cache_nodes.insert(0, element_id)
                                    cache_nodes.insert(1, body_id)
                                    cache_nodes.insert(2, nodes_per_element)
                                    # print(f"solid186 - hex20: {cache_nodes}")
                                    self.connectivity[body_id, "solid186_hex20"].append(cache_nodes)
                                    cache_nodes = list()
                        else:
                            continue

                except:
                    self.modo = None
                    pass   

            elif self.modo == "named_selection":

                if self.skip_format_row:
                    self.skip_format_row = False
                    number_of_cols, spacing_cols = self.get_named_selection_format_info(line)
                    # print(f"named selection: {number_of_cols}, {spacing_cols}")
                    continue

                try:
                    for ns_node_id in [int(valor) for valor in line.split()]:
                        self.nodes_from_named_selection[self.named_selection].append(ns_node_id)
                    
                except:

                    self.modo = None
        
        self.process_array_coordinates()
        self.post_process_connectivities()
        self.process_named_selection_elements(export=True)

    def get_named_selection_format_info(self, line):
        str_format = line[1:-2].split(",")
        num_cols = int(str_format[0].split("i")[0])
        space_cols = int(str_format[0].split("i")[1])
        return num_cols, space_cols

    def filter_collapsed_nodes(self, input_nodes):
        connectivity = list()
        for node_id in input_nodes:
            if node_id not in connectivity:
                connectivity.append(node_id)
        return connectivity

    def get_coordinates_format_info(self, line):
        str_format = line[1:-2].split(",")
        num_cols = int(str_format[0].split("i")[0])
        space_cols = int(str_format[0].split("i")[1])
        start_col = num_cols*space_cols
        fmt_coords = str_format[1].split("e")[1]
        spacing_cols = int(fmt_coords.split(".")[0])
        return start_col, spacing_cols

    def get_connectivity_format_info(self, line):
        str_format = line[1:-2].split("i")
        number_of_cols = int(str_format[0])
        spacing_cols = int(str_format[1])
        return number_of_cols, spacing_cols

    def post_process_connectivities(self):
        self.connectivity_arrays = dict()
        for key, data in self.connectivity.items():
            self.connectivity_arrays[key] = np.array(data, dtype=int)

    def export_nodal_coordinates(self):
        self.create_output_data_folder()
        if self.nodal_coordinates:
            header = "Node ID || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
            filename = f"{self.folder_name}/nodal_coordinates.dat"
            data = np.array(self.nodal_coordinates)
            np.savetxt(filename, data, delimiter=",", header=header)#, fmt="%i %18.12e %18.12e %18.12e")

    def export_connectivities(self):
        self.create_output_data_folder()
        if self.connectivity_arrays:
            header = "Element ID || Nodes"
            for key, data in self.connectivity_arrays.items():
                # filename = f"{self.folder_name}/connectivity_matrix_{key}.dat"
                filename = f"{self.folder_name}/connectivity_matrix.dat"
                np.savetxt(filename, data, header=header, fmt="%i", delimiter=",")

    def process_named_selection_elements(self, export=False):

        start, end = 0, 0
        self.elements_from_named_selection = dict()

        for key, data in self.connectivity.items():
            connect = np.array(data, dtype=int)
            for ns_key, ns_nodes in self.nodes_from_named_selection.items():
 
                other_nodes = list()
                face_connectivity = list()

                filt_1 = 0
                for ns_node in ns_nodes:
                    filt_1 += np.sum((connect[:, 3:] == ns_node), axis=1)

                mask = filt_1 == 3

                if np.sum(mask):

                    for _nodes in connect[mask, 3:]:

                        face_elements = list()
                        for _node in _nodes:
                            if _node in ns_nodes:
                                face_elements.append(_node)
                            else:
                                other_nodes.append(_node)

                        # verifies if the surface normals are pointed out to the
                        # outside of the solid element and revert it otherwise

                        if len(face_elements) == 3: # tet4/face3 elements
                            
                            normal_vector = self.get_element_face_normal(face_elements)
                            edge_vector = self.get_edge_vector(face_elements, other_nodes[-1])

                            if np.dot(normal_vector, edge_vector) > 0:
                                node_2 = face_elements[1]
                                face_elements.remove(node_2)
                                face_elements.append(node_2)
                                normal_vector *= -1

                            # TODO: implement same structure to other element types
                            # print("processed data: ", ns_key, normal_vector, face_elements, other_nodes)

                        face_connectivity.append(face_elements)

                if face_connectivity:

                    end += len(face_connectivity)
                    indexes = np.arange(1+start, end+1)
                    start = end

                    connect_data = np.array(face_connectivity, dtype=int)
                    other_data = np.array(other_nodes, dtype=int)

                    self.elements_from_named_selection[ns_key] = {  "element_indexes" : indexes,
                                                                       "connectivity" : connect_data,
                                                                        "outer_nodes" : other_data  }

                    if export:

                        rows, cols = connect_data.shape
                        exp_data = np.zeros((rows,cols+2), dtype=int)
                        exp_data[:, 0] = indexes
                        exp_data[:, 1:-1] = connect_data
                        exp_data[:, -1] = other_data

                        self.create_output_data_folder()

                        header = "Surface element ID || Nodes"
                        filename = f"{self.folder_name}/elements_from_{ns_key}.dat"
                        np.savetxt(filename, exp_data, header=header, fmt="%i", delimiter=",")

    def export_named_selection_nodes(self, folder_path : str):

        for ns_key, ns_nodes in self.nodes_from_named_selection.items():

            indexes = np.arange(1, len(ns_nodes) + 1)
            data = np.array([indexes, ns_nodes], dtype=int).T

            header = "Surface element ID || Nodes"
            filename = f"{folder_path}/nodes_from_{ns_key}.dat"
            np.savetxt(filename, data, header=header, fmt="%i", delimiter=",")

    def process_named_selection_data(self, export=False):
        self.process_named_selection_elements(export=export)

    def create_output_data_folder(self):
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
    
    def process_array_coordinates(self, index_zero=True):

        data = np.array(self.nodal_coordinates)

        rows, cols = data.shape

        indexes = data[:,0]
        if index_zero:
            indexes -= 1

        self.array_nodal_coordinates = np.zeros((rows, cols), dtype=float)
        self.array_nodal_coordinates[ :, 0 ] = indexes
        self.array_nodal_coordinates[ :, 1:] = data[:, 1:]

    def get_element_face_normal(self, connect):
        
        # ie = self.faces_connectivity[element_id, 4:]

        connect = np.array(connect) - 1
        coords = self.array_nodal_coordinates[connect, 1:]

        P1 = coords[0, :]
        P2 = coords[1, :]
        P3 = coords[2, :]

        P2P1 = np.array(P2 - P1)
        P3P1 = np.array(P3 - P1)

        cross = np.cross(P2P1, P3P1)
        normal = cross / np.linalg.norm(cross)

        return normal
    
    def get_edge_vector(self, connect, outer_node):

        connect = np.array(connect) - 1

        P1 = self.array_nodal_coordinates[connect[0], 1:]
        P4 = self.array_nodal_coordinates[outer_node-1, 1:]

        P4P1 = np.array(P4 - P1)

        return P4P1 / np.linalg.norm(P4P1)
