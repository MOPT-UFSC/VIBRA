from .faces_actor import FacesActor

from vtkmodules.vtkCommonCore import vtkIntArray


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
            cell3d = cell2d_to_cell3d(cell2d)
            cell_indexes.SetValue(i, cell3d)
    
    def configure_appearance(self):
        super().configure_appearance()
        self.set_color((255, 255, 0))
    
    def paint_cells(self, color, solids: list[int]):
        faces = []
        for solid in solids:
            faces.extend(cell3d_to_cell2d(solid))
        return super().paint_cells(color, faces)
