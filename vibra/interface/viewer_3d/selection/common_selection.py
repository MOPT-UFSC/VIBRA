from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkRenderer,
)

import numpy as np


def pick_actor_cell_info(
    x,
    y,
    target_actor: vtkActor,
    indexes_array: str,
    renderer: vtkRenderer,
) -> tuple[int, tuple[float, float, float]]:
    cell_picker = vtkCellPicker()
    cell_picker.SetTolerance(0.0018)

    pickability = narrow_pickability_to_actor(target_actor, renderer)
    cell_picker.Pick(x, y, 0, renderer)
    restore_pickability(pickability, renderer)

    cell_id = cell_picker.GetCellId()
    position = cell_picker.GetPickPosition()

    camera_position = np.array(renderer.GetActiveCamera().GetPosition())
    camera_distance = np.linalg.norm(camera_position - position) if cell_id >= 0 else float("inf")

    if cell_id < 0:
        return cell_id

    data: vtkPolyData = target_actor.GetMapper().GetInput()
    if not data:
        return cell_id

    cell_info_array: vtkIntArray = data.GetCellData().GetArray(indexes_array)
    if not cell_info_array:
        return cell_id

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
