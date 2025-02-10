from vtkmodules.vtkCommonCore import vtkIntArray

from vibra import app
from .faces_actor import FacesActor


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
        for i, xyz in enumerate(coordinates):
            points.SetPoint(i, xyz)
        points.Modified()

    def clear_colors(self):
        self.set_color((255, 255, 0))
    
    def paint_cells(self, color, solids: list[int]):
        faces = []
        for solid in solids:
            face_elements = self.mesh.solid_to_face_elements.get(solid, [])
            faces.extend(face_elements)
        return super().paint_cells(color, faces)
