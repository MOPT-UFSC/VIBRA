import numpy as np
from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkRenderer,
)

from vibra.utils.interface_utils import screen_to_world_coords
from vibra.utils.math_functions import points_in_between

DEFAULT_RETURN_VALUE = (-1, float("inf"))


def pick_actor_cell_info(
    x,
    y,
    target_actor: vtkActor,
    indices_array: str,
    renderer: vtkRenderer,
) -> tuple[int, tuple[float, float, float]]:
    cell_picker = vtkCellPicker()
    cell_picker.SetTolerance(0.0018)

    cell_picker.InitializePickList()
    cell_picker.AddPickList(target_actor)
    cell_picker.PickFromListOn()
    cell_picker.Pick(x, y, 0, renderer)

    cell_id = cell_picker.GetCellId()
    position = cell_picker.GetPickPosition()

    entities = [
        cell_picker.GetActor(),
        cell_picker.GetProp3D(),
        cell_picker.GetAssembly(),
        cell_picker.GetPropAssembly(),
    ]

    if all((entity is None) or (entity != target_actor) for entity in entities):
        return DEFAULT_RETURN_VALUE

    camera_position = np.array(renderer.GetActiveCamera().GetPosition())
    camera_distance = (
        np.linalg.norm(camera_position - position) 
        if cell_id >= 0 else float("inf")
    )  # fmt: skip

    if cell_id < 0:
        return DEFAULT_RETURN_VALUE

    if not hasattr(target_actor, "data"):
        return DEFAULT_RETURN_VALUE

    data: vtkPolyData = target_actor.data
    if not data:
        return DEFAULT_RETURN_VALUE

    cell_info_array: vtkIntArray = data.GetCellData().GetArray(indices_array)
    if not cell_info_array:
        return DEFAULT_RETURN_VALUE

    cell_info = cell_info_array.GetValue(cell_id)
    return cell_info, camera_distance


def narrow_pickability_to_actor(target_actor: vtkActor, renderer: vtkRenderer):
    actor: vtkActor
    pickability = dict()
    for actor in renderer.GetActors():
        pickability[actor] = actor.GetPickable()
        actor.SetPickable(actor == target_actor)
    return pickability


def restore_pickability(pickability: dict, renderer: vtkRenderer):
    actor: vtkActor
    for actor in renderer.GetActors():
        actor.SetPickable(pickability[actor])


def get_coordinates_inside_area(
    coordinates: np.ndarray,
    area: list[int, int, int, int],
    renderer: vtkRenderer,
) -> list[int]:
    x0, y0, x1, y1 = area

    upper_left_3d = screen_to_world_coords((x0, y0, 0), renderer)
    upper_right_3d = screen_to_world_coords((x1, y0, 0), renderer)
    bottom_left_3d = screen_to_world_coords((x0, y1, 0), renderer)

    mask_horizontal = points_in_between(
        coordinates,
        upper_left_3d,
        upper_right_3d,
    )

    mask_vertical = points_in_between(
        coordinates,
        upper_left_3d,
        bottom_left_3d,
    )

    return mask_horizontal & mask_vertical
