import numpy as np
from molde import Color
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from vibra.engine.model import Model
from vibra.engine.properties import Fluid, Material


class MeshActor(vtkActor):
    def __init__(self, model: Model):
        self.model = model

        self.points = None
        self.colors = None

    def build_mesh(self):
        if self.model.mesh is None:
            return

        coords = self.model.mesh.nodal_coordinates
        face_connectivity = self.model.mesh.faces_connectivity

        self.points = vtkPoints()
        self.points.SetData(numpy_to_vtk(coords[:, 1:]))

        triangles = face_connectivity[:, 4:]
        helper = np.insert(triangles, 0, triangles.shape[1], axis=1)  # Add a "len" column at the start, as expected by VTK
        vtk_id_array = numpy_to_vtkIdTypeArray(helper.flatten())

        cells = vtkCellArray()
        cells.SetCells(len(triangles), vtk_id_array)

        data = vtkPolyData()
        data.SetPoints(self.points)
        data.SetPolys(cells)

        self.colors = vtkUnsignedCharArray()
        self.colors.SetName("color")
        self.colors.SetNumberOfComponents(3)
        self.colors.SetNumberOfTuples(data.GetNumberOfCells())
        data.GetCellData().SetScalars(self.colors)

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        self.SetMapper(mapper)

        self.clear_colors()

    def clear_colors(self):
        for v in self.model.properties.volume_properties.values():
            if isinstance(v, Fluid | Material):
                self.set_color(Color.from_rgb(*v.color))
                return
        self.set_color(Color(255, 255, 255))

    def set_color(self, color: Color):
        rgb = color.to_rgb()
        for i in range(self.colors.GetNumberOfComponents()):
            self.colors.FillComponent(i, rgb[i])

    def paint_surfaces(self, surfaces: np.ndarray[int]):
        pass

    def paint_volumes(self, volumes: np.ndarray[int]):
        pass
