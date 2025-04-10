import numpy as np
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkRenderingCore import vtkRenderer

from vibra.interface.viewer_3d.actors.symbols.symbols_common import (
    SymbolActorFixedSize,
    SymbolTranform,
)

from vibra import app

class SymbolsActor(SymbolActorFixedSize):
    def __init__(self, renderer: vtkRenderer):

        self.model = app().project.model
        self.mesh = self.model.mesh

        source = self.get_source()
        self.transforms = self.get_transforms()
        self.show_nodal_normals()
        self.show_2d_element_normals()
        self.show_2d_element_normals_by_list()

        super().__init__(self.transforms, source)

        self.configure_appearance()

    def get_source(self):
        source = vtkArrowSource()
        source.SetTipLength(0.25)
        source.Update()
        return source.GetOutput()

    def get_transforms(self):

        transforms: list[SymbolTranform] = list()

        try:
            scale = self.mesh.principal_diagonal / 20
        except:
            return

        orientation = np.array([-1, 0, 0], dtype=float)

        for (property, surface_id), data in self.model.properties.surface_properties.items():
            if property == "surface_velocity":
                if "real_values" in data.keys():

                    if data["real_values"][0] < 0:
                        orientation = (-1, 0, 0)

                surface_nodes = self.mesh.nodes_from_surfaces[surface_id]
                nodal_coords = self.mesh.nodal_coordinates[surface_nodes, 1:]
                # center = self.mesh.get_average_nodal_coordinates(surface_id)

                for coords in nodal_coords:
                    shifted_coords = coords + (0/20) * orientation
                    t = SymbolTranform(position=shifted_coords, orientation=orientation, size = scale)
                    transforms.append(t)

        return transforms

    def show_nodal_normals(self):
        return

        try:
            scale = self.mesh.principal_diagonal / 20
        except:
            return

        self.transforms.clear()

        for node_id, normal_vector in self.mesh.nodal_normals_data.items():

            coords = self.mesh.nodal_coordinates[node_id, 1:]
            shifted_coords = coords + (1/100) * normal_vector
            t = SymbolTranform(position=shifted_coords, orientation = normal_vector, size = scale)
            self.transforms.append(t)

    def show_2d_element_normals(self):

        try:
            scale = self.mesh.principal_diagonal / 20
        except:
            return

        self.transforms.clear()

        for (property, surface_id) in self.model.properties.surface_properties.keys():
            if property == "normal_pressure_load":
                for elem_id in self.mesh.elements_from_surface[surface_id]:

                    connect = self.mesh.faces_connectivity[elem_id, 4:]
                    coords = np.average(self.mesh.nodal_coordinates[connect, 1:], axis=0)
                    normal_vector = self.mesh.get_element_face_normal(connect)
                    shifted_coords = coords + (1/100) * normal_vector
                    t = SymbolTranform(position=shifted_coords, orientation = normal_vector, size = scale)
                    self.transforms.append(t)

    # temporary
    def show_2d_element_normals_by_list(self):

        try:
            scale = self.mesh.principal_diagonal / 20
        except:
            return

        self.transforms.clear()

        for elem_id in self.mesh.list_elements:

            connect = self.mesh.faces_connectivity[elem_id, 4:]
            coords = np.average(self.mesh.nodal_coordinates[connect, 1:], axis=0)
            normal_vector = self.mesh.get_element_face_normal(connect)
            shifted_coords = coords + (1/100) * normal_vector
            t = SymbolTranform(position=shifted_coords, orientation = normal_vector, size = scale)
            self.transforms.append(t)

    def configure_appearance(self):
        self.GetProperty().SetColor(1, 0, 1)
        # self.GetProperty().LightingOff()
