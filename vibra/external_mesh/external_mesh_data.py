import os
from collections import defaultdict
from pathlib import Path

import numpy as np


class ExternalMeshData():
    def __init__(self):

        self.file_path = ""
        self.folder_name = "exported_mesh_files"

        self.modo = None
        self.type = None
        self.named_selection = None
        self.skip_format_row = False

        self.nodal_coordinates = list()
        self.faces_connectivities = dict()
        self.solids_connectivities = dict()

        self.connectivity = defaultdict(list)
        self.nodes_from_named_selection = defaultdict(list)


    def set_named_selections(self, named_selections):
        self.named_selections = named_selections


    def read_file(self, path):

        if isinstance(path, str):
            path = Path(path)

        self.file_path = path
        with open(self.file_path, "r", encoding="latin-1") as self.file:
            self.lines = self.file.readlines()


    def decode_mesh_data_from_file(self):

        for row, line in enumerate(self.lines[0: ]):

            if not line:
                continue

            if "NUMOFF,NODE," in line:
                line = line.replace(" ", "")
                number_nodes = int(line.split("NUMOFF,NODE,")[1])
                nodal_coordinates = np.zeros((number_nodes, 4), dtype=float)  # noqa: F841
                continue

            if "NUMOFF,ELEM," in line:
                line = line.replace(" ", "")
                number_elements = int(line.split("NUMOFF,ELEM,")[1])  # noqa: F841
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
                    
                    connect_data = [int(value) for value in line.split()]

                    if connect_data:
                        if len(connect_data) >= number_of_cols - 4:
                            body_id = connect_data[1]
                            element_id = connect_data[10]
                            _connect_data = filter_collapsed_nodes(connect_data[11:])

                            if connect_data[8] > 8:
                                nodes_per_element = connect_data[8]

                            elif connect_data[8] != len(_connect_data):
                                nodes_per_element = len(_connect_data)

                            else:
                                nodes_per_element = connect_data[8]

                        else:
                            _connect_data = connect_data

                        if nodes_per_element == 3:
                            if len(connect_data) == number_of_cols - 4:
                                _connect_data.insert(0, element_id)
                                _connect_data.insert(1, body_id)
                                _connect_data.insert(2, nodes_per_element)
                                # print(f"solid181 - tria3: {_connect_data}")
                                self.connectivity[body_id, "solid181_tria3"].append(_connect_data)

                        elif nodes_per_element == 4:
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

        self.post_process_nodal_coordinates()
        self.post_process_connectivities()
        self.process_named_selection_elements(export=False)
        self.post_process_faces_connectivities()


    def get_named_selection_format_info(self, line):
        str_format = line[1:-2].split(",")
        num_cols = int(str_format[0].split("i")[0])
        space_cols = int(str_format[0].split("i")[1])
        return num_cols, space_cols


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
        self.solids_connectivities.clear()
        for key, data in self.connectivity.items():
            self.solids_connectivities[key] = np.array(data, dtype=int)


    def export_nodal_coordinates(self):
        self.create_output_data_folder()
        if self.nodal_coordinates:
            header = "Node ID || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
            filename = f"{self.folder_name}/nodal_coordinates.dat"
            data = np.array(self.nodal_coordinates)
            np.savetxt(filename, data, delimiter=",", header=header)#, fmt="%i %18.12e %18.12e %18.12e")


    def export_connectivities(self):
        self.create_output_data_folder()
        if self.solids_connectivities:
            header = "Element ID || Nodes"
            for key, data in self.solids_connectivities.items():
                # filename = f"{self.folder_name}/connectivity_matrix_{key}.dat"
                filename = f"{self.folder_name}/connectivity_matrix.dat"
                np.savetxt(filename, data, header=header, fmt="%i", delimiter=",")


    def get_face_connectivity_indexes(self, element_type: str):

        indexes = np.array([])

        if element_type == "solid285_tet4":
            indexes = np.array([
                [2, 1, 3],
                [1, 2, 4],
                [2, 3, 4],
                [3, 1, 4],
                ], dtype=int) - 1

        elif element_type == "solid187_tet10":
            indexes = np.array([
                [2, 1, 3, 5,  7,  6],
                [1, 2, 4, 5,  9,  8],
                [2, 3, 4, 6, 10,  9],
                [3, 1, 4, 7,  8, 10],
                ], dtype=int) - 1

        if element_type == "solid185_hex8":
            indexes = np.array([
                [2, 1, 4, 3],
                [1, 2, 6, 5],
                [2, 3, 7, 6],
                [3, 4, 8, 7],
                [4, 1, 5, 8],
                [5, 6, 7, 8],
                ], dtype=int) - 1
            
        elif element_type == "solid186_hex20":
            indexes = np.array([
                [2, 1, 4, 3,  9, 12, 11, 10],
                [1, 2, 6, 5,  9, 18, 13, 17],
                [2, 3, 7, 6, 10, 19, 14, 18],
                [3, 4, 8, 7, 11, 20, 15, 19],
                [4, 1, 5, 8, 12, 17, 16, 20],
                [5, 6, 7, 8, 13, 14, 15, 16],
                ], dtype=int) - 1

        return indexes


    def get_nodes_from_face_and_solid_element(self, element_type: str):

        if element_type == "solid181_tria3":
            return 3, 0

        if element_type == "solid187_tet10":
            return 6, 10

        if element_type == "solid285_tet4":
            return 3, 4
        
        if element_type == "solid185_hex8":
            return 4, 8

        if element_type == "solid186_hex20":
            return 8, 20


    def process_named_selection_elements(self, export=False):

        start, end = 0, 0
        self.elements_from_named_selection = dict()

        for key, data in self.connectivity.items():
            vol_id, element_type = key
            nodes_face_element, nodes_solid_element = self.get_nodes_from_face_and_solid_element(element_type)

            faces_connect_indexes = self.get_face_connectivity_indexes(element_type)
            aux_indexes = np.arange(nodes_solid_element, dtype=int)

            surface_id = 0
            connect = np.array(data, dtype=int)
            for ns_key, ns_nodes in self.nodes_from_named_selection.items():

                surface_id += 1
                face_connectivity = list()

                mask = np.sum(np.isin(connect[:, 3:], ns_nodes), axis=1) == nodes_face_element

                if np.sum(mask) == 0:
                    continue

                for jj, _nodes in enumerate(connect[mask, 3:]):
                    if nodes_solid_element:
                        indexes = aux_indexes[np.isin(_nodes, ns_nodes)]
                        row = np.sum(np.isin(faces_connect_indexes, indexes), axis=1) == nodes_face_element
                        face_nodes = _nodes[faces_connect_indexes[row, :]].flatten()

                    else:
                        face_nodes = _nodes

                    face_connectivity.append(face_nodes)

                if face_connectivity:

                    end += len(face_connectivity)
                    indexes = np.arange(1+start, end+1)
                    start = end

                    connect_data = np.array(face_connectivity, dtype=int)

                    if ns_key in self.elements_from_named_selection.keys():
                        actual_connect_data = self.elements_from_named_selection[ns_key]["connectivity"]
                        if len(connect_data) < len(actual_connect_data):
                            continue

                    self.elements_from_named_selection[ns_key] = {  
                                                                  "element_indexes" : indexes,
                                                                  "connectivity" : connect_data,
                                                                  "surface_id" : surface_id,
                                                                  }

                    if not export:
                        continue

                    rows, cols = connect_data.shape
                    exp_data = np.zeros((rows, cols + 1), dtype=int)

                    exp_data[:, 0] = indexes
                    exp_data[:, 1:] = connect_data

                    self.create_output_data_folder()

                    header = "Surface element ID || Nodes"
                    filename = f"{self.folder_name}/elements_from_{ns_key}.dat"
                    np.savetxt(filename, exp_data, header=header, fmt="%i", delimiter=",")


    def post_process_faces_connectivities(self):

        faces_connectivity = list()
        self.faces_connectivities.clear()

        for ns_key, data in self.elements_from_named_selection.items():
            surface_id = data.get("surface_id", -1)
            connect_data = data.get("connectivity")
            indexes = np.arange(1, len(connect_data)+1, dtype=int) + len(faces_connectivity)
            surface_ids = np.ones_like(indexes, dtype=int) * surface_id
            nodes_per_element = np.ones_like(indexes, dtype=int) * len(connect_data[0])

            faces_connectivity = np.array(connect_data, dtype=int)
            faces_connectivity = np.insert(faces_connectivity, 0, indexes, axis=1)
            faces_connectivity = np.insert(faces_connectivity, 1, surface_ids, axis=1)
            faces_connectivity = np.insert(faces_connectivity, 2, nodes_per_element, axis=1)

            self.faces_connectivities[surface_id, "tria3/6"] = faces_connectivity

        np.savetxt("teste.dat", faces_connectivity, delimiter=",", fmt="%i")


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


    def post_process_nodal_coordinates(self, index_zero=True):

        data = np.array(self.nodal_coordinates)

        rows, cols = data.shape

        indexes = data[:,0]
        if index_zero:
            indexes -= 1

        self.array_nodal_coordinates = np.zeros((rows, cols), dtype=float)
        self.array_nodal_coordinates[ :, 0 ] = indexes
        self.array_nodal_coordinates[ :, 1:] = data[:, 1:]


    def get_element_face_normal(self, connect):

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


def filter_collapsed_nodes(input_nodes: list[int]):
    """
    This function filters the element connectivity while maintaining the original order. 
    Be careful, although NumPy's "unique" function performs a similar removal, it 
    reorders the elements in the array. This reordering should be avoided as it 
    compromises the finite element integration rules.
    """
    connectivity = list()
    for node_id in input_nodes:
        if node_id not in connectivity:
            connectivity.append(node_id)

    return connectivity