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

    def show_arrows(self, node_ids: list, orientations: list[float, float, float]):

        try:
            scale = self.mesh.principal_diagonal / 20
        except:
            return

        nodal_coords = self.mesh.nodal_coordinates[node_ids, 1:]

        for i, coords in enumerate(nodal_coords):
            shifted_coords = coords + (0/20) * orientations[i]
            t = SymbolTranform(position=shifted_coords, orientation = orientations[i], size = scale)
            self.transforms.append(t)

    def configure_appearance(self):
        self.GetProperty().SetColor(1, 0, 0)
        self.GetProperty().LightingOff()
