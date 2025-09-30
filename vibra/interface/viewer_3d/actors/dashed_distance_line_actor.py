from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData, vtkPolyLine
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
)

from vibra.interface.analysis_filter_menu import app

class DashedDistanceLineActor(vtkActor):
    def __init__(self):
        super().__init__()

    def build(self, start_point, finish_point):
        points = vtkPoints()
        points.InsertNextPoint(*start_point)
        points.InsertNextPoint(*finish_point)

        poly_line = vtkPolyLine()
        poly_line.GetPointIds().SetNumberOfIds(2)
        poly_line.GetPointIds().SetId(0, 0)
        poly_line.GetPointIds().SetId(1, 1)

        cell_array = vtkCellArray()
        cell_array.InsertNextCell(poly_line)

        lines_polydata = vtkPolyData()
        lines_polydata.SetPoints(points)
        lines_polydata.SetLines(cell_array)

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(lines_polydata)

        self.SetMapper(mapper)

        self.GetProperty().SetColor(1, 0, 0)
        self.GetProperty().SetLineWidth(app().config.user_preferences.lines_thickness + 60)

        shader_property = self.GetShaderProperty()
        shader_property.AddFragmentShaderReplacement(
            "//VTK::Light::Impl",
            False,
            """
            if (mod(ceil(gl_FragCoord.x / 20.0) + ceil(gl_FragCoord.y / 20.0), 2.0) == 0.0) {
                discard;
            }
            """,
            False
        )
    
    def clear_colors(self):
        self.GetProperty().SetColor(0, 0, 0)
