from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData, vtkPolyLine
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

class linhas(vtkActor):
    def __init__(self):
        super().__init__()

    def build(self, start_point, finish_point):
        points = vtkPoints()
        points.InsertNextPoint(*start_point)
        points.InsertNextPoint(*finish_point)

        poly_line = vtkPolyLine()
        poly_line.GetPointIds().SetNumberOfIds(2)
        for i in range(2):
            poly_line.GetPointIds().SetId(i, i)

        cell_array = vtkCellArray()
        cell_array.InsertNextCell(poly_line)

        lines_polydata = vtkPolyData()
        lines_polydata.SetPoints(points)
        lines_polydata.SetLines(cell_array)

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(lines_polydata)

        self.SetMapper(mapper)

        self.GetProperty().SetColor(1, 0, 0)
        self.GetProperty().SetLineWidth(3)

        sp = self.GetShaderProperty()
        sp.AddFragmentShaderReplacement(
            "//VTK::Light::Impl",
            False,
            """
            if (mod(gl_FragCoord.x + gl_FragCoord.y, 20.0) < 10.0) {
                discard;
            }
            """,
            False
        )

if __name__ == "__main__":
    renderer = vtkRenderer()
    renderer.SetBackground(0.2, 0.3, 0.4)

    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(800, 600)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    actors = [
        linhas(),
        linhas(),
    ]
    actors[0].build((0, 0, 0), (1, 1, 1))
    actors[1].build((1, 1, 1), (-1, 1, 1))

    for actor in actors:
        renderer.AddActor(actor)

    render_window.Render()
    interactor.Initialize()
    interactor.Start()
