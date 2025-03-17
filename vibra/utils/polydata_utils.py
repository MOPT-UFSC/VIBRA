from pathlib import Path

from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkIOGeometry import vtkOBJReader, vtkSTLReader


def read_obj_file(path: str | Path) -> vtkPolyData:
    reader = vtkOBJReader()
    reader.SetFileName(str(path))
    reader.Update()
    return reader.GetOutput()


def read_stl_file(path: str | Path) -> vtkPolyData:
    reader = vtkSTLReader()
    reader.SetFileName(str(path))
    reader.Update()
    return reader.GetOutput()


def transform_polydata(
    polydata: vtkPolyData,
    position=(0, 0, 0),
    rotation=(0, 0, 0),
    scale=(1, 1, 1),
) -> vtkPolyData:
    transform = vtkTransform()
    transform.Translate(position)
    transform.Scale(scale)
    transform.RotateX(rotation[0])
    transform.RotateY(rotation[1])
    transform.RotateZ(rotation[2])
    transform.Update()
    transformation = vtkTransformPolyDataFilter()
    transformation.SetTransform(transform)
    transformation.SetInputData(polydata)
    transformation.Update()
    return transformation.GetOutput()
