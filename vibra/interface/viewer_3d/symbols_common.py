import vtk


def load_symbol(path):
    reader = vtk.vtkOBJReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()


class SymbolActorCommon(vtk.vtkActor):
    def __init__(self, positions: list[tuple], source: vtk.vtkPolyData, renderer: vtk.vtkRenderer):
        self.renderer = renderer

        points = vtk.vtkPoints()
        polydata = vtk.vtkPolyData()
        for x, y, z in positions:
            points.InsertNextPoint(x, y, z)
        polydata.SetPoints(points)

        distance_to_camera = vtk.vtkDistanceToCamera()
        distance_to_camera.SetInputData(polydata)
        distance_to_camera.SetScreenSize(40)
        distance_to_camera.SetRenderer(renderer)

        glyph = vtk.vtkGlyph3D()
        glyph.SetInputConnection(distance_to_camera.GetOutputPort())
        glyph.SetSourceData(source)
        glyph.SetScaleModeToScaleByScalar()
        glyph.SetColorModeToColorByVector()
        glyph.SetInputArrayToProcess(0, 0, 0, 0, "DistanceToCamera")

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())
        self.SetMapper(mapper)
