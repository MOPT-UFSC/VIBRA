from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.vtkCommonCore import vtkIntArray

from vibra import app

from .faces_actor import FacesActor


class HollowSolidsActor(FacesActor):
    def __init__(self, mesh, allow_hidding=True):
        super().__init__(mesh, allow_hidding, update_normals=False)

    def create_geometry(self):
        super().create_geometry()

        face_indices: vtkIntArray = self.data.GetCellData().GetArray("face_indices")
        solid_indices = vtkIntArray()
        solid_indices.SetName("solid_indices")
        solid_indices.SetNumberOfValues(face_indices.GetNumberOfValues())

        for i in range(face_indices.GetNumberOfTuples()):
            cell2d = face_indices.GetValue(i)
            cell3d = self.mesh.face_to_solid_element.get(cell2d, -1)
            solid_indices.SetValue(i, cell3d)
        
        self.data.GetCellData().AddArray(solid_indices)

    def update_coordinates(self, coordinates):
        points = self.data.GetPoints()
        points.SetData(numpy_to_vtk(coordinates))
    
    def clear_colors(self):
        color = app().config.user_preferences.faces_color
        self.set_color(color)

    def paint_solids(self, color: tuple[3], volumes: tuple[int]):
        cells = []
        for solid in volumes:
            face_elements = self.mesh.solid_to_face_elements.get(solid, [])
            cells.extend(face_elements)
        return self.paint_cells(color, cells)

    def configure_appearance(self):
        super().configure_appearance()

        mapper = self.GetMapper()
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(1.1, 0)
