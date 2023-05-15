from dataclasses import dataclass

import vtk


def load_symbol(path):
    reader = vtk.vtkOBJReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()


X_VECTOR = (1, 0, 0)
Y_VECTOR = (0, 1, 0)
Z_VECTOR = (0, 0, 1)


class SymbolActorCommon(vtk.vtkActor):
    def __init__(
        self,
        positions: list[tuple],
        orientations: list[tuple],
        source: vtk.vtkPolyData,
        renderer: vtk.vtkRenderer,
    ):
        self.renderer = renderer

        points = vtk.vtkPoints()
        polydata = vtk.vtkPolyData()
        for x, y, z in positions:
            points.InsertNextPoint(x, y, z)
        polydata.SetPoints(points)

        directions = vtk.vtkFloatArray()
        directions.SetName("directions")
        directions.SetNumberOfComponents(3)
        for x, y, z in orientations:
            directions.InsertNextTuple3(x, y, z)
        polydata.GetPointData().AddArray(directions)

        distance_to_camera = vtk.vtkDistanceToCamera()
        distance_to_camera.SetInputData(polydata)
        distance_to_camera.SetScreenSize(40)
        distance_to_camera.SetRenderer(renderer)

        glyph = vtk.vtkGlyph3D()
        glyph.SetInputConnection(distance_to_camera.GetOutputPort())
        glyph.SetSourceData(source)
        glyph.SetScaleModeToScaleByScalar()
        glyph.SetVectorModeToUseVector()
        glyph.SetInputArrayToProcess(0, 0, 0, 0, "DistanceToCamera")
        glyph.SetInputArrayToProcess(1, 0, 0, 0, "directions")

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())
        mapper.ScalarVisibilityOff()
        self.SetMapper(mapper)
