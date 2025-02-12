from vtkmodules.vtkCommonCore import vtkIntArray

from vibra import app
from .faces_actor import FacesActor

from vtkmodules.util.numpy_support import numpy_to_vtk


class HollowSolidsActor(FacesActor):
    def __init__(self, mesh, allow_hidding=True):
        super().__init__(mesh, allow_hidding, update_normals=False)

    def create_geometry(self):
        super().create_geometry()
        cell_indexes: vtkIntArray = self.data.GetCellData().GetArray("cell_indexes")

        for i in range(cell_indexes.GetNumberOfTuples()):
            cell2d = cell_indexes.GetValue(i)
            cell3d = self.mesh.face_to_solid_element.get(cell2d, -1)
            cell_indexes.SetValue(i, cell3d)
    
    def update_coordinates(self, coordinates):
        points = self.data.GetPoints()
        points.SetData(numpy_to_vtk(coordinates))
    
    def paint_cells(self, color, solids: list[int]):
        faces = []
        for solid in solids:
            face_elements = self.mesh.solid_to_face_elements.get(solid, [])
            faces.extend(face_elements)
        return super().paint_cells(color, faces)

    def configure_appearance(self):
        super().configure_appearance()
        # Change the specular color to purple to differentiate
        # from the massive solids actor
        self.GetProperty().SetSpecularColor(1, 0, 1)
