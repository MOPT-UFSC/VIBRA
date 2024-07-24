from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkIOGeometry import vtkOBJReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDistanceToCamera,
    vtkPolyDataMapper,
    vtkRenderer,
)


def load_symbol(path):
    reader = vtkOBJReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()


X_VECTOR = (1, 0, 0)
Y_VECTOR = (0, 1, 0)
Z_VECTOR = (0, 0, 1)


class SymbolActorCommon(vtkActor):
    def __init__(
        self,
        positions: list[tuple],
        orientations: list[tuple],
        source: vtkPolyData,
        renderer: vtkRenderer,
    ):
        self.renderer = renderer

        points = vtkPoints()
        polydata = vtkPolyData()
        for x, y, z in positions:
            points.InsertNextPoint(x, y, z)
        polydata.SetPoints(points)

        directions = vtkFloatArray()
        directions.SetName("directions")
        directions.SetNumberOfComponents(3)
        for x, y, z in orientations:
            directions.InsertNextTuple3(x, y, z)
        polydata.GetPointData().AddArray(directions)

        distance_to_camera = vtkDistanceToCamera()
        distance_to_camera.SetInputData(polydata)
        distance_to_camera.SetScreenSize(40)
        distance_to_camera.SetRenderer(renderer)

        glyph = vtkGlyph3D()
        glyph.SetInputConnection(distance_to_camera.GetOutputPort())
        glyph.SetSourceData(source)
        glyph.SetScaleModeToScaleByScalar()
        glyph.SetVectorModeToUseVector()
        glyph.SetInputArrayToProcess(0, 0, 0, 0, "DistanceToCamera")
        glyph.SetInputArrayToProcess(1, 0, 0, 0, "directions")

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())
        mapper.ScalarVisibilityOff()
        self.SetMapper(mapper)
