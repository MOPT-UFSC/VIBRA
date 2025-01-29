from vtkmodules.vtkCommonCore import vtkIntArray

from .faces_actor import FacesActor

def cell2d_to_cell3d(cell2d: int) -> int:
    if cell2d in [759, 1009]:
        return 4574
    return 0


def cell3d_to_cell2d(cell3d: int) -> int:
    if cell3d == 4574:
        return [759, 1009]
    else:
        return [763, 1013]


class FakeSolidsActor(FacesActor):
    def create_geometry(self):
        super().create_geometry()
        cell_indexes: vtkIntArray = self.data.GetCellData().GetArray("cell_indexes")

        for i in range(cell_indexes.GetNumberOfTuples()):
            cell2d = cell_indexes.GetValue(i)
            cell3d = self.mesh.face_to_solid_element.get(cell2d, -1)
            cell_indexes.SetValue(i, cell3d)
    
    def clear_colors(self):
        self.set_color((255, 255, 0))
    
    def paint_cells(self, color, solids: list[int]):
        faces = []
        for solid in solids:
            face_elements = self.mesh.solid_to_face_elements.get(solid, [])
            faces.extend(face_elements)
        return super().paint_cells(color, faces)
