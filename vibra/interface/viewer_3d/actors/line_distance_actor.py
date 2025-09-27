from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData, vtkPolyLine
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkRenderWindow, vtkRenderWindowInteractor, vtkRenderer

class linhas(vtkActor):
    def __init__(self):
        super().__init__()
        
    def geometry(self, start_point: tuple[float, float, float], finish_point: tuple[float, float, float]):
        self.start_point = start_point
        self.finish_point = finish_point
        points = vtkPoints()
        points.InsertNextPoint(*self.start_point)
        points.InsertNextPoint(*self.finish_point)
        
        poly_line = vtkPolyLine()
        poly_line.GetPointIds().SetNumberOfIds(2)
        for i in range(2):
            poly_line.GetPointIds().SetId(i, i)
        
        cell_array = vtkCellArray()
        cell_array.InsertNextCell(poly_line)
        
        # --- PolyData que contém pontos e linhas ---
        lines_polydata = vtkPolyData()
        lines_polydata.SetPoints(points)
        lines_polydata.SetLines(cell_array)

        # --- Mapper e Actor ---
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(lines_polydata)

        self.SetMapper(mapper)
        self.GetProperty().SetColor(1, 0, 0)  # vermelho
        self.GetProperty().SetLineWidth(3)     # largura da linha
    
if __name__ == "__main__":
    
    # --- Renderer ---
    renderer = vtkRenderer()
    renderer.SetBackground(0.2, 0.3, 0.4)  # cor de fundo

    # --- Janela de render ---
    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(800, 600)
    

    # --- Interactor ---
    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # --- Aqui você adiciona seus actors ---
    renderer.AddActor(linhas((0, 0, 0), (1, 1, 1)))
    renderer.AddActor(linhas((1, 1, 1), (-1, 1, 1)))
    renderer.AddActor(linhas((-1, 1, 1), (3, 1, -1)))

    # --- Render e loop interativo ---
    render_window.Render()
    interactor.Initialize()
    interactor.Start()