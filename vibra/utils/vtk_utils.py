from collections.abc import Sequence
from itertools import combinations, pairwise
from pathlib import Path

import numpy as np
from vtkmodules.util.numpy_support import numpy_to_vtkIdTypeArray
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIdList,
    vtkIntArray,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkIOGeometry import vtkOBJReader, vtkSTLReader
from vtkmodules.vtkIOImage import vtkJPEGReader, vtkPNGReader
from vtkmodules.vtkRenderingCore import (
    vtkTexture,
)


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


def read_texture(path: str | Path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f'Texture file "{path}" not found')

    if path.suffix == ".png":
        reader = vtkPNGReader()
    elif path.suffix == ".jpg":
        reader = vtkJPEGReader()
    else:
        raise ValueError(f"Unsupported image format {path.suffix}")

    reader.SetFileName(str(path))
    reader.Update()

    texture = vtkTexture()
    texture.InterpolateOn()
    texture.RepeatOn()
    texture.SetInputData(reader.GetOutput())
    texture.Update()

    return texture


def create_cells(connectivity: np.ndarray) -> vtkCellArray:
    if connectivity.ndim == 1:
        connectivity = connectivity.reshape(-1, 1)

    helper = np.insert(connectivity, 0, connectivity.shape[1], axis=1)
    vtk_id_array = numpy_to_vtkIdTypeArray(helper.ravel())
    cell_array = vtkCellArray()
    cell_array.SetCells(connectivity.shape[0], vtk_id_array)
    return cell_array


def linearize_2d_cells(connectivity: np.ndarray) -> np.ndarray:
    n_nodes = connectivity[:, 4:].shape[1]
    match n_nodes:
        case 0:
            return np.zeros(shape=(0, 4 + 2), dtype=int)
        case 3 | 4:
            reorderings = list(pairwise(range(n_nodes)))
        case 6:
            reorderings = [
                [0, 3], [3, 1],
                [1, 4], [4, 2],
                [2, 5], [5, 0],
            ]  # fmt: skip
        case 8:
            reorderings = [
                [0, 4], [4, 1],
                [1, 5], [5, 2],
                [2, 6], [6, 3],
                [3, 7], [7, 0],
            ]  # fmt: skip
        case _:
            raise NotImplementedError(f"Exploding to 2D cells is not supported for {n_nodes}-node cells")
    return explode_cells(connectivity, reorderings)


def linearize_1d_cells(connectivity: np.ndarray) -> np.ndarray:
    n_nodes = connectivity[:, 4:].shape[1]
    match n_nodes:
        case 0:
            return np.zeros(shape=(0, 4 + 2), dtype=int)
        case 2:
            return connectivity
        case 3:
            reorderings = [[0, 2], [2, 1]]
        case _:
            raise NotImplementedError(f"Exploding to 1D cells is not supported for {n_nodes}-node cells")
    return explode_cells(connectivity, reorderings)


def linearize_3d_cells(connectivity: np.ndarray) -> np.ndarray:
    n_nodes = connectivity[:, 4:].shape[1]
    match n_nodes:
        case 0:
            return np.zeros(shape=(0, 4 + 2), dtype=int)
        case 4:
            reorderings = list(combinations(range(n_nodes), 2))
        case 8:
            reorderings = [
                [0, 1], [1, 2], [2, 3], [3, 0],
                [4, 5], [5, 6], [6, 7], [7, 4],
                [0, 4], [1, 5], [2, 6], [3, 7],
            ]  # fmt: skip
        case 10:
            reorderings = [
                [0, 4], [4, 1], [1, 5], [5, 2], [0, 6], [6, 2],
                [0, 7], [7, 3], [2, 8], [8, 3], [1, 9], [9, 3],
            ]  # fmt: skip
        case 20:
            reorderings = [
                [0, 8], [8, 1],
                [1, 11], [11, 2],
                [2, 13], [13, 3],
                [3, 9], [9, 0],
                [4, 16], [16, 5],
                [5, 18], [18, 6],
                [6, 19], [19, 7],
                [7, 17], [17, 4],
                [0, 10], [10, 4],
                [1, 12], [12, 5],
                [2, 14], [14, 6],
                [3, 15], [15, 7],
            ]  # fmt: skip
        case _:
            raise NotImplementedError(f"Exploding to 2D cells is not supported for {n_nodes}-node cells")
    return explode_cells(connectivity, reorderings)


