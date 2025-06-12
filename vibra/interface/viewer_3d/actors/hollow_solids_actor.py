from vtkmodules.vtkCommonCore import vtkIntArray

from vibra import app
from .faces_actor import FacesActor

from vtkmodules.util.numpy_support import numpy_to_vtk


class HollowSolidsActor(FacesActor):
    def __init__(self, mesh, allow_hidding=True):
        super().__init__(mesh, allow_hidding, update_normals=False)

    def create_geometry(self):
        super().create_geometry()

        face_indexes: vtkIntArray = self.data.GetCellData().GetArray("face_indexes")
        solid_indexes = vtkIntArray()
        solid_indexes.SetName("solid_indexes")
        solid_indexes.SetNumberOfValues(face_indexes.GetNumberOfValues())

        for i in range(face_indexes.GetNumberOfTuples()):
            cell2d = face_indexes.GetValue(i)
            cell3d = self.mesh.face_to_solid_element.get(cell2d, -1)
            solid_indexes.SetValue(i, cell3d)
        
        self.data.GetCellData().AddArray(solid_indexes)

    def update_coordinates(self, coordinates):
        points = self.data.GetPoints()
        points.SetData(numpy_to_vtk(coordinates))
    
    def clear_colors(self):
        color = app().config.user_preferences.faces_color
        self.set_color(color.to_rgba())

    def paint_cells(self, color, solids: list[int]):
        faces = []
        for solid in solids:
            face_elements = self.mesh.solid_to_face_elements.get(solid, [])
            faces.extend(face_elements)
        return super().paint_cells(color, faces)

    def configure_appearance(self):
        super().configure_appearance()

        mapper = self.GetMapper()
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(1.1, 0)
