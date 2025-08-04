from pathlib import Path

from vtkmodules.vtkCommonCore import vtkUnsignedCharArray, vtkIntArray, vtkFloatArray
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


def fill_array(data: vtkPolyData, name: str, value: int | float | tuple[int]):
    n_cells = data.GetNumberOfCells()

    if isinstance(value, int):
        array = vtkIntArray()
        array.SetName(name)
        array.SetNumberOfTuples(n_cells)
        array.Fill(value)

    elif isinstance(value, float):
        array = vtkFloatArray()
        array.SetName(name)
        array.SetNumberOfTuples(n_cells)
        array.Fill(value)

    elif isinstance(value, tuple):
        array = vtkUnsignedCharArray()
        array.SetName(name)
        array.SetNumberOfComponents(len(value))
        array.SetNumberOfTuples(n_cells)
        for i, val in enumerate(value):
            array.FillComponent(i, val)

    else:
        raise ValueError("Invalid data")

    data.GetCellData().AddArray(array)    
    return array
