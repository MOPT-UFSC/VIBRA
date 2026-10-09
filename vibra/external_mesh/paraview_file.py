import os
import vtk
import numpy as np
from vtk import vtkUnstructuredGrid, vtkPoints, vtkDoubleArray, vtkXMLUnstructuredGridWriter

class ParaviewFile:
    def __init__(self):
        self.reset()

    def reset(self):
        self.folder_name = "exported_vtu_files"
        self.element_type = "solid285_tet4"
        self.nodal_coordinates = None
        self.connectivities = None       

    def set_nodal_coordinates(self, nodal_coordinates):
        self.nodal_coordinates = nodal_coordinates

    def set_connectivity(self, connectivity):
        self.connectivities = connectivity

    def set_element_type(self, element_type):
        self.element_type = element_type

    def get_vtk_cell(self):
        _VTK_type = None
        if self.element_type == "solid285_tet4":
            _VTK_type = vtk.VTK_TETRA
        elif self.element_type == "solid185_hex8":
            _VTK_type = vtk.VTK_HEXAHEDRON
        elif self.element_type in ["solid186_tet10", "solid187_tet10"]:
            _VTK_type = vtk.VTK_QUADRATIC_TETRA
        elif self.element_type == "solid186_hex20":
            _VTK_type = vtk.VTK_QUADRATIC_HEXAHEDRON
        return _VTK_type

    def reorder_connectivity(self):
        if self.element_type == "solid285_tet4":
            order = [2, 0, 1, 3]
        elif self.element_type == "solid185_hex8":
            order = [0, 1, 2, 3, 4, 5, 6, 7]
        elif self.element_type in ["solid186_tet10", "solid187_tet10"]:
            order = [2, 0, 1, 3, 6, 4, 5, 8, 7, 9]
        elif self.element_type == "solid186_hex20":
            order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 13, 9, 16, 18, 19, 17, 10, 12, 14, 15]
        else:
            return
        _data = self.connectivities[:, 1:]
        self.connectivities[:, 1:] = _data[:, order]

    def create_output_data_folder(self):
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)

    def process_mesh_and_generate_vtu_file(self):
             
        for i, key, connect in enumerate(self.connectivities.items()):
            #conectivity = [185_TETRA, 185_HEXA, 186_TETRA, 186_HEXA, 187_TETRA] 
            self.generate_vtu(connect, i)
            
        # print('\nCoordenadas:', self.nodal_coordinates.shape)
        # print('Conectividade:', self.connect_file.shape, '\n')

    def generate_vtu(self):
    
        # connect = np.array(connect)

        # Pega a quantidade de nos e de elementos
        nnode = len(self.nodal_coordinates)
        nel = len(self.connectivities)

        print(f"Número de nós: {nnode} \nNúmero de elementos: {nel}")
        
        # Representa a malha
        my_vtk_dataset = vtkUnstructuredGrid()

        # Representa as coordenadas do nós da malha
        points = vtkPoints()

        # Adicionando os pontos 
        # for i in range(nnode):
        for coords in self.nodal_coordinates:
            points.InsertPoint(int(coords[0]), *coords[1:])
            # points.InsertPoint(i, [self.nodal_coordinates[i, 0], self.nodal_coordinates[i, 1], self.nodal_coordinates[i, 2]])

        # Adicionando os pontos a malha
        my_vtk_dataset.SetPoints(points)

        # Alocando espaço para as células
        my_vtk_dataset.Allocate(nel)
        
        # Inicializa um array numpy para os valores dos nós (complexos)
        unod1 = np.zeros((nnode, 3), dtype=complex)  # noqa: F841

        # Criação de um array VTK para armazenar os valores dos nós
        array1 = vtkDoubleArray()
        array1.SetNumberOfComponents(3)
        array1.SetNumberOfTuples(nnode)
        array1.SetName('Eigenvector')

        # # Preenche o array VTK com os valores dos nós
        # for id in range(nnode):
        #     values1 = [np.real(unod1[id, 0]), np.real(unod1[id, 1]), np.real(unod1[id, 2])]
        #     array1.SetTuple(id, values1)

        # my_vtk_dataset.GetPointData().AddArray(array1)

        # Criando as células
        self.VTK_type = self.get_vtk_cell()
        for node_ids in self.connectivities[:, 1:]:
            k = len(node_ids)
            my_vtk_dataset.InsertNextCell(self.VTK_type, k, node_ids)

        self.create_output_data_folder()

        # Gera o arquivo .vtu
        filename = f"{self.folder_name}/type_{self.element_type}.vtu"
        writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileName(filename)
        writer.SetInputData(my_vtk_dataset)
        writer.Write()

        print(f"Arquivo {filename} gerado com sucesso.\n")