def triangulate_2d_cells(connectivity: np.ndarray) -> np.ndarray:
    n_nodes = connectivity[:, 4:].shape[1]
    match n_nodes:
        case 0:
            return np.zeros(shape=(0, 4 + 3), dtype=int)
        case 3:
            return connectivity
        case 4:
            reorderings = [[0, 3, 1], [1, 3, 2]]
        case 6:
            reorderings = [[0, 3, 5], [1, 4, 3], [2, 5, 4], [3, 4, 5]]
        case 8:
            reorderings = [
                [0, 4, 7], [1, 5, 4], [2, 6, 5], [3, 7, 6], [4, 5, 6], [4, 6, 7],
            ]  # fmt: skip
        case _:
            raise NotImplementedError(f"Exploding to 2D cells is not supported for {n_nodes}-node cells")
    return explode_cells(connectivity, reorderings)


def triangulate_3d_cells(connectivity: np.ndarray) -> np.ndarray:
    n_nodes = connectivity[:, 4:].shape[1]

    match n_nodes:
        case 0:
            return np.zeros(shape=(0, 4 + 3), dtype=int)
        case 4:  # Tetrahedron Linear
            reorderings = list(combinations(range(n_nodes), 3))
        case 8:
            reorderings = [
                [0, 1, 2], [0, 2, 3],
                [4, 5, 6], [4, 6, 7],
                [0, 1, 5], [0, 5, 4],
                [3, 2, 6], [3, 6, 7],
                [0, 3, 7], [0, 7, 4],
                [1, 2, 6], [1, 6, 5],
            ]  # fmt: skip
        case 10:  # Tetrahedron Quadratic
            reorderings = [
                [0, 4, 6], [1, 5, 4], [2, 6, 5], [4, 5, 6],
                [0, 7, 4], [3, 9, 7], [1, 4, 9], [7, 9, 4],
                [0, 6, 7], [2, 8, 6], [3, 7, 8], [6, 8, 7],
                [1, 9, 5], [3, 8, 9], [2, 5, 8], [9, 8, 5],
            ]  # fmt: skip
        case 20:
            reorderings = [
                [0, 8, 9], [1, 11, 8], [2, 13, 11], [3, 9, 13], [8, 11, 13], [8, 13, 9],
                [4, 16, 17], [5, 18, 16], [6, 19, 18], [7, 17, 19], [16, 18, 19], [16, 19, 17],
                [0, 8, 10], [1, 12, 8], [5, 16, 12], [4, 10, 16], [8, 12, 16], [8, 16, 10],
                [2, 13, 14], [3, 15, 13], [7, 19, 15], [6, 14, 19], [13, 15, 19], [13, 19, 14],
                [0, 9, 10], [3, 15, 9], [7, 17, 15], [4, 10, 17], [9, 15, 17], [9, 17, 10],
                [1, 11, 12], [2, 14, 11], [6, 18, 14], [5, 12, 18], [11, 14, 18], [11, 18, 12],
            ]  # fmt: skip
        case _:
            raise NotImplementedError(f"Exploding to 2D cells is not supported for {n_nodes}-node cells")

    return explode_cells(connectivity, reorderings)


def explode_cells(connectivity: np.ndarray, reorderings: Sequence[Sequence[int]]) -> np.ndarray:
    column_order = [
        [0, 1, 2, 3] + [i + 4 for i in reordering]
        for reordering in reorderings
    ]  # fmt: skip

    stacked = []
    for order in column_order:
        connect = connectivity[:, order]
        stacked.append(connect)

    return np.concatenate(stacked)
