from pathlib import Path
from typing import Sequence

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIdList,
    vtkIntArray,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkIOGeometry import vtkOBJReader, vtkSTLReader
from vtkmodules.vtkIOImage import vtkJPEGReader, vtkPNGReader
from vtkmodules.vtkRenderingCore import (
    vtkTexture,
)
import numpy as np


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

    if isinstance(value, int | np.integer):
        array = vtkIntArray()
        array.SetName(name)
        array.SetNumberOfTuples(n_cells)
        array.Fill(value)

    elif isinstance(value, float | np.floating):
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
        raise ValueError(f'Invalid data type "{type(value)}"')

    data.GetCellData().AddArray(array)
    return array


def create_vtk_id_list(id_list: Sequence[int]) -> vtkIdList:
    vtk_id_list = vtkIdList()
    for id in id_list:
        vtk_id_list.InsertNextId(id)
    return vtk_id_list


def read_texture(path: str | Path | None):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f'Texture file "{path}" not found')

    if path.suffix == ".png":
        reader = vtkPNGReader()
    elif path.suffix == ".jpg":
        reader = vtkJPEGReader()
    else:
        raise ValueError(f"Unsupported image format {path.suffix}")

    reader.SetFileName(path)
    reader.Update()

    texture = vtkTexture()
    texture.InterpolateOn()
    texture.RepeatOn()
    texture.SetInputData(reader.GetOutput())
    texture.Update()

    return texture
