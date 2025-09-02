from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_LINE,
    VTK_QUAD,
    VTK_QUADRATIC_QUAD,
    VTK_QUADRATIC_TRIANGLE,
    VTK_TRIANGLE,
    vtkPlane,
    vtkPolyData,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkDataSetMapper

from vibra import app
from vibra.engine.mesher.visual_mesh import VisualMesh
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.utils.interface_utils import ColorMode


class ViewGeometry(vtkActor):
    def __init__(self, mesh: VisualMesh):
        self.GetProperty().RenderLinesAsTubesOn()

        points = vtkPoints()
        points.SetData(numpy_to_vtk(mesh.coords))

        data = vtkPolyData()
        for triangle in mesh.triangles:
            data.InsertNextCell(VTK_TRIANGLE, 3, list(triangle))

        for line in mesh.segments:
            data.InsertNextCell(VTK_LINE, 2, list(line))

        data.SetPoints(points)

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        self.SetMapper(mapper)