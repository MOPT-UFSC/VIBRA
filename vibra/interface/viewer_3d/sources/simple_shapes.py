from vibra.utils.polydata_utils import transform_polydata
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
)

def create_cone_source():
    source = vtkConeSource()
    source.SetHeight(1)
    source.SetRadius(0.5)
    source.SetResolution(12)
    source.Update()
    s = 0.6
    return transform_polydata(
        source.GetOutput(),
        position=(-s/2, 0, 0),
        scale=(s, s, s)
    )

def create_cube_source():
    source = vtkCubeSource()
    source.SetBounds(0, 1, 0, 1, 0, 1)
    source.Update()
    return source.GetOutput()
